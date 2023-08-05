"""
 PyVpn

 Setup.py to ensure that all build prerequisites are available

 Usage (Mac OS X):
     python setup.py install

 """
from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="vpnpy",
    version=1.0,
    author="Bhavishya Maheshwari",
    author_email="<maheshwaribhavishya19@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyyaml', 'pexpect', 'openconnect', 'netifaces'],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'vpn'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)