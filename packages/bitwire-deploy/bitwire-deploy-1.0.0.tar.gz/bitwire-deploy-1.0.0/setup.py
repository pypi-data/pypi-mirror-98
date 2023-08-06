from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bitwire-deploy",
    version="1.0.0",
    description="BitWire Cloud deployment tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitwire.cloud",
    author="BitWire",
    author_email="hello@bitwire.cloud",
    license='GPLv3+',
    project_urls={
        'Bug Tracker': 'https://github.com/bitwirecloud/bitwire-cloud/issues',
        'Documentation': 'https://bitwire.cloud/documentation/',
        'Source Code': 'https://github.com/bitwirecloud/bitwire-cloud',
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    include_package_data=True,
    install_requires=["pycryptodome", "requests"],
    scripts=[
        "bitwire-deploy",
    ],
    python_requires=">=3.6",
    data_files=[],
)