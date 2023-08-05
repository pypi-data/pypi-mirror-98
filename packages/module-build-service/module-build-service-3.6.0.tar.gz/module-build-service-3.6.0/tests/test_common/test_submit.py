# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
from __future__ import absolute_import

import mock

from module_build_service.common.modulemd import Modulemd
from module_build_service.common.submit import _is_eol_in_pdc, fetch_mmd
from tests.test_web.test_views import FakeSCM


@mock.patch("module_build_service.common.submit.requests")
def test_pdc_eol_check(requests):
    """ Push mock pdc responses through the eol check function. """

    response = mock.Mock()
    response.json.return_value = {
        "results": [{
            "id": 347907,
            "global_component": "mariadb",
            "name": "10.1",
            "slas": [{"id": 694207, "sla": "security_fixes", "eol": "2019-12-01"}],
            "type": "module",
            "active": True,
            "critical_path": False,
        }]
    }
    requests.get.return_value = response

    is_eol = _is_eol_in_pdc("mariadb", "10.1")
    assert not is_eol

    response.json.return_value["results"][0]["active"] = False

    is_eol = _is_eol_in_pdc("mariadb", "10.1")
    assert is_eol


@mock.patch("module_build_service.common.scm.SCM")
def test_fetch_mmd(mocked_scm):
    """ Test behavior for fetch_mmd """

    FakeSCM(
        mocked_scm,
        "testmodule",
        "testmodule.yaml",
        "620ec77321b2ea7b0d67d82992dda3e1d67055b4")

    mmd, scm = fetch_mmd('testurl')
    assert isinstance(mmd, Modulemd.ModuleStream)


@mock.patch("module_build_service.common.scm.SCM")
def test_fetch_mmd_packager_v3(mocked_scm):
    """ Test PackagerV3 behavior for fetch_mmd """

    FakeSCM(
        mocked_scm,
        "foo",
        "v3/mmd_packager.yaml",
        "620ec77321b2ea7b0d67d82992dda3e1d67055b4")

    mmd, scm = fetch_mmd('testurl')
    assert not isinstance(mmd, Modulemd.ModuleStream)
