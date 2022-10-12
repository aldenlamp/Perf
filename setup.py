from setuptools import setup, find_packages

VERSION = "0.0.0"
PACKAGE_NAME = "Performance Tracker"
REQUIREMENTS = ["yapf>=0.32.0", "matplotlib>=3.5.3"]

setup(name=PACKAGE_NAME,
      version=VERSION,
      author="Alden Lamp",
      author_email="aldenblamp@gmail.com",
      description=("This is a simple tool to help me track the runtime and "
                   "success stats of my C++ project"),
      long_description=open("README.md", "r", encoding="utf-8").read(),
      install_requires=REQUIREMENTS,
      packages=find_packages(where=".", include=["perf_tracker"]),
      entry_points={'console_scripts': ['perf = perf_tracker.main:main']})
