"""Tests for the config system."""

import os
from pathlib import Path

from jiuwenclaw.config import get_config, get_config_raw, get_merged_config_dict
from jiuwenclaw.utils import (
    get_config_dir,
    get_config_file,
    get_env_file,
    get_user_workspace_dir,
    merge_template_with_override,
    resolve_env_vars,
)


class TestMergeTemplateWithOverride:
    def test_user_wins_on_conflict(self):
        template = {"port": 19000, "host": "127.0.0.1"}
        override = {"port": 9999}
        result = merge_template_with_override(template, override)
        assert result["port"] == 9999  # user wins
        assert result["host"] == "127.0.0.1"  # template default

    def test_user_only_keys_preserved(self):
        template = {"a": 1}
        override = {"b": 2}
        result = merge_template_with_override(template, override)
        assert result["a"] == 1
        assert result["b"] == 2

    def test_nested_merge(self):
        template = {"web": {"host": "127.0.0.1", "port": 19000}}
        override = {"web": {"port": 3000}}
        result = merge_template_with_override(template, override)
        assert result["web"]["host"] == "127.0.0.1"
        assert result["web"]["port"] == 3000

    def test_empty_override(self):
        template = {"a": 1, "b": 2}
        result = merge_template_with_override(template, {})
        assert result == template


class TestResolveEnvVars:
    def test_simple_var(self):
        os.environ["TEST_VAR"] = "hello"
        result = resolve_env_vars("${TEST_VAR}")
        assert result == "hello"

    def test_var_with_default_not_set(self):
        os.environ.pop("TEST_MISSING", None)
        result = resolve_env_vars("${TEST_MISSING:-fallback}")
        assert result == "fallback"

    def test_var_with_default_is_set(self):
        os.environ["TEST_SET"] = "real_value"
        result = resolve_env_vars("${TEST_SET:-fallback}")
        assert result == "real_value"

    def test_var_not_set_no_default(self):
        os.environ.pop("TEST_MISSING", None)
        result = resolve_env_vars("${TEST_MISSING}")
        assert result == ""

    def test_nested_dict(self):
        os.environ["KEY"] = "sk-real"
        data = {"api": {"key": "${KEY:-sk-default}", "url": "https://api.example.com"}}
        result = resolve_env_vars(data)
        assert result["api"]["key"] == "sk-real"
        assert result["api"]["url"] == "https://api.example.com"

    def test_list(self):
        os.environ["A"] = "1"
        result = resolve_env_vars(["${A}", "${B:-2}"])
        assert result == ["1", "2"]

    def test_non_string_passthrough(self):
        assert resolve_env_vars(42) == 42
        assert resolve_env_vars(True) is True


class TestPathUtilities:
    def test_user_workspace_dir_default(self):
        path = get_user_workspace_dir()
        assert path.name == ".jiuwenclaw"

    def test_config_dir(self):
        path = get_config_dir()
        assert path.name == "config"

    def test_config_file(self):
        path = get_config_file()
        assert path.name == "config.yaml"

    def test_env_file(self):
        path = get_env_file()
        assert path.name == ".env"


class TestConfigIntegration:
    def test_get_merged_config_loads_template(self):
        config = get_merged_config_dict()
        assert "channels" in config
        assert config["channels"]["web"]["port"] == 19000
        assert "models" in config

    def test_get_config_resolves_env(self):
        config = get_config()
        assert "channels" in config
