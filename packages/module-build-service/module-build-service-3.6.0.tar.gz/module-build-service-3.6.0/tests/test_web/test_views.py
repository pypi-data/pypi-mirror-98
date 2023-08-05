# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
from __future__ import absolute_import
import json
from datetime import datetime
from functools import partial
import hashlib
from os import path, mkdir
from os.path import basename, dirname, splitext
import re
from shutil import copyfile

import koji
from mock import patch, PropertyMock, Mock
from requests.utils import quote
import pytest
import sqlalchemy
from sqlalchemy.orm import load_only

from module_build_service import version
from module_build_service.builder.utils import get_rpm_release
import module_build_service.common.config as mbs_config
from module_build_service.common.errors import UnprocessableEntity
from module_build_service.common.models import ModuleBuild, BUILD_STATES, ComponentBuild
from module_build_service.common.utils import load_mmd, import_mmd, mmd_to_str
from module_build_service.scheduler.db_session import db_session
import module_build_service.web.submit
from tests import (
    init_data,
    clean_database,
    make_module_in_db,
    read_staged_data,
    staged_data_filename,
    time_assert,
)
from tests.test_common.test_scm import base_dir as scm_base_dir


user = ("Homer J. Simpson", {"packager"})
other_user = ("some_other_user", {"packager"})
anonymous_user = ("anonymous", {"packager"})
import_module_user = ("Import M. King", {"mbs-import-module"})
base_dir = dirname(dirname(__file__))


class FakeSCM(object):
    def __init__(
        self,
        mocked_scm,
        name,
        mmd_filenames,
        commit=None,
        checkout_raise=False,
        get_latest_raise=False,
        get_latest_error=None,
        branch="master",
    ):
        """
        Adds default testing checkout, get_latest and name methods
        to mocked_scm SCM class.

        :param mmd_filenames: List of ModuleMetadata yaml files which
        will be checkouted by the SCM class in the same order as they
        are stored in the list.
        """
        self.mocked_scm = mocked_scm
        self.name = name
        self.commit = commit
        if not isinstance(mmd_filenames, list):
            mmd_filenames = [mmd_filenames]
        self.mmd_filenames = mmd_filenames
        self.checkout_id = 0
        self.sourcedir = None

        if checkout_raise:
            self.mocked_scm.return_value.checkout.side_effect = UnprocessableEntity(
                "checkout: The requested commit hash was not found within "
                "the repository. Perhaps you forgot to push. The original "
                "message was: "
            )
        else:
            self.mocked_scm.return_value.checkout = self.checkout

        self.mocked_scm.return_value.name = self.name
        self.mocked_scm.return_value.commit = self.commit
        if get_latest_raise:
            self.mocked_scm.return_value.get_latest.side_effect = \
                get_latest_error or UnprocessableEntity("Failed to get_latest commit")
        else:
            self.mocked_scm.return_value.get_latest = self.get_latest
        self.mocked_scm.return_value.repository_root = "https://src.stg.fedoraproject.org/modules/"
        self.mocked_scm.return_value.branch = branch
        self.mocked_scm.return_value.sourcedir = self.sourcedir
        self.mocked_scm.return_value.get_module_yaml = self.get_module_yaml
        self.mocked_scm.return_value.is_full_commit_hash.return_value = commit and len(commit) == 40
        self.mocked_scm.return_value.get_full_commit_hash.return_value = self.get_full_commit_hash

    def checkout(self, temp_dir):
        try:
            mmd_filename = self.mmd_filenames[self.checkout_id]
        except Exception:
            mmd_filename = self.mmd_filenames[0]

        self.sourcedir = path.join(temp_dir, self.name)
        mkdir(self.sourcedir)
        copyfile(staged_data_filename(mmd_filename), self.get_module_yaml())

        self.checkout_id += 1

        return self.sourcedir

    def get_latest(self, ref="master"):
        return hashlib.sha1(ref.encode("utf-8")).hexdigest()[:10]

    def get_module_yaml(self):
        return path.join(self.sourcedir, self.name + ".yaml")

    def get_full_commit_hash(self, commit_hash=None):
        if not commit_hash:
            commit_hash = self.commit
        sha1_hash = hashlib.sha1("random").hexdigest()
        return commit_hash + sha1_hash[len(commit_hash):]


@pytest.mark.usefixtures("provide_test_client")
@pytest.mark.usefixtures("provide_test_data_cls")
@pytest.mark.parametrize('provide_test_data_cls', [{"data_size": 2}], indirect=True)
class TestQueryModuleBuild:

    def test_query_build(self):
        rv = self.client.get("/module-build-service/1/module-builds/2")
        data = json.loads(rv.data)
        assert data["id"] == 2
        assert data["context"] == "00000000"
        assert data["name"] == "nginx"
        assert data["owner"] == "Moe Szyslak"
        assert data["scratch"] is False
        assert data["srpms"] == []
        assert data["stream"] == "1"
        assert data["siblings"] == []
        assert data["state"] == 5
        assert data["state_reason"] is None
        assert data["tasks"] == {
            "rpms": {
                "module-build-macros": {
                    "task_id": 2,
                    "state": 1,
                    "state_reason": None,
                    "nvr": "module-build-macros-01-1.module+2+b8661ee4",
                },
                "nginx": {
                    "task_id": 1,
                    "state": 1,
                    "state_reason": None,
                    "nvr": "nginx-1.10.1-2.module+2+b8661ee4",
                },
            }
        }
        assert data["time_completed"] == "2016-09-03T11:25:32Z"
        assert data["time_modified"] == "2016-09-03T11:25:32Z"
        assert data["time_submitted"] == "2016-09-03T11:23:20Z"
        assert data["rebuild_strategy"] == "changed-and-after"
        assert data["version"] == "2"

    @pytest.mark.parametrize("api_version", [0, 99])
    def test_query_builds_invalid_api_version(self, api_version):
        rv = self.client.get("/module-build-service/{0}/module-builds/".format(api_version))
        data = json.loads(rv.data)
        assert data["error"] == "Not Found"
        assert data["message"] == "The requested API version is not available"
        assert data["status"] == 404

    def test_query_build_short(self):
        rv = self.client.get("/module-build-service/1/module-builds/2?short=True")
        data = json.loads(rv.data)
        assert data["id"] == 2
        assert data["context"] == "00000000"
        assert data["name"] == "nginx"
        assert data["state"] == 5
        assert data["state_name"] == "ready"
        assert data["stream"] == "1"
        assert data["version"] == "2"
        assert data["scratch"] is False

    def test_query_build_with_verbose_mode(self):
        rv = self.client.get("/module-build-service/1/module-builds/2?verbose=true")
        data = json.loads(rv.data)
        assert data["base_module_buildrequires"] == []
        assert sorted(data["component_builds"]) == [1, 2]
        assert data["context"] == "00000000"
        # There is no xmd information on this module, so these values should be None
        assert data["build_context"] is None
        assert data["runtime_context"] is None
        assert data["id"] == 2
        assert data["modulemd"] == read_staged_data("nginx_mmd")
        assert data["name"] == "nginx"
        assert data["owner"] == "Moe Szyslak"
        assert data["rebuild_strategy"] == "changed-and-after"
        assert data["reused_module_id"] is None
        assert data["scmurl"] == \
            "git://pkgs.domain.local/modules/nginx?#ba95886c7a443b36a9ce31abda1f9bef22f2f8c9"
        assert data["scratch"] is False
        assert data["srpms"] == []
        assert data["siblings"] == []
        assert data["state"] == 5
        assert data["state_name"] == "ready"
        assert data["state_reason"] is None
        # State trace is empty because we directly created these builds and didn't have them
        # transition, which creates these entries
        assert data["state_trace"] == []
        assert data["state_url"] == "/module-build-service/1/module-builds/2"
        assert data["stream"] == "1"
        assert data["stream_version"] is None
        assert data["tasks"] == {
            "rpms": {
                "module-build-macros": {
                    "task_id": 2,
                    "state": 1,
                    "state_reason": None,
                    "nvr": "module-build-macros-01-1.module+2+b8661ee4",
                },
                "nginx": {
                    "task_id": 1,
                    "state": 1,
                    "state_reason": None,
                    "nvr": "nginx-1.10.1-2.module+2+b8661ee4",
                },
            }
        }
        assert data["time_completed"] == u"2016-09-03T11:25:32Z"
        assert data["time_modified"] == u"2016-09-03T11:25:32Z"
        assert data["time_submitted"] == u"2016-09-03T11:23:20Z"
        assert data["version"] == "2"
        assert data["virtual_streams"] == []

    def test_pagination_metadata(self):
        rv = self.client.get("/module-build-service/1/module-builds/?per_page=2&page=2")
        meta_data = json.loads(rv.data)["meta"]
        assert meta_data["prev"].split("?", 1)[1] in ["per_page=2&page=1", "page=1&per_page=2"]
        assert meta_data["next"].split("?", 1)[1] in ["per_page=2&page=3", "page=3&per_page=2"]
        assert meta_data["last"].split("?", 1)[1] in ["per_page=2&page=4", "page=4&per_page=2"]
        assert meta_data["first"].split("?", 1)[1] in ["per_page=2&page=1", "page=1&per_page=2"]
        assert meta_data["total"] == 7
        assert meta_data["per_page"] == 2
        assert meta_data["pages"] == 4
        assert meta_data["page"] == 2

    def test_pagination_metadata_with_args(self):
        rv = self.client.get("/module-build-service/1/module-builds/?per_page=2&page=2&order_by=id")
        meta_data = json.loads(rv.data)["meta"]
        for link in [meta_data["prev"], meta_data["next"], meta_data["last"], meta_data["first"]]:
            assert "order_by=id" in link
            assert "per_page=2" in link
        assert meta_data["total"] == 7
        assert meta_data["per_page"] == 2
        assert meta_data["pages"] == 4
        assert meta_data["page"] == 2

    def test_query_builds(self):
        rv = self.client.get("/module-build-service/1/module-builds/?per_page=2")
        items = json.loads(rv.data)["items"]
        expected = [
            {
                "component_builds": [11, 12],
                "context": "00000000",
                "id": 7,
                "koji_tag": None,
                "name": "testmodule",
                "owner": "some_other_user",
                "rebuild_strategy": "changed-and-after",
                "scmurl": (
                    "git://pkgs.domain.local/modules/testmodule"
                    "?#ca95886c7a443b36a9ce31abda1f9bef22f2f8c9"
                ),
                "scratch": False,
                "siblings": [],
                "srpms": [],
                "state": 1,
                "state_name": "wait",
                "state_reason": None,
                "stream": "4.3.43",
                "tasks": {
                    "rpms": {
                        "module-build-macros": {
                            "nvr": "module-build-macros-01-1.module+7+f95651e2",
                            "state": 1,
                            "state_reason": None,
                            "task_id": 47383994,
                        },
                        "rubygem-rails": {
                            "nvr": "postgresql-9.5.3-4.module+7+f95651e2",
                            "state": 3,
                            "state_reason": None,
                            "task_id": 2433434,
                        },
                    }
                },
                "time_completed": None,
                "time_modified": "2016-09-03T12:38:40Z",
                "time_submitted": "2016-09-03T12:38:33Z",
                "version": "7",
                "buildrequires": {},
            },
            {
                "component_builds": [9, 10],
                "context": "00000000",
                "id": 6,
                "koji_tag": "module-postgressql-1.2",
                "name": "postgressql",
                "owner": "some_user",
                "rebuild_strategy": "changed-and-after",
                "scmurl": (
                    "git://pkgs.domain.local/modules/postgressql"
                    "?#aa95886c7a443b36a9ce31abda1f9bef22f2f8c9"
                ),
                "scratch": False,
                "siblings": [],
                "srpms": [],
                "state": 3,
                "state_name": "done",
                "state_reason": None,
                "stream": "1",
                "tasks": {
                    "rpms": {
                        "module-build-macros": {
                            "nvr": "module-build-macros-01-1.module+6+fa947d31",
                            "state": 1,
                            "state_reason": None,
                            "task_id": 47383994,
                        },
                        "postgresql": {
                            "nvr": "postgresql-9.5.3-4.module+6+fa947d31",
                            "state": 1,
                            "state_reason": None,
                            "task_id": 2433434,
                        },
                    }
                },
                "time_completed": "2016-09-03T11:37:19Z",
                "time_modified": "2016-09-03T12:37:19Z",
                "time_submitted": "2016-09-03T12:35:33Z",
                "version": "3",
                "buildrequires": {},
            },
        ]

        for module_build in items:
            module_build["component_builds"].sort()
        assert items == expected

    def test_query_builds_with_id_error(self):
        rv = self.client.get("/module-build-service/1/module-builds/?id=1")
        actual = json.loads(rv.data)
        msg = (
            'The "id" query option is invalid. Did you mean to go to '
            '"/module-build-service/1/module-builds/1"?'
        )
        expected = {"error": "Bad Request", "message": msg, "status": 400}
        assert actual == expected

    def test_query_builds_with_nsvc(self):
        nsvcs = [
            "testmodule:4.3.43:7:00000000",
            "testmodule:4.3.43:7",
            "testmodule:4.3.43",
            "testmodule",
        ]

        results = []
        for nsvc in nsvcs:
            rv = self.client.get("/module-build-service/1/module-builds/?nsvc=%s&per_page=2" % nsvc)
            results.append(json.loads(rv.data)["items"])

        nsvc_keys = ["name", "stream", "version", "context"]

        for items, nsvc in zip(results, nsvcs):
            nsvc_parts = nsvc.split(":")
            for item in items:
                for key, part in zip(nsvc_keys, nsvc_parts):
                    assert item[key] == part

    @patch(
        "module_build_service.common.config.Config.system",
        new_callable=PropertyMock,
        return_value="invalid_builder",
    )
    def test_query_builds_with_binary_rpm_not_koji(self, mock_builder):
        rpm = quote("module-build-macros-0.1-1.testmodule_master_20170303190726.src.rpm")
        rv = self.client.get("/module-build-service/1/module-builds/?rpm=%s" % rpm)
        results = json.loads(rv.data)
        expected_error = {
            "error": "Bad Request",
            "message": "Configured builder does not allow to search by rpm binary name!",
            "status": 400,
        }
        assert rv.status_code == 400
        assert results == expected_error

    def test_query_builds_get_short_json_from_empty_list_of_builds(self):
        rv = self.client.get("/module-build-service/1/module-builds/?name=pkgname&short=true")
        data = json.loads(rv.data)
        assert [] == data["items"]
        assert 0 == data["meta"]["total"]

    # From here down, the class fixture gets overridden
    @pytest.mark.usefixtures("reuse_component_init_data")  # cleans the database
    def test_query_build_with_br_verbose_mode(self):
        rv = self.client.get("/module-build-service/1/module-builds/3?verbose=true")
        data = json.loads(rv.data)
        assert data["base_module_buildrequires"] == [{
            "context": "00000000",
            "id": 1,
            "name": "platform",
            "state": 5,
            "state_name": "ready",
            "stream": "f28",
            "stream_version": 280000,
            "version": "3",
        }]

    @patch("koji.ClientSession")
    @pytest.mark.usefixtures("reuse_component_init_data")  # cleans the database
    def test_query_builds_with_binary_rpm(self, ClientSession):
        """
        Test for querying MBS with the binary rpm filename. MBS should return all the modules,
        which contain the rpm.
        """
        # update database with builds which contain koji tags.
        mock_rpm_md = {"build_id": 1065871}
        mock_tags = [
            {"name": "module-testmodule-master-20170219191323-c40c156c"},
            {"name": "module-testmodule-master-20170219191323-c40c156c-build"},
            {"name": "non-module-tag"},
            {"name": "module-testmodule-master-20170109091357-78e4a6fd"},
        ]

        mock_session = ClientSession.return_value
        mock_session.getRPM.return_value = mock_rpm_md
        mock_session.listTags.return_value = mock_tags

        rpm = quote("module-build-macros-0.1-1.testmodule_master_20170303190726.src.rpm")
        with patch(
            "koji.read_config",
            return_value={
                "authtype": "kerberos",
                "timeout": 60,
                "server": "http://koji.example.com/",
            },
        ):
            rv = self.client.get("/module-build-service/1/module-builds/?rpm=%s" % rpm)
        results = json.loads(rv.data)["items"]

        assert len(results) == 2
        assert results[0]["koji_tag"] == "module-testmodule-master-20170219191323-c40c156c"
        assert results[1]["koji_tag"] == "module-testmodule-master-20170109091357-78e4a6fd"

        mock_session.getRPM.assert_called_once_with(
            "module-build-macros-0.1-1.testmodule_master_20170303190726.src.rpm")
        mock_session.listTags.assert_called_once_with(mock_rpm_md["build_id"])

        mock_session.krb_login.assert_not_called()

    @pytest.mark.parametrize(
        "provide_test_data", [{"data_size": 1, "contexts": True}], indirect=True
    )
    @pytest.mark.usefixtures("provide_test_data")  # cleans the database
    def test_query_builds_with_context(self):
        rv = self.client.get("/module-build-service/1/module-builds/?context=3a4057d2")
        items = json.loads(rv.data)["items"]

        checking_build_id = 3
        # Get component build ids dynamically rather than hardcode inside expected output.
        component_build_ids = db_session.query(ComponentBuild).filter(
            ComponentBuild.module_id == checking_build_id
        ).order_by(ComponentBuild.id).options(load_only("id")).all()

        expected = [
            {
                "component_builds": [cb.id for cb in component_build_ids],
                "context": "3a4057d2",
                "id": checking_build_id,
                "koji_tag": "module-nginx-1.2",
                "name": "nginx",
                "owner": "Moe Szyslak",
                "rebuild_strategy": "changed-and-after",
                "scmurl": (
                    "git://pkgs.domain.local/modules/nginx"
                    "?#ba95886c7a443b36a9ce31abda1f9bef22f2f8c9"
                ),
                "scratch": False,
                "siblings": [2],
                "srpms": [],
                "state": 5,
                "state_name": "ready",
                "state_reason": None,
                "stream": "0",
                "tasks": {
                    "rpms": {
                        "module-build-macros": {
                            "nvr": "module-build-macros-01-1.module+4+0557c87d",
                            "state": 1,
                            "state_reason": None,
                            "task_id": 47383993,
                        },
                        "postgresql": {
                            "nvr": "postgresql-9.5.3-4.module+4+0557c87d",
                            "state": 1,
                            "state_reason": None,
                            "task_id": 2433433,
                        },
                    }
                },
                "time_completed": "2016-09-03T11:25:32Z",
                "time_modified": "2016-09-03T11:25:32Z",
                "time_submitted": "2016-09-03T11:23:20Z",
                "version": "2",
                "buildrequires": {},
            }
        ]

        # To avoid different order of component builds impact the subsequent assertion.
        items[0]['component_builds'] = sorted(items[0]['component_builds'])
        assert items == expected


