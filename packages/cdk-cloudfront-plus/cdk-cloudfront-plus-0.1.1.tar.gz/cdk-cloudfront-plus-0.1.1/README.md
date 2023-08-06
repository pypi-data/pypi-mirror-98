[![NPM version](https://badge.fury.io/js/cdk-cloudfront-plus.svg)](https://badge.fury.io/js/cdk-cloudfront-plus)
[![PyPI version](https://badge.fury.io/py/cdk-cloudfront-plus.svg)](https://badge.fury.io/py/cdk-cloudfront-plus)
![Release](https://github.com/pahud/cdk-cloudfront-plus/workflows/Release/badge.svg?branch=main)

# cdk-cloudfront-plus

CDK constructs library that allows you to build [AWS CloudFront Extensions](https://github.com/awslabs/aws-cloudfront-extensions) in **JavaScript**, **TypeScript** or **Python**.

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk_cloudfront_plus as cfplus

app = cdk.App()

stack = cdk.Stack(app, "demo-stack")

# prepare the extension
my_extension = cfplus.ModifyResponseHeader(stack, "myext")

# create the cloudfront distribution with extension(s)
cfplus.Distribution(stack, "dist",
    default_behavior={
        "origin": origins.HttpOrigin("aws.amazon.com"),
        "edge_lambdas": [my_extension]
    }
)
```
