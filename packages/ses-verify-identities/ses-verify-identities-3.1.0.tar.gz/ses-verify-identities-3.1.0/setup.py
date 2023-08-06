import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "ses-verify-identities",
    "version": "3.1.0",
    "description": "@seeebiii/ses-verify-identities",
    "license": "MIT",
    "url": "https://github.com/seeebiii/ses-verify-identities",
    "long_description_content_type": "text/markdown",
    "author": "Sebastian Hesse<info@sebastianhesse.de>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/seeebiii/ses-verify-identities"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "ses_verify_identities",
        "ses_verify_identities._jsii"
    ],
    "package_data": {
        "ses_verify_identities._jsii": [
            "ses-verify-identities@3.1.0.jsii.tgz"
        ],
        "ses_verify_identities": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-iam>=1.93.0, <2.0.0",
        "aws-cdk.aws-route53>=1.93.0, <2.0.0",
        "aws-cdk.aws-sns>=1.93.0, <2.0.0",
        "aws-cdk.core>=1.93.0, <2.0.0",
        "aws-cdk.custom-resources>=1.93.0, <2.0.0",
        "aws-cdk.cx-api>=1.93.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
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
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