@pytest.mark.usefixtures("provide_test_client")
@pytest.mark.usefixtures("provide_test_data_cls")
class TestQueryComponentBuild:

    def test_query_component_build(self):
        rv = self.client.get("/module-build-service/1/component-builds/1")
        data = json.loads(rv.data)
        assert data["id"] == 1
        assert data["format"] == "rpms"
        assert data["module_build"] == 2
        assert data["nvr"] == "nginx-1.10.1-2.module+2+b8661ee4"
        assert data["package"] == "nginx"
        assert data["state"] == 1
        assert data["state_name"] == "COMPLETE"
        assert data["state_reason"] is None
        assert data["task_id"] == 1

    def test_query_component_build_short(self):
        rv = self.client.get("/module-build-service/1/component-builds/1?short=True")
        data = json.loads(rv.data)
        assert data["id"] == 1
        assert data["format"] == "rpms"
        assert data["module_build"] == 2
        assert data["nvr"] == "nginx-1.10.1-2.module+2+b8661ee4"
        assert data["package"] == "nginx"
        assert data["state"] == 1
        assert data["state_name"] == "COMPLETE"
        assert data["state_reason"] is None
        assert data["task_id"] == 1

    def test_query_component_build_verbose(self):
        rv = self.client.get("/module-build-service/1/component-builds/3?verbose=true")
        data = json.loads(rv.data)
        assert data["id"] == 3
        assert data["format"] == "rpms"
        assert data["module_build"] == 3
        assert data["nvr"] == "postgresql-9.5.3-4.module+3+0557c87d"
        assert data["package"] == "postgresql"
        assert data["state"] == 1
        assert data["state_name"] == "COMPLETE"
        assert data["state_reason"] is None
        assert data["task_id"] == 2433433
        assert data["state_trace"][0]["reason"] is None
        assert data["state_trace"][0]["time"] is not None
        assert data["state_trace"][0]["state"] == 1
        assert data["state_trace"][0]["state_name"] == "wait"
        assert data["state_url"], "/module-build-service/1/component-builds/3"

    def test_query_component_builds_trace_is_serialized_with_none_state(self):
        # Beside the module builds and their component builds created already
        # in setup_method, some new component builds with None state must be
        # created for this test to ensure the extended_json works well to
        # serialize component build trace correctly.

        module_build = make_module_in_db("cool-module:10:201907291454:c1")
        component_release = get_rpm_release(db_session, module_build)

        # No state is set.
        component_build = ComponentBuild(
            package="nginx",
            scmurl="git://pkgs.domain.local/rpms/nginx?"
                   "#ga95886c8a443b36a9ce31abda1f9bed22f2f8c3",
            format="rpms",
            task_id=1000,
            nvr="nginx-1.10.1-2.{0}".format(component_release),
            batch=1,
            module_id=module_build.id,
            tagged=True,
            tagged_in_final=True
        )
        db_session.add(component_build)
        db_session.commit()

        db_session.refresh(component_build)

        rv = self.client.get("/module-build-service/1/component-builds/?verbose=true")
        data = json.loads(rv.data)

        component_builds = [
            item for item in data["items"]
            if item["id"] == component_build.id
        ]
        assert component_builds[0]["state_trace"][0]["state_name"] is None


