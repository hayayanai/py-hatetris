# Available at setup time due to pyproject.toml
# from pybind11 import get_cmake_dir
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

__version__ = "0.1.0"

ext_modules = [
    Pybind11Extension("hate",
                      ["hatebind.cpp"],
                      language='c++',
                      # Example: passing in the version to the compiled code
                      define_macros=[('VERSION_INFO', __version__)],
                      ),
]

setup(
    name="hate",
    version=__version__,
    author="hayayanai",
    description="state written by cpp",
    long_description="",
    ext_modules=ext_modules,
    extras_require={"test": "pytest"},
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.10",
)
