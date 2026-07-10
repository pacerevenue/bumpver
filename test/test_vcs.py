# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os

import pytest

from bumpver import vcs


class TestVCSAPICommit:
    @pytest.mark.parametrize(
        ["env_overrides"],
        [({},), ({"SKIP": "flake8"},)],
        ids=["no_overrides", "with_overrides"],
    )
    def test_merges_env_overrides_into_environ(self, monkeypatch, env_overrides):
        monkeypatch.setenv("EXISTING_VAR", "original")
        vcs_api = vcs.VCSAPI(name='git')

        captured_env = {}

        def fake_check_output(cmd_parts, env=None, **kwargs):
            captured_env.update(env)
            return b""

        monkeypatch.setattr(vcs.sp, 'check_output', fake_check_output)

        vcs_api.commit("a message", env_overrides)

        assert captured_env["EXISTING_VAR"] == "original"
        for key, value in env_overrides.items():
            assert captured_env[key] == value