@pytest.mark.usefixtures("provide_test_client")
@pytest.mark.usefixtures("provide_test_data_cls")
@pytest.mark.parametrize("provide_test_data_cls", [{"data_size": 2}], indirect=True)
class TestQueryFilters:

    def test_query_component_builds_filter_format(self):
        rv = self.client.get("/module-build-service/1/component-builds/?format=rpms")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 12

    def test_query_component_builds_filter_ref(self):
        rv = self.client.get(
            "/module-build-service/1/component-builds/"
            "?ref=this-filter-query-should-return-zero-items"
        )
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 0

    def test_query_component_builds_filter_tagged(self):
        rv = self.client.get("/module-build-service/1/component-builds/?tagged=true")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 8

    def test_query_component_builds_filter_nvr(self):
        rv = self.client.get(
            "/module-build-service/1/component-builds/?nvr=nginx-1.10.1-2.module%2B2%2Bb8661ee4")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 1

    def test_query_component_builds_filter_task_id(self):
        rv = self.client.get("/module-build-service/1/component-builds/?task_id=1")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 1

    def test_query_component_builds_filter_state(self):
        rv = self.client.get("/module-build-service/1/component-builds/?state=3")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 2

    def test_query_component_builds_filter_multiple_states(self):
        rv = self.client.get("/module-build-service/1/component-builds/?state=3&state=1")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 12

    def test_query_builds_filter_name(self):
        rv = self.client.get("/module-build-service/1/module-builds/?name=nginx")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 2

    def test_query_builds_filter_koji_tag(self):
        rv = self.client.get("/module-build-service/1/module-builds/?koji_tag=module-nginx-1.2")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 2

    def test_query_builds_filter_completed_before(self):
        rv = self.client.get(
            "/module-build-service/1/module-builds/?completed_before=2016-09-03T11:30:00Z")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 2

    def test_query_builds_filter_completed_after(self):
        rv = self.client.get(
            "/module-build-service/1/module-builds/?completed_after=2016-09-03T11:35:00Z")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 3

    def test_query_builds_filter_submitted_before(self):
        rv = self.client.get(
            "/module-build-service/1/module-builds/?submitted_before=2016-09-03T11:35:00Z")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 2

    def test_query_builds_filter_submitted_after(self):
        rv = self.client.get(
            "/module-build-service/1/module-builds/?submitted_after=2016-09-03T11:35:00Z")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 5

    def test_query_builds_filter_modified_before(self):
        rv = self.client.get(
            "/module-build-service/1/module-builds/?modified_before=2016-09-03T11:35:00Z")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 1

    def test_query_builds_filter_modified_after(self):
        rv = self.client.get(
            "/module-build-service/1/module-builds/?modified_after=2016-09-03T11:35:00Z")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 6

    def test_query_builds_filter_owner(self):
        rv = self.client.get("/module-build-service/1/module-builds/?owner=Moe%20Szyslak")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 2

    def test_query_builds_filter_state(self):
        rv = self.client.get("/module-build-service/1/module-builds/?state=3")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 2

    def test_query_builds_filter_multiple_states(self):
        rv = self.client.get("/module-build-service/1/module-builds/?state=3&state=1")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 4

    def test_query_builds_two_filters(self):
        rv = self.client.get(
            "/module-build-service/1/module-builds/?owner=Moe%20Szyslak"
            "&modified_after=2016-09-03T11:35:00Z"
        )
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 1

    def test_query_builds_filter_nsv(self):
        rv = self.client.get(
            "/module-build-service/1/module-builds/?name=postgressql&stream=1&version=2")
        data = json.loads(rv.data)
        for item in data["items"]:
            assert item["name"] == "postgressql"
            assert item["stream"] == "1"
            assert item["version"] == "2"
        assert data["meta"]["total"] == 1

    def test_query_builds_filter_invalid_date(self):
        rv = self.client.get(
            "/module-build-service/1/module-builds/?modified_after=2016-09-03T12:25:00-05:00")
        data = json.loads(rv.data)
        assert data["error"] == "Bad Request"
        assert data["message"] == \
            "An invalid Zulu ISO 8601 timestamp was " 'provided for the "modified_after" parameter'
        assert data["status"] == 400

    def test_query_builds_order_by(self):
        build = ModuleBuild.get_by_id(db_session, 2)
        build.name = "candy"
        db_session.commit()
        rv = self.client.get("/module-build-service/1/module-builds/?per_page=10&order_by=name")
        items = json.loads(rv.data)["items"]
        assert items[0]["name"] == "candy"
        assert items[1]["name"] == "nginx"

    def test_query_builds_order_desc_by(self):
        rv = self.client.get(
            "/module-build-service/1/module-builds/?per_page=10&order_desc_by=id")
        items = json.loads(rv.data)["items"]
        # Check that the id is items[0]["id"], items[0]["id"] - 1, ...
        for idx, item in enumerate(items):
            assert item["id"] == items[0]["id"] - idx

    def test_query_builds_order_by_order_desc_by(self):
        """
        Test that when both order_by and order_desc_by are set, an error is returned.
        """
        rv = self.client.get(
            "/module-build-service/1/module-builds/?per_page=10&order_desc_by=id&order_by=name")
        error = json.loads(rv.data)
        expected = {
            "error": "Bad Request",
            "message": "You may not specify both order_by and order_desc_by",
            "status": 400,
        }
        assert error == expected

    def test_query_builds_order_by_wrong_key(self):
        rv = self.client.get(
            "/module-build-service/1/module-builds/?per_page=10&order_by=unknown")
        error = json.loads(rv.data)
        expected = {
            "error": "Bad Request",
            "message": 'An invalid ordering key of "unknown" was supplied',
            "status": 400,
        }
        assert error == expected

    def test_query_builds_order_by_multiple(self):
        platform_f28 = ModuleBuild.get_by_id(db_session, 1)
        platform_f28.version = "150"
        db_session.commit()
        # Simply assert the order of all module builds
        page_size = db_session.query(ModuleBuild).count()
        rv = self.client.get(
            "/module-build-service/1/module-builds/?order_desc_by=stream_version"
            "&order_desc_by=version&per_page={}".format(page_size)
        )
        items = json.loads(rv.data)["items"]
        actual_ids = [item["id"] for item in items]

        expected_ids = [
            build.id for build in db_session.query(ModuleBuild).order_by(
                ModuleBuild.stream_version.desc(),
                sqlalchemy.cast(ModuleBuild.version, sqlalchemy.BigInteger).desc()
            ).all()
        ]
        assert actual_ids == expected_ids

    # From here down, the class fixture gets overridden
    @pytest.mark.parametrize(
        "provide_test_data", [{"data_size": 2, "contexts": True}], indirect=True
    )
    @pytest.mark.usefixtures("provide_test_data")  # cleans the database
    def test_query_builds_order_desc_by_context(self):
        rv = self.client.get(
            "/module-build-service/1/module-builds/?per_page=10&name=nginx&order_desc_by=context")
        sorted_items = json.loads(rv.data)["items"]
        sorted_contexts = [m["context"] for m in sorted_items]

        expected_contexts = ["d5a6c0fa", "795e97c1", "3a4057d2", "10e50d06"]
        assert sorted_contexts == expected_contexts

    @pytest.mark.usefixtures("reuse_component_init_data")  # cleans the database
    def test_query_base_module_br_filters(self):
        mmd = load_mmd(read_staged_data("platform"))
        mmd = mmd.copy(mmd.get_module_name(), "f30.1.3")
        import_mmd(db_session, mmd)
        platform_f300103 = db_session.query(ModuleBuild).filter_by(stream="f30.1.3").one()
        build = ModuleBuild(
            name="testmodule",
            stream="master",
            version=20170109091357,
            state=5,
            build_context="dd4de1c346dcf09ce77d38cd4e75094ec1c08ec3",
            runtime_context="ec4de1c346dcf09ce77d38cd4e75094ec1c08ef7",
            context="7c29193d",
            koji_tag="module-testmodule-master-20170109091357-7c29193d",
            scmurl="https://src.stg.fedoraproject.org/modules/testmodule.git?#ff1ea79",
            batch=3,
            owner="Dr. Pepper",
            time_submitted=datetime(2018, 11, 15, 16, 8, 18),
            time_modified=datetime(2018, 11, 15, 16, 19, 35),
            rebuild_strategy="changed-and-after",
            modulemd=read_staged_data("testmodule"),
        )
        build.buildrequires.append(platform_f300103)
        db_session.add(build)
        db_session.commit()
        # Query by NSVC
        rv = self.client.get(
            "/module-build-service/1/module-builds/?base_module_br=platform:f28:3:00000000")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 2
        rv = self.client.get(
            "/module-build-service/1/module-builds/?base_module_br=platform:f30.1.3:3:00000000")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 1
        # Query by non-existent NVC
        rv = self.client.get(
            "/module-build-service/1/module-builds/?base_module_br=platform:f12:3:00000000")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 0
        # Query by name and stream
        rv = self.client.get(
            "/module-build-service/1/module-builds/?base_module_br_name=platform"
            "&base_module_br_stream=f28"
        )
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 2
        # Query by stream version
        rv = self.client.get(
            "/module-build-service/1/module-builds/?base_module_br_stream_version=280000")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 2
        # Query by lte stream version
        rv = self.client.get(
            "/module-build-service/1/module-builds/?base_module_br_stream_version_lte=290000")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 2
        # Query by lte stream version with no results
        rv = self.client.get(
            "/module-build-service/1/module-builds/?base_module_br_stream_version_lte=270000")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 0
        # Query by gte stream version
        rv = self.client.get(
            "/module-build-service/1/module-builds/?base_module_br_stream_version_gte=270000")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 3
        # Query by gte stream version with no results
        rv = self.client.get(
            "/module-build-service/1/module-builds/?base_module_br_stream_version_gte=320000")
        data = json.loads(rv.data)
        assert data["meta"]["total"] == 0

    @pytest.mark.parametrize(
        "stream_version_lte",
        ("280000", "280000.0", "290000", "293000", "invalid"),
    )
    @pytest.mark.parametrize(
        'provide_test_data', [{"data_size": 1, "multiple_stream_versions": True}], indirect=True
    )
    @pytest.mark.usefixtures("provide_test_data")  # cleans the database
    def test_query_builds_filter_stream_version_lte(self, stream_version_lte, ):
        url = (
            "/module-build-service/1/module-builds/?name=platform&verbose=true"
            "&stream_version_lte={}".format(stream_version_lte)
        )
        rv = self.client.get(url)
        data = json.loads(rv.data)
        total = data.get("meta", {}).get("total")
        if stream_version_lte == "invalid":
            assert data == {
                "error": "Bad Request",
                "message": (
                    "An invalid value of stream_version_lte was provided. It must be an "
                    "integer or float greater than or equal to 10000."
                ),
                "status": 400,
            }
        elif stream_version_lte in ("280000", "280000.0"):
            assert total == 2
        elif stream_version_lte == "290000":
            assert total == 1
        elif stream_version_lte == "293000":
            assert total == 3

    @pytest.mark.parametrize("virtual_streams", ([], ("f28",), ("f29",), ("f28", "f29")))
    @pytest.mark.parametrize(
        'provide_test_data', [{"data_size": 1, "multiple_stream_versions": True}], indirect=True
    )
    @pytest.mark.usefixtures("provide_test_data")  # cleans the database
    def test_query_builds_filter_virtual_streams(self, virtual_streams):
        url = "/module-build-service/1/module-builds/?name=platform&verbose=true"
        for virtual_stream in virtual_streams:
            url += "&virtual_stream={}".format(virtual_stream)
        rv = self.client.get(url)
        data = json.loads(rv.data)
        total = data["meta"]["total"]
        if virtual_streams == ("f28",):
            assert total == 1
            for module in data["items"]:
                assert module["virtual_streams"] == ["f28"]
        elif virtual_streams == ("f29",):
            assert total == 3
            for module in data["items"]:
                assert module["virtual_streams"] == ["f29"]
        elif virtual_streams == ("f28", "f29"):
            assert total == 4
            for module in data["items"]:
                assert len(set(module["virtual_streams"]) - {"f28", "f29"}) == 0
        elif len(virtual_streams) == 0:
            assert total == 5


