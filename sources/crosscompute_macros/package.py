from importlib import import_module
from packaging import version as version_module

from .error import PackageError


def import_attribute(attribute_string):
    module_string, attribute_name = attribute_string.rsplit('.', maxsplit=1)
    return getattr(import_module(module_string), attribute_name)


def is_newer_version(new_version_text, old_version_text):
    normalized_old_version, normalized_new_version = parse_versions([
        old_version_text, new_version_text])
    return normalized_old_version < normalized_new_version


def is_equivalent_version(
        new_version_text, old_version_text, version_depth=None):
    normalized_old_version, normalized_new_version = parse_versions([
        old_version_text, new_version_text])
    if version_depth:
        normalized_old_version = normalized_old_version[:version_depth]
        normalized_new_version = normalized_new_version[:version_depth]
    return normalized_old_version == normalized_new_version


def parse_versions(version_texts):
    versions = [parse_version(_) for _ in version_texts]
    maximum_version_depth = max(len(_) for _ in versions)
    return [normalize_version(_, maximum_version_depth) for _ in versions]


def normalize_version(version, depth):
    version_length = len(version)
    if version_length < depth:
        version = version + (0,) * (depth - version_length)
    elif version_length > depth:
        version = version[:depth]
    return version


def parse_version(text):
    try:
        version = version_module.parse(text).release
    except version_module.InvalidVersion:
        raise PackageError(f'version "{text}" is not valid')
    return version
