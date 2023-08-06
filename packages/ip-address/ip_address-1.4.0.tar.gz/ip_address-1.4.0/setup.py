from setuptools import setup, find_packages

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
    name = "ip_address",
    version = "1.4.0",
    license = "MIT",
    url = "https://github.com/dewittethomas/ip_address",
    
    description = "A tracker that gets your public IP address",
    long_description = long_description,
    long_description_content_type = "text/markdown",

    package_dir = {"ip_address": "ip_address"},
    install_requires = [
        "requests>=2.22.0"
    ],

    packages = find_packages(),

    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],

    keywords = "ip address ip-address public vpn dns ipv4 ipv6 isp location"
)