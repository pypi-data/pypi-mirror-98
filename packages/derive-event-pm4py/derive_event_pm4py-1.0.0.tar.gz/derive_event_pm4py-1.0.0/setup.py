import pathlib
from setuptools import setup

CURRENT_PATH = pathlib.Path(__file__).parent

README = (CURRENT_PATH/"README.md").read_text()

setup(
    name="derive_event_pm4py",
    version="1.0.0",
    description="It derives new events based on rules provided as inputs.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ajap10/derive_event_pm4py",
    author="Ajay Pandi",
    author_email="ajay.pandi@rwth-aachen.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["derive_event"],
    include_package_data=True,
    install_requires=['pandas', 'numpy', 'pm4py',
    ],
    entry_points={
        "console_scripts": [
            "derive=derive_event.derive:main",
        ]
    },
)