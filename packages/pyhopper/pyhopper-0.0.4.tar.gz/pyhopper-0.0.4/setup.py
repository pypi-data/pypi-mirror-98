# Copyright 2021 Mathias Lechner and the PyHopper team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from setuptools import setup, find_packages

setup(
    name="pyhopper",
    version="0.0.4",
    python_requires=">3.6.0",
    packages=find_packages(),  # include/exclude arguments take * as wildcard, . for any sub-package names
    description="TODO",
    url="https://github.com/PyHopper/PyHopper",
    author="Mathias Lechner and the PyHopper team",
    author_email="mlech26l@gmail.com",
    license="Apache Software License (Apache 2.0)",
    install_requires=["packaging", "future", "numpy", "loky", "tqdm"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
    ],
)