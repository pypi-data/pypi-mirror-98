from setuptools import find_packages
from distutils.core import setup
from distutils.command.build_ext import build_ext
from distutils.extension import Extension
import sys


compiler_directives = {"language_level": "3"}

if "--et_comp" in sys.argv:
    print("Compiling...")
    from setuptools import setup
    from Cython.Build import cythonize, build_ext
    sys.argv.remove("--et_comp")
    ext_modules = cythonize(
        Extension(
            name="easy_tcp.cython_server",
            sources=[
                "easy_tcp/cython_server.pyx",
                "easy_tcp/core/process.c",
                "easy_tcp/core/server.c",
            ],
            language="c",
            include_dirs=["easy_tcp/core/"],
        ),
        compiler_directives=compiler_directives,
    )
else:
    from setuptools import setup
    print("Packaging...")
    ext_modules = [
        Extension(
            "easy_tcp.cython_server",
            ["easy_tcp/cython_server.c"],
            language="c",
            include_dirs=['easy_tcp/, easy_tcp/core/'],
        )
    ]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="easy-tcp",
    version="0.0.8rc9",
    install_requires=[],
    description="Python TCP WSGI Server",
    packages=find_packages(),
    zip_safe=False,
    ext_modules=ext_modules,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: Unix",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joegasewicz/easy-tcp",
    author="Joe Gasewicz",
    author_email="joegasewicz@gmail.com",
    package_data={'*': ['*.pxd', '*.h']},
    cmdclass={
        "build_ext": build_ext,
    }
)