@pytest.mark.usefixtures("provide_test_client")
@pytest.mark.usefixtures("require_platform_and_default_arch")
class TestSubmitBuild:

    @pytest.mark.parametrize("api_version", [1, 2])
    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build(self, mocked_scm, mocked_get_user, api_version):
        FakeSCM(
            mocked_scm, "testmodule", "testmodule.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4")

        post_url = "/module-build-service/{0}/module-builds/".format(api_version)
        rv = self.client.post(
            post_url,
            data=json.dumps({
                "branch": "master",
                "scmurl": "https://src.stg.fedoraproject.org/modules/"
                          "testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49",
            }),
        )
        data = json.loads(rv.data)
        build_id = 2  # (platform required)

        if api_version >= 2:
            assert isinstance(data, list)
            assert len(data) == 1
            data = data[0]

        assert "component_builds" in data, data
        assert data["component_builds"] == []
        assert data["name"] == "testmodule"
        assert data["scmurl"] == (
            "https://src.stg.fedoraproject.org/modules/testmodule.git"
            "?#68931c90de214d9d13feefbd35246a81b6cb8d49"
        )
        assert data["version"] == "281"
        assert data["time_submitted"] is not None
        assert data["time_modified"] is not None
        assert data["time_completed"] is None
        assert data["stream"] == "master"
        assert data["owner"] == "Homer J. Simpson"
        assert data["id"] == build_id
        assert data["rebuild_strategy"] == "changed-and-after"
        assert data["state_name"] == "init"
        assert data["state_url"] == "/module-build-service/{0}/module-builds/{1}" \
            .format(api_version, build_id)
        assert len(data["state_trace"]) == 1
        assert data["state_trace"][0]["state"] == 0
        assert data["tasks"] == {}
        assert data["siblings"] == []
        load_mmd(data["modulemd"])

        # Make sure the buildrequires entry was created
        module = ModuleBuild.get_by_id(db_session, build_id)
        assert len(module.buildrequires) == 1
        assert module.buildrequires[0].name == "platform"
        assert module.buildrequires[0].stream == "f28"
        assert module.buildrequires[0].version == "3"
        assert module.buildrequires[0].context == "00000000"
        assert module.buildrequires[0].stream_version == 280000

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_no_base_module(self, mocked_scm, mocked_get_user):
        FakeSCM(
            mocked_scm,
            "testmodule",
            "testmodule-no-base-module.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4",
        )

        rv = self.client.post(
            "/module-build-service/2/module-builds/",
            data=json.dumps({
                "branch": "master",
                "scmurl": "https://src.stg.fedoraproject.org/modules/"
                          "testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49",
            }),
        )
        data = json.loads(rv.data)
        assert data == {
            "status": 422,
            "message": (
                "None of the base module (platform) streams in the buildrequires section "
                "could be found"
            ),
            "error": "Unprocessable Entity",
        }

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    @patch(
        "module_build_service.common.config.Config.rebuild_strategy_allow_override",
        new_callable=PropertyMock,
        return_value=True,
    )
    def test_submit_build_rebuild_strategy(self, mocked_rmao, mocked_scm, mocked_get_user):
        FakeSCM(
            mocked_scm, "testmodule", "testmodule.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4")

        rv = self.client.post(
            "/module-build-service/1/module-builds/",
            data=json.dumps({
                "branch": "master",
                "rebuild_strategy": "only-changed",
                "scmurl": (
                    "https://src.stg.fedoraproject.org/modules/testmodule.git?"
                    "#68931c90de214d9d13feefbd35246a81b6cb8d49"
                ),
            }),
        )
        data = json.loads(rv.data)
        assert data["rebuild_strategy"] == "only-changed"

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    @patch(
        "module_build_service.common.config.Config.rebuild_strategies_allowed",
        new_callable=PropertyMock,
        return_value=["all"],
    )
    @patch(
        "module_build_service.common.config.Config.rebuild_strategy_allow_override",
        new_callable=PropertyMock,
        return_value=True,
    )
    def test_submit_build_rebuild_strategy_not_allowed(
            self, mock_rsao, mock_rsa, mocked_scm, mocked_get_user
    ):
        FakeSCM(
            mocked_scm, "testmodule", "testmodule.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4")

        rv = self.client.post(
            "/module-build-service/1/module-builds/",
            data=json.dumps({
                "branch": "master",
                "rebuild_strategy": "only-changed",
                "scmurl": (
                    "https://src.stg.fedoraproject.org/modules/testmodule.git?"
                    "#68931c90de214d9d13feefbd35246a81b6cb8d49"
                ),
            }),
        )
        data = json.loads(rv.data)
        assert rv.status_code == 400
        expected_error = {
            "error": "Bad Request",
            "message": ('The rebuild method of "only-changed" is not allowed. Choose from: all.'),
            "status": 400,
        }
        assert data == expected_error

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_dep_not_present(self, mocked_scm, mocked_get_user):
        FakeSCM(
            mocked_scm,
            "testmodule",
            "testmodule-no-deps.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4",
        )

        rv = self.client.post(
            "/module-build-service/1/module-builds/",
            data=json.dumps({
                "branch": "master",
                "scmurl": (
                    "https://src.stg.fedoraproject.org/modules/testmodule.git?"
                    "#68931c90de214d9d13feefbd35246a81b6cb8d49"
                ),
            }),
        )
        data = json.loads(rv.data)
        assert rv.status_code == 422
        expected_error = {
            "error": "Unprocessable Entity",
            "message": "Cannot find any module builds for chineese_food:good",
            "status": 422,
        }
        assert data == expected_error

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_rebuild_strategy_override_not_allowed(self, mocked_scm, mocked_get_user):
        FakeSCM(
            mocked_scm, "testmodule", "testmodule.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4")

        rv = self.client.post(
            "/module-build-service/1/module-builds/",
            data=json.dumps({
                "branch": "master",
                "rebuild_strategy": "only-changed",
                "scmurl": (
                    "https://src.stg.fedoraproject.org/modules/testmodule.git?"
                    "#68931c90de214d9d13feefbd35246a81b6cb8d49"
                ),
            }),
        )
        data = json.loads(rv.data)
        assert rv.status_code == 400
        expected_error = {
            "error": "Bad Request",
            "message": (
                'The request contains the "rebuild_strategy" parameter but overriding '
                "the default isn't allowed"
            ),
            "status": 400,
        }
        assert data == expected_error

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_componentless_build(self, mocked_scm, mocked_get_user):
        FakeSCM(
            mocked_scm, "fakemodule", "fakemodule.yaml",
            "3da541559918a808c2402bba5012f6c60b27661c")

        rv = self.client.post(
            "/module-build-service/1/module-builds/",
            data=json.dumps({
                "branch": "master",
                "scmurl": "https://src.stg.fedoraproject.org/modules/"
                          "testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49",
            }),
        )
        data = json.loads(rv.data)
        build_id = 2  # (platform required)

        assert data["component_builds"] == []
        assert data["name"] == "fakemodule"
        assert data["scmurl"] == (
            "https://src.stg.fedoraproject.org/modules/testmodule.git"
            "?#68931c90de214d9d13feefbd35246a81b6cb8d49"
        )
        assert data["version"] == "281"
        assert data["time_submitted"] is not None
        assert data["time_modified"] is not None
        assert data["time_completed"] is None
        assert data["stream"] == "master"
        assert data["owner"] == "Homer J. Simpson"
        assert data["id"] == build_id
        assert data["state_name"] == "init"
        assert data["rebuild_strategy"] == "changed-and-after"

    def test_submit_build_auth_error(self):
        base_dir = path.abspath(path.dirname(__file__))
        client_secrets = path.join(base_dir, "client_secrets.json")
        with patch.dict("module_build_service.app.config",
                        {"OIDC_CLIENT_SECRETS": client_secrets}):
            rv = self.client.post(
                "/module-build-service/1/module-builds/",
                data=json.dumps({
                    "branch": "master",
                    "scmurl": "https://src.stg.fedoraproject.org/modules/"
                              "testmodule.git?#48931b90de214d9d13feefbd35246a81b6cb8d49",
                }),
            )
            data = json.loads(rv.data)
            assert data["message"] == "No 'authorization' header found."
            assert data["status"] == 401
            assert data["error"] == "Unauthorized"

    @patch("module_build_service.web.auth.get_user", return_value=user)
    def test_submit_build_scm_url_error(self, mocked_get_user):
        rv = self.client.post(
            "/module-build-service/1/module-builds/",
            data=json.dumps({"branch": "master", "scmurl": "git://badurl.com"}),
        )
        data = json.loads(rv.data)
        assert data["message"] == "The submitted scmurl git://badurl.com is not allowed"
        assert data["status"] == 403
        assert data["error"] == "Forbidden"

    @patch("module_build_service.web.auth.get_user", return_value=user)
    def test_submit_build_scm_url_without_hash(self, mocked_get_user):
        rv = self.client.post(
            "/module-build-service/1/module-builds/",
            data=json.dumps({
                "branch": "master",
                "scmurl": "https://src.stg.fedoraproject.org/modules/testmodule.git",
            }),
        )
        data = json.loads(rv.data)
        assert data["message"] == (
            "The submitted scmurl https://src.stg.fedoraproject.org"
            "/modules/testmodule.git is not valid"
        )
        assert data["status"] == 400
        assert data["error"] == "Bad Request"

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_bad_modulemd(self, mocked_scm, mocked_get_user):
        FakeSCM(mocked_scm, "bad", "bad.yaml")

        rv = self.client.post(
            "/module-build-service/1/module-builds/",
            data=json.dumps({
                "branch": "master",
                "scmurl": "https://src.stg.fedoraproject.org/modules/"
                          "testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49",
            }),
        )
        data = json.loads(rv.data)
        assert re.match(
            r"The modulemd .* is invalid\. ",
            data["message"]
        )
        assert "Please verify the syntax is correct" in data["message"]
        assert data["status"] == 422
        assert data["error"] == "Unprocessable Entity"

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_includedmodule_custom_repo_not_allowed(self, mocked_scm,
                                                                 mocked_get_user):
        FakeSCM(mocked_scm, "includedmodules", ["includedmodules.yaml", "testmodule.yaml"])
        rv = self.client.post(
            "/module-build-service/1/module-builds/",
            data=json.dumps({
                "branch": "master",
                "scmurl": "https://src.stg.fedoraproject.org/modules/"
                          "testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49",
            }),
        )
        data = json.loads(rv.data)

        assert data["status"] == 403
        assert data["error"] == "Forbidden"

    @patch("module_build_service.web.auth.get_user", return_value=user)
    def test_submit_build_unsupported_scm_scheme(self, mocked_get_user):
        scmurl = "unsupported://example.com/modules/"
        "testmodule.git?#0000000000000000000000000000000000000000"
        rv = self.client.post(
            "/module-build-service/1/module-builds/",
            data=json.dumps({"branch": "master", "scmurl": scmurl}),
        )
        data = json.loads(rv.data)
        assert data["message"] in (
            "The submitted scmurl {} is not allowed".format(scmurl),
            "The submitted scmurl {} is not valid".format(scmurl),
        )
        assert data["status"] in (400, 403)
        assert data["error"] in ("Bad Request", "Forbidden")

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_version_set_error(self, mocked_scm, mocked_get_user):
        FakeSCM(
            mocked_scm,
            "testmodule",
            "testmodule-version-set.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4",
        )

        rv = self.client.post(
            "/module-build-service/1/module-builds/",
            data=json.dumps({
                "branch": "master",
                "scmurl": "https://src.stg.fedoraproject.org/modules/"
                          "testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49",
            }),
        )
        data = json.loads(rv.data)
        assert data["status"] == 400
        assert data["message"] == (
            'The version "123456789" is already defined in the modulemd but it shouldn\'t be since '
            "the version is generated based on the commit time"
        )
        assert data["error"] == "Bad Request"

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_wrong_stream(self, mocked_scm, mocked_get_user):
        FakeSCM(
            mocked_scm,
            "testmodule",
            "testmodule-wrong-stream.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4",
        )

        rv = self.client.post(
            "/module-build-service/1/module-builds/",
            data=json.dumps({
                "branch": "master",
                "scmurl": "https://src.stg.fedoraproject.org/modules/"
                          "testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49",
            }),
        )
        data = json.loads(rv.data)
        assert data["status"] == 400
        assert data["message"] == (
            'The stream "wrong_stream" that is stored in the modulemd '
            'does not match the branch "master"'
        )
        assert data["error"] == "Bad Request"

    @patch("module_build_service.web.auth.get_user", return_value=user)
    def test_submit_build_set_owner(self, mocked_get_user):
        data = {
            "branch": "master",
            "scmurl": "https://src.stg.fedoraproject.org/modules/"
                      "testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49",
            "owner": "foo",
        }
        rv = self.client.post("/module-build-service/1/module-builds/", data=json.dumps(data))
        result = json.loads(rv.data)
        assert result["status"] == 400
        assert "The request contains 'owner' parameter" in result["message"]

    @patch("module_build_service.web.auth.get_user", return_value=anonymous_user)
    @patch("module_build_service.common.scm.SCM")
    @patch(
        "module_build_service.common.config.Config.no_auth",
        new_callable=PropertyMock,
        return_value=True,
    )
    def test_submit_build_no_auth_set_owner(self, mocked_conf, mocked_scm, mocked_get_user):
        FakeSCM(
            mocked_scm, "testmodule", "testmodule.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4")

        data = {
            "branch": "master",
            "scmurl": "https://src.stg.fedoraproject.org/modules/"
                      "testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49",
            "owner": "foo",
        }
        rv = self.client.post("/module-build-service/1/module-builds/", data=json.dumps(data))
        result = json.loads(rv.data)

        build = ModuleBuild.get_by_id(db_session, result["id"])
        assert (build.owner == result["owner"] == "foo") is True

    @patch("module_build_service.web.auth.get_user", return_value=("svc_account", set()))
    @patch("module_build_service.common.scm.SCM")
    @patch("module_build_service.common.config.Config.allowed_users", new_callable=PropertyMock)
    def test_submit_build_allowed_users(self, allowed_users, mocked_scm, mocked_get_user):
        FakeSCM(
            mocked_scm, "testmodule", "testmodule.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4")

        allowed_users.return_value = {"svc_account"}
        data = {
            "branch": "master",
            "scmurl": "https://src.stg.fedoraproject.org/modules/"
                      "testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49",
        }
        rv = self.client.post("/module-build-service/1/module-builds/", data=json.dumps(data))
        assert rv.status_code == 201

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_commit_hash_not_found(self, mocked_scm, mocked_get_user):
        FakeSCM(
            mocked_scm,
            "testmodule",
            "testmodule.yaml",
            "7035bd33614972ac66559ac1fdd019ff6027ad22",
            checkout_raise=True,
        )

        rv = self.client.post(
            "/module-build-service/1/module-builds/",
            data=json.dumps({
                "branch": "master",
                "scmurl": "https://src.stg.fedoraproject.org/modules/"
                          "testmodule.git?#7035bd33614972ac66559ac1fdd019ff6027ad22",
            }),
        )
        data = json.loads(rv.data)
        assert "The requested commit hash was not found within the repository." in data["message"]
        assert "Perhaps you forgot to push. The original message was: " in data["message"]
        assert data["status"] == 422
        assert data["error"] == "Unprocessable Entity"

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    @patch(
        "module_build_service.common.config.Config.allow_custom_scmurls",
        new_callable=PropertyMock,
    )
    def test_submit_custom_scmurl(self, allow_custom_scmurls, mocked_scm, mocked_get_user):
        FakeSCM(
            mocked_scm, "testmodule", "testmodule.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4")

        def submit(scmurl):
            return self.client.post(
                "/module-build-service/1/module-builds/",
                data=json.dumps({"branch": "master", "scmurl": scmurl}),
            )

        allow_custom_scmurls.return_value = False
        res1 = submit("git://some.custom.url.org/modules/testmodule.git?#68931c9")
        data = json.loads(res1.data)
        assert data["status"] == 403
        assert data["message"].startswith("The submitted scmurl") is True
        assert data["message"].endswith("is not allowed") is True

        allow_custom_scmurls.return_value = True
        res2 = submit("git://some.custom.url.org/modules/testmodule.git?#68931c9")
        assert res2.status_code == 201

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_with_base_module_name(self, mocked_scm, mocked_get_user):
        FakeSCM(
            mocked_scm, "platform", "testmodule.yaml", "620ec77321b2ea7b0d67d82992dda3e1d67055b4")

        data = {
            "branch": "master",
            "scmurl": "https://src.stg.fedoraproject.org/modules/"
                      "platform.git?#68931c90de214d9d13feefbd35246a81b6cb8d49",
        }
        rv = self.client.post("/module-build-service/1/module-builds/", data=json.dumps(data))
        result = json.loads(rv.data)
        assert result == {
            "error": "Bad Request",
            "status": 400,
            "message": 'You cannot build a module named "platform" since it is a base module',
        }
        assert rv.status_code == 400

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_with_xmd(self, mocked_scm, mocked_get_user):
        FakeSCM(
            mocked_scm,
            "testmodule",
            "testmodule-forbidden-xmd.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4",
        )

        data = {
            "branch": "master",
            "scmurl": "https://src.stg.fedoraproject.org/modules/"
                      "testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49",
        }
        rv = self.client.post("/module-build-service/1/module-builds/", data=json.dumps(data))
        result = json.loads(rv.data)
        assert result == {
            "error": "Bad Request",
            "status": 400,
            "message": 'The "mbs" xmd field is reserved for MBS',
        }
        assert rv.status_code == 400

    @pytest.mark.parametrize("dep_type", ("buildrequire", "require"))
    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_override_unused(self, mocked_scm, mocked_get_user, dep_type):
        FakeSCM(
            mocked_scm,
            "testmodule",
            "testmodule_platform_f290000.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4",
        )

        post_url = "/module-build-service/2/module-builds/"
        scm_url = (
            "https://src.stg.fedoraproject.org/modules/testmodule.git?#68931c90de214d9d13f"
            "eefbd35246a81b6cb8d49"
        )
        json_input = {"branch": "master", "scmurl": scm_url}
        json_input[dep_type + "_overrides"] = {"nonexistent": ["23"], "nonexistent2": ["2"]}

        rv = self.client.post(post_url, data=json.dumps(json_input))
        data = json.loads(rv.data)

        assert data == {
            "error": "Bad Request",
            "message": (
                "The {} overrides for the following modules aren't applicable: "
                "nonexistent, nonexistent2"
            ).format(dep_type),
            "status": 400,
        }

    @pytest.mark.parametrize(
        "optional_params",
        (
            {"buildrequire_overrides": {"platform": "f28"}},
            {"buildrequire_overrides": {"platform": 28}},
            {"buildrequire_overrides": "platform:f28"},
            {"require_overrides": {"platform": "f28"}},
            {"require_overrides": {"platform": 28}},
            {"require_overrides": "platform:f28"},
        ),
    )
    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_invalid_override(self, mocked_scm, mocked_get_user, optional_params):
        FakeSCM(
            mocked_scm,
            "testmodule",
            "testmodule_platform_f290000.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4",
        )

        post_url = "/module-build-service/2/module-builds/"
        scm_url = (
            "https://src.stg.fedoraproject.org/modules/testmodule.git?#"
            "68931c90de214d9d13feefbd35246a81b6cb8d49"
        )
        json_input = {"branch": "master", "scmurl": scm_url}
        json_input.update(optional_params)

        rv = self.client.post(post_url, data=json.dumps(json_input))
        data = json.loads(rv.data)

        msg = (
            'The "{}" parameter must be an object with the keys as module names and the values '
            "as arrays of streams"
        )
        if "buildrequire_overrides" in optional_params:
            msg = msg.format("buildrequire_overrides")
        elif "require_overrides" in optional_params:
            msg = msg.format("require_overrides")
        assert data == {"error": "Bad Request", "message": msg, "status": 400}

    @pytest.mark.parametrize("api_version", [1, 2])
    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_module_name_override_not_allowed(
            self, mocked_scm, mocked_get_user, api_version
    ):
        FakeSCM(
            mocked_scm, "testmodule", "testmodule.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4")

        post_url = "/module-build-service/{0}/module-builds/".format(api_version)
        rv = self.client.post(
            post_url,
            data=json.dumps({
                "branch": "master",
                "scmurl": "https://src.stg.fedoraproject.org/modules/"
                          "testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49",
                "module_name": "altname",
            }),
        )
        # module name is allowed only when a modulemd file is submitted
        assert rv.status_code == 400
        result = json.loads(rv.data)
        assert result["error"] == "Bad Request"
        assert result["message"] == (
            "Module name override is only allowed when a YAML file is submitted"
        )

    @pytest.mark.parametrize("api_version", [1, 2])
    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_stream_name_override_not_allowed(
            self, mocked_scm, mocked_get_user, api_version
    ):
        FakeSCM(
            mocked_scm, "testmodule", "testmodule.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4")

        post_url = "/module-build-service/{0}/module-builds/".format(api_version)
        rv = self.client.post(
            post_url,
            data=json.dumps({
                "branch": "master",
                "scmurl": "https://src.stg.fedoraproject.org/modules/"
                          "testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49",
                "module_stream": "altstream",
            }),
        )
        # stream name override is allowed only when a modulemd file is submitted
        assert rv.status_code == 400
        result = json.loads(rv.data)
        assert result["error"] == "Bad Request"
        assert result["message"] == (
            "Stream name override is only allowed when a YAML file is submitted"
        )

    @pytest.mark.parametrize("api_version", [1, 2])
    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    @patch(
        "module_build_service.common.config.Config.modules_allow_scratch",
        new_callable=PropertyMock,
        return_value=True,
    )
    def test_submit_scratch_build(
            self, mocked_allow_scratch, mocked_scm, mocked_get_user, api_version
    ):
        FakeSCM(
            mocked_scm, "testmodule", "testmodule.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4")

        post_url = "/module-build-service/{0}/module-builds/".format(api_version)
        post_data = {
            "branch": "master",
            "scmurl": "https://src.stg.fedoraproject.org/modules/"
                      "testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49",
            "scratch": True,
        }
        rv = self.client.post(post_url, data=json.dumps(post_data))
        data = json.loads(rv.data)

        if api_version >= 2:
            assert isinstance(data, list)
            assert len(data) == 1
            data = data[0]

        assert "component_builds" in data, data
        assert data["component_builds"] == []
        assert data["name"] == "testmodule"
        assert data["scmurl"] == (
            "https://src.stg.fedoraproject.org/modules/testmodule.git"
            "?#68931c90de214d9d13feefbd35246a81b6cb8d49"
        )
        assert data["scratch"] is True
        assert data["version"] == "281"
        assert data["time_submitted"] is not None
        assert data["time_modified"] is not None
        assert data["time_completed"] is None
        assert data["stream"] == "master"
        assert data["owner"] == "Homer J. Simpson"
        assert data["id"] == 2
        assert data["rebuild_strategy"] == "changed-and-after"
        assert data["state_name"] == "init"
        assert data["state_url"] == "/module-build-service/{0}/module-builds/2".format(api_version)
        assert len(data["state_trace"]) == 1
        assert data["state_trace"][0]["state"] == 0
        assert data["tasks"] == {}
        assert data["siblings"] == []
        load_mmd(data["modulemd"])

        # Make sure the buildrequires entry was created
        module = ModuleBuild.get_by_id(db_session, 2)
        assert len(module.buildrequires) == 1
        assert module.buildrequires[0].name == "platform"
        assert module.buildrequires[0].stream == "f28"
        assert module.buildrequires[0].version == "3"
        assert module.buildrequires[0].context == "00000000"
        assert module.buildrequires[0].stream_version == 280000

    @pytest.mark.parametrize("api_version", [1, 2])
    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    @patch(
        "module_build_service.common.config.Config.modules_allow_scratch",
        new_callable=PropertyMock,
        return_value=False,
    )
    def test_submit_scratch_build_not_allowed(
            self, mocked_allow_scratch, mocked_scm, mocked_get_user, api_version
    ):
        FakeSCM(
            mocked_scm, "testmodule", "testmodule.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4")

        post_url = "/module-build-service/{0}/module-builds/".format(api_version)
        post_data = {
            "branch": "master",
            "scmurl": "https://src.stg.fedoraproject.org/modules/"
                      "testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49",
            "scratch": True,
        }
        rv = self.client.post(post_url, data=json.dumps(post_data))
        data = json.loads(rv.data)
        expected_error = {
            "error": "Forbidden",
            "message": "Scratch builds are not enabled",
            "status": 403,
        }
        assert data == expected_error
        assert rv.status_code == expected_error["status"]

    @pytest.mark.parametrize("api_version", [1, 2])
    @pytest.mark.parametrize("mod_stream", [None, "alternate"])
    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch(
        "module_build_service.common.config.Config.yaml_submit_allowed",
        new_callable=PropertyMock,
        return_value=True,
    )
    def test_submit_build_with_mmd(
            self, mocked_allow_yaml, mocked_get_user, mod_stream, api_version
    ):
        modulemd = read_staged_data("testmodule")

        post_data = {
            "branch": "master",
            "modulemd": modulemd,
            "module_name": str(splitext(basename(staged_data_filename("testmodule")))[0]),
        }
        if mod_stream:
            post_data["module_stream"] = mod_stream
            expected_stream = mod_stream
        else:
            expected_stream = "master"
        post_url = "/module-build-service/{0}/module-builds/".format(api_version)
        rv = self.client.post(post_url, data=json.dumps(post_data))
        data = json.loads(rv.data)

        if api_version >= 2:
            assert isinstance(data, list)
            assert len(data) == 1
            data = data[0]

        assert data["name"] == "testmodule"
        assert data["scratch"] is False
        assert data["stream"] == expected_stream
        # Assertions for other "testmodule" attributes are done in
        # test_submit_scratch_build_with_mmd()

    @pytest.mark.parametrize("api_version", [1, 2])
    @pytest.mark.parametrize("mod_stream", [None, "alternate"])
    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch(
        "module_build_service.common.config.Config.modules_allow_scratch",
        new_callable=PropertyMock,
        return_value=True,
    )
    @patch(
        "module_build_service.common.config.Config.yaml_submit_allowed",
        new_callable=PropertyMock,
        return_value=True,
    )
    def test_submit_scratch_build_with_mmd(
            self, mocked_allow_yaml, mocked_allow_scratch, mocked_get_user, mod_stream, api_version
    ):
        modulemd = read_staged_data("testmodule")

        post_data = {
            "branch": "master",
            "scratch": True,
            "modulemd": modulemd,
            "module_name": str(splitext(basename(staged_data_filename("testmodule")))[0]),
        }
        if mod_stream:
            post_data["module_stream"] = mod_stream
            expected_stream = mod_stream
        else:
            expected_stream = "master"
        post_url = "/module-build-service/{0}/module-builds/".format(api_version)
        rv = self.client.post(post_url, data=json.dumps(post_data))
        data = json.loads(rv.data)

        if api_version >= 2:
            assert isinstance(data, list)
            assert len(data) == 1
            data = data[0]

        assert "component_builds" in data, data
        assert data["component_builds"] == []
        assert data["name"] == "testmodule"
        assert data["scmurl"] is None
        # generated modulemd is nondeterministic, so just make sure it is set
        assert data["modulemd"] is not None
        assert data["scratch"] is True
        # generated version is nondeterministic, so just make sure it is set
        assert data["version"] is not None
        assert data["time_submitted"] is not None
        assert data["time_modified"] is not None
        assert data["time_completed"] is None
        assert data["stream"] == expected_stream
        assert data["owner"] == "Homer J. Simpson"
        assert data["id"] == 2
        assert data["rebuild_strategy"] == "changed-and-after"
        assert data["state_name"] == "init"
        assert data["state_url"] == "/module-build-service/{0}/module-builds/2".format(api_version)
        assert len(data["state_trace"]) == 1
        assert data["state_trace"][0]["state"] == 0
        assert data["tasks"] == {}
        assert data["siblings"] == []
        load_mmd(data["modulemd"])

        # Make sure the buildrequires entry was created
        module = ModuleBuild.get_by_id(db_session, 2)
        assert len(module.buildrequires) == 1
        assert module.buildrequires[0].name == "platform"
        assert module.buildrequires[0].stream == "f28"
        assert module.buildrequires[0].version == "3"
        assert module.buildrequires[0].context == "00000000"
        assert module.buildrequires[0].stream_version == 280000

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch(
        "module_build_service.common.config.Config.modules_allow_scratch",
        new_callable=PropertyMock,
        return_value=True,
    )
    @patch(
        "module_build_service.common.config.Config.yaml_submit_allowed",
        new_callable=PropertyMock,
        return_value=True,
    )
    def test_submit_scratch_build_with_mmd_no_module_name(
            self, mocked_allow_yaml, mocked_allow_scratch, mocked_get_user
    ):
        post_data = {
            "branch": "master",
            "scratch": True,
            "modulemd": read_staged_data("testmodule")
        }
        post_url = "/module-build-service/1/module-builds/"
        rv = self.client.post(post_url, data=json.dumps(post_data))
        assert rv.status_code == 400
        data = json.loads(rv.data)
        expected_error = {
            "error": "Bad Request",
            "message": (
                "The module's name was not present in the modulemd file. Please use the "
                '"module_name" parameter'
            ),
            "status": 400,
        }
        assert data == expected_error

    @pytest.mark.parametrize("api_version", [1, 2])
    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch(
        "module_build_service.common.config.Config.modules_allow_scratch",
        new_callable=PropertyMock,
        return_value=True,
    )
    @patch(
        "module_build_service.common.config.Config.yaml_submit_allowed",
        new_callable=PropertyMock,
        return_value=False,
    )
    def test_submit_scratch_build_with_mmd_yaml_not_allowed(
            self, mocked_allow_yaml, mocked_allow_scratch, mocked_get_user, api_version
    ):
        post_data = {
            "branch": "master",
            "scratch": True,
            "modulemd": read_staged_data("testmodule"),
            "module_name": str(splitext(basename(staged_data_filename("testmodule")))[0]),
        }
        post_url = "/module-build-service/{0}/module-builds/".format(api_version)
        rv = self.client.post(post_url, data=json.dumps(post_data))
        data = json.loads(rv.data)

        if api_version >= 2:
            assert isinstance(data, list)
            assert len(data) == 1
            data = data[0]

        # this test is the same as the previous except YAML_SUBMIT_ALLOWED is False,
        # but it should still succeed since yaml is always allowed for scratch builds
        assert rv.status_code == 201

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    @patch(
        "module_build_service.common.config.Config.allowed_privileged_module_names",
        new_callable=PropertyMock,
        return_value=["build"],
    )
    def test_submit_build_with_disttag_marking_in_xmd(
            self, mocked_admmn, mocked_scm, mocked_get_user
    ):
        """
        Test that white-listed modules may set the disttag_marking in xmd.mbs.
        """
        FakeSCM(
            mocked_scm,
            "build",
            "build_metadata_module_not_processed.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4",
            branch="product1.2",
        )

        post_url = "/module-build-service/2/module-builds/"
        scm_url = (
            "https://src.stg.fedoraproject.org/modules/testmodule.git?#"
            "68931c90de214d9d13feefbd35246a81b6cb8d49"
        )

        rv = self.client.post(
            post_url, data=json.dumps({"branch": "product1.2", "scmurl": scm_url}))
        assert rv.status_code == 201
        data = json.loads(rv.data)[0]
        mmd = load_mmd(data["modulemd"])
        assert mmd.get_xmd()["mbs"]["disttag_marking"] == "product12"

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_request_platform_virtual_stream(self, mocked_scm, mocked_get_user):
        # Create a platform with el8.25.0 but with the virtual stream el8
        mmd = load_mmd(read_staged_data("platform"))
        mmd = mmd.copy(mmd.get_module_name(), "el8.25.0")
        xmd = mmd.get_xmd()
        xmd["mbs"]["virtual_streams"] = ["el8"]
        mmd.set_xmd(xmd)
        import_mmd(db_session, mmd)

        # Use a testmodule that buildrequires platform:el8
        FakeSCM(
            mocked_scm,
            "testmodule",
            "testmodule_el8.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4",
        )

        post_url = "/module-build-service/2/module-builds/"
        scm_url = (
            "https://src.stg.fedoraproject.org/modules/testmodule.git?#"
            "68931c90de214d9d13feefbd35246a81b6cb8d49"
        )
        rv = self.client.post(post_url, data=json.dumps({"branch": "master", "scmurl": scm_url}))
        data = json.loads(rv.data)

        mmd = load_mmd(data[0]["modulemd"])
        assert len(mmd.get_dependencies()) == 1
        dep = mmd.get_dependencies()[0]
        assert dep.get_buildtime_streams("platform") == ["el8.25.0"]
        assert dep.get_runtime_streams("platform") == ["el8"]

    @pytest.mark.parametrize(
        "pp_url, pp_streams, pp_sched, get_rv, br_stream, br_override, expected_stream, utcnow",
        (
            # Test a stream of a major release
            (
                "https://pp.domain.local/pp/",
                {r"el.+": (".z", "rhel-{x}-{y}.{z}", "rhel-{x}-{y}")},
                None,
                {"ga_date": "2019-05-07"},
                "el8.0.0",
                {},
                "el8.0.0.z",
                datetime(2019, 9, 16, 12, 00, 00, 0),
            ),
            # Test when the releases GA date is far in the future
            (
                "https://pp.domain.local/pp/",
                {r"el.+": (".z", "rhel-{x}-{y}.{z}", "rhel-{x}-{y}")},
                None,
                {"ga_date": "2099-10-30"},
                "el8.0.0",
                {},
                "el8.0.0",
                datetime(2019, 9, 16, 12, 00, 00, 0),
            ),
            # Test when the release's GA date is same day
            (
                "https://pp.domain.local/pp/",
                {r"el.+": (".z", "rhel-{x}-{y}.{z}", "rhel-{x}-{y}")},
                None,
                {"ga_date": "2019-09-16"},
                "el8.0.0",
                {},
                "el8.0.0",
                datetime(2019, 9, 16, 12, 00, 00, 0),
            ),
            # Test when product_pages_url isn't set
            (
                "",
                {r"el.+": (".z", "rhel-{x}-{y}.{z}", "rhel-{x}-{y}")},
                None,
                {"ga_date": "2019-05-07"},
                "el8.0.0",
                {},
                "el8.0.0",
                datetime(2019, 9, 16, 12, 00, 00, 0),
            ),
            # Test when the release isn't found in Product Pages
            (
                "https://pp.domain.local/pp/",
                {r"el.+": (".z", "rhel-{x}-{y}.{z}", "rhel-{x}-{y}")},
                None,
                {"detail": "Not found."},
                "el8.0.0",
                {},
                "el8.0.0",
                datetime(2019, 9, 16, 12, 00, 00, 0),
            ),
            # Test when a non-major release stream
            (
                "https://pp.domain.local/pp/",
                {r"el.+": (".z", "rhel-{x}-{y}.{z}", "rhel-{x}-{y}")},
                None,
                {"ga_date": "2019-05-07"},
                "el8.2.1",
                {},
                "el8.2.1.z",
                datetime(2019, 9, 16, 12, 00, 00, 0),
            ),
            # Test that when buildrequire overrides is set for platform, nothing changes
            (
                "https://pp.domain.local/pp/",
                {r"el.+": (".z", "rhel-{x}-{y}.{z}", "rhel-{x}-{y}")},
                None,
                {"ga_date": "2019-05-07"},
                "el8.0.0",
                {"platform": ["el8.0.0"]},
                "el8.0.0",
                datetime(2019, 9, 16, 12, 00, 00, 0),
            ),
            # Test when product_pages_module_streams is not set
            (
                "https://pp.domain.local/pp/",
                {},
                None,
                {"ga_date": "2019-05-07"},
                "el8.0.0",
                {},
                "el8.0.0",
                datetime(2019, 9, 16, 12, 00, 00, 0),
            ),
            # Test when there is no stream that matches the configured regexes
            (
                "https://pp.domain.local/pp/",
                {r"js.+": (".z", "js-{x}-{y}", "js-{x}-{y}")},
                None,
                {"ga_date": "2019-05-07"},
                "el8.0.0",
                {},
                "el8.0.0",
                datetime(2019, 9, 16, 12, 00, 00, 0),
            ),
            # Test when there is no configured special Product Pages template
            # for major releases
            (
                "https://pp.domain.local/pp/",
                {r"el.+": (".z", "rhel-{x}-{y}", None)},
                None,
                {"ga_date": "2019-05-07"},
                "el8.0.0",
                {},
                "el8.0.0.z",
                datetime(2019, 9, 16, 12, 00, 00, 0),
            ),
            # Test when there is a schedule date set for early release
            (
                "https://pp.domain.local/pp/",
                {r"el.+": (".z", "rhel-{x}-{y}", None)},
                "test_sched",
                [{"name": "test_sched", "date_finish": "2019-09-02"}],
                "el8.0.0",
                {},
                "el8.0.0.z",
                datetime(2019, 9, 16, 12, 00, 00, 0),
            ),
        ),
    )
    @patch.object(
        module_build_service.web.submit,
        "datetime",
        new_callable=partial(Mock, wraps=datetime),
    )
    @patch(
        "module_build_service.common.config.Config.product_pages_url",
        new_callable=PropertyMock,
    )
    @patch(
        "module_build_service.common.config.Config.product_pages_module_streams",
        new_callable=PropertyMock,
    )
    @patch(
        "module_build_service.common.config.Config.product_pages_schedule_task_name",
        new_callable=PropertyMock,
    )
    @patch("requests.get")
    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_automatic_z_stream_detection(
            self, mocked_scm, mocked_get_user, mock_get, mock_pp_sched, mock_pp_streams,
            mock_pp_url,
            mock_datetime, pp_url, pp_streams, pp_sched, get_rv, br_stream, br_override,
            expected_stream, utcnow,
    ):
        # Configure the Product Pages URL
        mock_pp_url.return_value = pp_url
        mock_pp_streams.return_value = pp_streams
        mock_pp_sched.return_value = pp_sched
        # Mock the Product Pages query
        mock_get.return_value.json.return_value = get_rv
        # Mock the date
        mock_datetime.utcnow.return_value = utcnow
        mmd = load_mmd(read_staged_data("platform"))
        # Create the required platforms
        for stream in ("el8.0.0", "el8.0.0.z", "el8.2.1", "el8.2.1.z"):
            mmd = mmd.copy(mmd.get_module_name(), stream)
            import_mmd(db_session, mmd)

        # Use a testmodule that buildrequires platform:el8.0.0 or platform:el8.2.1
        FakeSCM(
            mocked_scm,
            "testmodule",
            "testmodule_{}.yaml".format(br_stream.replace(".", "")),
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4",
        )

        post_url = "/module-build-service/2/module-builds/"
        scm_url = (
            "https://src.stg.fedoraproject.org/modules/testmodule.git?#"
            "68931c90de214d9d13feefbd35246a81b6cb8d49"
        )
        payload = {"branch": "master", "scmurl": scm_url}
        if br_override:
            payload["buildrequire_overrides"] = br_override
        rv = self.client.post(post_url, data=json.dumps(payload))
        data = json.loads(rv.data)

        mmd = load_mmd(data[0]["modulemd"])
        assert len(mmd.get_dependencies()) == 1
        dep = mmd.get_dependencies()[0]
        assert dep.get_buildtime_streams("platform") == [expected_stream]
        # The runtime stream suffix should remain unchanged
        assert dep.get_runtime_streams("platform") == ["el8.0.0"]

        if (pp_url or pp_sched) and not br_override and pp_streams.get(r"el.+"):
            if br_stream == "el8.0.0":
                pp_release = "rhel-8-0"
            else:
                pp_release = "rhel-8-2.1"
            if pp_url:
                expected_url = "{}api/v7/releases/{}/?fields=ga_date".format(pp_url, pp_release)
            if pp_sched:
                expected_url = \
                    "{}api/v7/releases/{}/schedule-tasks/?fields=name,date_finish".format(
                        pp_url, pp_release)
            mock_get.assert_called_once_with(expected_url, timeout=15)
        else:
            mock_get.assert_not_called()

    @pytest.mark.parametrize("reuse_components_from", (4, "testmodule:4.3.43:6:00000000"))
    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_reuse_components_from(
            self, mocked_scm, mocked_get_user, reuse_components_from, provide_test_data
    ):
        """Test a build submission using the reuse_components_from parameter."""
        module_to_reuse = ModuleBuild.get_by_id(db_session, 4)
        module_to_reuse.state = BUILD_STATES["ready"]
        for c in module_to_reuse.component_builds:
            c.state = koji.BUILD_STATES["COMPLETE"]
        db_session.commit()

        FakeSCM(
            mocked_scm, "testmodule", "testmodule.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4")
        rv = self.client.post(
            "/module-build-service/1/module-builds/",
            data=json.dumps({
                "branch": "master",
                "reuse_components_from": reuse_components_from,
                "scmurl": (
                    "https://src.stg.fedoraproject.org/modules/testmodule.git?"
                    "#68931c90de214d9d13feefbd35246a81b6cb8d49"
                ),
            }),
        )
        data = json.loads(rv.data)
        assert data["reused_module_id"] == 4

    @pytest.mark.parametrize(
        "reuse_components_from, expected_error",
        (
            (
                "testmodule:4.3.43:7",
                'The parameter "reuse_components_from" contains an invalid module identifier'
            ),
            (
                {},
                'The parameter "reuse_components_from" contains an invalid module identifier'
            ),
            (
                912312312,
                'The module in the parameter "reuse_components_from" could not be found'),
            (
                4,
                'The module in the parameter "reuse_components_from" must be in the ready state'
            )
        )
    )
    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_reuse_components_from_errors(self, mocked_scm, mocked_get_user,
                                                       reuse_components_from, expected_error,
                                                       provide_test_data):
        """
        Test a build submission using an invalid value for the reuse_components_from parameter.
        """
        FakeSCM(
            mocked_scm, "testmodule", "testmodule.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4")
        rv = self.client.post(
            "/module-build-service/1/module-builds/",
            data=json.dumps({
                "branch": "master",
                "reuse_components_from": reuse_components_from,
                "scmurl": (
                    "https://src.stg.fedoraproject.org/modules/testmodule.git?"
                    "#68931c90de214d9d13feefbd35246a81b6cb8d49"
                ),
            }),
        )
        data = json.loads(rv.data)
        assert rv.status_code == 400
        assert data["message"] == expected_error

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    @patch(
        "module_build_service.common.config.Config.rebuild_strategy_allow_override",
        new_callable=PropertyMock,
        return_value=True,
    )
    def test_submit_build_reuse_components_rebuild_strategy_all(
            self, mock_rsao, mocked_scm, mocked_get_user,
    ):
        """
        Test a build submission using reuse_components_from and the rebuild_strategy of all.
        """
        FakeSCM(
            mocked_scm, "testmodule", "testmodule.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4")
        rv = self.client.post(
            "/module-build-service/1/module-builds/",
            data=json.dumps({
                "branch": "master",
                "rebuild_strategy": "all",
                "reuse_components_from": 7,
                "scmurl": (
                    "https://src.stg.fedoraproject.org/modules/testmodule.git?"
                    "#68931c90de214d9d13feefbd35246a81b6cb8d49"
                ),
            }),
        )
        data = json.loads(rv.data)
        assert rv.status_code == 400
        assert data["message"] == (
            'You cannot specify the parameter "reuse_components_from" when the "rebuild_strategy" '
            'parameter is set to "all"'
        )

    @pytest.mark.parametrize(
        "br_override_streams, req_override_streams", ((["f28"], None), (["f28"], ["f28"]))
    )
    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_dep_override(
            self, mocked_scm, mocked_get_user, br_override_streams, req_override_streams
    ):
        FakeSCM(
            mocked_scm,
            "testmodule",
            "testmodule_platform_f290000.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4",
        )

        post_url = "/module-build-service/2/module-builds/"
        scm_url = (
            "https://src.stg.fedoraproject.org/modules/testmodule.git?#68931c90de214d9d13fe"
            "efbd35246a81b6cb8d49"
        )
        json_input = {"branch": "master", "scmurl": scm_url}

        if br_override_streams:
            json_input["buildrequire_overrides"] = {"platform": br_override_streams}
            expected_br = set(br_override_streams)
        else:
            expected_br = {"f29.0.0"}

        if req_override_streams:
            json_input["require_overrides"] = {"platform": req_override_streams}
            expected_req = set(req_override_streams)
        else:
            expected_req = {"f29.0.0"}

        rv = self.client.post(post_url, data=json.dumps(json_input))
        data = json.loads(rv.data)

        mmd = load_mmd(data[0]["modulemd"])
        assert len(mmd.get_dependencies()) == 1
        dep = mmd.get_dependencies()[0]
        assert set(dep.get_buildtime_streams("platform")) == expected_br
        assert set(dep.get_runtime_streams("platform")) == expected_req

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_invalid_basemodule_stream(self, mocked_scm, mocked_get_user):
        # By default tests do not provide platform:f28.0.0, but just platform:f28.
        # Therefore we want to enable multiple_stream_versions.
        FakeSCM(
            mocked_scm, "testmodule", "testmodule.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4")

        data = {
            "branch": "master",
            "scmurl": "https://src.stg.fedoraproject.org/modules/"
                      "testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49",
            "buildrequire_overrides": {"platform": ["28.0.0"]},
            "require_overrides": {"platform": ["f28.0.0"]},
        }
        rv = self.client.post("/module-build-service/1/module-builds/", data=json.dumps(data))
        result = json.loads(rv.data)
        assert result == {
            "error": "Unprocessable Entity",
            "status": 422,
            "message": (
                "None of the base module (platform) streams in the buildrequires "
                "section could be found"
            ),
        }
        assert rv.status_code == 422

    @pytest.mark.parametrize(
        "branch, platform_override",
        (("10", None), ("10-rhel-8.0.0", "el8.0.0"), ("10-LP-product1.2", "product1.2")),
    )
    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    @patch.object(
        module_build_service.common.config.Config,
        "br_stream_override_regexes",
        new_callable=PropertyMock,
    )
    def test_submit_build_dep_override_from_branch(
            self, mocked_regexes, mocked_scm, mocked_get_user, branch, platform_override
    ):
        """
        Test that MBS will parse the SCM branch to determine the platform stream to buildrequire.
        """
        mocked_regexes.return_value = [r"(?:rh)(el)(?:\-)(\d+\.\d+\.\d+)$", r"(?:\-LP\-)(.+)$"]
        # Create a platform for whatever the override is so the build submission succeeds
        if platform_override:
            platform_mmd = load_mmd(read_staged_data("platform"))
            platform_mmd = platform_mmd.copy(platform_mmd.get_module_name(), platform_override)
            if platform_override == "el8.0.0":
                xmd = platform_mmd.get_xmd()
                xmd["mbs"]["virtual_streams"] = ["el8"]
                platform_mmd.set_xmd(xmd)
            import_mmd(db_session, platform_mmd)

        FakeSCM(
            mocked_scm, "testmodule", "testmodule.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4")

        post_url = "/module-build-service/2/module-builds/"
        scm_url = (
            "https://src.stg.fedoraproject.org/modules/testmodule.git?#"
            "68931c90de214d9d13feefbd35246a81b6cb8d49"
        )

        rv = self.client.post(post_url, data=json.dumps({"branch": branch, "scmurl": scm_url}))
        data = json.loads(rv.data)
        assert rv.status_code == 201

        mmd = load_mmd(data[0]["modulemd"])
        assert len(mmd.get_dependencies()) == 1
        dep = mmd.get_dependencies()[0]
        if platform_override:
            expected_br = {platform_override}
        else:
            expected_br = {"f28"}
        assert set(dep.get_buildtime_streams("platform")) == expected_br
        # The requires should not change
        assert dep.get_runtime_streams("platform") == ["f28"]

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    @patch.object(
        module_build_service.common.config.Config,
        "br_stream_override_regexes",
        new_callable=PropertyMock,
    )
    def test_submit_build_dep_override_from_branch_br_override(
            self, mocked_regexes, mocked_scm, mocked_get_user
    ):
        """
        Test that when the branch includes a stream override for the platform module, that the
        provided "buildrequire_override" for the platform module takes precedence.
        """
        mocked_regexes.return_value = [r"(?:\-LP\-)(.+)$"]
        # Create a platform for the override so the build submission succeeds
        platform_mmd = load_mmd(read_staged_data('platform'))
        platform_mmd = platform_mmd.copy(platform_mmd.get_module_name(), "product1.3")
        import_mmd(db_session, platform_mmd)

        FakeSCM(
            mocked_scm, "testmodule", "testmodule.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4")

        post_url = "/module-build-service/2/module-builds/"
        scm_url = (
            "https://src.stg.fedoraproject.org/modules/testmodule.git?#"
            "68931c90de214d9d13feefbd35246a81b6cb8d49"
        )
        json_input = {
            "branch": "10-LP-product1.2",
            "scmurl": scm_url,
            "buildrequire_overrides": {"platform": ["product1.3"]},
        }

        rv = self.client.post(post_url, data=json.dumps(json_input))
        data = json.loads(rv.data)
        assert rv.status_code == 201

        mmd = load_mmd(data[0]["modulemd"])
        assert len(mmd.get_dependencies()) == 1
        dep = mmd.get_dependencies()[0]
        # The buildrequire_override value should take precedence over the stream override from
        # parsing the branch
        assert dep.get_buildtime_streams("platform") == ["product1.3"]
        # The requires should not change
        assert dep.get_runtime_streams("platform") == ["f28"]

    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch("module_build_service.common.scm.SCM")
    def test_submit_build_br_xyz_version_no_virtual_streams(self, mocked_scm, mocked_get_user):
        """
        Test that when a build is submitted with a buildrequire on a base module with x.y.z
        versioning and no virtual streams, that the dependency resolution succeeds.
        """
        platform_mmd = load_mmd(read_staged_data("platform"))
        platform_mmd = platform_mmd.copy(platform_mmd.get_module_name(), "el8.0.0")
        import_mmd(db_session, platform_mmd)

        FakeSCM(
            mocked_scm,
            "testmodule",
            "testmodule_el800.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4",
        )

        post_url = "/module-build-service/2/module-builds/"
        scm_url = (
            "https://src.stg.fedoraproject.org/modules/testmodule.git?#"
            "68931c90de214d9d13feefbd35246a81b6cb8d49"
        )

        rv = self.client.post(post_url, data=json.dumps({"branch": "master", "scmurl": scm_url}))
        assert rv.status_code == 201


