import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cloudcomponents.cdk-stripe-webhook",
    "version": "1.30.1",
    "description": "Create, update and delete stripe webhooks with your app deployment",
    "license": "MIT",
    "url": "https://github.com/cloudcomponents/cdk-constructs",
    "long_description_content_type": "text/markdown",
    "author": "hupe1980",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cloudcomponents/cdk-constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cloudcomponents.cdk_stripe_webhook",
        "cloudcomponents.cdk_stripe_webhook._jsii"
    ],
    "package_data": {
        "cloudcomponents.cdk_stripe_webhook._jsii": [
            "cdk-stripe-webhook@1.30.1.jsii.tgz"
        ],
        "cloudcomponents.cdk_stripe_webhook": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-apigateway>=1.94.1, <2.0.0",
        "aws-cdk.aws-events>=1.94.1, <2.0.0",
        "aws-cdk.aws-iam>=1.94.1, <2.0.0",
        "aws-cdk.aws-lambda>=1.94.1, <2.0.0",
        "aws-cdk.core>=1.94.1, <2.0.0",
        "cloudcomponents.cdk-secret-key>=1.2.1, <2.0.0",
        "constructs>=3.2.0, <4.0.0",
        "jsii>=1.25.0, <2.0.0",
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
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
