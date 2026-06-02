"""Configuration system — template + sparse user override."""

from __future__ import annotations

from typing import Any

from jiuwenclaw.utils import (
    get_config_file,
    load_yaml_dict,
    merge_template_with_override,
    resolve_env_vars,
    resolve_shipped_config_path,
)


def get_merged_config_dict() -> dict[str, Any]:
    """Merge template with user override. User wins on conflicts."""
    template = load_yaml_dict(resolve_shipped_config_path())
    override = load_yaml_dict(get_config_file())
    return merge_template_with_override(template, override)


def get_config() -> dict[str, Any]:
    """Get fully resolved config (merged + env vars resolved)."""
    return resolve_env_vars(get_merged_config_dict())


def get_config_raw() -> dict[str, Any]:
    """Get merged config without env var resolution."""
    return get_merged_config_dict()