@pytest.mark.usefixtures("provide_test_client")
@pytest.mark.usefixtures("provide_test_data")
# only the 3rd build (with platform, id=4) in provide_test_data is eligible, it is in 'wait' state
class TestCancelBuild:

    @patch("module_build_service.web.auth.get_user", return_value=other_user)
    def test_cancel_build(self, mocked_get_user):
        rv = self.client.patch(
            "/module-build-service/1/module-builds/4", data=json.dumps({"state": "failed"}))
        data = json.loads(rv.data)

        assert data["state"] == 4
        assert data["state_reason"] == "Canceled by some_other_user."

    @pytest.mark.parametrize("module_state", (BUILD_STATES["failed"], BUILD_STATES["ready"]))
    @patch("module_build_service.web.auth.get_user", return_value=other_user)
    def test_cancel_build_in_invalid_state(self, mocked_get_user, module_state):
        module = ModuleBuild.get_by_id(db_session, 4)
        module.state = module_state
        db_session.commit()

        rv = self.client.patch(
            "/module-build-service/1/module-builds/4", data=json.dumps({"state": "failed"}))

        assert rv.status_code == 400
        assert json.loads(rv.data) == {
            "error": "Bad Request",
            "message": (
                "To cancel a module build, it must be in one of the following states: "
                "build, init, wait"
            ),
            "status": 400,
        }

    @patch("module_build_service.web.auth.get_user", return_value=("sammy", set()))
    def test_cancel_build_unauthorized_no_groups(self, mocked_get_user):
        rv = self.client.patch(
            "/module-build-service/1/module-builds/4", data=json.dumps({"state": "failed"}))
        data = json.loads(rv.data)

        assert data["status"] == 403
        assert data["error"] == "Forbidden"

    @patch("module_build_service.web.auth.get_user", return_value=("sammy", {"packager"}))
    def test_cancel_build_unauthorized_not_owner(self, mocked_get_user):
        rv = self.client.patch(
            "/module-build-service/1/module-builds/4", data=json.dumps({"state": "failed"}))
        data = json.loads(rv.data)

        assert data["status"] == 403
        assert data["error"] == "Forbidden"

    @patch(
        "module_build_service.web.auth.get_user", return_value=("sammy", {"packager", "mbs-admin"})
    )
    def test_cancel_build_admin(self, mocked_get_user):
        with patch(
                "module_build_service.common.config.Config.admin_groups",
                new_callable=PropertyMock,
                return_value={"mbs-admin"},
        ):
            rv = self.client.patch(
                "/module-build-service/1/module-builds/4", data=json.dumps({"state": "failed"}))
            data = json.loads(rv.data)

            assert data["state"] == 4
            assert data["state_reason"] == "Canceled by sammy."

    @patch("module_build_service.web.auth.get_user", return_value=("sammy", {"packager"}))
    def test_cancel_build_no_admin(self, mocked_get_user):
        with patch(
                "module_build_service.common.config.Config.admin_groups",
                new_callable=PropertyMock,
                return_value={"mbs-admin"},
        ):
            rv = self.client.patch(
                "/module-build-service/1/module-builds/4", data=json.dumps({"state": "failed"}))
            data = json.loads(rv.data)

            assert data["status"] == 403
            assert data["error"] == "Forbidden"

    @patch("module_build_service.web.auth.get_user", return_value=other_user)
    def test_cancel_build_wrong_param(self, mocked_get_user):
        rv = self.client.patch(
            "/module-build-service/1/module-builds/4", data=json.dumps({"some_param": "value"}))
        data = json.loads(rv.data)

        assert data["status"] == 400
        assert data["error"] == "Bad Request"
        assert data["message"] == "Invalid JSON submitted"

    @patch("module_build_service.web.auth.get_user", return_value=other_user)
    def test_cancel_build_wrong_state(self, mocked_get_user):
        rv = self.client.patch(
            "/module-build-service/1/module-builds/4", data=json.dumps({"state": "some_state"}))

        assert rv.status_code == 400
        assert json.loads(rv.data) == {
            "error": "Bad Request",
            "message": "An invalid state was submitted. Valid states values are: failed, 4",
            "status": 400,
        }


