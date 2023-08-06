from setuptools import setup, find_packages

package_name = "burp"
description = "Burp interface with typing hints"
readme = open("README.rst").read()
requirements = []

package = __import__(package_name)
package_version = package.__version__
package_url = package.__url__

setup(
    name=package_name,
    version=package_version,
    packages=["burp"],
    url=package.__url__,
    license='MIT',
    author='Erlend Leiknes',
    author_email=package.__author_email__,
    description=description,
    install_requires=requirements,
    long_description = readme,
    classifiers = [
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: Jython',
        'Intended Audience :: Developers',
    ]
)
