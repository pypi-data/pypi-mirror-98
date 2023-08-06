import shutil
import os
from setuptools import setup, find_packages, Command

with open("requirements.txt", encoding="utf-8") as r:
    requires = r.read().splitlines()

with open("readme.md", encoding="utf-8") as f:
    readme = f.read()


class Clean(Command):
    DIST = ["./build", "./dist", "./python_objectionlol.egg-info"]
    ALL = DIST
    description = "clean generated files"
    user_options = [("dist", None, "clean distribution files"),
                    ("all", None, "clean all generated files")]

    def __init__(self, dist, **kw):
        super().__init__(dist, **kw)

        self.dist = None
        self.api = None
        self.docs = None
        self.all = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        paths = list()
        if self.dist:
            paths += Clean.DIST
        if self.all or not paths:
            paths += Clean.ALL

        for path in paths:
            try:
                shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
            except OSError:
                print("skipping {}".format(path))
            else:
                print("removing {}".format(path))


setup(
    name="python-objectionlol",
    version="0.0.2",
    author="LёNya",
    description="python wrapper for objection.lol",
    license="WTFPL-2",
    keywords="wrapper objectionlol objection.lol python",
    url="https://gitlab.com/LeNya/python-objectionlol",
    packages=find_packages(exclude="examples"),
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires="~=3.7",
    install_requires=requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "License :: Public Domain"
    ],
    cmdclass={
        "clean": Clean,
    }
)
