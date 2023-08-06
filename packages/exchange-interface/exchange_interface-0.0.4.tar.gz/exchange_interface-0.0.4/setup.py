from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

packages = ['exchange_interface']

setup(
    name="exchange_interface",

    version="0.0.4",
    # 0.0.4 - Added 'return resp' to .UpdateCalendar()
    # 0.0.3 - added EWS.errorMessage to get more info about Disconnected state

    packages=packages,
    install_requires=[
        'calendar_base',
        'requests',
    ],

    author="Grant miller",
    author_email="grant@grant-miller.com",
    description="An interface to Microsoft Exchange Web Services (EWS). Allows the user to manipulate the outlook calendar events.",
    long_description=long_description,
    license="PSF",
    keywords="grant miller microsoft office365 ews",
    url="https://github.com/GrantGMiller/exchange_interface",  # project home page, if any
    project_urls={
        "Source Code": "https://github.com/GrantGMiller/exchange_interface",
    }

)
