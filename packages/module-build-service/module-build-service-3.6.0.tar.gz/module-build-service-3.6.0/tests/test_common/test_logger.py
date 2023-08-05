# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
from __future__ import absolute_import
import os
from os import path
import pytest
import shutil
import tempfile

from module_build_service.common import log, models
from module_build_service.common.logger import ModuleBuildLogs
from module_build_service.scheduler.consumer import MBSConsumer
from module_build_service.scheduler.db_session import db_session


@pytest.fixture()
def test_logger_fixture(request, provide_test_data):
    log.debug(request.function.__module__)
    try:
        # py2
        test_id = ".".join([
            path.splitext(path.basename(__file__))[0],
            request.function.im_class.__name__,
            request.function.im_func.__name__,
        ])
    except AttributeError:
        # py3
        test_id = ".".join([
            path.splitext(path.basename(__file__))[0],
            request.function.__self__.__class__.__name__,
            request.function.__self__.__class__.__name__,
        ])

    base = tempfile.mkdtemp(prefix="mbs-", suffix="-%s" % test_id)
    name_format = "build-{id}.log"
    print("Storing build logs in %r" % base)
    request.cls.build_log = ModuleBuildLogs(base, name_format)
    request.cls.base = base
    yield
    MBSConsumer.current_module_build_id = None
    shutil.rmtree(base)


@pytest.mark.usefixtures("test_logger_fixture")
class TestLogger:

    def test_module_build_logs(self):
        """
        Tests that ModuleBuildLogs is logging properly to build log file.
        """
        build = models.ModuleBuild.get_by_id(db_session, 2)

        # Initialize logging, get the build log path and remove it to
        # ensure we are not using some garbage from previous failed test.
        self.build_log.start(db_session, build)
        path = self.build_log.path(db_session, build)
        assert path[len(self.base):] == "/build-2.log"
        if os.path.exists(path):
            os.unlink(path)

        # Try logging without the MBSConsumer.current_module_build_id set.
        # No log file should be created.
        log.debug("ignore this test msg")
        log.info("ignore this test msg")
        log.warning("ignore this test msg")
        log.error("ignore this test msg")
        self.build_log.stop(build)
        assert not os.path.exists(path)

        # Try logging with current_module_build_id set to 2 and then to 2.
        # Only messages with current_module_build_id set to 2 should appear in
        # the log.
        self.build_log.start(db_session, build)
        MBSConsumer.current_module_build_id = 1
        log.debug("ignore this test msg1")
        log.info("ignore this test msg1")
        log.warning("ignore this test msg1")
        log.error("ignore this test msg1")

        MBSConsumer.current_module_build_id = 2
        log.debug("ignore this test msg2")
        log.info("ignore this test msg2")
        log.warning("ignore this test msg2")
        log.error("ignore this test msg2")

        self.build_log.stop(build)
        assert os.path.exists(path)
        with open(path, "r") as f:
            data = f.read()
            # Note that DEBUG is not present unless configured server-wide.
            for level in ["INFO", "WARNING", "ERROR"]:
                assert data.find("MBS - {0} - ignore this test msg2".format(level)) != -1

        # Try to log more messages when build_log for module 1 is stopped.
        # New messages should not appear in a log.
        MBSConsumer.current_module_build_id = 2
        log.debug("ignore this test msg3")
        log.info("ignore this test msg3")
        log.warning("ignore this test msg3")
        log.error("ignore this test msg3")
        self.build_log.stop(build)
        with open(path, "r") as f:
            data = f.read()
            assert data.find("ignore this test msg3") == -1

    def test_module_build_logs_name_format(self):
        build = models.ModuleBuild.get_by_id(db_session, 2)

        log1 = ModuleBuildLogs("/some/path", "build-{id}.log")
        assert log1.name(db_session, build) == "build-2.log"
        assert log1.path(db_session, build) == "/some/path/build-2.log"

        log2 = ModuleBuildLogs("/some/path", "build-{name}-{stream}-{version}.log")
        assert log2.name(db_session, build) == "build-nginx-1-2.log"
        assert log2.path(db_session, build) == "/some/path/build-nginx-1-2.log"