@pytest.mark.usefixtures("provide_test_client")
class TestImportBuild:

    @pytest.mark.parametrize("api_version", [1, 2])
    @patch("module_build_service.web.auth.get_user", return_value=user)
    @patch.object(
        module_build_service.common.config.Config,
        "allowed_groups_to_import_module",
        new_callable=PropertyMock,
        return_value=set(),
    )
    def test_import_build_disabled(self, mocked_groups, mocked_get_user, api_version):
        post_url = "/module-build-service/{0}/import-module/".format(api_version)
        rv = self.client.post(post_url)
        data = json.loads(rv.data)

        assert data["error"] == "Forbidden"
        assert data["message"] == "Import module API is disabled."

    @pytest.mark.parametrize("api_version", [1, 2])
    @patch("module_build_service.web.auth.get_user", return_value=user)
    def test_import_build_user_not_allowed(self, mocked_get_user, api_version):
        post_url = "/module-build-service/{0}/import-module/".format(api_version)
        rv = self.client.post(post_url)
        data = json.loads(rv.data)

        assert data["error"] == "Forbidden"
        assert data["message"] == (
            "Homer J. Simpson is not in any of {0}, only {1}".format(
                {"mbs-import-module"}, {"packager"})
        )

    @pytest.mark.parametrize("api_version", [1, 2])
    @patch("module_build_service.web.auth.get_user", return_value=import_module_user)
    def test_import_build_scm_invalid_json(self, mocked_get_user, api_version):
        post_url = "/module-build-service/{0}/import-module/".format(api_version)
        rv = self.client.post(post_url, data="")
        data = json.loads(rv.data)

        assert data["error"] == "Bad Request"
        assert data["message"] == "Invalid JSON submitted"

    @pytest.mark.parametrize("api_version", [1, 2])
    @patch("module_build_service.web.auth.get_user", return_value=import_module_user)
    def test_import_build_scm_url_not_allowed(self, mocked_get_user, api_version):
        post_url = "/module-build-service/{0}/import-module/".format(api_version)
        rv = self.client.post(
            post_url, data=json.dumps({"scmurl": "file://" + scm_base_dir + "/mariadb"}))
        data = json.loads(rv.data)

        assert data["error"] == "Forbidden"
        assert data["message"].startswith("The submitted scmurl ")
        assert data["message"].endswith("/tests/scm_data/mariadb is not allowed")

    @pytest.mark.parametrize("api_version", [1, 2])
    @patch("module_build_service.web.auth.get_user", return_value=import_module_user)
    @patch.object(
        module_build_service.common.config.Config,
        "allow_custom_scmurls",
        new_callable=PropertyMock,
        return_value=True,
    )
    def test_import_build_scm_url_not_in_list(self, mocked_scmurls, mocked_get_user, api_version):
        post_url = "/module-build-service/{0}/import-module/".format(api_version)
        rv = self.client.post(
            post_url,
            data=json.dumps({
                "scmurl": "file://{}/mariadb?#b17bea85de2d03558f24d506578abcfcf467e5bc".format(
                    scm_base_dir)
            }),
        )
        data = json.loads(rv.data)

        assert data["error"] == "Forbidden"
        assert data["message"].endswith(
            "/tests/scm_data/mariadb?#b17bea85de2d03558f24d506578abcfcf467e5bc "
            "is not in the list of allowed SCMs"
        )

    @pytest.mark.parametrize("api_version", [1, 2])
    @patch("module_build_service.web.auth.get_user", return_value=import_module_user)
    @patch.object(
        module_build_service.common.config.Config,
        "scmurls",
        new_callable=PropertyMock,
        return_value=["file://"],
    )
    def test_import_build_scm(self, mocked_scmurls, mocked_get_user, api_version):
        post_url = "/module-build-service/{0}/import-module/".format(api_version)
        rv = self.client.post(
            post_url,
            data=json.dumps({
                "scmurl": "file://{}/mariadb?#e9742ed681f82e3ef5281fc652b4e68a3826cea6".format(
                    scm_base_dir)
            }),
        )
        data = json.loads(rv.data)

        assert "Module mariadb:10.2:20180724000000:00000000 imported" in data["messages"]
        assert data["module"]["name"] == "mariadb"
        assert data["module"]["stream"] == "10.2"
        assert data["module"]["version"] == "20180724000000"
        assert data["module"]["context"] == "00000000"
        assert data["module"]["owner"] == "mbs_import"
        assert data["module"]["state"] == 5
        assert data["module"]["state_reason"] is None
        assert data["module"]["state_name"] == "ready"
        assert data["module"]["scmurl"] is None
        assert data["module"]["component_builds"] == []
        assert time_assert(
            data["module"]["time_submitted"],
            data["module"]["time_modified"],
            data["module"]["time_completed"]
        )
        assert data["module"]["koji_tag"] == "mariadb-10.2-20180724000000-00000000"
        assert data["module"]["siblings"] == []
        assert data["module"]["rebuild_strategy"] == "all"

    @pytest.mark.parametrize("api_version", [1, 2])
    @patch("module_build_service.web.auth.get_user", return_value=import_module_user)
    @patch.object(
        module_build_service.common.config.Config,
        "scmurls",
        new_callable=PropertyMock,
        return_value=["file://"],
    )
    def test_import_build_scm_another_commit_hash(
            self, mocked_scmurls, mocked_get_user, api_version
    ):
        post_url = "/module-build-service/{0}/import-module/".format(api_version)
        rv = self.client.post(
            post_url,
            data=json.dumps({
                "scmurl": "file://{}/mariadb?#8b43f38cdafdd773e7d0308e758105bf9f0f67a8".format(
                    scm_base_dir)
            }),
        )
        data = json.loads(rv.data)

        assert "Module mariadb:10.2:20180724065109:00000000 imported" in data["messages"]
        assert data["module"]["name"] == "mariadb"
        assert data["module"]["stream"] == "10.2"
        assert data["module"]["version"] == "20180724065109"
        assert data["module"]["context"] == "00000000"
        assert data["module"]["owner"] == "mbs_import"
        assert data["module"]["state"] == 5
        assert data["module"]["state_reason"] is None
        assert data["module"]["state_name"] == "ready"
        assert data["module"]["scmurl"] is None
        assert data["module"]["component_builds"] == []
        assert time_assert(
            data["module"]["time_submitted"],
            data["module"]["time_modified"],
            data["module"]["time_completed"]
        )
        assert data["module"]["koji_tag"] == "mariadb-10.2-20180724065109-00000000"
        assert data["module"]["siblings"] == []
        assert data["module"]["rebuild_strategy"] == "all"

    @pytest.mark.parametrize("api_version", [1, 2])
    @patch("module_build_service.web.auth.get_user", return_value=import_module_user)
    @patch.object(
        module_build_service.common.config.Config,
        "scmurls",
        new_callable=PropertyMock,
        return_value=["file://"],
    )
    def test_import_build_scm_incomplete_nsvc(self, mocked_scmurls, mocked_get_user, api_version):
        post_url = "/module-build-service/{0}/import-module/".format(api_version)
        rv = self.client.post(
            post_url,
            data=json.dumps({
                "scmurl": "file://{}/mariadb?#b17bea85de2d03558f24d506578abcfcf467e5bc".format(
                    scm_base_dir)
            }),
        )
        data = json.loads(rv.data)

        assert data["error"] == "Unprocessable Entity"
        expected_msg = "Both the name and stream must be set for the modulemd being imported."
        assert data["message"] == expected_msg

    @pytest.mark.parametrize("api_version", [1, 2])
    @patch("module_build_service.web.auth.get_user", return_value=import_module_user)
    @patch.object(
        module_build_service.common.config.Config,
        "scmurls",
        new_callable=PropertyMock,
        return_value=["file://"],
    )
    def test_import_build_scm_yaml_is_bad(self, mocked_scmurls, mocked_get_user, api_version):
        post_url = "/module-build-service/{0}/import-module/".format(api_version)
        rv = self.client.post(
            post_url,
            data=json.dumps({
                "scmurl": "file://{}/mariadb?#f7c5c7218c9a197d7fd245eeb4eee3d7abffd75d".format(
                    scm_base_dir)
            }),
        )
        data = json.loads(rv.data)

        assert data["error"] == "Unprocessable Entity"
        assert re.match(
            r"The modulemd .* is invalid\. ", data["message"]
        )
        assert "Please verify the syntax is correct" in data["message"]


