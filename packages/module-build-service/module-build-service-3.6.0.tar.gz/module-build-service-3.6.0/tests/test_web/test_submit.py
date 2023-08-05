# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
from __future__ import absolute_import
import io
from os import path
from shutil import rmtree
import tempfile

import mock
import pytest
from werkzeug.datastructures import FileStorage

from module_build_service.common import models
from module_build_service.common.errors import ValidationError
from module_build_service.common.utils import (mmd_to_str, load_mmd,
                                               provide_module_stream_version_from_timestamp)
from module_build_service.scheduler.db_session import db_session
from module_build_service.web.submit import (
    get_prefixed_version, submit_module_build, submit_module_build_from_yaml,
    process_module_context_configuration, _apply_side_tag,
)
from tests import (
    scheduler_init_data,
    make_module_in_db,
    make_module,
    read_staged_data,
    init_data,
)


class TestSubmit:
    def test_get_prefixed_version_f28(self):
        scheduler_init_data(1)
        build_one = models.ModuleBuild.get_by_id(db_session, 2)
        v = get_prefixed_version(build_one.mmd())
        assert v == 2820180205135154

    def test_get_prefixed_version_fl701(self):
        scheduler_init_data(1)
        build_one = models.ModuleBuild.get_by_id(db_session, 2)
        mmd = build_one.mmd()
        xmd = mmd.get_xmd()
        xmd["mbs"]["buildrequires"]["platform"]["stream"] = "fl7.0.1-beta"
        mmd.set_xmd(xmd)
        v = get_prefixed_version(mmd)
        assert v == 7000120180205135154

    def test_submit_build_static_context(self):
        """
        Test that we can now build modules with static contexts. The contexts are defined in
        the `xmd` property by the `contexts` property of the initial modulemd yaml file. The
        `contexts` is not pressent in the resulting module build. The generated contexts of a
        module is overridden by the static context defined by the user and the `mse` property
        is set to False.
        """

        yaml_str = read_staged_data("static_context_v2")
        mmd = load_mmd(yaml_str)

        ux_timestamp = "1613048427"
        version = provide_module_stream_version_from_timestamp(ux_timestamp)
        builds = submit_module_build(db_session, "app", mmd, {}, version)

        expected_context = ["context1", "context2"]

        assert len(builds) == 2

        for build in builds:
            assert build.context in expected_context
            mmd = build.mmd()
            xmd = mmd.get_xmd()
            assert mmd.get_version() == int("28" + str(version))
            assert "mbs_options" not in xmd
            assert xmd["mbs"]["static_context"]

    def test_submit_build_static_context_preserve_mbs_options(self):
        """
        This tests that the `mbs_options` will be preserved after static context build if there
        are more options configured then `contexts` option..
        """

        yaml_str = read_staged_data("static_context_v2")
        mmd = load_mmd(yaml_str)
        xmd = mmd.get_xmd()
        xmd["mbs_options"]["another_option"] = "test"
        xmd["mbs_options"]["contexts"] = {
            "context3": xmd["mbs_options"]["contexts"]["context1"]
        }
        mmd.set_xmd(xmd)

        ux_timestamp = "1613048427"
        version = provide_module_stream_version_from_timestamp(ux_timestamp)

        builds = submit_module_build(db_session, "app", mmd, {}, version)

        assert len(builds) == 1
        mmd = builds[0].mmd()
        xmd = mmd.get_xmd()
        assert "mbs_options" in xmd
        assert "another_option" in xmd["mbs_options"]
        assert "test" == xmd["mbs_options"]["another_option"]

    def test_submit_build_module_context_configurations(self):
        """
        With the introduction of the v3 packager yaml format we replace MSE with static contexts.
        This test tests the submission of such a packager file.
        """
        init_data(multiple_stream_versions=True)
        yaml_str = read_staged_data("v3/mmd_packager")
        mmd = load_mmd(yaml_str)
        ux_timestamp = "1613048427"
        version = provide_module_stream_version_from_timestamp(ux_timestamp)
        builds = submit_module_build(db_session, "foo", mmd, {}, version)

        assert len(builds) == 2

        expected_deps = {"CTX1": {"buildrequires": {"platform": ["f28"]},
                                  "requires": {"nginx": ["1"]}},
                         "CTX2": {"buildrequires": {"platform": ["f29.2.0"]},
                                  "requires": {}}}

        for build in builds:
            mmd = build.mmd()
            context = mmd.get_context()
            assert context in expected_deps
            assert mmd.get_mdversion() == 2

            deps = mmd.get_dependencies()[0]

            btms = deps.get_buildtime_modules()
            rtms = deps.get_runtime_modules()

            for btm in btms:
                expected_stream = expected_deps[context]["buildrequires"][btm][0]
                actual_stream = deps.get_buildtime_streams(btm)[0]
                assert expected_stream == actual_stream

            for rtm in rtms:
                expected_stream = expected_deps[context]["requires"][rtm][0]
                actual_stream = deps.get_runtime_streams(rtm)[0]
                assert expected_stream == actual_stream

            xmd = mmd.get_xmd()
            assert "mbs_options" not in xmd
            assert xmd["mbs"]["static_context"]


