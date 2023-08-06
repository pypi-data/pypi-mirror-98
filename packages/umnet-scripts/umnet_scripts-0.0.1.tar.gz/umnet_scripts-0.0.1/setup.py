import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="umnet_scripts",
    version="0.0.1",
    author="University of Michigan",
    author_email="amylieb@umich.edu",
    license='MIT',
    description="Python tools for interacting with UMnet's network tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.umich.edu/its-inf-net/umnet-scripts",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'regex',
        'netaddr',
        'psycopg2-binary',
        'sqlalchemy',
        'pynetbox',
        'cx_Oracle',
        'ncclient',
    ],
    python_requires='>=3.6',
    scripts=['bin/equipdb_rancid_audit.py'],
)
