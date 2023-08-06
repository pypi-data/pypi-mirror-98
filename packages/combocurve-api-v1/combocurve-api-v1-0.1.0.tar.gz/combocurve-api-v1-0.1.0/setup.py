from setuptools import setup

setup(
    install_requires=[
        "cffi==1.14.5",
        "cryptography==3.4.6",
        "dataclasses==0.8; python_version == '3.6'",
        "pycparser==2.20; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pyjwt[crypto]==2.0.1",
    ],
    dependency_links=[],
)