class TestProcessModuleContextConfiguration:
    """
    With the introduction of static contexts, we have now several different configuration of
    static contexts for different major/minor RHEL releases.
    """

    def test_process_mse_configuration(self):
        """
        Testing the processing of MSE type packager (v2) file i. e. no static context.
        """

        yaml_str = read_staged_data("static_context_v2")
        mmd = load_mmd(yaml_str)
        mmd.set_xmd({})

        streams, static_context = process_module_context_configuration(mmd)

        assert not static_context
        assert len(streams) == 1
        assert not mmd.get_context()

    def test_process_initial_xmd_static_configuration(self):
        """
        Testing the processing of MSE type packager (v2) file with static context
        configuration in XMD
        """
        yaml_str = read_staged_data("static_context_v2")
        mmd = load_mmd(yaml_str)

        streams, static_context = process_module_context_configuration(mmd)

        assert static_context
        assert len(streams) == 2
        expected_contexts = ["context1", "context2"]
        for stream in streams:
            assert stream.get_context() in expected_contexts

    def test_process_xmd_static_context_rebuild(self):
        """
        Testing the processing of MSE type file (v2) used for rebuild with set static_context in
        mbs metadata in xmd.
        """

        yaml_str = read_staged_data("testmodule_v2")
        mmd = load_mmd(yaml_str)
        mmd.set_context("context1")
        mmd.set_xmd({"mbs": {"static_context": True}})

        streams, static_context = process_module_context_configuration(mmd)

        assert static_context
        assert len(streams) == 1
        assert streams[0].get_context() == "context1"

    def test_process_v3_packager_file(self):
        """
        Testing the processing of v3 packager file with static context configurations.
        """

        yaml_str = read_staged_data("v3/mmd_packager")
        mmd = load_mmd(yaml_str)

        streams, static_context = process_module_context_configuration(mmd)

        assert static_context
        assert len(streams) == 2
        expected_contexts = ["CTX1", "CTX2"]
        for stream in streams:
            assert stream.get_mdversion() == 2
            assert stream.get_context() in expected_contexts
            assert stream.is_static_context()


class TestApplySideTag:
    def get_mmd(self):
        yaml_str = """
document: modulemd
version: 2
data:
    name: app
    stream: test
    summary: "A test module"
    description: >
        "A test module stream"
    license:
        module: [ MIT ]
    dependencies:
        - buildrequires:
            platform: []
            gtk: []
          requires:
            platform: []
            gtk: []
        """
        return load_mmd(yaml_str)

    def test_apply_side_tag(self):
        """
        Test that the side tag option is correctly added into the xmd
        """
        mmd = self.get_mmd()
        side_tag = "SIDETAG"
        _apply_side_tag(mmd, {"side_tag": side_tag})

        xmd = mmd.get_xmd()
        assert xmd["mbs"]["side_tag"] == side_tag

    def test_apply_side_tag_no_option(self):
        """
        Test that the xmd is unchanged when option not given
        """
        mmd = self.get_mmd()
        xmd_orig = mmd.get_xmd()
        _apply_side_tag(mmd, {})

        xmd = mmd.get_xmd()
        assert xmd == xmd_orig
        assert "side_tag" not in xmd.get("mbs", {})


