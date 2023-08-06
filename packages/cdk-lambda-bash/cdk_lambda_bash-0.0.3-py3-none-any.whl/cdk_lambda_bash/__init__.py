'''
[![NPM version](https://badge.fury.io/js/cdk-lambda-bash.svg)](https://badge.fury.io/js/cdk-lambda-bash)
[![PyPI version](https://badge.fury.io/py/cdk-lambda-bash.svg)](https://badge.fury.io/py/cdk-lambda-bash)
[![Build](https://github.com/pahud/cdk-lambda-bash/actions/workflows/build.yml/badge.svg)](https://github.com/pahud/cdk-lambda-bash/actions/workflows/build.yml)

# cdk-lambda-bash

Deploy Lambda container image with Bash script support in AWS CDK

# Why

AWS Lambda has the [docker container image support](https://aws.amazon.com/tw/blogs/aws/new-for-aws-lambda-container-image-support/) since AWS re:Invent 2020 which allows you to run your Lambda code in a custom container image. Inspired by [nikovirtala/cdk-eks-experiment](https://github.com/nikovirtala/cdk-eks-experiment/), `cdk-lambda-bash` allows you to specify a local shell script and bundle it up as a custom resource in your cdk stack. On cdk deployment, your shell script will be executed in a Lambda container environment.

# BashExecFunction

At this moment, we are offering `BashExecFunction` construct class which is a high-level abstraction of `lambda.Function`. By defining the `script` property which poins to your local shell script, on `cdk deploy`, this script will be bundled into a custom docker image and published as a `lambda.DockerImageFunction`.

If you `fn.run()`, a custom resource will be created and the `lambda.DockerImageFunction` will be executed on deployment.

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app = cdk.App()

stack = cdk.Stack(app, "my-stack")

# bundle your Lambda function to execute the local demo.sh in container
fn = BashExecFunction(stack, "Demo",
    script=path.join(__dirname, "../demo.sh")
)

# run it as custom resource on deployment
fn.run()
```

# In Action

See this [tweet](https://twitter.com/pahudnet/status/1370301964836241408)

![](https://pbs.twimg.com/media/EwRGRxnUcAQBng-?format=jpg&name=4096x4096)

![](https://pbs.twimg.com/media/EwRKGfsUYAENjP-?format=jpg&name=4096x4096)
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

import aws_cdk.aws_lambda
import aws_cdk.core


class BashExecFunction(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-lambda-bash.BashExecFunction",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        script: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param script: The path of the shell script to be executed.
        '''
        props = BashExecFunctionProps(script=script)

        jsii.create(BashExecFunction, self, [scope, id, props])

    @jsii.member(jsii_name="run")
    def run(self) -> None:
        return typing.cast(None, jsii.invoke(self, "run", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="handler")
    def handler(self) -> aws_cdk.aws_lambda.DockerImageFunction:
        return typing.cast(aws_cdk.aws_lambda.DockerImageFunction, jsii.get(self, "handler"))


@jsii.data_type(
    jsii_type="cdk-lambda-bash.BashExecFunctionProps",
    jsii_struct_bases=[],
    name_mapping={"script": "script"},
)
class BashExecFunctionProps:
    def __init__(self, *, script: builtins.str) -> None:
        '''
        :param script: The path of the shell script to be executed.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "script": script,
        }

    @builtins.property
    def script(self) -> builtins.str:
        '''The path of the shell script to be executed.'''
        result = self._values.get("script")
        assert result is not None, "Required property 'script' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BashExecFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BashExecFunction",
    "BashExecFunctionProps",
]

publication.publish()
