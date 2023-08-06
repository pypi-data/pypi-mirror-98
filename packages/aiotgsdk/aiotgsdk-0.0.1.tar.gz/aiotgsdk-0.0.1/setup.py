#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020-2021 Evgeniy Privalov, https://linkedin.com/in/evgeniyprivalov/

from setuptools import (
	setup,
	find_packages
)

from aiotgsdk.__version__ import __version__

if __name__ == "__main__":
	packages = find_packages()

	requirements = []
	with open("requirements.txt", "r") as requirements_txt:
		for requirement in requirements_txt:
			requirements.append(requirement.strip())

	with open("./README.md", "r") as file:
		long_description = file.read()

	options = dict(
		script_name="setup.py",
		name="aiotgsdk",
		version=__version__,
		author="Evgeniy Privalov",
		author_email="evgeniyprivalov94@gmail.com",
		license="GPLv3+",
		url="https://github.com/evgeniyprivalov/aiotgsdk",
		project_urls={
			"Documentation": "https://github.com/evgeniyprivalov/aiotgsdk",
			"Bug Tracker": "https://github.com/evgeniyprivalov/aiotgsdk",
			"Source Code": "https://github.com/evgeniyprivalov/aiotgsdk",
			"News": "https://github.com/evgeniyprivalov/aiotgsdk",
			"Changelog": "https://github.com/evgeniyprivalov/aiotgsdk/blob/main/CHANGELOG.md",
		},
		download_url="https://pypi.org/project/aiotgsdk/",
		keywords="Python Telegram Asynchronous API Bot SDK",
		description="Python Telegram SDK to help make asynchronous requests to Telegram API",
		long_description=long_description,
		long_description_content_type="text/markdown",
		packages=packages,
		install_requires=requirements,
		include_package_data=True,
		classifiers=[
			"Development Status :: 5 - Production/Stable",
			"Intended Audience :: Developers",
			"License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
			"Natural Language :: English",
			"Operating System :: OS Independent",
			"Topic :: Software Development :: Libraries :: Python Modules",
			"Topic :: Communications :: Chat",
			"Topic :: Internet",
			"Programming Language :: Python",
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.7",
			"Programming Language :: Python :: 3.8",
			"Programming Language :: Python :: 3.9"
		],
		python_requires=">=3.7"
	)

	setup(**options)