@pytest.mark.usefixtures("reuse_component_init_data")
class TestUtilsComponentReuse:
    @mock.patch("module_build_service.web.submit.submit_module_build")
    def test_submit_module_build_from_yaml_with_skiptests(self, mock_submit):
        """
        Tests local module build from a yaml file with the skiptests option

        Args:
            mock_submit (MagickMock): mocked function submit_module_build, which we then
                inspect if it was called with correct arguments
        """
        module_dir = tempfile.mkdtemp()
        module = models.ModuleBuild.get_by_id(db_session, 3)
        mmd = module.mmd()
        modulemd_yaml = mmd_to_str(mmd)
        modulemd_file_path = path.join(module_dir, "testmodule.yaml")

        username = "test"
        stream = "dev"

        with io.open(modulemd_file_path, "w", encoding="utf-8") as fd:
            fd.write(modulemd_yaml)

        with open(modulemd_file_path, "rb") as fd:
            handle = FileStorage(fd)
            submit_module_build_from_yaml(
                db_session, username, handle, {}, stream=stream, skiptests=True)
            mock_submit_args = mock_submit.call_args[0]
            username_arg = mock_submit_args[1]
            mmd_arg = mock_submit_args[2]
            assert mmd_arg.get_stream_name() == stream
            assert "\n\n%__spec_check_pre exit 0\n" in mmd_arg.get_buildopts().get_rpm_macros()
            assert username_arg == username
        rmtree(module_dir)

    @mock.patch("module_build_service.web.submit.submit_module_build")
    def test_submit_module_build_from_yaml_packager_v3(self, mock_submit):
        """
        Tests local module build from a yaml file with the skiptests option

        Args:
            mock_submit (MagickMock): mocked function submit_module_build, which we then
                inspect if it was called with correct arguments
        """
        module_dir = tempfile.mkdtemp()
        modulemd_yaml = read_staged_data("v3/mmd_packager")
        modulemd_file_path = path.join(module_dir, "testmodule.yaml")

        username = "test"
        stream = "dev"

        with io.open(modulemd_file_path, "w", encoding="utf-8") as fd:
            fd.write(modulemd_yaml)

        with open(modulemd_file_path, "rb") as fd:
            handle = FileStorage(fd)
            submit_module_build_from_yaml(
                db_session, username, handle, {}, stream=stream, skiptests=False)
            mock_submit_args = mock_submit.call_args[0]
            username_arg = mock_submit_args[1]
            mmd_arg = mock_submit_args[2]
            assert mmd_arg.get_stream_name() == stream
            assert username_arg == username
        rmtree(module_dir)

    @mock.patch("module_build_service.web.submit.generate_expanded_mmds")
    def test_submit_build_new_mse_build(self, generate_expanded_mmds):
        """
        Tests that finished build can be resubmitted in case the resubmitted
        build adds new MSE build (it means there are new expanded
        buildrequires).
        """
        build = make_module_in_db("foo:stream:0:c1")
        assert build.state == models.BUILD_STATES["ready"]

        mmd1 = build.mmd()
        mmd2 = build.mmd()

        mmd2.set_context("c2")
        generate_expanded_mmds.return_value = [mmd1, mmd2]
        # Create a copy of mmd1 without xmd.mbs, since that will cause validate_mmd to fail
        mmd1_copy = mmd1.copy()
        mmd1_copy.set_xmd({})

        ux_timestamp = "1613048427"
        version = provide_module_stream_version_from_timestamp(ux_timestamp)

        builds = submit_module_build(db_session, "foo", mmd1_copy, {}, version)
        ret = {b.mmd().get_context(): b.state for b in builds}

        assert ret == {"c1": models.BUILD_STATES["ready"], "c2": models.BUILD_STATES["init"]}
        assert builds[0].siblings(db_session) == [builds[1].id]
        assert builds[1].siblings(db_session) == [builds[0].id]

    @mock.patch("module_build_service.web.submit.generate_expanded_mmds")
    @mock.patch(
        "module_build_service.common.config.Config.scratch_build_only_branches",
        new_callable=mock.PropertyMock,
        return_value=["^private-.*"],
    )
    def test_submit_build_scratch_build_only_branches(self, cfg, generate_expanded_mmds):
        """
        Tests the "scratch_build_only_branches" config option.
        """
        mmd = make_module("foo:stream:0:c1")
        generate_expanded_mmds.return_value = [mmd]
        # Create a copy of mmd1 without xmd.mbs, since that will cause validate_mmd to fail
        mmd_copy = mmd.copy()
        mmd_copy.set_xmd({})

        ux_timestamp = "1613048427"
        version = provide_module_stream_version_from_timestamp(ux_timestamp)

        with pytest.raises(
            ValidationError,
            match="Only scratch module builds can be built from this branch.",
        ):
            submit_module_build(db_session, "foo", mmd_copy, {"branch": "private-foo"}, version)

        submit_module_build(db_session, "foo", mmd_copy, {"branch": "otherbranch"}, version)
