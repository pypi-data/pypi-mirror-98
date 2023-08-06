from pathlib import Path
import shlex

import pkg_resources
from grpc_tools import protoc
from setuptools import setup, find_packages
from setuptools.command.egg_info import egg_info
from setuptools.command.build_py import build_py
from setuptools.command.install import install


def get_pkg_dirs():
    return [pkg_dir for pkg_dir in Path("arkon_schema").rglob("*") if pkg_dir.is_dir()]


def cleanup():
    for p in Path("arkon_schema").rglob("*.py"):
        p.unlink()


INIT_CONTENTS = """
import pkgutil

__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module
"""


def touch_init_py(path):
    (path / "__init__.py").resolve().write_text(INIT_CONTENTS)


def autogenerate_package():

    proto_include = pkg_resources.resource_filename("grpc_tools", "_proto")

    for proto in Path("arkon_schema").rglob("*.proto"):
        args = f"grpc_tools.protoc -I{proto_include} --proto_path={Path('.').absolute()} --python_out=. --grpc_python_out=. {proto.absolute()}"  # noqa: E501
        failure = protoc.main(shlex.split(args))
        if failure:
            raise Exception(f"Failed to compile proto {proto}")

    touch_init_py(Path("arkon_schema"))
    for d in get_pkg_dirs():
        touch_init_py(d)


class CustomEggInstall(egg_info):
    def run(self):
        autogenerate_package()
        super().run()


class CustomBuildInstall(build_py):
    def run(self):
        autogenerate_package()
        super().run()


class CustomCleanup(install):
    def run(self):
        super().run()
        cleanup()


cmdclass = {
    "build_py": CustomBuildInstall,
    "egg_info": CustomEggInstall,
    "install": CustomCleanup,
}


def setup_package():
    setup(
        name="arkon-schema",
        url="https://github.com/arkon/arkon-schema",
        version="0.0.1.dev1",
        packages=find_packages(),
        cmdclass=cmdclass,
    )


if __name__ == "__main__":
    setup_package()
