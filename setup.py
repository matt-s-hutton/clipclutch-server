from setuptools import setup

setup(
    name="ccserv",
    version="0.1.0",
    packages=[
        "ccserv",
        "ccserv.configuration",
        "ccserv.model",
        "ccserv.router",
        "ccserv.service",
    ],
    install_requires=[
        'fastapi',
        'uvicorn',
        'pydantic[dotenv]',
        'pydantic[email]',
        'aiosmtplib'
    ],
    entry_points={
        "console_scripts": [
            "ccserv = ccserv.run:main",
        ],
    },
    python_requires=">=3.7",
)