from distutils.core import setup

setup(
    name='ccserv',
    version='1.0',
    py_modules=['main'],
    install_requires=[
        'fastapi',
        'uvicorn',
        'pydantic[dotenv]',
        'pydantic[email]',
        'aiosmtplib'
    ],
    include_package_data=True,
    zip_safe=False
)