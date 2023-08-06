'''
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
        "edge_lambdas": [my_extension
        ]
    }
)
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_certificatemanager
import aws_cdk.aws_cloudfront
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.core


class Distribution(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-cloudfront-plus.Distribution",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        default_behavior: aws_cdk.aws_cloudfront.BehaviorOptions,
        additional_behaviors: typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_cloudfront.BehaviorOptions]] = None,
        certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate] = None,
        comment: typing.Optional[builtins.str] = None,
        default_root_object: typing.Optional[builtins.str] = None,
        domain_names: typing.Optional[typing.List[builtins.str]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        enable_ipv6: typing.Optional[builtins.bool] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        error_responses: typing.Optional[typing.List[aws_cdk.aws_cloudfront.ErrorResponse]] = None,
        geo_restriction: typing.Optional[aws_cdk.aws_cloudfront.GeoRestriction] = None,
        http_version: typing.Optional[aws_cdk.aws_cloudfront.HttpVersion] = None,
        log_bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
        log_file_prefix: typing.Optional[builtins.str] = None,
        log_includes_cookies: typing.Optional[builtins.bool] = None,
        minimum_protocol_version: typing.Optional[aws_cdk.aws_cloudfront.SecurityPolicyProtocol] = None,
        price_class: typing.Optional[aws_cdk.aws_cloudfront.PriceClass] = None,
        web_acl_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param default_behavior: The default behavior for the distribution.
        :param additional_behaviors: Additional behaviors for the distribution, mapped by the pathPattern that specifies which requests to apply the behavior to. Default: - no additional behaviors are added.
        :param certificate: A certificate to associate with the distribution. The certificate must be located in N. Virginia (us-east-1). Default: - the CloudFront wildcard certificate (*.cloudfront.net) will be used.
        :param comment: Any comments you want to include about the distribution. Default: - no comment
        :param default_root_object: The object that you want CloudFront to request from your origin (for example, index.html) when a viewer requests the root URL for your distribution. If no default object is set, the request goes to the origin's root (e.g., example.com/). Default: - no default root object
        :param domain_names: Alternative domain names for this distribution. If you want to use your own domain name, such as www.example.com, instead of the cloudfront.net domain name, you can add an alternate domain name to your distribution. If you attach a certificate to the distribution, you must add (at least one of) the domain names of the certificate to this list. Default: - The distribution will only support the default generated name (e.g., d111111abcdef8.cloudfront.net)
        :param enabled: Enable or disable the distribution. Default: true
        :param enable_ipv6: Whether CloudFront will respond to IPv6 DNS requests with an IPv6 address. If you specify false, CloudFront responds to IPv6 DNS requests with the DNS response code NOERROR and with no IP addresses. This allows viewers to submit a second request, for an IPv4 address for your distribution. Default: true
        :param enable_logging: Enable access logging for the distribution. Default: - false, unless ``logBucket`` is specified.
        :param error_responses: How CloudFront should handle requests that are not successful (e.g., PageNotFound). Default: - No custom error responses.
        :param geo_restriction: Controls the countries in which your content is distributed. Default: - No geographic restrictions
        :param http_version: Specify the maximum HTTP version that you want viewers to use to communicate with CloudFront. For viewers and CloudFront to use HTTP/2, viewers must support TLS 1.2 or later, and must support server name identification (SNI). Default: HttpVersion.HTTP2
        :param log_bucket: The Amazon S3 bucket to store the access logs in. Default: - A bucket is created if ``enableLogging`` is true
        :param log_file_prefix: An optional string that you want CloudFront to prefix to the access log filenames for this distribution. Default: - no prefix
        :param log_includes_cookies: Specifies whether you want CloudFront to include cookies in access logs. Default: false
        :param minimum_protocol_version: The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections. CloudFront serves your objects only to browsers or devices that support at least the SSL version that you specify. Default: SecurityPolicyProtocol.TLS_V1_2_2019
        :param price_class: The price class that corresponds with the maximum price that you want to pay for CloudFront service. If you specify PriceClass_All, CloudFront responds to requests for your objects from all CloudFront edge locations. If you specify a price class other than PriceClass_All, CloudFront serves your objects from the CloudFront edge location that has the lowest latency among the edge locations in your price class. Default: PriceClass.PRICE_CLASS_ALL
        :param web_acl_id: Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution. To specify a web ACL created using the latest version of AWS WAF, use the ACL ARN, for example ``arn:aws:wafv2:us-east-1:123456789012:global/webacl/ExampleWebACL/473e64fd-f30b-4765-81a0-62ad96dd167a``. To specify a web ACL created using AWS WAF Classic, use the ACL ID, for example ``473e64fd-f30b-4765-81a0-62ad96dd167a``. Default: - No AWS Web Application Firewall web access control list (web ACL).
        '''
        props = DistributionProps(
            default_behavior=default_behavior,
            additional_behaviors=additional_behaviors,
            certificate=certificate,
            comment=comment,
            default_root_object=default_root_object,
            domain_names=domain_names,
            enabled=enabled,
            enable_ipv6=enable_ipv6,
            enable_logging=enable_logging,
            error_responses=error_responses,
            geo_restriction=geo_restriction,
            http_version=http_version,
            log_bucket=log_bucket,
            log_file_prefix=log_file_prefix,
            log_includes_cookies=log_includes_cookies,
            minimum_protocol_version=minimum_protocol_version,
            price_class=price_class,
            web_acl_id=web_acl_id,
        )

        jsii.create(Distribution, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="extensions")
    def extensions(self) -> typing.List["IExtensions"]:
        return typing.cast(typing.List["IExtensions"], jsii.get(self, "extensions"))


