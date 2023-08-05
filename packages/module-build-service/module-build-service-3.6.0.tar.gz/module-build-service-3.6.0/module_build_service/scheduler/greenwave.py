# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
from __future__ import absolute_import
from functools import reduce
import json

import requests

from module_build_service.common import log, conf
from module_build_service.common.errors import GreenwaveError


class Greenwave(object):
    def __init__(self):
        """
        Initialize greenwave instance with config
        """
        self.url = conf.greenwave_url
        self._decision_context = conf.greenwave_decision_context
        if not self.decision_context:
            raise RuntimeError("No Greenwave decision context set")
        self._subj_type = conf.greenwave_subject_type
        self._gw_timeout = conf.greenwave_timeout
        self.error_occurred = False

    def _greenwave_query(self, query_type, payload=None):
        """
        Make a query to greenwave
        :param query_type: will be part of url
        :type query_type: str
        :param payload: request payload used in 'decision' query
        :type payload: str
        :return: response
        :rtype: dict
        """
        query_func = requests.post if payload else requests.get
        kwargs = {"url": "{0}/{1}".format(self.url, query_type), "timeout": self.timeout}

        if payload:
            kwargs["headers"] = {"Content-Type": "application/json"}
            kwargs["data"] = payload

        try:
            response = query_func(**kwargs)
        except requests.exceptions.Timeout:
            raise GreenwaveError("Greenwave request timed out")
        except Exception as exc:
            error_message = "Unspecified greenwave request error " \
                            '(original exception was: "{0}")'.format(str(exc))
            log.exception(error_message)
            raise GreenwaveError(error_message)

        try:
            resp_json = response.json()
        except ValueError:
            log.debug("Greenwave response content (status {0}): {1}".format(
                response.status_code, response.text
            ))
            raise GreenwaveError("Greenwave returned invalid JSON.")

        log.debug(
            'Query to Greenwave (%s) result: status=%d, content="%s"',
            kwargs["url"], response.status_code, resp_json
        )

        if response.status_code == 200:
            return resp_json

        try:
            err_msg = resp_json["message"]
        except KeyError:
            err_msg = response.text
        raise GreenwaveError("Greenwave returned {0} status code. Message: {1}".format(
            response.status_code, err_msg
        ))

    def query_decision(self, build, prod_version):
        """
        Query decision to greenwave
        :param build: build object
        :type build: module_build_service.common.models.ModuleBuild
        :param prod_version: The product version string used for querying WaiverDB
        :type prod_version: str
        :return: response
        :rtype: dict
        """
        payload = {
            "decision_context": self.decision_context,
            "product_version": prod_version,
            "subject_type": self.subject_type,
            "subject_identifier": build.nvr_string
        }
        return self._greenwave_query('decision', json.dumps(payload))

    def query_policies(self, return_all=False):
        """
        Query policies to greenwave
        :param return_all: Return all policies, if False select by subject_type and decision_context
        :type return_all: bool
        :return: response
        :rtype: dict
        """
        response = self._greenwave_query('policies')

        if return_all:
            return response

        try:
            selective_resp = {
                "policies": [
                    pol for pol in response["policies"]
                    if pol["decision_context"] == self.decision_context
                    and pol["subject_type"] == self.subject_type
                ]
            }
        except KeyError:
            log.exception("Incorrect greenwave response (Mandatory key is missing)")
            raise GreenwaveError("Incorrect greenwave response (Mandatory key is missing)")
        return selective_resp

    def get_product_versions(self):
        """
        Return a set of product versions according to decision_context and subject_type
        :return: product versions
        :rtype: set
        """
        return reduce(
            lambda old, new: old.union(new),
            [pol["product_versions"] for pol in self.query_policies()["policies"]],
            set()
        )

    def check_gating(self, build):
        """
        Query decision to greenwave
        :param build: build object
        :type build: module_build_service.common.models.ModuleBuild
        :return: True if at least one GW response contains policies_satisfied set to true
        :rtype: bool
        """
        self.error_occurred = False
        try:
            versions = self.get_product_versions()
        except GreenwaveError:
            log.warning('An error occured while getting a product versions')
            self.error_occurred = True
            return False

        for ver in versions:
            try:
                if self.query_decision(build, ver)["policies_satisfied"]:
                    # at least one positive result is enough
                    return True
            except (KeyError, GreenwaveError) as exc:
                self.error_occurred = True
                log.warning('Incorrect greenwave result "%s", ignoring', str(exc))

        return False

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        value = value.rstrip("/")
        if not value:
            raise RuntimeError("No Greenwave URL set")
        self._url = value

    @property
    def decision_context(self):
        return self._decision_context

    @property
    def subject_type(self):
        return self._subj_type

    @property
    def timeout(self):
        return self._gw_timeout

    @timeout.setter
    def timeout(self, value):
        self._gw_timeout = value


try:
    greenwave = Greenwave()
except RuntimeError:
    log.warning('Greenwave is not configured or configured improperly')
    greenwave = None
