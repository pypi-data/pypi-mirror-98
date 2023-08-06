from pyfonycore.bootstrap.config.raw import container_init_resolver


def resolve(raw_config, pyproject_source: str):
    if "root_module_name" in raw_config:
        return raw_config["root_module_name"]

    container_init_spec = container_init_resolver.get_container_init(raw_config, pyproject_source)

    return _resolve_root_module_name(container_init_spec[0])


def _resolve_root_module_name(module_name):
    return module_name[0 : module_name.find(".")]  # noqa: E203