@pytest.mark.usefixtures("provide_test_client")
class TestViewsMisc:

    def test_about(self):
        with patch.object(mbs_config.Config, "auth_method", new_callable=PropertyMock) as auth:
            auth.return_value = "kerberos"
            rv = self.client.get("/module-build-service/1/about/")
        data = json.loads(rv.data)
        assert rv.status_code == 200
        assert data == {"auth_method": "kerberos", "api_version": 2, "version": version}

    def test_rebuild_strategy_api(self):
        rv = self.client.get("/module-build-service/1/rebuild-strategies/")
        data = json.loads(rv.data)
        assert rv.status_code == 200
        expected = {
            "items": [
                {
                    "allowed": False,
                    "default": False,
                    "description": "All components will be rebuilt",
                    "name": "all",
                },
                {
                    "allowed": True,
                    "default": True,
                    "description": (
                        "All components that have changed and those in subsequent "
                        "batches will be rebuilt"
                    ),
                    "name": "changed-and-after",
                },
                {
                    "allowed": False,
                    "default": False,
                    "description": "All changed components will be rebuilt",
                    "name": "only-changed",
                },
            ]
        }
        assert data == expected

    def test_rebuild_strategy_api_only_changed_default(self):
        with patch.object(mbs_config.Config, "rebuild_strategy", new_callable=PropertyMock) as r_s:
            r_s.return_value = "only-changed"
            rv = self.client.get("/module-build-service/1/rebuild-strategies/")
        data = json.loads(rv.data)
        assert rv.status_code == 200
        expected = {
            "items": [
                {
                    "allowed": False,
                    "default": False,
                    "description": "All components will be rebuilt",
                    "name": "all",
                },
                {
                    "allowed": False,
                    "default": False,
                    "description": (
                        "All components that have changed and those in subsequent "
                        "batches will be rebuilt"
                    ),
                    "name": "changed-and-after",
                },
                {
                    "allowed": True,
                    "default": True,
                    "description": "All changed components will be rebuilt",
                    "name": "only-changed",
                },
            ]
        }
        assert data == expected

    def test_rebuild_strategy_api_override_allowed(self):
        with patch.object(
            mbs_config.Config, "rebuild_strategy_allow_override", new_callable=PropertyMock
        ) as rsao:
            rsao.return_value = True
            rv = self.client.get("/module-build-service/1/rebuild-strategies/")
        data = json.loads(rv.data)
        assert rv.status_code == 200
        expected = {
            "items": [
                {
                    "allowed": True,
                    "default": False,
                    "description": "All components will be rebuilt",
                    "name": "all",
                },
                {
                    "allowed": True,
                    "default": True,
                    "description": (
                        "All components that have changed and those in subsequent "
                        "batches will be rebuilt"
                    ),
                    "name": "changed-and-after",
                },
                {
                    "allowed": True,
                    "default": False,
                    "description": "All changed components will be rebuilt",
                    "name": "only-changed",
                },
            ]
        }
        assert data == expected

    def test_cors_header_decorator(self):
        rv = self.client.get("/module-build-service/1/module-builds/")
        assert rv.headers["Access-Control-Allow-Origin"] == "*"

    @patch("module_build_service.web.auth.get_user", return_value=anonymous_user)
    @patch("module_build_service.common.scm.SCM")
    @patch("module_build_service.common.config.Config.no_auth", new_callable=PropertyMock)
    @pytest.mark.usefixtures("require_platform_and_default_arch")
    def test_patch_set_different_owner(self, mocked_no_auth, mocked_scm, mocked_get_user):
        FakeSCM(
            mocked_scm, "testmodule", "testmodule.yaml",
            "620ec77321b2ea7b0d67d82992dda3e1d67055b4")

        mocked_no_auth.return_value = True
        data = {
            "branch": "master",
            "scmurl": "https://src.stg.fedoraproject.org/modules/"
                      "testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49",
            "owner": "foo",
        }
        rv = self.client.post("/module-build-service/1/module-builds/", data=json.dumps(data))
        r1 = json.loads(rv.data)

        url = "/module-build-service/1/module-builds/" + str(r1["id"])
        r2 = self.client.patch(url, data=json.dumps({"state": "failed"}))
        assert r2.status_code == 403

        r3 = self.client.patch(url, data=json.dumps({"state": "failed", "owner": "foo"}))
        assert r3.status_code == 200

        mocked_no_auth.return_value = False
        r3 = self.client.patch(url, data=json.dumps({"state": "failed", "owner": "foo"}))
        assert r3.status_code == 400
        assert "The request contains 'owner' parameter" in json.loads(r3.data)["message"]

    @pytest.mark.usefixtures("require_platform_and_default_arch")
    def test_buildrequires_is_included_in_json_output(self):
        # Inject xmd/mbs/buildrequires into an existing module build for
        # assertion later.
        br_modulea = dict(stream="6", version="1", context="1234")
        br_moduleb = dict(stream="10", version="1", context="5678")
        build = db_session.query(ModuleBuild).first()
        mmd = build.mmd()
        xmd = mmd.get_xmd()
        mbs = xmd.setdefault("mbs", {})
        buildrequires = mbs.setdefault("buildrequires", {})
        buildrequires["modulea"] = br_modulea
        buildrequires["moduleb"] = br_moduleb
        mmd.set_xmd(xmd)
        build.modulemd = mmd_to_str(mmd)
        db_session.commit()

        rv = self.client.get("/module-build-service/1/module-builds/{}".format(build.id))
        data = json.loads(rv.data)
        buildrequires = data.get("buildrequires", {})

        assert br_modulea == buildrequires.get("modulea")
        assert br_moduleb == buildrequires.get("moduleb")