@jsii.data_type(
    jsii_type="cdk-cloudfront-plus.DistributionProps",
    jsii_struct_bases=[aws_cdk.aws_cloudfront.DistributionProps],
    name_mapping={
        "default_behavior": "defaultBehavior",
        "additional_behaviors": "additionalBehaviors",
        "certificate": "certificate",
        "comment": "comment",
        "default_root_object": "defaultRootObject",
        "domain_names": "domainNames",
        "enabled": "enabled",
        "enable_ipv6": "enableIpv6",
        "enable_logging": "enableLogging",
        "error_responses": "errorResponses",
        "geo_restriction": "geoRestriction",
        "http_version": "httpVersion",
        "log_bucket": "logBucket",
        "log_file_prefix": "logFilePrefix",
        "log_includes_cookies": "logIncludesCookies",
        "minimum_protocol_version": "minimumProtocolVersion",
        "price_class": "priceClass",
        "web_acl_id": "webAclId",
    },
)
class DistributionProps(aws_cdk.aws_cloudfront.DistributionProps):
    def __init__(
        self,
        *,
        default_behavior: aws_cdk.aws_cloudfront.BehaviorOptions,
        additional_behaviors: typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_cloudfront.BehaviorOptions]] = None,
        certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate] = None,
        comment: typing.Optional[builtins.str] = None,
        default_root_object: typing.Optional[builtins.str] = None,
        domain_names: typing.Optional[typing.List[builtins.str]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        enable_ipv6: typing.Optional[builtins.bool] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        error_responses: typing.Optional[typing.List[aws_cdk.aws_cloudfront.ErrorResponse]] = None,
        geo_restriction: typing.Optional[aws_cdk.aws_cloudfront.GeoRestriction] = None,
        http_version: typing.Optional[aws_cdk.aws_cloudfront.HttpVersion] = None,
        log_bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
        log_file_prefix: typing.Optional[builtins.str] = None,
        log_includes_cookies: typing.Optional[builtins.bool] = None,
        minimum_protocol_version: typing.Optional[aws_cdk.aws_cloudfront.SecurityPolicyProtocol] = None,
        price_class: typing.Optional[aws_cdk.aws_cloudfront.PriceClass] = None,
        web_acl_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_behavior: The default behavior for the distribution.
        :param additional_behaviors: Additional behaviors for the distribution, mapped by the pathPattern that specifies which requests to apply the behavior to. Default: - no additional behaviors are added.
        :param certificate: A certificate to associate with the distribution. The certificate must be located in N. Virginia (us-east-1). Default: - the CloudFront wildcard certificate (*.cloudfront.net) will be used.
        :param comment: Any comments you want to include about the distribution. Default: - no comment
        :param default_root_object: The object that you want CloudFront to request from your origin (for example, index.html) when a viewer requests the root URL for your distribution. If no default object is set, the request goes to the origin's root (e.g., example.com/). Default: - no default root object
        :param domain_names: Alternative domain names for this distribution. If you want to use your own domain name, such as www.example.com, instead of the cloudfront.net domain name, you can add an alternate domain name to your distribution. If you attach a certificate to the distribution, you must add (at least one of) the domain names of the certificate to this list. Default: - The distribution will only support the default generated name (e.g., d111111abcdef8.cloudfront.net)
        :param enabled: Enable or disable the distribution. Default: true
        :param enable_ipv6: Whether CloudFront will respond to IPv6 DNS requests with an IPv6 address. If you specify false, CloudFront responds to IPv6 DNS requests with the DNS response code NOERROR and with no IP addresses. This allows viewers to submit a second request, for an IPv4 address for your distribution. Default: true
        :param enable_logging: Enable access logging for the distribution. Default: - false, unless ``logBucket`` is specified.
        :param error_responses: How CloudFront should handle requests that are not successful (e.g., PageNotFound). Default: - No custom error responses.
        :param geo_restriction: Controls the countries in which your content is distributed. Default: - No geographic restrictions
        :param http_version: Specify the maximum HTTP version that you want viewers to use to communicate with CloudFront. For viewers and CloudFront to use HTTP/2, viewers must support TLS 1.2 or later, and must support server name identification (SNI). Default: HttpVersion.HTTP2
        :param log_bucket: The Amazon S3 bucket to store the access logs in. Default: - A bucket is created if ``enableLogging`` is true
        :param log_file_prefix: An optional string that you want CloudFront to prefix to the access log filenames for this distribution. Default: - no prefix
        :param log_includes_cookies: Specifies whether you want CloudFront to include cookies in access logs. Default: false
        :param minimum_protocol_version: The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections. CloudFront serves your objects only to browsers or devices that support at least the SSL version that you specify. Default: SecurityPolicyProtocol.TLS_V1_2_2019
        :param price_class: The price class that corresponds with the maximum price that you want to pay for CloudFront service. If you specify PriceClass_All, CloudFront responds to requests for your objects from all CloudFront edge locations. If you specify a price class other than PriceClass_All, CloudFront serves your objects from the CloudFront edge location that has the lowest latency among the edge locations in your price class. Default: PriceClass.PRICE_CLASS_ALL
        :param web_acl_id: Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution. To specify a web ACL created using the latest version of AWS WAF, use the ACL ARN, for example ``arn:aws:wafv2:us-east-1:123456789012:global/webacl/ExampleWebACL/473e64fd-f30b-4765-81a0-62ad96dd167a``. To specify a web ACL created using AWS WAF Classic, use the ACL ID, for example ``473e64fd-f30b-4765-81a0-62ad96dd167a``. Default: - No AWS Web Application Firewall web access control list (web ACL).
        '''
        if isinstance(default_behavior, dict):
            default_behavior = aws_cdk.aws_cloudfront.BehaviorOptions(**default_behavior)
        self._values: typing.Dict[str, typing.Any] = {
            "default_behavior": default_behavior,
        }
        if additional_behaviors is not None:
            self._values["additional_behaviors"] = additional_behaviors
        if certificate is not None:
            self._values["certificate"] = certificate
        if comment is not None:
            self._values["comment"] = comment
        if default_root_object is not None:
            self._values["default_root_object"] = default_root_object
        if domain_names is not None:
            self._values["domain_names"] = domain_names
        if enabled is not None:
            self._values["enabled"] = enabled
        if enable_ipv6 is not None:
            self._values["enable_ipv6"] = enable_ipv6
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if error_responses is not None:
            self._values["error_responses"] = error_responses
        if geo_restriction is not None:
            self._values["geo_restriction"] = geo_restriction
        if http_version is not None:
            self._values["http_version"] = http_version
        if log_bucket is not None:
            self._values["log_bucket"] = log_bucket
        if log_file_prefix is not None:
            self._values["log_file_prefix"] = log_file_prefix
        if log_includes_cookies is not None:
            self._values["log_includes_cookies"] = log_includes_cookies
        if minimum_protocol_version is not None:
            self._values["minimum_protocol_version"] = minimum_protocol_version
        if price_class is not None:
            self._values["price_class"] = price_class
        if web_acl_id is not None:
            self._values["web_acl_id"] = web_acl_id

    @builtins.property
    def default_behavior(self) -> aws_cdk.aws_cloudfront.BehaviorOptions:
        '''The default behavior for the distribution.'''
        result = self._values.get("default_behavior")
        assert result is not None, "Required property 'default_behavior' is missing"
        return typing.cast(aws_cdk.aws_cloudfront.BehaviorOptions, result)

    @builtins.property
    def additional_behaviors(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_cloudfront.BehaviorOptions]]:
        '''Additional behaviors for the distribution, mapped by the pathPattern that specifies which requests to apply the behavior to.

        :default: - no additional behaviors are added.
        '''
        result = self._values.get("additional_behaviors")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_cloudfront.BehaviorOptions]], result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]:
        '''A certificate to associate with the distribution.

        The certificate must be located in N. Virginia (us-east-1).

        :default: - the CloudFront wildcard certificate (*.cloudfront.net) will be used.
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[aws_cdk.aws_certificatemanager.ICertificate], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Any comments you want to include about the distribution.

        :default: - no comment
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_root_object(self) -> typing.Optional[builtins.str]:
        '''The object that you want CloudFront to request from your origin (for example, index.html) when a viewer requests the root URL for your distribution. If no default object is set, the request goes to the origin's root (e.g., example.com/).

        :default: - no default root object
        '''
        result = self._values.get("default_root_object")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Alternative domain names for this distribution.

        If you want to use your own domain name, such as www.example.com, instead of the cloudfront.net domain name,
        you can add an alternate domain name to your distribution. If you attach a certificate to the distribution,
        you must add (at least one of) the domain names of the certificate to this list.

        :default: - The distribution will only support the default generated name (e.g., d111111abcdef8.cloudfront.net)
        '''
        result = self._values.get("domain_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Enable or disable the distribution.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_ipv6(self) -> typing.Optional[builtins.bool]:
        '''Whether CloudFront will respond to IPv6 DNS requests with an IPv6 address.

        If you specify false, CloudFront responds to IPv6 DNS requests with the DNS response code NOERROR and with no IP addresses.
        This allows viewers to submit a second request, for an IPv4 address for your distribution.

        :default: true
        '''
        result = self._values.get("enable_ipv6")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        '''Enable access logging for the distribution.

        :default: - false, unless ``logBucket`` is specified.
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def error_responses(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_cloudfront.ErrorResponse]]:
        '''How CloudFront should handle requests that are not successful (e.g., PageNotFound).

        :default: - No custom error responses.
        '''
        result = self._values.get("error_responses")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_cloudfront.ErrorResponse]], result)

    @builtins.property
    def geo_restriction(self) -> typing.Optional[aws_cdk.aws_cloudfront.GeoRestriction]:
        '''Controls the countries in which your content is distributed.

        :default: - No geographic restrictions
        '''
        result = self._values.get("geo_restriction")
        return typing.cast(typing.Optional[aws_cdk.aws_cloudfront.GeoRestriction], result)

    @builtins.property
    def http_version(self) -> typing.Optional[aws_cdk.aws_cloudfront.HttpVersion]:
        '''Specify the maximum HTTP version that you want viewers to use to communicate with CloudFront.

        For viewers and CloudFront to use HTTP/2, viewers must support TLS 1.2 or later, and must support server name identification (SNI).

        :default: HttpVersion.HTTP2
        '''
        result = self._values.get("http_version")
        return typing.cast(typing.Optional[aws_cdk.aws_cloudfront.HttpVersion], result)

    @builtins.property
    def log_bucket(self) -> typing.Optional[aws_cdk.aws_s3.IBucket]:
        '''The Amazon S3 bucket to store the access logs in.

        :default: - A bucket is created if ``enableLogging`` is true
        '''
        result = self._values.get("log_bucket")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.IBucket], result)

    @builtins.property
    def log_file_prefix(self) -> typing.Optional[builtins.str]:
        '''An optional string that you want CloudFront to prefix to the access log filenames for this distribution.

        :default: - no prefix
        '''
        result = self._values.get("log_file_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_includes_cookies(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether you want CloudFront to include cookies in access logs.

        :default: false
        '''
        result = self._values.get("log_includes_cookies")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minimum_protocol_version(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudfront.SecurityPolicyProtocol]:
        '''The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections.

        CloudFront serves your objects only to browsers or devices that support at
        least the SSL version that you specify.

        :default: SecurityPolicyProtocol.TLS_V1_2_2019
        '''
        result = self._values.get("minimum_protocol_version")
        return typing.cast(typing.Optional[aws_cdk.aws_cloudfront.SecurityPolicyProtocol], result)

    @builtins.property
    def price_class(self) -> typing.Optional[aws_cdk.aws_cloudfront.PriceClass]:
        '''The price class that corresponds with the maximum price that you want to pay for CloudFront service.

        If you specify PriceClass_All, CloudFront responds to requests for your objects from all CloudFront edge locations.
        If you specify a price class other than PriceClass_All, CloudFront serves your objects from the CloudFront edge location
        that has the lowest latency among the edge locations in your price class.

        :default: PriceClass.PRICE_CLASS_ALL
        '''
        result = self._values.get("price_class")
        return typing.cast(typing.Optional[aws_cdk.aws_cloudfront.PriceClass], result)

    @builtins.property
    def web_acl_id(self) -> typing.Optional[builtins.str]:
        '''Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution.

        To specify a web ACL created using the latest version of AWS WAF, use the ACL ARN, for example
        ``arn:aws:wafv2:us-east-1:123456789012:global/webacl/ExampleWebACL/473e64fd-f30b-4765-81a0-62ad96dd167a``.
        To specify a web ACL created using AWS WAF Classic, use the ACL ID, for example ``473e64fd-f30b-4765-81a0-62ad96dd167a``.

        :default: - No AWS Web Application Firewall web access control list (web ACL).

        :see: https://docs.aws.amazon.com/cloudfront/latest/APIReference/API_CreateDistribution.html#API_CreateDistribution_RequestParameters.
        '''
        result = self._values.get("web_acl_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DistributionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cdk-cloudfront-plus.IExtensions")
class IExtensions(typing_extensions.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IExtensionsProxy"]:
        return _IExtensionsProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="functionVersion")
    def function_version(self) -> aws_cdk.aws_lambda.Version:
        ...


class _IExtensionsProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-cloudfront-plus.IExtensions"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="functionVersion")
    def function_version(self) -> aws_cdk.aws_lambda.Version:
        return typing.cast(aws_cdk.aws_lambda.Version, jsii.get(self, "functionVersion"))


class ServerlessApp(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-cloudfront-plus.ServerlessApp",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        semantic_version: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param application_id: 
        :param semantic_version: 
        '''
        props = ServerlessAppProps(
            application_id=application_id, semantic_version=semantic_version
        )

        jsii.create(ServerlessApp, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="resource")
    def resource(self) -> aws_cdk.core.CfnResource:
        return typing.cast(aws_cdk.core.CfnResource, jsii.get(self, "resource"))


@jsii.data_type(
    jsii_type="cdk-cloudfront-plus.ServerlessAppProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "semantic_version": "semanticVersion",
    },
)
class ServerlessAppProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        semantic_version: builtins.str,
    ) -> None:
        '''
        :param application_id: 
        :param semantic_version: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "application_id": application_id,
            "semantic_version": semantic_version,
        }

    @builtins.property
    def application_id(self) -> builtins.str:
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def semantic_version(self) -> builtins.str:
        result = self._values.get("semantic_version")
        assert result is not None, "Required property 'semantic_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerlessAppProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IExtensions)
class ModifyResponseHeader(
    ServerlessApp,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-cloudfront-plus.ModifyResponseHeader",
):
    def __init__(self, scope: aws_cdk.core.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        jsii.create(ModifyResponseHeader, self, [scope, id])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="eventType")
    def event_type(self) -> aws_cdk.aws_cloudfront.LambdaEdgeEventType:
        return typing.cast(aws_cdk.aws_cloudfront.LambdaEdgeEventType, jsii.get(self, "eventType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="functionVersion")
    def function_version(self) -> aws_cdk.aws_lambda.Version:
        return typing.cast(aws_cdk.aws_lambda.Version, jsii.get(self, "functionVersion"))


__all__ = [
    "Distribution",
    "DistributionProps",
    "IExtensions",
    "ModifyResponseHeader",
    "ServerlessApp",
    "ServerlessAppProps",
]

publication.publish()
