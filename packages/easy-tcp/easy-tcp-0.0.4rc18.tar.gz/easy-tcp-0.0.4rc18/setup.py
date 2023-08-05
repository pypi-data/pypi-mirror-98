from setuptools import setup, Extension
import sys

# if "--compile" in sys.argv:
#     print("Compiling...")
#     from Cython.Build import cythonize
#     sys.argv.remove("--compile")
#     ext_modules = cythonize(
#         Extension(
#             "easy_tcp",
#             sources=[
#                 "process.c",
#                 "server.c",
#                 "easy_tcp/cython_src/server.pyx"
#             ],
#         )
#     )
# else:
#     print("Releasing...")
ext_modules = [
    Extension(
        "easy_tcp",
        [
            "easy_tcp",
            "easy_tcp.cython_src",
        ],
    )
]


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name="easy-tcp",
        version="0.0.4rc18",
        description="Python TCP WSGI Server",
        packages=["easy_tcp", "easy_tcp.cython_src"],
        install_requires=[
            "cython"
    ],
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
)