@pytest.mark.usefixtures("provide_test_client")
class TestViewsLogMessage:

    def setup_method(self, test_method):
        clean_database()
        init_data(2)
        self.module_id = 2
        self.module_build = ModuleBuild.get_by_id(db_session, self.module_id)
        self.module_build.log_message(db_session, "Build-1 msg")
        self.module_build.log_message(db_session, "Build-2 msg")
        self.component_build = self.module_build.component_builds[0]
        self.component_build.log_message(db_session, "Component-1 msg")

    def test_view_log_messages_for_module_builds(self):
        url = "/module-build-service/1/module-builds/{module_id}/messages".format(
            module_id=self.module_id)
        res = self.client.get(url)

        json_res = str(res.data)

        assert "Build-1" in json_res
        assert "Build-2" in json_res
        assert "Component-1" in json_res

    def test_view_log_messages_for_component_builds(self):
        url = "/module-build-service/1/component-builds/{component_id}/messages".format(
            component_id=self.component_build.id)
        res = self.client.get(url)

        json_res = str(res.data)

        assert "Build-1" not in json_res
        assert "Build-2" not in json_res
        assert "Component-1" in json_res


@pytest.mark.usefixtures("provide_test_client")
@pytest.mark.usefixtures("provide_test_data")
class TestViewsFinalModulemd:

    @patch("module_build_service.builder.KojiContentGenerator.KojiContentGenerator.get_final_mmds")
    def test_view_final_modulemd(self, mocked_cg):
        mocked_cg.return_value = {'x86_64': 'finalized mmd'}
        url = "/module-build-service/1/final-modulemd/2"
        res = self.client.get(url)
        json_res = str(res.data)

        assert "x86_64" in json_res
        assert "finalized mmd" in json_res
