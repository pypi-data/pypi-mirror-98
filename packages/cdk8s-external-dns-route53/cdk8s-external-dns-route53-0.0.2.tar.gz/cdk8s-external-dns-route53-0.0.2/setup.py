import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk8s-external-dns-route53",
    "version": "0.0.2",
    "description": "@opencdk8s/cdk8s-external-dns-route53",
    "license": "Apache-2.0",
    "url": "https://github.com/opencdk8s/cdk8s-external-dns-route53",
    "long_description_content_type": "text/markdown",
    "author": "Hunter Thompson<aatman@auroville.org.in>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/opencdk8s/cdk8s-external-dns-route53"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk8s_external_dns_route53",
        "cdk8s_external_dns_route53._jsii"
    ],
    "package_data": {
        "cdk8s_external_dns_route53._jsii": [
            "cdk8s-external-dns-route53@0.0.2.jsii.tgz"
        ],
        "cdk8s_external_dns_route53": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-iam>=1.92.0, <2.0.0",
        "aws-cdk.core>=1.92.0, <2.0.0",
        "cdk8s-plus-17>=1.0.0.b10, <2.0.0",
        "cdk8s>=1.0.0.b10, <2.0.0",
        "constructs>=3.3.65, <4.0.0",
        "jsii>=1.24.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
