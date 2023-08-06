'''
# replace this
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
