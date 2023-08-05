import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

import constructs
from .. import (
    CfnResource as _CfnResource_e0a482dc,
    Construct as _Construct_e78e779f,
    Duration as _Duration_070aa057,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    Resource as _Resource_abff4495,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_cloudwatch import (
    Metric as _Metric_5b2b8e58,
    MetricOptions as _MetricOptions_1c185ae8,
    Unit as _Unit_113c79f9,
)
from ..aws_iam import (
    Grant as _Grant_bcb5eae7,
    IGrantable as _IGrantable_4c5a91d1,
    IPrincipal as _IPrincipal_93b48231,
    IRole as _IRole_59af6f50,
    PolicyStatement as _PolicyStatement_296fe8a3,
)
from ..aws_logs import ILogGroup as _ILogGroup_846e17a0


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.ActivityProps",
    jsii_struct_bases=[],
    name_mapping={"activity_name": "activityName"},
)
class ActivityProps:
    def __init__(self, *, activity_name: typing.Optional[builtins.str] = None) -> None:
        '''(experimental) Properties for defining a new Step Functions Activity.

        :param activity_name: (experimental) The name for this activity. Default: - If not supplied, a name is generated

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if activity_name is not None:
            self._values["activity_name"] = activity_name

    @builtins.property
    def activity_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for this activity.

        :default: - If not supplied, a name is generated

        :stability: experimental
        '''
        result = self._values.get("activity_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActivityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.AfterwardsOptions",
    jsii_struct_bases=[],
    name_mapping={
        "include_error_handlers": "includeErrorHandlers",
        "include_otherwise": "includeOtherwise",
    },
)
class AfterwardsOptions:
    def __init__(
        self,
        *,
        include_error_handlers: typing.Optional[builtins.bool] = None,
        include_otherwise: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for selecting the choice paths.

        :param include_error_handlers: (experimental) Whether to include error handling states. If this is true, all states which are error handlers (added through 'onError') and states reachable via error handlers will be included as well. Default: false
        :param include_otherwise: (experimental) Whether to include the default/otherwise transition for the current Choice state. If this is true and the current Choice does not have a default outgoing transition, one will be added included when .next() is called on the chain. Default: false

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if include_error_handlers is not None:
            self._values["include_error_handlers"] = include_error_handlers
        if include_otherwise is not None:
            self._values["include_otherwise"] = include_otherwise

    @builtins.property
    def include_error_handlers(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to include error handling states.

        If this is true, all states which are error handlers (added through 'onError')
        and states reachable via error handlers will be included as well.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("include_error_handlers")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def include_otherwise(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to include the default/otherwise transition for the current Choice state.

        If this is true and the current Choice does not have a default outgoing
        transition, one will be added included when .next() is called on the chain.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("include_otherwise")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AfterwardsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.CatchProps",
    jsii_struct_bases=[],
    name_mapping={"errors": "errors", "result_path": "resultPath"},
)
class CatchProps:
    def __init__(
        self,
        *,
        errors: typing.Optional[typing.List[builtins.str]] = None,
        result_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Error handler details.

        :param errors: (experimental) Errors to recover from by going to the given state. A list of error strings to retry, which can be either predefined errors (for example Errors.NoChoiceMatched) or a self-defined error. Default: All errors
        :param result_path: (experimental) JSONPath expression to indicate where to inject the error data. May also be the special value DISCARD, which will cause the error data to be discarded. Default: $

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if errors is not None:
            self._values["errors"] = errors
        if result_path is not None:
            self._values["result_path"] = result_path

    @builtins.property
    def errors(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Errors to recover from by going to the given state.

        A list of error strings to retry, which can be either predefined errors
        (for example Errors.NoChoiceMatched) or a self-defined error.

        :default: All errors

        :stability: experimental
        '''
        result = self._values.get("errors")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to indicate where to inject the error data.

        May also be the special value DISCARD, which will cause the error
        data to be discarded.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("result_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CatchProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnActivity(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_stepfunctions.CfnActivity",
):
    '''A CloudFormation ``AWS::StepFunctions::Activity``.

    :cloudformationResource: AWS::StepFunctions::Activity
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-activity.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: builtins.str,
        tags: typing.Optional[typing.List["CfnActivity.TagsEntryProperty"]] = None,
    ) -> None:
        '''Create a new ``AWS::StepFunctions::Activity``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::StepFunctions::Activity.Name``.
        :param tags: ``AWS::StepFunctions::Activity.Tags``.
        '''
        props = CfnActivityProps(name=name, tags=tags)

        jsii.create(CfnActivity, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::StepFunctions::Activity.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-activity.html#cfn-stepfunctions-activity-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''``AWS::StepFunctions::Activity.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-activity.html#cfn-stepfunctions-activity-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_stepfunctions.CfnActivity.TagsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsEntryProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''
            :param key: ``CfnActivity.TagsEntryProperty.Key``.
            :param value: ``CfnActivity.TagsEntryProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-activity-tagsentry.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnActivity.TagsEntryProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-activity-tagsentry.html#cfn-stepfunctions-activity-tagsentry-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnActivity.TagsEntryProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-activity-tagsentry.html#cfn-stepfunctions-activity-tagsentry-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.CfnActivityProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "tags": "tags"},
)
class CfnActivityProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        tags: typing.Optional[typing.List[CfnActivity.TagsEntryProperty]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::StepFunctions::Activity``.

        :param name: ``AWS::StepFunctions::Activity.Name``.
        :param tags: ``AWS::StepFunctions::Activity.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-activity.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''``AWS::StepFunctions::Activity.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-activity.html#cfn-stepfunctions-activity-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[CfnActivity.TagsEntryProperty]]:
        '''``AWS::StepFunctions::Activity.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-activity.html#cfn-stepfunctions-activity-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[CfnActivity.TagsEntryProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnActivityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnStateMachine(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_stepfunctions.CfnStateMachine",
):
    '''A CloudFormation ``AWS::StepFunctions::StateMachine``.

    :cloudformationResource: AWS::StepFunctions::StateMachine
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        role_arn: builtins.str,
        definition: typing.Optional[typing.Union["CfnStateMachine.DefinitionProperty", _IResolvable_a771d0ef]] = None,
        definition_s3_location: typing.Optional[typing.Union["CfnStateMachine.S3LocationProperty", _IResolvable_a771d0ef]] = None,
        definition_string: typing.Optional[builtins.str] = None,
        definition_substitutions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        logging_configuration: typing.Optional[typing.Union["CfnStateMachine.LoggingConfigurationProperty", _IResolvable_a771d0ef]] = None,
        state_machine_name: typing.Optional[builtins.str] = None,
        state_machine_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List["CfnStateMachine.TagsEntryProperty"]] = None,
        tracing_configuration: typing.Optional[typing.Union["CfnStateMachine.TracingConfigurationProperty", _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::StepFunctions::StateMachine``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param role_arn: ``AWS::StepFunctions::StateMachine.RoleArn``.
        :param definition: ``AWS::StepFunctions::StateMachine.Definition``.
        :param definition_s3_location: ``AWS::StepFunctions::StateMachine.DefinitionS3Location``.
        :param definition_string: ``AWS::StepFunctions::StateMachine.DefinitionString``.
        :param definition_substitutions: ``AWS::StepFunctions::StateMachine.DefinitionSubstitutions``.
        :param logging_configuration: ``AWS::StepFunctions::StateMachine.LoggingConfiguration``.
        :param state_machine_name: ``AWS::StepFunctions::StateMachine.StateMachineName``.
        :param state_machine_type: ``AWS::StepFunctions::StateMachine.StateMachineType``.
        :param tags: ``AWS::StepFunctions::StateMachine.Tags``.
        :param tracing_configuration: ``AWS::StepFunctions::StateMachine.TracingConfiguration``.
        '''
        props = CfnStateMachineProps(
            role_arn=role_arn,
            definition=definition,
            definition_s3_location=definition_s3_location,
            definition_string=definition_string,
            definition_substitutions=definition_substitutions,
            logging_configuration=logging_configuration,
            state_machine_name=state_machine_name,
            state_machine_type=state_machine_type,
            tags=tags,
            tracing_configuration=tracing_configuration,
        )

        jsii.create(CfnStateMachine, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::StepFunctions::StateMachine.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''``AWS::StepFunctions::StateMachine.RoleArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        jsii.set(self, "roleArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="definition")
    def definition(
        self,
    ) -> typing.Optional[typing.Union["CfnStateMachine.DefinitionProperty", _IResolvable_a771d0ef]]:
        '''``AWS::StepFunctions::StateMachine.Definition``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-definition
        '''
        return typing.cast(typing.Optional[typing.Union["CfnStateMachine.DefinitionProperty", _IResolvable_a771d0ef]], jsii.get(self, "definition"))

    @definition.setter
    def definition(
        self,
        value: typing.Optional[typing.Union["CfnStateMachine.DefinitionProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "definition", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="definitionS3Location")
    def definition_s3_location(
        self,
    ) -> typing.Optional[typing.Union["CfnStateMachine.S3LocationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::StepFunctions::StateMachine.DefinitionS3Location``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-definitions3location
        '''
        return typing.cast(typing.Optional[typing.Union["CfnStateMachine.S3LocationProperty", _IResolvable_a771d0ef]], jsii.get(self, "definitionS3Location"))

    @definition_s3_location.setter
    def definition_s3_location(
        self,
        value: typing.Optional[typing.Union["CfnStateMachine.S3LocationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "definitionS3Location", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="definitionString")
    def definition_string(self) -> typing.Optional[builtins.str]:
        '''``AWS::StepFunctions::StateMachine.DefinitionString``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-definitionstring
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "definitionString"))

    @definition_string.setter
    def definition_string(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "definitionString", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="definitionSubstitutions")
    def definition_substitutions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::StepFunctions::StateMachine.DefinitionSubstitutions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-definitionsubstitutions
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "definitionSubstitutions"))

    @definition_substitutions.setter
    def definition_substitutions(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "definitionSubstitutions", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loggingConfiguration")
    def logging_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnStateMachine.LoggingConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::StepFunctions::StateMachine.LoggingConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-loggingconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnStateMachine.LoggingConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "loggingConfiguration"))

    @logging_configuration.setter
    def logging_configuration(
        self,
        value: typing.Optional[typing.Union["CfnStateMachine.LoggingConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "loggingConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stateMachineName")
    def state_machine_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::StepFunctions::StateMachine.StateMachineName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-statemachinename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateMachineName"))

    @state_machine_name.setter
    def state_machine_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "stateMachineName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stateMachineType")
    def state_machine_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::StepFunctions::StateMachine.StateMachineType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-statemachinetype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateMachineType"))

    @state_machine_type.setter
    def state_machine_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "stateMachineType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tracingConfiguration")
    def tracing_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnStateMachine.TracingConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::StepFunctions::StateMachine.TracingConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-tracingconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnStateMachine.TracingConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "tracingConfiguration"))

    @tracing_configuration.setter
    def tracing_configuration(
        self,
        value: typing.Optional[typing.Union["CfnStateMachine.TracingConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "tracingConfiguration", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_stepfunctions.CfnStateMachine.CloudWatchLogsLogGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_arn": "logGroupArn"},
    )
    class CloudWatchLogsLogGroupProperty:
        def __init__(
            self,
            *,
            log_group_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param log_group_arn: ``CfnStateMachine.CloudWatchLogsLogGroupProperty.LogGroupArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-cloudwatchlogsloggroup.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if log_group_arn is not None:
                self._values["log_group_arn"] = log_group_arn

        @builtins.property
        def log_group_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.CloudWatchLogsLogGroupProperty.LogGroupArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-cloudwatchlogsloggroup.html#cfn-stepfunctions-statemachine-cloudwatchlogsloggroup-loggrouparn
            '''
            result = self._values.get("log_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsLogGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_stepfunctions.CfnStateMachine.DefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class DefinitionProperty:
        def __init__(self) -> None:
            '''
            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-definition.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_stepfunctions.CfnStateMachine.LogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch_logs_log_group": "cloudWatchLogsLogGroup"},
    )
    class LogDestinationProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_log_group: typing.Optional[typing.Union["CfnStateMachine.CloudWatchLogsLogGroupProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param cloud_watch_logs_log_group: ``CfnStateMachine.LogDestinationProperty.CloudWatchLogsLogGroup``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if cloud_watch_logs_log_group is not None:
                self._values["cloud_watch_logs_log_group"] = cloud_watch_logs_log_group

        @builtins.property
        def cloud_watch_logs_log_group(
            self,
        ) -> typing.Optional[typing.Union["CfnStateMachine.CloudWatchLogsLogGroupProperty", _IResolvable_a771d0ef]]:
            '''``CfnStateMachine.LogDestinationProperty.CloudWatchLogsLogGroup``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination.html#cfn-stepfunctions-statemachine-logdestination-cloudwatchlogsloggroup
            '''
            result = self._values.get("cloud_watch_logs_log_group")
            return typing.cast(typing.Optional[typing.Union["CfnStateMachine.CloudWatchLogsLogGroupProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_stepfunctions.CfnStateMachine.LoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destinations": "destinations",
            "include_execution_data": "includeExecutionData",
            "level": "level",
        },
    )
    class LoggingConfigurationProperty:
        def __init__(
            self,
            *,
            destinations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnStateMachine.LogDestinationProperty", _IResolvable_a771d0ef]]]] = None,
            include_execution_data: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            level: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destinations: ``CfnStateMachine.LoggingConfigurationProperty.Destinations``.
            :param include_execution_data: ``CfnStateMachine.LoggingConfigurationProperty.IncludeExecutionData``.
            :param level: ``CfnStateMachine.LoggingConfigurationProperty.Level``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if destinations is not None:
                self._values["destinations"] = destinations
            if include_execution_data is not None:
                self._values["include_execution_data"] = include_execution_data
            if level is not None:
                self._values["level"] = level

        @builtins.property
        def destinations(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnStateMachine.LogDestinationProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnStateMachine.LoggingConfigurationProperty.Destinations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html#cfn-stepfunctions-statemachine-loggingconfiguration-destinations
            '''
            result = self._values.get("destinations")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnStateMachine.LogDestinationProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def include_execution_data(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnStateMachine.LoggingConfigurationProperty.IncludeExecutionData``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html#cfn-stepfunctions-statemachine-loggingconfiguration-includeexecutiondata
            '''
            result = self._values.get("include_execution_data")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def level(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.LoggingConfigurationProperty.Level``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html#cfn-stepfunctions-statemachine-loggingconfiguration-level
            '''
            result = self._values.get("level")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_stepfunctions.CfnStateMachine.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param bucket: ``CfnStateMachine.S3LocationProperty.Bucket``.
            :param key: ``CfnStateMachine.S3LocationProperty.Key``.
            :param version: ``CfnStateMachine.S3LocationProperty.Version``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-s3location.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket": bucket,
                "key": key,
            }
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnStateMachine.S3LocationProperty.Bucket``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-s3location.html#cfn-stepfunctions-statemachine-s3location-bucket
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnStateMachine.S3LocationProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-s3location.html#cfn-stepfunctions-statemachine-s3location-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.S3LocationProperty.Version``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-s3location.html#cfn-stepfunctions-statemachine-s3location-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_stepfunctions.CfnStateMachine.TagsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsEntryProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''
            :param key: ``CfnStateMachine.TagsEntryProperty.Key``.
            :param value: ``CfnStateMachine.TagsEntryProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-tagsentry.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnStateMachine.TagsEntryProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-tagsentry.html#cfn-stepfunctions-statemachine-tagsentry-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnStateMachine.TagsEntryProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-tagsentry.html#cfn-stepfunctions-statemachine-tagsentry-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_stepfunctions.CfnStateMachine.TracingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class TracingConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param enabled: ``CfnStateMachine.TracingConfigurationProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-tracingconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnStateMachine.TracingConfigurationProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-tracingconfiguration.html#cfn-stepfunctions-statemachine-tracingconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TracingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.CfnStateMachineProps",
    jsii_struct_bases=[],
    name_mapping={
        "role_arn": "roleArn",
        "definition": "definition",
        "definition_s3_location": "definitionS3Location",
        "definition_string": "definitionString",
        "definition_substitutions": "definitionSubstitutions",
        "logging_configuration": "loggingConfiguration",
        "state_machine_name": "stateMachineName",
        "state_machine_type": "stateMachineType",
        "tags": "tags",
        "tracing_configuration": "tracingConfiguration",
    },
)
class CfnStateMachineProps:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        definition: typing.Optional[typing.Union[CfnStateMachine.DefinitionProperty, _IResolvable_a771d0ef]] = None,
        definition_s3_location: typing.Optional[typing.Union[CfnStateMachine.S3LocationProperty, _IResolvable_a771d0ef]] = None,
        definition_string: typing.Optional[builtins.str] = None,
        definition_substitutions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        logging_configuration: typing.Optional[typing.Union[CfnStateMachine.LoggingConfigurationProperty, _IResolvable_a771d0ef]] = None,
        state_machine_name: typing.Optional[builtins.str] = None,
        state_machine_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[CfnStateMachine.TagsEntryProperty]] = None,
        tracing_configuration: typing.Optional[typing.Union[CfnStateMachine.TracingConfigurationProperty, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::StepFunctions::StateMachine``.

        :param role_arn: ``AWS::StepFunctions::StateMachine.RoleArn``.
        :param definition: ``AWS::StepFunctions::StateMachine.Definition``.
        :param definition_s3_location: ``AWS::StepFunctions::StateMachine.DefinitionS3Location``.
        :param definition_string: ``AWS::StepFunctions::StateMachine.DefinitionString``.
        :param definition_substitutions: ``AWS::StepFunctions::StateMachine.DefinitionSubstitutions``.
        :param logging_configuration: ``AWS::StepFunctions::StateMachine.LoggingConfiguration``.
        :param state_machine_name: ``AWS::StepFunctions::StateMachine.StateMachineName``.
        :param state_machine_type: ``AWS::StepFunctions::StateMachine.StateMachineType``.
        :param tags: ``AWS::StepFunctions::StateMachine.Tags``.
        :param tracing_configuration: ``AWS::StepFunctions::StateMachine.TracingConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "role_arn": role_arn,
        }
        if definition is not None:
            self._values["definition"] = definition
        if definition_s3_location is not None:
            self._values["definition_s3_location"] = definition_s3_location
        if definition_string is not None:
            self._values["definition_string"] = definition_string
        if definition_substitutions is not None:
            self._values["definition_substitutions"] = definition_substitutions
        if logging_configuration is not None:
            self._values["logging_configuration"] = logging_configuration
        if state_machine_name is not None:
            self._values["state_machine_name"] = state_machine_name
        if state_machine_type is not None:
            self._values["state_machine_type"] = state_machine_type
        if tags is not None:
            self._values["tags"] = tags
        if tracing_configuration is not None:
            self._values["tracing_configuration"] = tracing_configuration

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''``AWS::StepFunctions::StateMachine.RoleArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def definition(
        self,
    ) -> typing.Optional[typing.Union[CfnStateMachine.DefinitionProperty, _IResolvable_a771d0ef]]:
        '''``AWS::StepFunctions::StateMachine.Definition``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-definition
        '''
        result = self._values.get("definition")
        return typing.cast(typing.Optional[typing.Union[CfnStateMachine.DefinitionProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def definition_s3_location(
        self,
    ) -> typing.Optional[typing.Union[CfnStateMachine.S3LocationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::StepFunctions::StateMachine.DefinitionS3Location``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-definitions3location
        '''
        result = self._values.get("definition_s3_location")
        return typing.cast(typing.Optional[typing.Union[CfnStateMachine.S3LocationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def definition_string(self) -> typing.Optional[builtins.str]:
        '''``AWS::StepFunctions::StateMachine.DefinitionString``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-definitionstring
        '''
        result = self._values.get("definition_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def definition_substitutions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::StepFunctions::StateMachine.DefinitionSubstitutions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-definitionsubstitutions
        '''
        result = self._values.get("definition_substitutions")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def logging_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnStateMachine.LoggingConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::StepFunctions::StateMachine.LoggingConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-loggingconfiguration
        '''
        result = self._values.get("logging_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnStateMachine.LoggingConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def state_machine_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::StepFunctions::StateMachine.StateMachineName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-statemachinename
        '''
        result = self._values.get("state_machine_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state_machine_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::StepFunctions::StateMachine.StateMachineType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-statemachinetype
        '''
        result = self._values.get("state_machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[CfnStateMachine.TagsEntryProperty]]:
        '''``AWS::StepFunctions::StateMachine.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[CfnStateMachine.TagsEntryProperty]], result)

    @builtins.property
    def tracing_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnStateMachine.TracingConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::StepFunctions::StateMachine.TracingConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html#cfn-stepfunctions-statemachine-tracingconfiguration
        '''
        result = self._values.get("tracing_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnStateMachine.TracingConfigurationProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStateMachineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.ChoiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "comment": "comment",
        "input_path": "inputPath",
        "output_path": "outputPath",
    },
)
class ChoiceProps:
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for defining a Choice state.

        :param comment: (experimental) An optional description for this state. Default: No comment
        :param input_path: (experimental) JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: (experimental) JSONPath expression to select part of the state to be the output to this state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: $

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if comment is not None:
            self._values["comment"] = comment
        if input_path is not None:
            self._values["input_path"] = input_path
        if output_path is not None:
            self._values["output_path"] = output_path

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''(experimental) An optional description for this state.

        :default: No comment

        :stability: experimental
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to select part of the state to be the input to this state.

        May also be the special value DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("input_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to select part of the state to be the output to this state.

        May also be the special value DISCARD, which will cause the effective
        output to be the empty object {}.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("output_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChoiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Condition(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_stepfunctions.Condition",
):
    '''(experimental) A Condition for use in a Choice state branch.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_ConditionProxy"]:
        return _ConditionProxy

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(Condition, self, [])

    @jsii.member(jsii_name="and") # type: ignore[misc]
    @builtins.classmethod
    def and_(cls, *conditions: "Condition") -> "Condition":
        '''(experimental) Combine two or more conditions with a logical AND.

        :param conditions: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "and", [*conditions]))

    @jsii.member(jsii_name="booleanEquals") # type: ignore[misc]
    @builtins.classmethod
    def boolean_equals(
        cls,
        variable: builtins.str,
        value: builtins.bool,
    ) -> "Condition":
        '''(experimental) Matches if a boolean field has the given value.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "booleanEquals", [variable, value]))

    @jsii.member(jsii_name="booleanEqualsJsonPath") # type: ignore[misc]
    @builtins.classmethod
    def boolean_equals_json_path(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a boolean field equals to a value at a given mapping path.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "booleanEqualsJsonPath", [variable, value]))

    @jsii.member(jsii_name="isBoolean") # type: ignore[misc]
    @builtins.classmethod
    def is_boolean(cls, variable: builtins.str) -> "Condition":
        '''(experimental) Matches if variable is boolean.

        :param variable: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "isBoolean", [variable]))

    @jsii.member(jsii_name="isNotBoolean") # type: ignore[misc]
    @builtins.classmethod
    def is_not_boolean(cls, variable: builtins.str) -> "Condition":
        '''(experimental) Matches if variable is not boolean.

        :param variable: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "isNotBoolean", [variable]))

    @jsii.member(jsii_name="isNotNull") # type: ignore[misc]
    @builtins.classmethod
    def is_not_null(cls, variable: builtins.str) -> "Condition":
        '''(experimental) Matches if variable is not null.

        :param variable: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "isNotNull", [variable]))

    @jsii.member(jsii_name="isNotNumeric") # type: ignore[misc]
    @builtins.classmethod
    def is_not_numeric(cls, variable: builtins.str) -> "Condition":
        '''(experimental) Matches if variable is not numeric.

        :param variable: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "isNotNumeric", [variable]))

    @jsii.member(jsii_name="isNotPresent") # type: ignore[misc]
    @builtins.classmethod
    def is_not_present(cls, variable: builtins.str) -> "Condition":
        '''(experimental) Matches if variable is not present.

        :param variable: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "isNotPresent", [variable]))

    @jsii.member(jsii_name="isNotString") # type: ignore[misc]
    @builtins.classmethod
    def is_not_string(cls, variable: builtins.str) -> "Condition":
        '''(experimental) Matches if variable is not a string.

        :param variable: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "isNotString", [variable]))

    @jsii.member(jsii_name="isNotTimestamp") # type: ignore[misc]
    @builtins.classmethod
    def is_not_timestamp(cls, variable: builtins.str) -> "Condition":
        '''(experimental) Matches if variable is not a timestamp.

        :param variable: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "isNotTimestamp", [variable]))

    @jsii.member(jsii_name="isNull") # type: ignore[misc]
    @builtins.classmethod
    def is_null(cls, variable: builtins.str) -> "Condition":
        '''(experimental) Matches if variable is Null.

        :param variable: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "isNull", [variable]))

    @jsii.member(jsii_name="isNumeric") # type: ignore[misc]
    @builtins.classmethod
    def is_numeric(cls, variable: builtins.str) -> "Condition":
        '''(experimental) Matches if variable is numeric.

        :param variable: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "isNumeric", [variable]))

    @jsii.member(jsii_name="isPresent") # type: ignore[misc]
    @builtins.classmethod
    def is_present(cls, variable: builtins.str) -> "Condition":
        '''(experimental) Matches if variable is present.

        :param variable: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "isPresent", [variable]))

    @jsii.member(jsii_name="isString") # type: ignore[misc]
    @builtins.classmethod
    def is_string(cls, variable: builtins.str) -> "Condition":
        '''(experimental) Matches if variable is a string.

        :param variable: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "isString", [variable]))

    @jsii.member(jsii_name="isTimestamp") # type: ignore[misc]
    @builtins.classmethod
    def is_timestamp(cls, variable: builtins.str) -> "Condition":
        '''(experimental) Matches if variable is a timestamp.

        :param variable: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "isTimestamp", [variable]))

    @jsii.member(jsii_name="not") # type: ignore[misc]
    @builtins.classmethod
    def not_(cls, condition: "Condition") -> "Condition":
        '''(experimental) Negate a condition.

        :param condition: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "not", [condition]))

    @jsii.member(jsii_name="numberEquals") # type: ignore[misc]
    @builtins.classmethod
    def number_equals(cls, variable: builtins.str, value: jsii.Number) -> "Condition":
        '''(experimental) Matches if a numeric field has the given value.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "numberEquals", [variable, value]))

    @jsii.member(jsii_name="numberEqualsJsonPath") # type: ignore[misc]
    @builtins.classmethod
    def number_equals_json_path(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a numeric field has the value in a given mapping path.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "numberEqualsJsonPath", [variable, value]))

    @jsii.member(jsii_name="numberGreaterThan") # type: ignore[misc]
    @builtins.classmethod
    def number_greater_than(
        cls,
        variable: builtins.str,
        value: jsii.Number,
    ) -> "Condition":
        '''(experimental) Matches if a numeric field is greater than the given value.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "numberGreaterThan", [variable, value]))

    @jsii.member(jsii_name="numberGreaterThanEquals") # type: ignore[misc]
    @builtins.classmethod
    def number_greater_than_equals(
        cls,
        variable: builtins.str,
        value: jsii.Number,
    ) -> "Condition":
        '''(experimental) Matches if a numeric field is greater than or equal to the given value.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "numberGreaterThanEquals", [variable, value]))

    @jsii.member(jsii_name="numberGreaterThanEqualsJsonPath") # type: ignore[misc]
    @builtins.classmethod
    def number_greater_than_equals_json_path(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a numeric field is greater than or equal to the value at a given mapping path.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "numberGreaterThanEqualsJsonPath", [variable, value]))

    @jsii.member(jsii_name="numberGreaterThanJsonPath") # type: ignore[misc]
    @builtins.classmethod
    def number_greater_than_json_path(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a numeric field is greater than the value at a given mapping path.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "numberGreaterThanJsonPath", [variable, value]))

    @jsii.member(jsii_name="numberLessThan") # type: ignore[misc]
    @builtins.classmethod
    def number_less_than(
        cls,
        variable: builtins.str,
        value: jsii.Number,
    ) -> "Condition":
        '''(experimental) Matches if a numeric field is less than the given value.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "numberLessThan", [variable, value]))

    @jsii.member(jsii_name="numberLessThanEquals") # type: ignore[misc]
    @builtins.classmethod
    def number_less_than_equals(
        cls,
        variable: builtins.str,
        value: jsii.Number,
    ) -> "Condition":
        '''(experimental) Matches if a numeric field is less than or equal to the given value.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "numberLessThanEquals", [variable, value]))

    @jsii.member(jsii_name="numberLessThanEqualsJsonPath") # type: ignore[misc]
    @builtins.classmethod
    def number_less_than_equals_json_path(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a numeric field is less than or equal to the numeric value at given mapping path.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "numberLessThanEqualsJsonPath", [variable, value]))

    @jsii.member(jsii_name="numberLessThanJsonPath") # type: ignore[misc]
    @builtins.classmethod
    def number_less_than_json_path(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a numeric field is less than the value at the given mapping path.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "numberLessThanJsonPath", [variable, value]))

    @jsii.member(jsii_name="or") # type: ignore[misc]
    @builtins.classmethod
    def or_(cls, *conditions: "Condition") -> "Condition":
        '''(experimental) Combine two or more conditions with a logical OR.

        :param conditions: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "or", [*conditions]))

    @jsii.member(jsii_name="stringEquals") # type: ignore[misc]
    @builtins.classmethod
    def string_equals(cls, variable: builtins.str, value: builtins.str) -> "Condition":
        '''(experimental) Matches if a string field has the given value.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "stringEquals", [variable, value]))

    @jsii.member(jsii_name="stringEqualsJsonPath") # type: ignore[misc]
    @builtins.classmethod
    def string_equals_json_path(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a string field equals to a value at a given mapping path.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "stringEqualsJsonPath", [variable, value]))

    @jsii.member(jsii_name="stringGreaterThan") # type: ignore[misc]
    @builtins.classmethod
    def string_greater_than(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a string field sorts after a given value.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "stringGreaterThan", [variable, value]))

    @jsii.member(jsii_name="stringGreaterThanEquals") # type: ignore[misc]
    @builtins.classmethod
    def string_greater_than_equals(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a string field sorts after or equal to a given value.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "stringGreaterThanEquals", [variable, value]))

    @jsii.member(jsii_name="stringGreaterThanEqualsJsonPath") # type: ignore[misc]
    @builtins.classmethod
    def string_greater_than_equals_json_path(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a string field sorts after or equal to value at a given mapping path.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "stringGreaterThanEqualsJsonPath", [variable, value]))

    @jsii.member(jsii_name="stringGreaterThanJsonPath") # type: ignore[misc]
    @builtins.classmethod
    def string_greater_than_json_path(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a string field sorts after a value at a given mapping path.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "stringGreaterThanJsonPath", [variable, value]))

    @jsii.member(jsii_name="stringLessThan") # type: ignore[misc]
    @builtins.classmethod
    def string_less_than(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a string field sorts before a given value.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "stringLessThan", [variable, value]))

    @jsii.member(jsii_name="stringLessThanEquals") # type: ignore[misc]
    @builtins.classmethod
    def string_less_than_equals(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a string field sorts equal to or before a given value.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "stringLessThanEquals", [variable, value]))

    @jsii.member(jsii_name="stringLessThanEqualsJsonPath") # type: ignore[misc]
    @builtins.classmethod
    def string_less_than_equals_json_path(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a string field sorts equal to or before a given mapping.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "stringLessThanEqualsJsonPath", [variable, value]))

    @jsii.member(jsii_name="stringLessThanJsonPath") # type: ignore[misc]
    @builtins.classmethod
    def string_less_than_json_path(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a string field sorts before a given value at a particular mapping.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "stringLessThanJsonPath", [variable, value]))

    @jsii.member(jsii_name="stringMatches") # type: ignore[misc]
    @builtins.classmethod
    def string_matches(cls, variable: builtins.str, value: builtins.str) -> "Condition":
        '''(experimental) Matches if a field matches a string pattern that can contain a wild card (*) e.g: log-*.txt or *LATEST*. No other characters other than "*" have any special meaning - * can be escaped: \\*.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "stringMatches", [variable, value]))

    @jsii.member(jsii_name="timestampEquals") # type: ignore[misc]
    @builtins.classmethod
    def timestamp_equals(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a timestamp field is the same time as the given timestamp.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "timestampEquals", [variable, value]))

    @jsii.member(jsii_name="timestampEqualsJsonPath") # type: ignore[misc]
    @builtins.classmethod
    def timestamp_equals_json_path(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a timestamp field is the same time as the timestamp at a given mapping path.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "timestampEqualsJsonPath", [variable, value]))

    @jsii.member(jsii_name="timestampGreaterThan") # type: ignore[misc]
    @builtins.classmethod
    def timestamp_greater_than(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a timestamp field is after the given timestamp.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "timestampGreaterThan", [variable, value]))

    @jsii.member(jsii_name="timestampGreaterThanEquals") # type: ignore[misc]
    @builtins.classmethod
    def timestamp_greater_than_equals(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a timestamp field is after or equal to the given timestamp.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "timestampGreaterThanEquals", [variable, value]))

    @jsii.member(jsii_name="timestampGreaterThanEqualsJsonPath") # type: ignore[misc]
    @builtins.classmethod
    def timestamp_greater_than_equals_json_path(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a timestamp field is after or equal to the timestamp at a given mapping path.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "timestampGreaterThanEqualsJsonPath", [variable, value]))

    @jsii.member(jsii_name="timestampGreaterThanJsonPath") # type: ignore[misc]
    @builtins.classmethod
    def timestamp_greater_than_json_path(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a timestamp field is after the timestamp at a given mapping path.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "timestampGreaterThanJsonPath", [variable, value]))

    @jsii.member(jsii_name="timestampLessThan") # type: ignore[misc]
    @builtins.classmethod
    def timestamp_less_than(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a timestamp field is before the given timestamp.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "timestampLessThan", [variable, value]))

    @jsii.member(jsii_name="timestampLessThanEquals") # type: ignore[misc]
    @builtins.classmethod
    def timestamp_less_than_equals(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a timestamp field is before or equal to the given timestamp.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "timestampLessThanEquals", [variable, value]))

    @jsii.member(jsii_name="timestampLessThanEqualsJsonPath") # type: ignore[misc]
    @builtins.classmethod
    def timestamp_less_than_equals_json_path(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a timestamp field is before or equal to the timestamp at a given mapping path.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "timestampLessThanEqualsJsonPath", [variable, value]))

    @jsii.member(jsii_name="timestampLessThanJsonPath") # type: ignore[misc]
    @builtins.classmethod
    def timestamp_less_than_json_path(
        cls,
        variable: builtins.str,
        value: builtins.str,
    ) -> "Condition":
        '''(experimental) Matches if a timestamp field is before the timestamp at a given mapping path.

        :param variable: -
        :param value: -

        :stability: experimental
        '''
        return typing.cast("Condition", jsii.sinvoke(cls, "timestampLessThanJsonPath", [variable, value]))

    @jsii.member(jsii_name="renderCondition") # type: ignore[misc]
    @abc.abstractmethod
    def render_condition(self) -> typing.Any:
        '''(experimental) Render Amazon States Language JSON for the condition.

        :stability: experimental
        '''
        ...


class _ConditionProxy(Condition):
    @jsii.member(jsii_name="renderCondition")
    def render_condition(self) -> typing.Any:
        '''(experimental) Render Amazon States Language JSON for the condition.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "renderCondition", []))


class Context(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_stepfunctions.Context"):
    '''(deprecated) Extract a field from the State Machine Context data.

    :deprecated: replaced by ``JsonPath``

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#wait-token-contextobject
    :stability: deprecated
    '''

    @jsii.member(jsii_name="numberAt") # type: ignore[misc]
    @builtins.classmethod
    def number_at(cls, path: builtins.str) -> jsii.Number:
        '''(deprecated) Instead of using a literal number, get the value from a JSON path.

        :param path: -

        :stability: deprecated
        '''
        return typing.cast(jsii.Number, jsii.sinvoke(cls, "numberAt", [path]))

    @jsii.member(jsii_name="stringAt") # type: ignore[misc]
    @builtins.classmethod
    def string_at(cls, path: builtins.str) -> builtins.str:
        '''(deprecated) Instead of using a literal string, get the value from a JSON path.

        :param path: -

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "stringAt", [path]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="entireContext")
    def entire_context(cls) -> builtins.str:
        '''(deprecated) Use the entire context data structure.

        Will be an object at invocation time, but is represented in the CDK
        application as a string.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "entireContext"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="taskToken")
    def task_token(cls) -> builtins.str:
        '''(deprecated) Return the Task Token field.

        External actions will need this token to report step completion
        back to StepFunctions using the ``SendTaskSuccess`` or ``SendTaskFailure``
        calls.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "taskToken"))


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.CustomStateProps",
    jsii_struct_bases=[],
    name_mapping={"state_json": "stateJson"},
)
class CustomStateProps:
    def __init__(self, *, state_json: typing.Mapping[builtins.str, typing.Any]) -> None:
        '''(experimental) Properties for defining a custom state definition.

        :param state_json: (experimental) Amazon States Language (JSON-based) definition of the state.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "state_json": state_json,
        }

    @builtins.property
    def state_json(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) Amazon States Language (JSON-based) definition of the state.

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html
        :stability: experimental
        '''
        result = self._values.get("state_json")
        assert result is not None, "Required property 'state_json' is missing"
        return typing.cast(typing.Mapping[builtins.str, typing.Any], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomStateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Data(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_stepfunctions.Data"):
    '''(deprecated) Extract a field from the State Machine data that gets passed around between states.

    :deprecated: replaced by ``JsonPath``

    :stability: deprecated
    '''

    @jsii.member(jsii_name="isJsonPathString") # type: ignore[misc]
    @builtins.classmethod
    def is_json_path_string(cls, value: builtins.str) -> builtins.bool:
        '''(deprecated) Determines if the indicated string is an encoded JSON path.

        :param value: string to be evaluated.

        :stability: deprecated
        '''
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isJsonPathString", [value]))

    @jsii.member(jsii_name="listAt") # type: ignore[misc]
    @builtins.classmethod
    def list_at(cls, path: builtins.str) -> typing.List[builtins.str]:
        '''(deprecated) Instead of using a literal string list, get the value from a JSON path.

        :param path: -

        :stability: deprecated
        '''
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "listAt", [path]))

    @jsii.member(jsii_name="numberAt") # type: ignore[misc]
    @builtins.classmethod
    def number_at(cls, path: builtins.str) -> jsii.Number:
        '''(deprecated) Instead of using a literal number, get the value from a JSON path.

        :param path: -

        :stability: deprecated
        '''
        return typing.cast(jsii.Number, jsii.sinvoke(cls, "numberAt", [path]))

    @jsii.member(jsii_name="stringAt") # type: ignore[misc]
    @builtins.classmethod
    def string_at(cls, path: builtins.str) -> builtins.str:
        '''(deprecated) Instead of using a literal string, get the value from a JSON path.

        :param path: -

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "stringAt", [path]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="entirePayload")
    def entire_payload(cls) -> builtins.str:
        '''(deprecated) Use the entire data structure.

        Will be an object at invocation time, but is represented in the CDK
        application as a string.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "entirePayload"))


class Errors(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_stepfunctions.Errors"):
    '''(experimental) Predefined error strings Error names in Amazon States Language - https://states-language.net/spec.html#appendix-a Error handling in Step Functions - https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(Errors, self, [])

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="ALL")
    def ALL(cls) -> builtins.str:
        '''(experimental) Matches any Error.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "ALL"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="BRANCH_FAILED")
    def BRANCH_FAILED(cls) -> builtins.str:
        '''(experimental) A branch of a Parallel state failed.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "BRANCH_FAILED"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="NO_CHOICE_MATCHED")
    def NO_CHOICE_MATCHED(cls) -> builtins.str:
        '''(experimental) A Choice state failed to find a match for the condition field extracted from its input.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "NO_CHOICE_MATCHED"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="PARAMETER_PATH_FAILURE")
    def PARAMETER_PATH_FAILURE(cls) -> builtins.str:
        '''(experimental) Within a state’s “Parameters” field, the attempt to replace a field whose name ends in “.$” using a Path failed.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PARAMETER_PATH_FAILURE"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="PERMISSIONS")
    def PERMISSIONS(cls) -> builtins.str:
        '''(experimental) A Task State failed because it had insufficient privileges to execute the specified code.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PERMISSIONS"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="RESULT_PATH_MATCH_FAILURE")
    def RESULT_PATH_MATCH_FAILURE(cls) -> builtins.str:
        '''(experimental) A Task State’s “ResultPath” field cannot be applied to the input the state received.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "RESULT_PATH_MATCH_FAILURE"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="TASKS_FAILED")
    def TASKS_FAILED(cls) -> builtins.str:
        '''(experimental) A Task State failed during the execution.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "TASKS_FAILED"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="TIMEOUT")
    def TIMEOUT(cls) -> builtins.str:
        '''(experimental) A Task State either ran longer than the “TimeoutSeconds” value, or failed to heartbeat for a time longer than the “HeartbeatSeconds” value.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "TIMEOUT"))


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.FailProps",
    jsii_struct_bases=[],
    name_mapping={"cause": "cause", "comment": "comment", "error": "error"},
)
class FailProps:
    def __init__(
        self,
        *,
        cause: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        error: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for defining a Fail state.

        :param cause: (experimental) A description for the cause of the failure. Default: No description
        :param comment: (experimental) An optional description for this state. Default: No comment
        :param error: (experimental) Error code used to represent this failure. Default: No error code

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if cause is not None:
            self._values["cause"] = cause
        if comment is not None:
            self._values["comment"] = comment
        if error is not None:
            self._values["error"] = error

    @builtins.property
    def cause(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the cause of the failure.

        :default: No description

        :stability: experimental
        '''
        result = self._values.get("cause")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''(experimental) An optional description for this state.

        :default: No comment

        :stability: experimental
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error(self) -> typing.Optional[builtins.str]:
        '''(experimental) Error code used to represent this failure.

        :default: No error code

        :stability: experimental
        '''
        result = self._values.get("error")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FailProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FieldUtils(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_stepfunctions.FieldUtils",
):
    '''(experimental) Helper functions to work with structures containing fields.

    :stability: experimental
    '''

    @jsii.member(jsii_name="containsTaskToken") # type: ignore[misc]
    @builtins.classmethod
    def contains_task_token(
        cls,
        obj: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> builtins.bool:
        '''(experimental) Returns whether the given task structure contains the TaskToken field anywhere.

        The field is considered included if the field itself or one of its containing
        fields occurs anywhere in the payload.

        :param obj: -

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "containsTaskToken", [obj]))

    @jsii.member(jsii_name="findReferencedPaths") # type: ignore[misc]
    @builtins.classmethod
    def find_referenced_paths(
        cls,
        obj: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> typing.List[builtins.str]:
        '''(experimental) Return all JSON paths used in the given structure.

        :param obj: -

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "findReferencedPaths", [obj]))

    @jsii.member(jsii_name="renderObject") # type: ignore[misc]
    @builtins.classmethod
    def render_object(
        cls,
        obj: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Render a JSON structure containing fields to the right StepFunctions structure.

        :param obj: -

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], jsii.sinvoke(cls, "renderObject", [obj]))


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.FindStateOptions",
    jsii_struct_bases=[],
    name_mapping={"include_error_handlers": "includeErrorHandlers"},
)
class FindStateOptions:
    def __init__(
        self,
        *,
        include_error_handlers: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for finding reachable states.

        :param include_error_handlers: (experimental) Whether or not to follow error-handling transitions. Default: false

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if include_error_handlers is not None:
            self._values["include_error_handlers"] = include_error_handlers

    @builtins.property
    def include_error_handlers(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to follow error-handling transitions.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("include_error_handlers")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FindStateOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_stepfunctions.IActivity")
class IActivity(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Represents a Step Functions Activity https://docs.aws.amazon.com/step-functions/latest/dg/concepts-activities.html.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IActivityProxy"]:
        return _IActivityProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="activityArn")
    def activity_arn(self) -> builtins.str:
        '''(experimental) The ARN of the activity.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="activityName")
    def activity_name(self) -> builtins.str:
        '''(experimental) The name of the activity.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IActivityProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''(experimental) Represents a Step Functions Activity https://docs.aws.amazon.com/step-functions/latest/dg/concepts-activities.html.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_stepfunctions.IActivity"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="activityArn")
    def activity_arn(self) -> builtins.str:
        '''(experimental) The ARN of the activity.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "activityArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="activityName")
    def activity_name(self) -> builtins.str:
        '''(experimental) The name of the activity.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "activityName"))


@jsii.interface(jsii_type="monocdk.aws_stepfunctions.IChainable")
class IChainable(typing_extensions.Protocol):
    '''(experimental) Interface for objects that can be used in a Chain.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IChainableProxy"]:
        return _IChainableProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        '''(experimental) The chainable end state(s) of this chainable.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) Descriptive identifier for this chainable.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="startState")
    def start_state(self) -> "State":
        '''(experimental) The start state of this chainable.

        :stability: experimental
        '''
        ...


class _IChainableProxy:
    '''(experimental) Interface for objects that can be used in a Chain.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_stepfunctions.IChainable"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List["INextable"]:
        '''(experimental) The chainable end state(s) of this chainable.

        :stability: experimental
        '''
        return typing.cast(typing.List["INextable"], jsii.get(self, "endStates"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) Descriptive identifier for this chainable.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="startState")
    def start_state(self) -> "State":
        '''(experimental) The start state of this chainable.

        :stability: experimental
        '''
        return typing.cast("State", jsii.get(self, "startState"))


@jsii.interface(jsii_type="monocdk.aws_stepfunctions.INextable")
class INextable(typing_extensions.Protocol):
    '''(experimental) Interface for states that can have 'next' states.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_INextableProxy"]:
        return _INextableProxy

    @jsii.member(jsii_name="next")
    def next(self, state: IChainable) -> "Chain":
        '''(experimental) Go to the indicated state after this state.

        :param state: -

        :return: The chain of states built up

        :stability: experimental
        '''
        ...


class _INextableProxy:
    '''(experimental) Interface for states that can have 'next' states.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_stepfunctions.INextable"

    @jsii.member(jsii_name="next")
    def next(self, state: IChainable) -> "Chain":
        '''(experimental) Go to the indicated state after this state.

        :param state: -

        :return: The chain of states built up

        :stability: experimental
        '''
        return typing.cast("Chain", jsii.invoke(self, "next", [state]))


@jsii.interface(jsii_type="monocdk.aws_stepfunctions.IStateMachine")
class IStateMachine(
    _IResource_8c1dbbbd,
    _IGrantable_4c5a91d1,
    typing_extensions.Protocol,
):
    '''(experimental) A State Machine.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IStateMachineProxy"]:
        return _IStateMachineProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stateMachineArn")
    def state_machine_arn(self) -> builtins.str:
        '''(experimental) The ARN of the state machine.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        identity: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity custom permissions.

        :param identity: The principal.
        :param actions: The list of desired actions.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantExecution")
    def grant_execution(
        self,
        identity: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity permissions for all executions of a state machine.

        :param identity: The principal.
        :param actions: The list of desired actions.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity read permissions for this state machine.

        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantStartExecution")
    def grant_start_execution(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity permissions to start an execution of this state machine.

        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantTaskResponse")
    def grant_task_response(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity read permissions for this state machine.

        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Return the given named metric for this State Machine's executions.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricAborted")
    def metric_aborted(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of executions that were aborted.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricFailed")
    def metric_failed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of executions that failed.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricStarted")
    def metric_started(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of executions that were started.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricSucceeded")
    def metric_succeeded(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of executions that succeeded.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricThrottled")
    def metric_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of executions that were throttled.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: sum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricTime")
    def metric_time(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the interval, in milliseconds, between the time the execution starts and the time it closes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricTimedOut")
    def metric_timed_out(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of executions that timed out.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...


class _IStateMachineProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
    jsii.proxy_for(_IGrantable_4c5a91d1), # type: ignore[misc]
):
    '''(experimental) A State Machine.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_stepfunctions.IStateMachine"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stateMachineArn")
    def state_machine_arn(self) -> builtins.str:
        '''(experimental) The ARN of the state machine.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "stateMachineArn"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        identity: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity custom permissions.

        :param identity: The principal.
        :param actions: The list of desired actions.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [identity, *actions]))

    @jsii.member(jsii_name="grantExecution")
    def grant_execution(
        self,
        identity: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity permissions for all executions of a state machine.

        :param identity: The principal.
        :param actions: The list of desired actions.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantExecution", [identity, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity read permissions for this state machine.

        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantRead", [identity]))

    @jsii.member(jsii_name="grantStartExecution")
    def grant_start_execution(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity permissions to start an execution of this state machine.

        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantStartExecution", [identity]))

    @jsii.member(jsii_name="grantTaskResponse")
    def grant_task_response(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity read permissions for this state machine.

        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantTaskResponse", [identity]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Return the given named metric for this State Machine's executions.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricAborted")
    def metric_aborted(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of executions that were aborted.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricAborted", [props]))

    @jsii.member(jsii_name="metricFailed")
    def metric_failed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of executions that failed.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricFailed", [props]))

    @jsii.member(jsii_name="metricStarted")
    def metric_started(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of executions that were started.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricStarted", [props]))

    @jsii.member(jsii_name="metricSucceeded")
    def metric_succeeded(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of executions that succeeded.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSucceeded", [props]))

    @jsii.member(jsii_name="metricThrottled")
    def metric_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of executions that were throttled.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricThrottled", [props]))

    @jsii.member(jsii_name="metricTime")
    def metric_time(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the interval, in milliseconds, between the time the execution starts and the time it closes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricTime", [props]))

    @jsii.member(jsii_name="metricTimedOut")
    def metric_timed_out(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of executions that timed out.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricTimedOut", [props]))


@jsii.interface(jsii_type="monocdk.aws_stepfunctions.IStepFunctionsTask")
class IStepFunctionsTask(typing_extensions.Protocol):
    '''(experimental) Interface for resources that can be used as tasks.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IStepFunctionsTaskProxy"]:
        return _IStepFunctionsTaskProxy

    @jsii.member(jsii_name="bind")
    def bind(self, task: "Task") -> "StepFunctionsTaskConfig":
        '''(experimental) Called when the task object is used in a workflow.

        :param task: -

        :stability: experimental
        '''
        ...


class _IStepFunctionsTaskProxy:
    '''(experimental) Interface for resources that can be used as tasks.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_stepfunctions.IStepFunctionsTask"

    @jsii.member(jsii_name="bind")
    def bind(self, task: "Task") -> "StepFunctionsTaskConfig":
        '''(experimental) Called when the task object is used in a workflow.

        :param task: -

        :stability: experimental
        '''
        return typing.cast("StepFunctionsTaskConfig", jsii.invoke(self, "bind", [task]))


@jsii.enum(jsii_type="monocdk.aws_stepfunctions.InputType")
class InputType(enum.Enum):
    '''(experimental) The type of task input.

    :stability: experimental
    '''

    TEXT = "TEXT"
    '''(experimental) Use a literal string This might be a JSON-encoded object, or just text.

    valid JSON text: standalone, quote-delimited strings; objects; arrays; numbers; Boolean values; and null.

    example: ``literal string``
    example: {"json": "encoded"}

    :stability: experimental
    '''
    OBJECT = "OBJECT"
    '''(experimental) Use an object which may contain Data and Context fields as object values, if desired.

    example:
    {
    literal: 'literal',
    SomeInput: sfn.JsonPath.stringAt('$.someField')
    }

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/input-output-contextobject.html
    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.aws_stepfunctions.IntegrationPattern")
class IntegrationPattern(enum.Enum):
    '''(experimental) AWS Step Functions integrates with services directly in the Amazon States Language.

    You can control these AWS services using service integration patterns:

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html
    :stability: experimental
    '''

    REQUEST_RESPONSE = "REQUEST_RESPONSE"
    '''(experimental) Step Functions will wait for an HTTP response and then progress to the next state.

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-default
    :stability: experimental
    '''
    RUN_JOB = "RUN_JOB"
    '''(experimental) Step Functions can wait for a request to complete before progressing to the next state.

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-sync
    :stability: experimental
    '''
    WAIT_FOR_TASK_TOKEN = "WAIT_FOR_TASK_TOKEN"
    '''(experimental) Callback tasks provide a way to pause a workflow until a task token is returned.

    You must set a task token when using the callback pattern

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
    :stability: experimental
    '''


class JsonPath(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_stepfunctions.JsonPath"):
    '''(experimental) Extract a field from the State Machine data or context that gets passed around between states.

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-paths.html
    :stability: experimental
    '''

    @jsii.member(jsii_name="isEncodedJsonPath") # type: ignore[misc]
    @builtins.classmethod
    def is_encoded_json_path(cls, value: builtins.str) -> builtins.bool:
        '''(experimental) Determines if the indicated string is an encoded JSON path.

        :param value: string to be evaluated.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isEncodedJsonPath", [value]))

    @jsii.member(jsii_name="listAt") # type: ignore[misc]
    @builtins.classmethod
    def list_at(cls, path: builtins.str) -> typing.List[builtins.str]:
        '''(experimental) Instead of using a literal string list, get the value from a JSON path.

        :param path: -

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.sinvoke(cls, "listAt", [path]))

    @jsii.member(jsii_name="numberAt") # type: ignore[misc]
    @builtins.classmethod
    def number_at(cls, path: builtins.str) -> jsii.Number:
        '''(experimental) Instead of using a literal number, get the value from a JSON path.

        :param path: -

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.sinvoke(cls, "numberAt", [path]))

    @jsii.member(jsii_name="stringAt") # type: ignore[misc]
    @builtins.classmethod
    def string_at(cls, path: builtins.str) -> builtins.str:
        '''(experimental) Instead of using a literal string, get the value from a JSON path.

        :param path: -

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "stringAt", [path]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="DISCARD")
    def DISCARD(cls) -> builtins.str:
        '''(experimental) Special string value to discard state input, output or result.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "DISCARD"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="entireContext")
    def entire_context(cls) -> builtins.str:
        '''(experimental) Use the entire context data structure.

        Will be an object at invocation time, but is represented in the CDK
        application as a string.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "entireContext"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="entirePayload")
    def entire_payload(cls) -> builtins.str:
        '''(experimental) Use the entire data structure.

        Will be an object at invocation time, but is represented in the CDK
        application as a string.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "entirePayload"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="taskToken")
    def task_token(cls) -> builtins.str:
        '''(experimental) Return the Task Token field.

        External actions will need this token to report step completion
        back to StepFunctions using the ``SendTaskSuccess`` or ``SendTaskFailure``
        calls.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "taskToken"))


@jsii.enum(jsii_type="monocdk.aws_stepfunctions.LogLevel")
class LogLevel(enum.Enum):
    '''(experimental) Defines which category of execution history events are logged.

    :default: ERROR

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/cloudwatch-log-level.html
    :stability: experimental
    '''

    OFF = "OFF"
    '''(experimental) No Logging.

    :stability: experimental
    '''
    ALL = "ALL"
    '''(experimental) Log everything.

    :stability: experimental
    '''
    ERROR = "ERROR"
    '''(experimental) Log all errors.

    :stability: experimental
    '''
    FATAL = "FATAL"
    '''(experimental) Log fatal errors.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.LogOptions",
    jsii_struct_bases=[],
    name_mapping={
        "destination": "destination",
        "include_execution_data": "includeExecutionData",
        "level": "level",
    },
)
class LogOptions:
    def __init__(
        self,
        *,
        destination: _ILogGroup_846e17a0,
        include_execution_data: typing.Optional[builtins.bool] = None,
        level: typing.Optional[LogLevel] = None,
    ) -> None:
        '''(experimental) Defines what execution history events are logged and where they are logged.

        :param destination: (experimental) The log group where the execution history events will be logged.
        :param include_execution_data: (experimental) Determines whether execution data is included in your log. Default: true
        :param level: (experimental) Defines which category of execution history events are logged. Default: ERROR

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "destination": destination,
        }
        if include_execution_data is not None:
            self._values["include_execution_data"] = include_execution_data
        if level is not None:
            self._values["level"] = level

    @builtins.property
    def destination(self) -> _ILogGroup_846e17a0:
        '''(experimental) The log group where the execution history events will be logged.

        :stability: experimental
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(_ILogGroup_846e17a0, result)

    @builtins.property
    def include_execution_data(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Determines whether execution data is included in your log.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("include_execution_data")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def level(self) -> typing.Optional[LogLevel]:
        '''(experimental) Defines which category of execution history events are logged.

        :default: ERROR

        :stability: experimental
        '''
        result = self._values.get("level")
        return typing.cast(typing.Optional[LogLevel], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.MapProps",
    jsii_struct_bases=[],
    name_mapping={
        "comment": "comment",
        "input_path": "inputPath",
        "items_path": "itemsPath",
        "max_concurrency": "maxConcurrency",
        "output_path": "outputPath",
        "parameters": "parameters",
        "result_path": "resultPath",
    },
)
class MapProps:
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        items_path: typing.Optional[builtins.str] = None,
        max_concurrency: typing.Optional[jsii.Number] = None,
        output_path: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        result_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for defining a Map state.

        :param comment: (experimental) An optional description for this state. Default: No comment
        :param input_path: (experimental) JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param items_path: (experimental) JSONPath expression to select the array to iterate over. Default: $
        :param max_concurrency: (experimental) MaxConcurrency. An upper bound on the number of iterations you want running at once. Default: - full concurrency
        :param output_path: (experimental) JSONPath expression to select part of the state to be the output to this state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param parameters: (experimental) The JSON that you want to override your default iteration input. Default: $
        :param result_path: (experimental) JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: $

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if comment is not None:
            self._values["comment"] = comment
        if input_path is not None:
            self._values["input_path"] = input_path
        if items_path is not None:
            self._values["items_path"] = items_path
        if max_concurrency is not None:
            self._values["max_concurrency"] = max_concurrency
        if output_path is not None:
            self._values["output_path"] = output_path
        if parameters is not None:
            self._values["parameters"] = parameters
        if result_path is not None:
            self._values["result_path"] = result_path

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''(experimental) An optional description for this state.

        :default: No comment

        :stability: experimental
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("input_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def items_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to select the array to iterate over.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("items_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_concurrency(self) -> typing.Optional[jsii.Number]:
        '''(experimental) MaxConcurrency.

        An upper bound on the number of iterations you want running at once.

        :default: - full concurrency

        :stability: experimental
        '''
        result = self._values.get("max_concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to select part of the state to be the output to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("output_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) The JSON that you want to override your default iteration input.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("result_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MapProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.ParallelProps",
    jsii_struct_bases=[],
    name_mapping={
        "comment": "comment",
        "input_path": "inputPath",
        "output_path": "outputPath",
        "result_path": "resultPath",
    },
)
class ParallelProps:
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for defining a Parallel state.

        :param comment: (experimental) An optional description for this state. Default: No comment
        :param input_path: (experimental) JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: (experimental) JSONPath expression to select part of the state to be the output to this state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param result_path: (experimental) JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: $

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if comment is not None:
            self._values["comment"] = comment
        if input_path is not None:
            self._values["input_path"] = input_path
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''(experimental) An optional description for this state.

        :default: No comment

        :stability: experimental
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("input_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to select part of the state to be the output to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("output_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("result_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParallelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.PassProps",
    jsii_struct_bases=[],
    name_mapping={
        "comment": "comment",
        "input_path": "inputPath",
        "output_path": "outputPath",
        "parameters": "parameters",
        "result": "result",
        "result_path": "resultPath",
    },
)
class PassProps:
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        result: typing.Optional["Result"] = None,
        result_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for defining a Pass state.

        :param comment: (experimental) An optional description for this state. Default: No comment
        :param input_path: (experimental) JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: (experimental) JSONPath expression to select part of the state to be the output to this state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param parameters: (experimental) Parameters pass a collection of key-value pairs, either static values or JSONPath expressions that select from the input. Default: No parameters
        :param result: (experimental) If given, treat as the result of this operation. Can be used to inject or replace the current execution state. Default: No injected result
        :param result_path: (experimental) JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: $

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if comment is not None:
            self._values["comment"] = comment
        if input_path is not None:
            self._values["input_path"] = input_path
        if output_path is not None:
            self._values["output_path"] = output_path
        if parameters is not None:
            self._values["parameters"] = parameters
        if result is not None:
            self._values["result"] = result
        if result_path is not None:
            self._values["result_path"] = result_path

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''(experimental) An optional description for this state.

        :default: No comment

        :stability: experimental
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("input_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to select part of the state to be the output to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("output_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Parameters pass a collection of key-value pairs, either static values or JSONPath expressions that select from the input.

        :default: No parameters

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/input-output-inputpath-params.html#input-output-parameters
        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def result(self) -> typing.Optional["Result"]:
        '''(experimental) If given, treat as the result of this operation.

        Can be used to inject or replace the current execution state.

        :default: No injected result

        :stability: experimental
        '''
        result = self._values.get("result")
        return typing.cast(typing.Optional["Result"], result)

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("result_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PassProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Result(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_stepfunctions.Result"):
    '''(experimental) The result of a Pass operation.

    :stability: experimental
    '''

    def __init__(self, value: typing.Any) -> None:
        '''
        :param value: result of the Pass operation.

        :stability: experimental
        '''
        jsii.create(Result, self, [value])

    @jsii.member(jsii_name="fromArray") # type: ignore[misc]
    @builtins.classmethod
    def from_array(cls, value: typing.List[typing.Any]) -> "Result":
        '''(experimental) The result of the operation is an array.

        :param value: -

        :stability: experimental
        '''
        return typing.cast("Result", jsii.sinvoke(cls, "fromArray", [value]))

    @jsii.member(jsii_name="fromBoolean") # type: ignore[misc]
    @builtins.classmethod
    def from_boolean(cls, value: builtins.bool) -> "Result":
        '''(experimental) The result of the operation is a boolean.

        :param value: -

        :stability: experimental
        '''
        return typing.cast("Result", jsii.sinvoke(cls, "fromBoolean", [value]))

    @jsii.member(jsii_name="fromNumber") # type: ignore[misc]
    @builtins.classmethod
    def from_number(cls, value: jsii.Number) -> "Result":
        '''(experimental) The result of the operation is a number.

        :param value: -

        :stability: experimental
        '''
        return typing.cast("Result", jsii.sinvoke(cls, "fromNumber", [value]))

    @jsii.member(jsii_name="fromObject") # type: ignore[misc]
    @builtins.classmethod
    def from_object(cls, value: typing.Mapping[builtins.str, typing.Any]) -> "Result":
        '''(experimental) The result of the operation is an object.

        :param value: -

        :stability: experimental
        '''
        return typing.cast("Result", jsii.sinvoke(cls, "fromObject", [value]))

    @jsii.member(jsii_name="fromString") # type: ignore[misc]
    @builtins.classmethod
    def from_string(cls, value: builtins.str) -> "Result":
        '''(experimental) The result of the operation is a string.

        :param value: -

        :stability: experimental
        '''
        return typing.cast("Result", jsii.sinvoke(cls, "fromString", [value]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''(experimental) result of the Pass operation.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "value"))


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.RetryProps",
    jsii_struct_bases=[],
    name_mapping={
        "backoff_rate": "backoffRate",
        "errors": "errors",
        "interval": "interval",
        "max_attempts": "maxAttempts",
    },
)
class RetryProps:
    def __init__(
        self,
        *,
        backoff_rate: typing.Optional[jsii.Number] = None,
        errors: typing.Optional[typing.List[builtins.str]] = None,
        interval: typing.Optional[_Duration_070aa057] = None,
        max_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Retry details.

        :param backoff_rate: (experimental) Multiplication for how much longer the wait interval gets on every retry. Default: 2
        :param errors: (experimental) Errors to retry. A list of error strings to retry, which can be either predefined errors (for example Errors.NoChoiceMatched) or a self-defined error. Default: All errors
        :param interval: (experimental) How many seconds to wait initially before retrying. Default: Duration.seconds(1)
        :param max_attempts: (experimental) How many times to retry this particular error. May be 0 to disable retry for specific errors (in case you have a catch-all retry policy). Default: 3

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if backoff_rate is not None:
            self._values["backoff_rate"] = backoff_rate
        if errors is not None:
            self._values["errors"] = errors
        if interval is not None:
            self._values["interval"] = interval
        if max_attempts is not None:
            self._values["max_attempts"] = max_attempts

    @builtins.property
    def backoff_rate(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Multiplication for how much longer the wait interval gets on every retry.

        :default: 2

        :stability: experimental
        '''
        result = self._values.get("backoff_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def errors(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Errors to retry.

        A list of error strings to retry, which can be either predefined errors
        (for example Errors.NoChoiceMatched) or a self-defined error.

        :default: All errors

        :stability: experimental
        '''
        result = self._values.get("errors")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def interval(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) How many seconds to wait initially before retrying.

        :default: Duration.seconds(1)

        :stability: experimental
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def max_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) How many times to retry this particular error.

        May be 0 to disable retry for specific errors (in case you have
        a catch-all retry policy).

        :default: 3

        :stability: experimental
        '''
        result = self._values.get("max_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RetryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_stepfunctions.ServiceIntegrationPattern")
class ServiceIntegrationPattern(enum.Enum):
    '''(experimental) Three ways to call an integrated service: Request Response, Run a Job and Wait for a Callback with Task Token.

    :default: FIRE_AND_FORGET

    :see:

    https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html

    Here, they are named as FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN respectly.
    :stability: experimental
    '''

    FIRE_AND_FORGET = "FIRE_AND_FORGET"
    '''(experimental) Call a service and progress to the next state immediately after the API call completes.

    :stability: experimental
    '''
    SYNC = "SYNC"
    '''(experimental) Call a service and wait for a job to complete.

    :stability: experimental
    '''
    WAIT_FOR_TASK_TOKEN = "WAIT_FOR_TASK_TOKEN"
    '''(experimental) Call a service with a task token and wait until that token is returned by SendTaskSuccess/SendTaskFailure with paylaod.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.SingleStateOptions",
    jsii_struct_bases=[ParallelProps],
    name_mapping={
        "comment": "comment",
        "input_path": "inputPath",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "prefix_states": "prefixStates",
        "state_id": "stateId",
    },
)
class SingleStateOptions(ParallelProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        prefix_states: typing.Optional[builtins.str] = None,
        state_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for creating a single state.

        :param comment: (experimental) An optional description for this state. Default: No comment
        :param input_path: (experimental) JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: (experimental) JSONPath expression to select part of the state to be the output to this state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param result_path: (experimental) JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: $
        :param prefix_states: (experimental) String to prefix all stateIds in the state machine with. Default: stateId
        :param state_id: (experimental) ID of newly created containing state. Default: Construct ID of the StateMachineFragment

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if comment is not None:
            self._values["comment"] = comment
        if input_path is not None:
            self._values["input_path"] = input_path
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if prefix_states is not None:
            self._values["prefix_states"] = prefix_states
        if state_id is not None:
            self._values["state_id"] = state_id

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''(experimental) An optional description for this state.

        :default: No comment

        :stability: experimental
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("input_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to select part of the state to be the output to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("output_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("result_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix_states(self) -> typing.Optional[builtins.str]:
        '''(experimental) String to prefix all stateIds in the state machine with.

        :default: stateId

        :stability: experimental
        '''
        result = self._values.get("prefix_states")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) ID of newly created containing state.

        :default: Construct ID of the StateMachineFragment

        :stability: experimental
        '''
        result = self._values.get("state_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SingleStateOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IChainable)
class State(
    _Construct_e78e779f,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_stepfunctions.State",
):
    '''(experimental) Base class for all other state classes.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_StateProxy"]:
        return _StateProxy

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        comment: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        result_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param comment: (experimental) A comment describing this state. Default: No comment
        :param input_path: (experimental) JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: (experimental) JSONPath expression to select part of the state to be the output to this state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param parameters: (experimental) Parameters pass a collection of key-value pairs, either static values or JSONPath expressions that select from the input. Default: No parameters
        :param result_path: (experimental) JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: $

        :stability: experimental
        '''
        props = StateProps(
            comment=comment,
            input_path=input_path,
            output_path=output_path,
            parameters=parameters,
            result_path=result_path,
        )

        jsii.create(State, self, [scope, id, props])

    @jsii.member(jsii_name="filterNextables") # type: ignore[misc]
    @builtins.classmethod
    def filter_nextables(cls, states: typing.List["State"]) -> typing.List[INextable]:
        '''(experimental) Return only the states that allow chaining from an array of states.

        :param states: -

        :stability: experimental
        '''
        return typing.cast(typing.List[INextable], jsii.sinvoke(cls, "filterNextables", [states]))

    @jsii.member(jsii_name="findReachableEndStates") # type: ignore[misc]
    @builtins.classmethod
    def find_reachable_end_states(
        cls,
        start: "State",
        *,
        include_error_handlers: typing.Optional[builtins.bool] = None,
    ) -> typing.List["State"]:
        '''(experimental) Find the set of end states states reachable through transitions from the given start state.

        :param start: -
        :param include_error_handlers: (experimental) Whether or not to follow error-handling transitions. Default: false

        :stability: experimental
        '''
        options = FindStateOptions(include_error_handlers=include_error_handlers)

        return typing.cast(typing.List["State"], jsii.sinvoke(cls, "findReachableEndStates", [start, options]))

    @jsii.member(jsii_name="findReachableStates") # type: ignore[misc]
    @builtins.classmethod
    def find_reachable_states(
        cls,
        start: "State",
        *,
        include_error_handlers: typing.Optional[builtins.bool] = None,
    ) -> typing.List["State"]:
        '''(experimental) Find the set of states reachable through transitions from the given start state.

        This does not retrieve states from within sub-graphs, such as states within a Parallel state's branch.

        :param start: -
        :param include_error_handlers: (experimental) Whether or not to follow error-handling transitions. Default: false

        :stability: experimental
        '''
        options = FindStateOptions(include_error_handlers=include_error_handlers)

        return typing.cast(typing.List["State"], jsii.sinvoke(cls, "findReachableStates", [start, options]))

    @jsii.member(jsii_name="prefixStates") # type: ignore[misc]
    @builtins.classmethod
    def prefix_states(cls, root: constructs.IConstruct, prefix: builtins.str) -> None:
        '''(experimental) Add a prefix to the stateId of all States found in a construct tree.

        :param root: -
        :param prefix: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.sinvoke(cls, "prefixStates", [root, prefix]))

    @jsii.member(jsii_name="addBranch")
    def _add_branch(self, branch: "StateGraph") -> None:
        '''(experimental) Add a paralle branch to this state.

        :param branch: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addBranch", [branch]))

    @jsii.member(jsii_name="addChoice")
    def _add_choice(self, condition: Condition, next: "State") -> None:
        '''(experimental) Add a choice branch to this state.

        :param condition: -
        :param next: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addChoice", [condition, next]))

    @jsii.member(jsii_name="addIterator")
    def _add_iterator(self, iteration: "StateGraph") -> None:
        '''(experimental) Add a map iterator to this state.

        :param iteration: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addIterator", [iteration]))

    @jsii.member(jsii_name="addPrefix")
    def add_prefix(self, x: builtins.str) -> None:
        '''(experimental) Add a prefix to the stateId of this state.

        :param x: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addPrefix", [x]))

    @jsii.member(jsii_name="bindToGraph")
    def bind_to_graph(self, graph: "StateGraph") -> None:
        '''(experimental) Register this state as part of the given graph.

        Don't call this. It will be called automatically when you work
        with states normally.

        :param graph: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "bindToGraph", [graph]))

    @jsii.member(jsii_name="makeDefault")
    def _make_default(self, def_: "State") -> None:
        '''(experimental) Make the indicated state the default choice transition of this state.

        :param def_: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "makeDefault", [def_]))

    @jsii.member(jsii_name="makeNext")
    def _make_next(self, next: "State") -> None:
        '''(experimental) Make the indicated state the default transition of this state.

        :param next: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "makeNext", [next]))

    @jsii.member(jsii_name="renderBranches")
    def _render_branches(self) -> typing.Any:
        '''(experimental) Render parallel branches in ASL JSON format.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "renderBranches", []))

    @jsii.member(jsii_name="renderChoices")
    def _render_choices(self) -> typing.Any:
        '''(experimental) Render the choices in ASL JSON format.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "renderChoices", []))

    @jsii.member(jsii_name="renderInputOutput")
    def _render_input_output(self) -> typing.Any:
        '''(experimental) Render InputPath/Parameters/OutputPath in ASL JSON format.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "renderInputOutput", []))

    @jsii.member(jsii_name="renderIterator")
    def _render_iterator(self) -> typing.Any:
        '''(experimental) Render map iterator in ASL JSON format.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "renderIterator", []))

    @jsii.member(jsii_name="renderNextEnd")
    def _render_next_end(self) -> typing.Any:
        '''(experimental) Render the default next state in ASL JSON format.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "renderNextEnd", []))

    @jsii.member(jsii_name="renderRetryCatch")
    def _render_retry_catch(self) -> typing.Any:
        '''(experimental) Render error recovery options in ASL JSON format.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "renderRetryCatch", []))

    @jsii.member(jsii_name="toStateJson") # type: ignore[misc]
    @abc.abstractmethod
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        '''(experimental) Render the state as JSON.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="whenBoundToGraph")
    def _when_bound_to_graph(self, graph: "StateGraph") -> None:
        '''(experimental) Called whenever this state is bound to a graph.

        Can be overridden by subclasses.

        :param graph: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "whenBoundToGraph", [graph]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="branches")
    def _branches(self) -> typing.List["StateGraph"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List["StateGraph"], jsii.get(self, "branches"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    @abc.abstractmethod
    def end_states(self) -> typing.List[INextable]:
        '''(experimental) Continuable states of this Chainable.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) Descriptive identifier for this chainable.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="startState")
    def start_state(self) -> "State":
        '''(experimental) First state of this Chainable.

        :stability: experimental
        '''
        return typing.cast("State", jsii.get(self, "startState"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stateId")
    def state_id(self) -> builtins.str:
        '''(experimental) Tokenized string that evaluates to the state's ID.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "stateId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="comment")
    def _comment(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comment"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="inputPath")
    def _input_path(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputPath"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="outputPath")
    def _output_path(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputPath"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="parameters")
    def _parameters(self) -> typing.Optional[typing.Mapping[typing.Any, typing.Any]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[typing.Any, typing.Any]], jsii.get(self, "parameters"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="resultPath")
    def _result_path(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resultPath"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultChoice")
    def _default_choice(self) -> typing.Optional["State"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["State"], jsii.get(self, "defaultChoice"))

    @_default_choice.setter
    def _default_choice(self, value: typing.Optional["State"]) -> None:
        jsii.set(self, "defaultChoice", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="iteration")
    def _iteration(self) -> typing.Optional["StateGraph"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["StateGraph"], jsii.get(self, "iteration"))

    @_iteration.setter
    def _iteration(self, value: typing.Optional["StateGraph"]) -> None:
        jsii.set(self, "iteration", value)


class _StateProxy(State):
    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        '''(experimental) Render the state as JSON.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toStateJson", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List[INextable]:
        '''(experimental) Continuable states of this Chainable.

        :stability: experimental
        '''
        return typing.cast(typing.List[INextable], jsii.get(self, "endStates"))


class StateGraph(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_stepfunctions.StateGraph",
):
    '''(experimental) A collection of connected states.

    A StateGraph is used to keep track of all states that are connected (have
    transitions between them). It does not include the substatemachines in
    a Parallel's branches: those are their own StateGraphs, but the graphs
    themselves have a hierarchical relationship as well.

    By assigning states to a definitive StateGraph, we verify that no state
    machines are constructed. In particular:

    - Every state object can only ever be in 1 StateGraph, and not inadvertently
      be used in two graphs.
    - Every stateId must be unique across all states in the entire state
      machine.

    All policy statements in all states in all substatemachines are bubbled so
    that the top-level StateMachine instantiation can read them all and add
    them to the IAM Role.

    You do not need to instantiate this class; it is used internally.

    :stability: experimental
    '''

    def __init__(self, start_state: State, graph_description: builtins.str) -> None:
        '''
        :param start_state: state that gets executed when the state machine is launched.
        :param graph_description: description of the state machine.

        :stability: experimental
        '''
        jsii.create(StateGraph, self, [start_state, graph_description])

    @jsii.member(jsii_name="registerPolicyStatement")
    def register_policy_statement(self, statement: _PolicyStatement_296fe8a3) -> None:
        '''(experimental) Register a Policy Statement used by states in this graph.

        :param statement: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "registerPolicyStatement", [statement]))

    @jsii.member(jsii_name="registerState")
    def register_state(self, state: State) -> None:
        '''(experimental) Register a state as part of this graph.

        Called by State.bindToGraph().

        :param state: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "registerState", [state]))

    @jsii.member(jsii_name="registerSuperGraph")
    def register_super_graph(self, graph: "StateGraph") -> None:
        '''(experimental) Register this graph as a child of the given graph.

        Resource changes will be bubbled up to the given graph.

        :param graph: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "registerSuperGraph", [graph]))

    @jsii.member(jsii_name="toGraphJson")
    def to_graph_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        '''(experimental) Return the Amazon States Language JSON for this graph.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toGraphJson", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string description of this graph.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policyStatements")
    def policy_statements(self) -> typing.List[_PolicyStatement_296fe8a3]:
        '''(experimental) The accumulated policy statements.

        :stability: experimental
        '''
        return typing.cast(typing.List[_PolicyStatement_296fe8a3], jsii.get(self, "policyStatements"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="startState")
    def start_state(self) -> State:
        '''(experimental) state that gets executed when the state machine is launched.

        :stability: experimental
        '''
        return typing.cast(State, jsii.get(self, "startState"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Set a timeout to render into the graph JSON.

        Read/write. Only makes sense on the top-level graph, subgraphs
        do not support this feature.

        :default: No timeout

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_Duration_070aa057], jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: typing.Optional[_Duration_070aa057]) -> None:
        jsii.set(self, "timeout", value)


@jsii.implements(IStateMachine)
class StateMachine(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_stepfunctions.StateMachine",
):
    '''(experimental) Define a StepFunctions State Machine.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        definition: IChainable,
        logs: typing.Optional[LogOptions] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        state_machine_name: typing.Optional[builtins.str] = None,
        state_machine_type: typing.Optional["StateMachineType"] = None,
        timeout: typing.Optional[_Duration_070aa057] = None,
        tracing_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param definition: (experimental) Definition for this state machine.
        :param logs: (experimental) Defines what execution history events are logged and where they are logged. Default: No logging
        :param role: (experimental) The execution role for the state machine service. Default: A role is automatically created
        :param state_machine_name: (experimental) A name for the state machine. Default: A name is automatically generated
        :param state_machine_type: (experimental) Type of the state machine. Default: StateMachineType.STANDARD
        :param timeout: (experimental) Maximum run time for this state machine. Default: No timeout
        :param tracing_enabled: (experimental) Specifies whether Amazon X-Ray tracing is enabled for this state machine. Default: false

        :stability: experimental
        '''
        props = StateMachineProps(
            definition=definition,
            logs=logs,
            role=role,
            state_machine_name=state_machine_name,
            state_machine_type=state_machine_type,
            timeout=timeout,
            tracing_enabled=tracing_enabled,
        )

        jsii.create(StateMachine, self, [scope, id, props])

    @jsii.member(jsii_name="fromStateMachineArn") # type: ignore[misc]
    @builtins.classmethod
    def from_state_machine_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        state_machine_arn: builtins.str,
    ) -> IStateMachine:
        '''(experimental) Import a state machine.

        :param scope: -
        :param id: -
        :param state_machine_arn: -

        :stability: experimental
        '''
        return typing.cast(IStateMachine, jsii.sinvoke(cls, "fromStateMachineArn", [scope, id, state_machine_arn]))

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: _PolicyStatement_296fe8a3) -> None:
        '''(experimental) Add the given statement to the role's policy.

        :param statement: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addToRolePolicy", [statement]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        identity: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity custom permissions.

        :param identity: -
        :param actions: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [identity, *actions]))

    @jsii.member(jsii_name="grantExecution")
    def grant_execution(
        self,
        identity: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity permissions on all executions of the state machine.

        :param identity: -
        :param actions: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantExecution", [identity, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity permissions to read results from state machine.

        :param identity: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantRead", [identity]))

    @jsii.member(jsii_name="grantStartExecution")
    def grant_start_execution(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity permissions to start an execution of this state machine.

        :param identity: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantStartExecution", [identity]))

    @jsii.member(jsii_name="grantTaskResponse")
    def grant_task_response(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity task response permissions on a state machine.

        :param identity: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantTaskResponse", [identity]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Return the given named metric for this State Machine's executions.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricAborted")
    def metric_aborted(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of executions that were aborted.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricAborted", [props]))

    @jsii.member(jsii_name="metricFailed")
    def metric_failed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of executions that failed.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricFailed", [props]))

    @jsii.member(jsii_name="metricStarted")
    def metric_started(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of executions that were started.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricStarted", [props]))

    @jsii.member(jsii_name="metricSucceeded")
    def metric_succeeded(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of executions that succeeded.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSucceeded", [props]))

    @jsii.member(jsii_name="metricThrottled")
    def metric_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of executions that were throttled.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricThrottled", [props]))

    @jsii.member(jsii_name="metricTime")
    def metric_time(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the interval, in milliseconds, between the time the execution starts and the time it closes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricTime", [props]))

    @jsii.member(jsii_name="metricTimedOut")
    def metric_timed_out(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of executions that timed out.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricTimedOut", [props]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_93b48231:
        '''(experimental) The principal this state machine is running as.

        :stability: experimental
        '''
        return typing.cast(_IPrincipal_93b48231, jsii.get(self, "grantPrincipal"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="role")
    def role(self) -> _IRole_59af6f50:
        '''(experimental) Execution role of this state machine.

        :stability: experimental
        '''
        return typing.cast(_IRole_59af6f50, jsii.get(self, "role"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stateMachineArn")
    def state_machine_arn(self) -> builtins.str:
        '''(experimental) The ARN of the state machine.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "stateMachineArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stateMachineName")
    def state_machine_name(self) -> builtins.str:
        '''(experimental) The name of the state machine.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "stateMachineName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stateMachineType")
    def state_machine_type(self) -> "StateMachineType":
        '''(experimental) Type of the state machine.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast("StateMachineType", jsii.get(self, "stateMachineType"))


@jsii.implements(IChainable)
class StateMachineFragment(
    _Construct_e78e779f,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_stepfunctions.StateMachineFragment",
):
    '''(experimental) Base class for reusable state machine fragments.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_StateMachineFragmentProxy"]:
        return _StateMachineFragmentProxy

    def __init__(self, scope: constructs.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        jsii.create(StateMachineFragment, self, [scope, id])

    @jsii.member(jsii_name="next")
    def next(self, next: IChainable) -> "Chain":
        '''(experimental) Continue normal execution with the given state.

        :param next: -

        :stability: experimental
        '''
        return typing.cast("Chain", jsii.invoke(self, "next", [next]))

    @jsii.member(jsii_name="prefixStates")
    def prefix_states(
        self,
        prefix: typing.Optional[builtins.str] = None,
    ) -> "StateMachineFragment":
        '''(experimental) Prefix the IDs of all states in this state machine fragment.

        Use this to avoid multiple copies of the state machine all having the
        same state IDs.

        :param prefix: The prefix to add. Will use construct ID by default.

        :stability: experimental
        '''
        return typing.cast("StateMachineFragment", jsii.invoke(self, "prefixStates", [prefix]))

    @jsii.member(jsii_name="toSingleState")
    def to_single_state(
        self,
        *,
        prefix_states: typing.Optional[builtins.str] = None,
        state_id: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
    ) -> "Parallel":
        '''(experimental) Wrap all states in this state machine fragment up into a single state.

        This can be used to add retry or error handling onto this state
        machine fragment.

        Be aware that this changes the result of the inner state machine
        to be an array with the result of the state machine in it. Adjust
        your paths accordingly. For example, change 'outputPath' to
        '$[0]'.

        :param prefix_states: (experimental) String to prefix all stateIds in the state machine with. Default: stateId
        :param state_id: (experimental) ID of newly created containing state. Default: Construct ID of the StateMachineFragment
        :param comment: (experimental) An optional description for this state. Default: No comment
        :param input_path: (experimental) JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: (experimental) JSONPath expression to select part of the state to be the output to this state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param result_path: (experimental) JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: $

        :stability: experimental
        '''
        options = SingleStateOptions(
            prefix_states=prefix_states,
            state_id=state_id,
            comment=comment,
            input_path=input_path,
            output_path=output_path,
            result_path=result_path,
        )

        return typing.cast("Parallel", jsii.invoke(self, "toSingleState", [options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    @abc.abstractmethod
    def end_states(self) -> typing.List[INextable]:
        '''(experimental) The states to chain onto if this fragment is used.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) Descriptive identifier for this chainable.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="startState")
    @abc.abstractmethod
    def start_state(self) -> State:
        '''(experimental) The start state of this state machine fragment.

        :stability: experimental
        '''
        ...


class _StateMachineFragmentProxy(StateMachineFragment):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List[INextable]:
        '''(experimental) The states to chain onto if this fragment is used.

        :stability: experimental
        '''
        return typing.cast(typing.List[INextable], jsii.get(self, "endStates"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="startState")
    def start_state(self) -> State:
        '''(experimental) The start state of this state machine fragment.

        :stability: experimental
        '''
        return typing.cast(State, jsii.get(self, "startState"))


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.StateMachineProps",
    jsii_struct_bases=[],
    name_mapping={
        "definition": "definition",
        "logs": "logs",
        "role": "role",
        "state_machine_name": "stateMachineName",
        "state_machine_type": "stateMachineType",
        "timeout": "timeout",
        "tracing_enabled": "tracingEnabled",
    },
)
class StateMachineProps:
    def __init__(
        self,
        *,
        definition: IChainable,
        logs: typing.Optional[LogOptions] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        state_machine_name: typing.Optional[builtins.str] = None,
        state_machine_type: typing.Optional["StateMachineType"] = None,
        timeout: typing.Optional[_Duration_070aa057] = None,
        tracing_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for defining a State Machine.

        :param definition: (experimental) Definition for this state machine.
        :param logs: (experimental) Defines what execution history events are logged and where they are logged. Default: No logging
        :param role: (experimental) The execution role for the state machine service. Default: A role is automatically created
        :param state_machine_name: (experimental) A name for the state machine. Default: A name is automatically generated
        :param state_machine_type: (experimental) Type of the state machine. Default: StateMachineType.STANDARD
        :param timeout: (experimental) Maximum run time for this state machine. Default: No timeout
        :param tracing_enabled: (experimental) Specifies whether Amazon X-Ray tracing is enabled for this state machine. Default: false

        :stability: experimental
        '''
        if isinstance(logs, dict):
            logs = LogOptions(**logs)
        self._values: typing.Dict[str, typing.Any] = {
            "definition": definition,
        }
        if logs is not None:
            self._values["logs"] = logs
        if role is not None:
            self._values["role"] = role
        if state_machine_name is not None:
            self._values["state_machine_name"] = state_machine_name
        if state_machine_type is not None:
            self._values["state_machine_type"] = state_machine_type
        if timeout is not None:
            self._values["timeout"] = timeout
        if tracing_enabled is not None:
            self._values["tracing_enabled"] = tracing_enabled

    @builtins.property
    def definition(self) -> IChainable:
        '''(experimental) Definition for this state machine.

        :stability: experimental
        '''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(IChainable, result)

    @builtins.property
    def logs(self) -> typing.Optional[LogOptions]:
        '''(experimental) Defines what execution history events are logged and where they are logged.

        :default: No logging

        :stability: experimental
        '''
        result = self._values.get("logs")
        return typing.cast(typing.Optional[LogOptions], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The execution role for the state machine service.

        :default: A role is automatically created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def state_machine_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the state machine.

        :default: A name is automatically generated

        :stability: experimental
        '''
        result = self._values.get("state_machine_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state_machine_type(self) -> typing.Optional["StateMachineType"]:
        '''(experimental) Type of the state machine.

        :default: StateMachineType.STANDARD

        :stability: experimental
        '''
        result = self._values.get("state_machine_type")
        return typing.cast(typing.Optional["StateMachineType"], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Maximum run time for this state machine.

        :default: No timeout

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def tracing_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether Amazon X-Ray tracing is enabled for this state machine.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("tracing_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StateMachineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_stepfunctions.StateMachineType")
class StateMachineType(enum.Enum):
    '''(experimental) Two types of state machines are available in AWS Step Functions: EXPRESS AND STANDARD.

    :default: STANDARD

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/concepts-standard-vs-express.html
    :stability: experimental
    '''

    EXPRESS = "EXPRESS"
    '''(experimental) Express Workflows are ideal for high-volume, event processing workloads.

    :stability: experimental
    '''
    STANDARD = "STANDARD"
    '''(experimental) Standard Workflows are ideal for long-running, durable, and auditable workflows.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.StateProps",
    jsii_struct_bases=[],
    name_mapping={
        "comment": "comment",
        "input_path": "inputPath",
        "output_path": "outputPath",
        "parameters": "parameters",
        "result_path": "resultPath",
    },
)
class StateProps:
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        result_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties shared by all states.

        :param comment: (experimental) A comment describing this state. Default: No comment
        :param input_path: (experimental) JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: (experimental) JSONPath expression to select part of the state to be the output to this state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param parameters: (experimental) Parameters pass a collection of key-value pairs, either static values or JSONPath expressions that select from the input. Default: No parameters
        :param result_path: (experimental) JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: $

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if comment is not None:
            self._values["comment"] = comment
        if input_path is not None:
            self._values["input_path"] = input_path
        if output_path is not None:
            self._values["output_path"] = output_path
        if parameters is not None:
            self._values["parameters"] = parameters
        if result_path is not None:
            self._values["result_path"] = result_path

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''(experimental) A comment describing this state.

        :default: No comment

        :stability: experimental
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("input_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to select part of the state to be the output to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("output_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Parameters pass a collection of key-value pairs, either static values or JSONPath expressions that select from the input.

        :default: No parameters

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/input-output-inputpath-params.html#input-output-parameters
        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("result_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StateTransitionMetric(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_stepfunctions.StateTransitionMetric",
):
    '''(experimental) Metrics on the rate limiting performed on state machine execution.

    These rate limits are shared across all state machines.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(StateTransitionMetric, self, [])

    @jsii.member(jsii_name="metric") # type: ignore[misc]
    @builtins.classmethod
    def metric(
        cls,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Return the given named metric for the service's state transition metrics.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.sinvoke(cls, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricConsumedCapacity") # type: ignore[misc]
    @builtins.classmethod
    def metric_consumed_capacity(
        cls,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of available state transitions per second.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.sinvoke(cls, "metricConsumedCapacity", [props]))

    @jsii.member(jsii_name="metricProvisionedBucketSize") # type: ignore[misc]
    @builtins.classmethod
    def metric_provisioned_bucket_size(
        cls,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of available state transitions.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.sinvoke(cls, "metricProvisionedBucketSize", [props]))

    @jsii.member(jsii_name="metricProvisionedRefillRate") # type: ignore[misc]
    @builtins.classmethod
    def metric_provisioned_refill_rate(
        cls,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the provisioned steady-state execution rate.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.sinvoke(cls, "metricProvisionedRefillRate", [props]))

    @jsii.member(jsii_name="metricThrottledEvents") # type: ignore[misc]
    @builtins.classmethod
    def metric_throttled_events(
        cls,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of throttled state transitions.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.sinvoke(cls, "metricThrottledEvents", [props]))


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.StepFunctionsTaskConfig",
    jsii_struct_bases=[],
    name_mapping={
        "resource_arn": "resourceArn",
        "heartbeat": "heartbeat",
        "metric_dimensions": "metricDimensions",
        "metric_prefix_plural": "metricPrefixPlural",
        "metric_prefix_singular": "metricPrefixSingular",
        "parameters": "parameters",
        "policy_statements": "policyStatements",
    },
)
class StepFunctionsTaskConfig:
    def __init__(
        self,
        *,
        resource_arn: builtins.str,
        heartbeat: typing.Optional[_Duration_070aa057] = None,
        metric_dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        metric_prefix_plural: typing.Optional[builtins.str] = None,
        metric_prefix_singular: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        policy_statements: typing.Optional[typing.List[_PolicyStatement_296fe8a3]] = None,
    ) -> None:
        '''(experimental) Properties that define what kind of task should be created.

        :param resource_arn: (experimental) The resource that represents the work to be executed. Either the ARN of a Lambda Function or Activity, or a special ARN.
        :param heartbeat: (experimental) Maximum time between heart beats. If the time between heart beats takes longer than this, a 'Timeout' error is raised. This is only relevant when using an Activity type as resource. Default: No heart beat timeout
        :param metric_dimensions: (experimental) The dimensions to attach to metrics. Default: No metrics
        :param metric_prefix_plural: (experimental) Prefix for plural metric names of activity actions. Default: No such metrics
        :param metric_prefix_singular: (experimental) Prefix for singular metric names of activity actions. Default: No such metrics
        :param parameters: (experimental) Parameters pass a collection of key-value pairs, either static values or JSONPath expressions that select from the input. The meaning of these parameters is task-dependent. Its values will be merged with the ``parameters`` property which is configured directly on the Task state. Default: No parameters
        :param policy_statements: (experimental) Additional policy statements to add to the execution role. Default: No policy roles

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "resource_arn": resource_arn,
        }
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if metric_dimensions is not None:
            self._values["metric_dimensions"] = metric_dimensions
        if metric_prefix_plural is not None:
            self._values["metric_prefix_plural"] = metric_prefix_plural
        if metric_prefix_singular is not None:
            self._values["metric_prefix_singular"] = metric_prefix_singular
        if parameters is not None:
            self._values["parameters"] = parameters
        if policy_statements is not None:
            self._values["policy_statements"] = policy_statements

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''(experimental) The resource that represents the work to be executed.

        Either the ARN of a Lambda Function or Activity, or a special
        ARN.

        :stability: experimental
        '''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def heartbeat(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Maximum time between heart beats.

        If the time between heart beats takes longer than this, a 'Timeout' error is raised.

        This is only relevant when using an Activity type as resource.

        :default: No heart beat timeout

        :stability: experimental
        '''
        result = self._values.get("heartbeat")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def metric_dimensions(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) The dimensions to attach to metrics.

        :default: No metrics

        :stability: experimental
        '''
        result = self._values.get("metric_dimensions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def metric_prefix_plural(self) -> typing.Optional[builtins.str]:
        '''(experimental) Prefix for plural metric names of activity actions.

        :default: No such metrics

        :stability: experimental
        '''
        result = self._values.get("metric_prefix_plural")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metric_prefix_singular(self) -> typing.Optional[builtins.str]:
        '''(experimental) Prefix for singular metric names of activity actions.

        :default: No such metrics

        :stability: experimental
        '''
        result = self._values.get("metric_prefix_singular")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Parameters pass a collection of key-value pairs, either static values or JSONPath expressions that select from the input.

        The meaning of these parameters is task-dependent.

        Its values will be merged with the ``parameters`` property which is configured directly
        on the Task state.

        :default: No parameters

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/input-output-inputpath-params.html#input-output-parameters
        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def policy_statements(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''(experimental) Additional policy statements to add to the execution role.

        :default: No policy roles

        :stability: experimental
        '''
        result = self._values.get("policy_statements")
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StepFunctionsTaskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Succeed(
    State,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_stepfunctions.Succeed",
):
    '''(experimental) Define a Succeed state in the state machine.

    Reaching a Succeed state terminates the state execution in success.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        comment: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param comment: (experimental) An optional description for this state. Default: No comment
        :param input_path: (experimental) JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: (experimental) JSONPath expression to select part of the state to be the output to this state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: $

        :stability: experimental
        '''
        props = SucceedProps(
            comment=comment, input_path=input_path, output_path=output_path
        )

        jsii.create(Succeed, self, [scope, id, props])

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        '''(experimental) Return the Amazon States Language object for this state.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toStateJson", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List[INextable]:
        '''(experimental) Continuable states of this Chainable.

        :stability: experimental
        '''
        return typing.cast(typing.List[INextable], jsii.get(self, "endStates"))


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.SucceedProps",
    jsii_struct_bases=[],
    name_mapping={
        "comment": "comment",
        "input_path": "inputPath",
        "output_path": "outputPath",
    },
)
class SucceedProps:
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for defining a Succeed state.

        :param comment: (experimental) An optional description for this state. Default: No comment
        :param input_path: (experimental) JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: (experimental) JSONPath expression to select part of the state to be the output to this state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: $

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if comment is not None:
            self._values["comment"] = comment
        if input_path is not None:
            self._values["input_path"] = input_path
        if output_path is not None:
            self._values["output_path"] = output_path

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''(experimental) An optional description for this state.

        :default: No comment

        :stability: experimental
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("input_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to select part of the state to be the output to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default: $

        :stability: experimental
        '''
        result = self._values.get("output_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SucceedProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(INextable)
class Task(State, metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_stepfunctions.Task"):
    '''(deprecated) Define a Task state in the state machine.

    Reaching a Task state causes some work to be executed, represented by the
    Task's resource property. Task constructs represent a generic Amazon
    States Language Task.

    For some resource types, more specific subclasses of Task may be available
    which are more convenient to use.

    :deprecated: - replaced by service integration specific classes (i.e. LambdaInvoke, SnsPublish)

    :stability: deprecated
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        task: IStepFunctionsTask,
        comment: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_Duration_070aa057] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param task: (deprecated) Actual task to be invoked in this workflow.
        :param comment: (deprecated) An optional description for this state. Default: No comment
        :param input_path: (deprecated) JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: (deprecated) JSONPath expression to select part of the state to be the output to this state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param parameters: (deprecated) Parameters to invoke the task with. It is not recommended to use this field. The object that is passed in the ``task`` property will take care of returning the right values for the ``Parameters`` field in the Step Functions definition. The various classes that implement ``IStepFunctionsTask`` will take a properties which make sense for the task type. For example, for ``InvokeFunction`` the field that populates the ``parameters`` field will be called ``payload``, and for the ``PublishToTopic`` the ``parameters`` field will be populated via a combination of the referenced topic, subject and message. If passed anyway, the keys in this map will override the parameters returned by the task object. Default: - Use the parameters implied by the ``task`` property
        :param result_path: (deprecated) JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: $
        :param timeout: (deprecated) Maximum run time of this state. If the state takes longer than this amount of time to complete, a 'Timeout' error is raised. Default: 60

        :stability: deprecated
        '''
        props = TaskProps(
            task=task,
            comment=comment,
            input_path=input_path,
            output_path=output_path,
            parameters=parameters,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(Task, self, [scope, id, props])

    @jsii.member(jsii_name="addCatch")
    def add_catch(
        self,
        handler: IChainable,
        *,
        errors: typing.Optional[typing.List[builtins.str]] = None,
        result_path: typing.Optional[builtins.str] = None,
    ) -> "Task":
        '''(deprecated) Add a recovery handler for this state.

        When a particular error occurs, execution will continue at the error
        handler instead of failing the state machine execution.

        :param handler: -
        :param errors: (experimental) Errors to recover from by going to the given state. A list of error strings to retry, which can be either predefined errors (for example Errors.NoChoiceMatched) or a self-defined error. Default: All errors
        :param result_path: (experimental) JSONPath expression to indicate where to inject the error data. May also be the special value DISCARD, which will cause the error data to be discarded. Default: $

        :stability: deprecated
        '''
        props = CatchProps(errors=errors, result_path=result_path)

        return typing.cast("Task", jsii.invoke(self, "addCatch", [handler, props]))

    @jsii.member(jsii_name="addRetry")
    def add_retry(
        self,
        *,
        backoff_rate: typing.Optional[jsii.Number] = None,
        errors: typing.Optional[typing.List[builtins.str]] = None,
        interval: typing.Optional[_Duration_070aa057] = None,
        max_attempts: typing.Optional[jsii.Number] = None,
    ) -> "Task":
        '''(deprecated) Add retry configuration for this state.

        This controls if and how the execution will be retried if a particular
        error occurs.

        :param backoff_rate: (experimental) Multiplication for how much longer the wait interval gets on every retry. Default: 2
        :param errors: (experimental) Errors to retry. A list of error strings to retry, which can be either predefined errors (for example Errors.NoChoiceMatched) or a self-defined error. Default: All errors
        :param interval: (experimental) How many seconds to wait initially before retrying. Default: Duration.seconds(1)
        :param max_attempts: (experimental) How many times to retry this particular error. May be 0 to disable retry for specific errors (in case you have a catch-all retry policy). Default: 3

        :stability: deprecated
        '''
        props = RetryProps(
            backoff_rate=backoff_rate,
            errors=errors,
            interval=interval,
            max_attempts=max_attempts,
        )

        return typing.cast("Task", jsii.invoke(self, "addRetry", [props]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(deprecated) Return the given named metric for this Task.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: sum over 5 minutes

        :stability: deprecated
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricFailed")
    def metric_failed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(deprecated) Metric for the number of times this activity fails.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: sum over 5 minutes

        :stability: deprecated
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricFailed", [props]))

    @jsii.member(jsii_name="metricHeartbeatTimedOut")
    def metric_heartbeat_timed_out(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(deprecated) Metric for the number of times the heartbeat times out for this activity.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: sum over 5 minutes

        :stability: deprecated
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricHeartbeatTimedOut", [props]))

    @jsii.member(jsii_name="metricRunTime")
    def metric_run_time(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(deprecated) The interval, in milliseconds, between the time the Task starts and the time it closes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: average over 5 minutes

        :stability: deprecated
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricRunTime", [props]))

    @jsii.member(jsii_name="metricScheduled")
    def metric_scheduled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(deprecated) Metric for the number of times this activity is scheduled.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: sum over 5 minutes

        :stability: deprecated
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricScheduled", [props]))

    @jsii.member(jsii_name="metricScheduleTime")
    def metric_schedule_time(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(deprecated) The interval, in milliseconds, for which the activity stays in the schedule state.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: average over 5 minutes

        :stability: deprecated
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricScheduleTime", [props]))

    @jsii.member(jsii_name="metricStarted")
    def metric_started(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(deprecated) Metric for the number of times this activity is started.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: sum over 5 minutes

        :stability: deprecated
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricStarted", [props]))

    @jsii.member(jsii_name="metricSucceeded")
    def metric_succeeded(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(deprecated) Metric for the number of times this activity succeeds.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: sum over 5 minutes

        :stability: deprecated
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSucceeded", [props]))

    @jsii.member(jsii_name="metricTime")
    def metric_time(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(deprecated) The interval, in milliseconds, between the time the activity is scheduled and the time it closes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: average over 5 minutes

        :stability: deprecated
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricTime", [props]))

    @jsii.member(jsii_name="metricTimedOut")
    def metric_timed_out(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(deprecated) Metric for the number of times this activity times out.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: sum over 5 minutes

        :stability: deprecated
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricTimedOut", [props]))

    @jsii.member(jsii_name="next")
    def next(self, next: IChainable) -> "Chain":
        '''(deprecated) Continue normal execution with the given state.

        :param next: -

        :stability: deprecated
        '''
        return typing.cast("Chain", jsii.invoke(self, "next", [next]))

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        '''(deprecated) Return the Amazon States Language object for this state.

        :stability: deprecated
        '''
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toStateJson", []))

    @jsii.member(jsii_name="whenBoundToGraph")
    def _when_bound_to_graph(self, graph: StateGraph) -> None:
        '''(deprecated) Called whenever this state is bound to a graph.

        Can be overridden by subclasses.

        :param graph: -

        :stability: deprecated
        '''
        return typing.cast(None, jsii.invoke(self, "whenBoundToGraph", [graph]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List[INextable]:
        '''(deprecated) Continuable states of this Chainable.

        :stability: deprecated
        '''
        return typing.cast(typing.List[INextable], jsii.get(self, "endStates"))


class TaskInput(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_stepfunctions.TaskInput",
):
    '''(experimental) Type union for task classes that accept multiple types of payload.

    :stability: experimental
    '''

    @jsii.member(jsii_name="fromContextAt") # type: ignore[misc]
    @builtins.classmethod
    def from_context_at(cls, path: builtins.str) -> "TaskInput":
        '''(experimental) Use a part of the task context as task input.

        Use this when you want to use a subobject or string from
        the current task context as complete payload
        to a task.

        :param path: -

        :stability: experimental
        '''
        return typing.cast("TaskInput", jsii.sinvoke(cls, "fromContextAt", [path]))

    @jsii.member(jsii_name="fromDataAt") # type: ignore[misc]
    @builtins.classmethod
    def from_data_at(cls, path: builtins.str) -> "TaskInput":
        '''(experimental) Use a part of the execution data as task input.

        Use this when you want to use a subobject or string from
        the current state machine execution as complete payload
        to a task.

        :param path: -

        :stability: experimental
        '''
        return typing.cast("TaskInput", jsii.sinvoke(cls, "fromDataAt", [path]))

    @jsii.member(jsii_name="fromJsonPathAt") # type: ignore[misc]
    @builtins.classmethod
    def from_json_path_at(cls, path: builtins.str) -> "TaskInput":
        '''(experimental) Use a part of the execution data or task context as task input.

        Use this when you want to use a subobject or string from
        the current state machine execution or the current task context
        as complete payload to a task.

        :param path: -

        :stability: experimental
        '''
        return typing.cast("TaskInput", jsii.sinvoke(cls, "fromJsonPathAt", [path]))

    @jsii.member(jsii_name="fromObject") # type: ignore[misc]
    @builtins.classmethod
    def from_object(cls, obj: typing.Mapping[builtins.str, typing.Any]) -> "TaskInput":
        '''(experimental) Use an object as task input.

        This object may contain Data and Context fields
        as object values, if desired.

        :param obj: -

        :stability: experimental
        '''
        return typing.cast("TaskInput", jsii.sinvoke(cls, "fromObject", [obj]))

    @jsii.member(jsii_name="fromText") # type: ignore[misc]
    @builtins.classmethod
    def from_text(cls, text: builtins.str) -> "TaskInput":
        '''(experimental) Use a literal string as task input.

        This might be a JSON-encoded object, or just a text.

        :param text: -

        :stability: experimental
        '''
        return typing.cast("TaskInput", jsii.sinvoke(cls, "fromText", [text]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> InputType:
        '''(experimental) type of task input.

        :stability: experimental
        '''
        return typing.cast(InputType, jsii.get(self, "type"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''(experimental) payload for the corresponding input type.

        It can be a JSON-encoded object, context, data, etc.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "value"))


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.TaskMetricsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "metric_dimensions": "metricDimensions",
        "metric_prefix_plural": "metricPrefixPlural",
        "metric_prefix_singular": "metricPrefixSingular",
    },
)
class TaskMetricsConfig:
    def __init__(
        self,
        *,
        metric_dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        metric_prefix_plural: typing.Optional[builtins.str] = None,
        metric_prefix_singular: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Task Metrics.

        :param metric_dimensions: (experimental) The dimensions to attach to metrics. Default: - No metrics
        :param metric_prefix_plural: (experimental) Prefix for plural metric names of activity actions. Default: - No such metrics
        :param metric_prefix_singular: (experimental) Prefix for singular metric names of activity actions. Default: - No such metrics

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if metric_dimensions is not None:
            self._values["metric_dimensions"] = metric_dimensions
        if metric_prefix_plural is not None:
            self._values["metric_prefix_plural"] = metric_prefix_plural
        if metric_prefix_singular is not None:
            self._values["metric_prefix_singular"] = metric_prefix_singular

    @builtins.property
    def metric_dimensions(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) The dimensions to attach to metrics.

        :default: - No metrics

        :stability: experimental
        '''
        result = self._values.get("metric_dimensions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def metric_prefix_plural(self) -> typing.Optional[builtins.str]:
        '''(experimental) Prefix for plural metric names of activity actions.

        :default: - No such metrics

        :stability: experimental
        '''
        result = self._values.get("metric_prefix_plural")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metric_prefix_singular(self) -> typing.Optional[builtins.str]:
        '''(experimental) Prefix for singular metric names of activity actions.

        :default: - No such metrics

        :stability: experimental
        '''
        result = self._values.get("metric_prefix_singular")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskMetricsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.TaskProps",
    jsii_struct_bases=[],
    name_mapping={
        "task": "task",
        "comment": "comment",
        "input_path": "inputPath",
        "output_path": "outputPath",
        "parameters": "parameters",
        "result_path": "resultPath",
        "timeout": "timeout",
    },
)
class TaskProps:
    def __init__(
        self,
        *,
        task: IStepFunctionsTask,
        comment: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_Duration_070aa057] = None,
    ) -> None:
        '''(deprecated) Props that are common to all tasks.

        :param task: (deprecated) Actual task to be invoked in this workflow.
        :param comment: (deprecated) An optional description for this state. Default: No comment
        :param input_path: (deprecated) JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: (deprecated) JSONPath expression to select part of the state to be the output to this state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param parameters: (deprecated) Parameters to invoke the task with. It is not recommended to use this field. The object that is passed in the ``task`` property will take care of returning the right values for the ``Parameters`` field in the Step Functions definition. The various classes that implement ``IStepFunctionsTask`` will take a properties which make sense for the task type. For example, for ``InvokeFunction`` the field that populates the ``parameters`` field will be called ``payload``, and for the ``PublishToTopic`` the ``parameters`` field will be populated via a combination of the referenced topic, subject and message. If passed anyway, the keys in this map will override the parameters returned by the task object. Default: - Use the parameters implied by the ``task`` property
        :param result_path: (deprecated) JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: $
        :param timeout: (deprecated) Maximum run time of this state. If the state takes longer than this amount of time to complete, a 'Timeout' error is raised. Default: 60

        :deprecated: - replaced by service integration specific classes (i.e. LambdaInvoke, SnsPublish)

        :stability: deprecated
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "task": task,
        }
        if comment is not None:
            self._values["comment"] = comment
        if input_path is not None:
            self._values["input_path"] = input_path
        if output_path is not None:
            self._values["output_path"] = output_path
        if parameters is not None:
            self._values["parameters"] = parameters
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def task(self) -> IStepFunctionsTask:
        '''(deprecated) Actual task to be invoked in this workflow.

        :stability: deprecated
        '''
        result = self._values.get("task")
        assert result is not None, "Required property 'task' is missing"
        return typing.cast(IStepFunctionsTask, result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''(deprecated) An optional description for this state.

        :default: No comment

        :stability: deprecated
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        '''(deprecated) JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: $

        :stability: deprecated
        '''
        result = self._values.get("input_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        '''(deprecated) JSONPath expression to select part of the state to be the output to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default: $

        :stability: deprecated
        '''
        result = self._values.get("output_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(deprecated) Parameters to invoke the task with.

        It is not recommended to use this field. The object that is passed in
        the ``task`` property will take care of returning the right values for the
        ``Parameters`` field in the Step Functions definition.

        The various classes that implement ``IStepFunctionsTask`` will take a
        properties which make sense for the task type. For example, for
        ``InvokeFunction`` the field that populates the ``parameters`` field will be
        called ``payload``, and for the ``PublishToTopic`` the ``parameters`` field
        will be populated via a combination of the referenced topic, subject and
        message.

        If passed anyway, the keys in this map will override the parameters
        returned by the task object.

        :default: - Use the parameters implied by the ``task`` property

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/input-output-inputpath-params.html#input-output-parameters
        :stability: deprecated
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        '''(deprecated) JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: $

        :stability: deprecated
        '''
        result = self._values.get("result_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_070aa057]:
        '''(deprecated) Maximum run time of this state.

        If the state takes longer than this amount of time to complete, a 'Timeout' error is raised.

        :default: 60

        :stability: deprecated
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(INextable)
class TaskStateBase(
    State,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_stepfunctions.TaskStateBase",
):
    '''(experimental) Define a Task state in the state machine.

    Reaching a Task state causes some work to be executed, represented by the
    Task's resource property. Task constructs represent a generic Amazon
    States Language Task.

    For some resource types, more specific subclasses of Task may be available
    which are more convenient to use.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_TaskStateBaseProxy"]:
        return _TaskStateBaseProxy

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[_Duration_070aa057] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_Duration_070aa057] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param comment: (experimental) An optional description for this state. Default: - No comment
        :param heartbeat: (experimental) Timeout for the heartbeat. Default: - None
        :param input_path: (experimental) JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: (experimental) AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: (experimental) JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: (experimental) JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: (experimental) Timeout for the state machine. Default: - None

        :stability: experimental
        '''
        props = TaskStateBaseProps(
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(TaskStateBase, self, [scope, id, props])

    @jsii.member(jsii_name="addCatch")
    def add_catch(
        self,
        handler: IChainable,
        *,
        errors: typing.Optional[typing.List[builtins.str]] = None,
        result_path: typing.Optional[builtins.str] = None,
    ) -> "TaskStateBase":
        '''(experimental) Add a recovery handler for this state.

        When a particular error occurs, execution will continue at the error
        handler instead of failing the state machine execution.

        :param handler: -
        :param errors: (experimental) Errors to recover from by going to the given state. A list of error strings to retry, which can be either predefined errors (for example Errors.NoChoiceMatched) or a self-defined error. Default: All errors
        :param result_path: (experimental) JSONPath expression to indicate where to inject the error data. May also be the special value DISCARD, which will cause the error data to be discarded. Default: $

        :stability: experimental
        '''
        props = CatchProps(errors=errors, result_path=result_path)

        return typing.cast("TaskStateBase", jsii.invoke(self, "addCatch", [handler, props]))

    @jsii.member(jsii_name="addRetry")
    def add_retry(
        self,
        *,
        backoff_rate: typing.Optional[jsii.Number] = None,
        errors: typing.Optional[typing.List[builtins.str]] = None,
        interval: typing.Optional[_Duration_070aa057] = None,
        max_attempts: typing.Optional[jsii.Number] = None,
    ) -> "TaskStateBase":
        '''(experimental) Add retry configuration for this state.

        This controls if and how the execution will be retried if a particular
        error occurs.

        :param backoff_rate: (experimental) Multiplication for how much longer the wait interval gets on every retry. Default: 2
        :param errors: (experimental) Errors to retry. A list of error strings to retry, which can be either predefined errors (for example Errors.NoChoiceMatched) or a self-defined error. Default: All errors
        :param interval: (experimental) How many seconds to wait initially before retrying. Default: Duration.seconds(1)
        :param max_attempts: (experimental) How many times to retry this particular error. May be 0 to disable retry for specific errors (in case you have a catch-all retry policy). Default: 3

        :stability: experimental
        '''
        props = RetryProps(
            backoff_rate=backoff_rate,
            errors=errors,
            interval=interval,
            max_attempts=max_attempts,
        )

        return typing.cast("TaskStateBase", jsii.invoke(self, "addRetry", [props]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Return the given named metric for this Task.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricFailed")
    def metric_failed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of times this activity fails.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricFailed", [props]))

    @jsii.member(jsii_name="metricHeartbeatTimedOut")
    def metric_heartbeat_timed_out(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of times the heartbeat times out for this activity.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricHeartbeatTimedOut", [props]))

    @jsii.member(jsii_name="metricRunTime")
    def metric_run_time(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The interval, in milliseconds, between the time the Task starts and the time it closes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricRunTime", [props]))

    @jsii.member(jsii_name="metricScheduled")
    def metric_scheduled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of times this activity is scheduled.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricScheduled", [props]))

    @jsii.member(jsii_name="metricScheduleTime")
    def metric_schedule_time(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The interval, in milliseconds, for which the activity stays in the schedule state.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricScheduleTime", [props]))

    @jsii.member(jsii_name="metricStarted")
    def metric_started(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of times this activity is started.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricStarted", [props]))

    @jsii.member(jsii_name="metricSucceeded")
    def metric_succeeded(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of times this activity succeeds.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSucceeded", [props]))

    @jsii.member(jsii_name="metricTime")
    def metric_time(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The interval, in milliseconds, between the time the activity is scheduled and the time it closes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricTime", [props]))

    @jsii.member(jsii_name="metricTimedOut")
    def metric_timed_out(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of times this activity times out.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricTimedOut", [props]))

    @jsii.member(jsii_name="next")
    def next(self, next: IChainable) -> "Chain":
        '''(experimental) Continue normal execution with the given state.

        :param next: -

        :stability: experimental
        '''
        return typing.cast("Chain", jsii.invoke(self, "next", [next]))

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        '''(experimental) Return the Amazon States Language object for this state.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toStateJson", []))

    @jsii.member(jsii_name="whenBoundToGraph")
    def _when_bound_to_graph(self, graph: StateGraph) -> None:
        '''(experimental) Called whenever this state is bound to a graph.

        Can be overridden by subclasses.

        :param graph: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "whenBoundToGraph", [graph]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List[INextable]:
        '''(experimental) Continuable states of this Chainable.

        :stability: experimental
        '''
        return typing.cast(typing.List[INextable], jsii.get(self, "endStates"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="taskMetrics")
    @abc.abstractmethod
    def _task_metrics(self) -> typing.Optional[TaskMetricsConfig]:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="taskPolicies")
    @abc.abstractmethod
    def _task_policies(self) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''
        :stability: experimental
        '''
        ...


class _TaskStateBaseProxy(
    TaskStateBase, jsii.proxy_for(State) # type: ignore[misc]
):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(self) -> typing.Optional[TaskMetricsConfig]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[TaskMetricsConfig], jsii.get(self, "taskMetrics"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(self) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], jsii.get(self, "taskPolicies"))


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.TaskStateBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
    },
)
class TaskStateBaseProps:
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[_Duration_070aa057] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_Duration_070aa057] = None,
    ) -> None:
        '''(experimental) Props that are common to all tasks.

        :param comment: (experimental) An optional description for this state. Default: - No comment
        :param heartbeat: (experimental) Timeout for the heartbeat. Default: - None
        :param input_path: (experimental) JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: (experimental) AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: (experimental) JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: (experimental) JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: (experimental) Timeout for the state machine. Default: - None

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''(experimental) An optional description for this state.

        :default: - No comment

        :stability: experimental
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def heartbeat(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Timeout for the heartbeat.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("heartbeat")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')

        :stability: experimental
        '''
        result = self._values.get("input_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integration_pattern(self) -> typing.Optional[IntegrationPattern]:
        '''(experimental) AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        :stability: experimental
        '''
        result = self._values.get("integration_pattern")
        return typing.cast(typing.Optional[IntegrationPattern], result)

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')

        :stability: experimental
        '''
        result = self._values.get("output_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')

        :stability: experimental
        '''
        result = self._values.get("result_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Timeout for the state machine.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskStateBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(INextable)
class Wait(State, metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_stepfunctions.Wait"):
    '''(experimental) Define a Wait state in the state machine.

    A Wait state can be used to delay execution of the state machine for a while.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        time: "WaitTime",
        comment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param time: (experimental) Wait duration.
        :param comment: (experimental) An optional description for this state. Default: No comment

        :stability: experimental
        '''
        props = WaitProps(time=time, comment=comment)

        jsii.create(Wait, self, [scope, id, props])

    @jsii.member(jsii_name="next")
    def next(self, next: IChainable) -> "Chain":
        '''(experimental) Continue normal execution with the given state.

        :param next: -

        :stability: experimental
        '''
        return typing.cast("Chain", jsii.invoke(self, "next", [next]))

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        '''(experimental) Return the Amazon States Language object for this state.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toStateJson", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List[INextable]:
        '''(experimental) Continuable states of this Chainable.

        :stability: experimental
        '''
        return typing.cast(typing.List[INextable], jsii.get(self, "endStates"))


@jsii.data_type(
    jsii_type="monocdk.aws_stepfunctions.WaitProps",
    jsii_struct_bases=[],
    name_mapping={"time": "time", "comment": "comment"},
)
class WaitProps:
    def __init__(
        self,
        *,
        time: "WaitTime",
        comment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for defining a Wait state.

        :param time: (experimental) Wait duration.
        :param comment: (experimental) An optional description for this state. Default: No comment

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "time": time,
        }
        if comment is not None:
            self._values["comment"] = comment

    @builtins.property
    def time(self) -> "WaitTime":
        '''(experimental) Wait duration.

        :stability: experimental
        '''
        result = self._values.get("time")
        assert result is not None, "Required property 'time' is missing"
        return typing.cast("WaitTime", result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''(experimental) An optional description for this state.

        :default: No comment

        :stability: experimental
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WaitProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WaitTime(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_stepfunctions.WaitTime"):
    '''(experimental) Represents the Wait state which delays a state machine from continuing for a specified time.

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-wait-state.html
    :stability: experimental
    '''

    @jsii.member(jsii_name="duration") # type: ignore[misc]
    @builtins.classmethod
    def duration(cls, duration: _Duration_070aa057) -> "WaitTime":
        '''(experimental) Wait a fixed amount of time.

        :param duration: -

        :stability: experimental
        '''
        return typing.cast("WaitTime", jsii.sinvoke(cls, "duration", [duration]))

    @jsii.member(jsii_name="secondsPath") # type: ignore[misc]
    @builtins.classmethod
    def seconds_path(cls, path: builtins.str) -> "WaitTime":
        '''(experimental) Wait for a number of seconds stored in the state object.

        :param path: -

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            $.wait_seconds
        '''
        return typing.cast("WaitTime", jsii.sinvoke(cls, "secondsPath", [path]))

    @jsii.member(jsii_name="timestamp") # type: ignore[misc]
    @builtins.classmethod
    def timestamp(cls, timestamp: builtins.str) -> "WaitTime":
        '''(experimental) Wait until the given ISO8601 timestamp.

        :param timestamp: -

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            2016 - 03 - 14T01:5900Z
        '''
        return typing.cast("WaitTime", jsii.sinvoke(cls, "timestamp", [timestamp]))

    @jsii.member(jsii_name="timestampPath") # type: ignore[misc]
    @builtins.classmethod
    def timestamp_path(cls, path: builtins.str) -> "WaitTime":
        '''(experimental) Wait until a timestamp found in the state object.

        :param path: -

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            $.wait_timestamp
        '''
        return typing.cast("WaitTime", jsii.sinvoke(cls, "timestampPath", [path]))


@jsii.implements(IActivity)
class Activity(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_stepfunctions.Activity",
):
    '''(experimental) Define a new Step Functions Activity.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        activity_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param activity_name: (experimental) The name for this activity. Default: - If not supplied, a name is generated

        :stability: experimental
        '''
        props = ActivityProps(activity_name=activity_name)

        jsii.create(Activity, self, [scope, id, props])

    @jsii.member(jsii_name="fromActivityArn") # type: ignore[misc]
    @builtins.classmethod
    def from_activity_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        activity_arn: builtins.str,
    ) -> IActivity:
        '''(experimental) Construct an Activity from an existing Activity ARN.

        :param scope: -
        :param id: -
        :param activity_arn: -

        :stability: experimental
        '''
        return typing.cast(IActivity, jsii.sinvoke(cls, "fromActivityArn", [scope, id, activity_arn]))

    @jsii.member(jsii_name="fromActivityName") # type: ignore[misc]
    @builtins.classmethod
    def from_activity_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        activity_name: builtins.str,
    ) -> IActivity:
        '''(experimental) Construct an Activity from an existing Activity Name.

        :param scope: -
        :param id: -
        :param activity_name: -

        :stability: experimental
        '''
        return typing.cast(IActivity, jsii.sinvoke(cls, "fromActivityName", [scope, id, activity_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        identity: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity permissions on this Activity.

        :param identity: The principal.
        :param actions: The list of desired actions.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [identity, *actions]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Return the given named metric for this Activity.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricFailed")
    def metric_failed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of times this activity fails.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricFailed", [props]))

    @jsii.member(jsii_name="metricHeartbeatTimedOut")
    def metric_heartbeat_timed_out(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of times the heartbeat times out for this activity.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricHeartbeatTimedOut", [props]))

    @jsii.member(jsii_name="metricRunTime")
    def metric_run_time(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The interval, in milliseconds, between the time the activity starts and the time it closes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricRunTime", [props]))

    @jsii.member(jsii_name="metricScheduled")
    def metric_scheduled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of times this activity is scheduled.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricScheduled", [props]))

    @jsii.member(jsii_name="metricScheduleTime")
    def metric_schedule_time(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The interval, in milliseconds, for which the activity stays in the schedule state.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricScheduleTime", [props]))

    @jsii.member(jsii_name="metricStarted")
    def metric_started(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of times this activity is started.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricStarted", [props]))

    @jsii.member(jsii_name="metricSucceeded")
    def metric_succeeded(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of times this activity succeeds.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSucceeded", [props]))

    @jsii.member(jsii_name="metricTime")
    def metric_time(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) The interval, in milliseconds, between the time the activity is scheduled and the time it closes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricTime", [props]))

    @jsii.member(jsii_name="metricTimedOut")
    def metric_timed_out(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of times this activity times out.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricTimedOut", [props]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="activityArn")
    def activity_arn(self) -> builtins.str:
        '''(experimental) The ARN of the activity.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "activityArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="activityName")
    def activity_name(self) -> builtins.str:
        '''(experimental) The name of the activity.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "activityName"))


@jsii.implements(IChainable)
class Chain(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_stepfunctions.Chain"):
    '''(experimental) A collection of states to chain onto.

    A Chain has a start and zero or more chainable ends. If there are
    zero ends, calling next() on the Chain will fail.

    :stability: experimental
    '''

    @jsii.member(jsii_name="custom") # type: ignore[misc]
    @builtins.classmethod
    def custom(
        cls,
        start_state: State,
        end_states: typing.List[INextable],
        last_added: IChainable,
    ) -> "Chain":
        '''(experimental) Make a Chain with specific start and end states, and a last-added Chainable.

        :param start_state: -
        :param end_states: -
        :param last_added: -

        :stability: experimental
        '''
        return typing.cast("Chain", jsii.sinvoke(cls, "custom", [start_state, end_states, last_added]))

    @jsii.member(jsii_name="sequence") # type: ignore[misc]
    @builtins.classmethod
    def sequence(cls, start: IChainable, next: IChainable) -> "Chain":
        '''(experimental) Make a Chain with the start from one chain and the ends from another.

        :param start: -
        :param next: -

        :stability: experimental
        '''
        return typing.cast("Chain", jsii.sinvoke(cls, "sequence", [start, next]))

    @jsii.member(jsii_name="start") # type: ignore[misc]
    @builtins.classmethod
    def start(cls, state: IChainable) -> "Chain":
        '''(experimental) Begin a new Chain from one chainable.

        :param state: -

        :stability: experimental
        '''
        return typing.cast("Chain", jsii.sinvoke(cls, "start", [state]))

    @jsii.member(jsii_name="next")
    def next(self, next: IChainable) -> "Chain":
        '''(experimental) Continue normal execution with the given state.

        :param next: -

        :stability: experimental
        '''
        return typing.cast("Chain", jsii.invoke(self, "next", [next]))

    @jsii.member(jsii_name="toSingleState")
    def to_single_state(
        self,
        id: builtins.str,
        *,
        comment: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
    ) -> "Parallel":
        '''(experimental) Return a single state that encompasses all states in the chain.

        This can be used to add error handling to a sequence of states.

        Be aware that this changes the result of the inner state machine
        to be an array with the result of the state machine in it. Adjust
        your paths accordingly. For example, change 'outputPath' to
        '$[0]'.

        :param id: -
        :param comment: (experimental) An optional description for this state. Default: No comment
        :param input_path: (experimental) JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: (experimental) JSONPath expression to select part of the state to be the output to this state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param result_path: (experimental) JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: $

        :stability: experimental
        '''
        props = ParallelProps(
            comment=comment,
            input_path=input_path,
            output_path=output_path,
            result_path=result_path,
        )

        return typing.cast("Parallel", jsii.invoke(self, "toSingleState", [id, props]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List[INextable]:
        '''(experimental) The chainable end state(s) of this chain.

        :stability: experimental
        '''
        return typing.cast(typing.List[INextable], jsii.get(self, "endStates"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) Identify this Chain.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="startState")
    def start_state(self) -> State:
        '''(experimental) The start state of this chain.

        :stability: experimental
        '''
        return typing.cast(State, jsii.get(self, "startState"))


class Choice(
    State,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_stepfunctions.Choice",
):
    '''(experimental) Define a Choice in the state machine.

    A choice state can be used to make decisions based on the execution
    state.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        comment: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param comment: (experimental) An optional description for this state. Default: No comment
        :param input_path: (experimental) JSONPath expression to select part of the state to be the input to this state. May also be the special value DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: (experimental) JSONPath expression to select part of the state to be the output to this state. May also be the special value DISCARD, which will cause the effective output to be the empty object {}. Default: $

        :stability: experimental
        '''
        props = ChoiceProps(
            comment=comment, input_path=input_path, output_path=output_path
        )

        jsii.create(Choice, self, [scope, id, props])

    @jsii.member(jsii_name="afterwards")
    def afterwards(
        self,
        *,
        include_error_handlers: typing.Optional[builtins.bool] = None,
        include_otherwise: typing.Optional[builtins.bool] = None,
    ) -> Chain:
        '''(experimental) Return a Chain that contains all reachable end states from this Choice.

        Use this to combine all possible choice paths back.

        :param include_error_handlers: (experimental) Whether to include error handling states. If this is true, all states which are error handlers (added through 'onError') and states reachable via error handlers will be included as well. Default: false
        :param include_otherwise: (experimental) Whether to include the default/otherwise transition for the current Choice state. If this is true and the current Choice does not have a default outgoing transition, one will be added included when .next() is called on the chain. Default: false

        :stability: experimental
        '''
        options = AfterwardsOptions(
            include_error_handlers=include_error_handlers,
            include_otherwise=include_otherwise,
        )

        return typing.cast(Chain, jsii.invoke(self, "afterwards", [options]))

    @jsii.member(jsii_name="otherwise")
    def otherwise(self, def_: IChainable) -> "Choice":
        '''(experimental) If none of the given conditions match, continue execution with the given state.

        If no conditions match and no otherwise() has been given, an execution
        error will be raised.

        :param def_: -

        :stability: experimental
        '''
        return typing.cast("Choice", jsii.invoke(self, "otherwise", [def_]))

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        '''(experimental) Return the Amazon States Language object for this state.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toStateJson", []))

    @jsii.member(jsii_name="when")
    def when(self, condition: Condition, next: IChainable) -> "Choice":
        '''(experimental) If the given condition matches, continue execution with the given state.

        :param condition: -
        :param next: -

        :stability: experimental
        '''
        return typing.cast("Choice", jsii.invoke(self, "when", [condition, next]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List[INextable]:
        '''(experimental) Continuable states of this Chainable.

        :stability: experimental
        '''
        return typing.cast(typing.List[INextable], jsii.get(self, "endStates"))


@jsii.implements(IChainable, INextable)
class CustomState(
    State,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_stepfunctions.CustomState",
):
    '''(experimental) State defined by supplying Amazon States Language (ASL) in the state machine.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        state_json: typing.Mapping[builtins.str, typing.Any],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param state_json: (experimental) Amazon States Language (JSON-based) definition of the state.

        :stability: experimental
        '''
        props = CustomStateProps(state_json=state_json)

        jsii.create(CustomState, self, [scope, id, props])

    @jsii.member(jsii_name="next")
    def next(self, next: IChainable) -> Chain:
        '''(experimental) Continue normal execution with the given state.

        :param next: -

        :stability: experimental
        '''
        return typing.cast(Chain, jsii.invoke(self, "next", [next]))

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        '''(experimental) Returns the Amazon States Language object for this state.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toStateJson", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List[INextable]:
        '''(experimental) Continuable states of this Chainable.

        :stability: experimental
        '''
        return typing.cast(typing.List[INextable], jsii.get(self, "endStates"))


class Fail(State, metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_stepfunctions.Fail"):
    '''(experimental) Define a Fail state in the state machine.

    Reaching a Fail state terminates the state execution in failure.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cause: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        error: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cause: (experimental) A description for the cause of the failure. Default: No description
        :param comment: (experimental) An optional description for this state. Default: No comment
        :param error: (experimental) Error code used to represent this failure. Default: No error code

        :stability: experimental
        '''
        props = FailProps(cause=cause, comment=comment, error=error)

        jsii.create(Fail, self, [scope, id, props])

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        '''(experimental) Return the Amazon States Language object for this state.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toStateJson", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List[INextable]:
        '''(experimental) Continuable states of this Chainable.

        :stability: experimental
        '''
        return typing.cast(typing.List[INextable], jsii.get(self, "endStates"))


@jsii.implements(INextable)
class Map(State, metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_stepfunctions.Map"):
    '''(experimental) Define a Map state in the state machine.

    A ``Map`` state can be used to run a set of steps for each element of an input array.
    A Map state will execute the same steps for multiple entries of an array in the state input.

    While the Parallel state executes multiple branches of steps using the same input, a Map state
    will execute the same steps for multiple entries of an array in the state input.

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-map-state.html
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        comment: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        items_path: typing.Optional[builtins.str] = None,
        max_concurrency: typing.Optional[jsii.Number] = None,
        output_path: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        result_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param comment: (experimental) An optional description for this state. Default: No comment
        :param input_path: (experimental) JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param items_path: (experimental) JSONPath expression to select the array to iterate over. Default: $
        :param max_concurrency: (experimental) MaxConcurrency. An upper bound on the number of iterations you want running at once. Default: - full concurrency
        :param output_path: (experimental) JSONPath expression to select part of the state to be the output to this state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param parameters: (experimental) The JSON that you want to override your default iteration input. Default: $
        :param result_path: (experimental) JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: $

        :stability: experimental
        '''
        props = MapProps(
            comment=comment,
            input_path=input_path,
            items_path=items_path,
            max_concurrency=max_concurrency,
            output_path=output_path,
            parameters=parameters,
            result_path=result_path,
        )

        jsii.create(Map, self, [scope, id, props])

    @jsii.member(jsii_name="addCatch")
    def add_catch(
        self,
        handler: IChainable,
        *,
        errors: typing.Optional[typing.List[builtins.str]] = None,
        result_path: typing.Optional[builtins.str] = None,
    ) -> "Map":
        '''(experimental) Add a recovery handler for this state.

        When a particular error occurs, execution will continue at the error
        handler instead of failing the state machine execution.

        :param handler: -
        :param errors: (experimental) Errors to recover from by going to the given state. A list of error strings to retry, which can be either predefined errors (for example Errors.NoChoiceMatched) or a self-defined error. Default: All errors
        :param result_path: (experimental) JSONPath expression to indicate where to inject the error data. May also be the special value DISCARD, which will cause the error data to be discarded. Default: $

        :stability: experimental
        '''
        props = CatchProps(errors=errors, result_path=result_path)

        return typing.cast("Map", jsii.invoke(self, "addCatch", [handler, props]))

    @jsii.member(jsii_name="addRetry")
    def add_retry(
        self,
        *,
        backoff_rate: typing.Optional[jsii.Number] = None,
        errors: typing.Optional[typing.List[builtins.str]] = None,
        interval: typing.Optional[_Duration_070aa057] = None,
        max_attempts: typing.Optional[jsii.Number] = None,
    ) -> "Map":
        '''(experimental) Add retry configuration for this state.

        This controls if and how the execution will be retried if a particular
        error occurs.

        :param backoff_rate: (experimental) Multiplication for how much longer the wait interval gets on every retry. Default: 2
        :param errors: (experimental) Errors to retry. A list of error strings to retry, which can be either predefined errors (for example Errors.NoChoiceMatched) or a self-defined error. Default: All errors
        :param interval: (experimental) How many seconds to wait initially before retrying. Default: Duration.seconds(1)
        :param max_attempts: (experimental) How many times to retry this particular error. May be 0 to disable retry for specific errors (in case you have a catch-all retry policy). Default: 3

        :stability: experimental
        '''
        props = RetryProps(
            backoff_rate=backoff_rate,
            errors=errors,
            interval=interval,
            max_attempts=max_attempts,
        )

        return typing.cast("Map", jsii.invoke(self, "addRetry", [props]))

    @jsii.member(jsii_name="iterator")
    def iterator(self, iterator: IChainable) -> "Map":
        '''(experimental) Define iterator state machine in Map.

        :param iterator: -

        :stability: experimental
        '''
        return typing.cast("Map", jsii.invoke(self, "iterator", [iterator]))

    @jsii.member(jsii_name="next")
    def next(self, next: IChainable) -> Chain:
        '''(experimental) Continue normal execution with the given state.

        :param next: -

        :stability: experimental
        '''
        return typing.cast(Chain, jsii.invoke(self, "next", [next]))

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        '''(experimental) Return the Amazon States Language object for this state.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toStateJson", []))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validate this state.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List[INextable]:
        '''(experimental) Continuable states of this Chainable.

        :stability: experimental
        '''
        return typing.cast(typing.List[INextable], jsii.get(self, "endStates"))


@jsii.implements(INextable)
class Parallel(
    State,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_stepfunctions.Parallel",
):
    '''(experimental) Define a Parallel state in the state machine.

    A Parallel state can be used to run one or more state machines at the same
    time.

    The Result of a Parallel state is an array of the results of its substatemachines.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        comment: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param comment: (experimental) An optional description for this state. Default: No comment
        :param input_path: (experimental) JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: (experimental) JSONPath expression to select part of the state to be the output to this state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param result_path: (experimental) JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: $

        :stability: experimental
        '''
        props = ParallelProps(
            comment=comment,
            input_path=input_path,
            output_path=output_path,
            result_path=result_path,
        )

        jsii.create(Parallel, self, [scope, id, props])

    @jsii.member(jsii_name="addCatch")
    def add_catch(
        self,
        handler: IChainable,
        *,
        errors: typing.Optional[typing.List[builtins.str]] = None,
        result_path: typing.Optional[builtins.str] = None,
    ) -> "Parallel":
        '''(experimental) Add a recovery handler for this state.

        When a particular error occurs, execution will continue at the error
        handler instead of failing the state machine execution.

        :param handler: -
        :param errors: (experimental) Errors to recover from by going to the given state. A list of error strings to retry, which can be either predefined errors (for example Errors.NoChoiceMatched) or a self-defined error. Default: All errors
        :param result_path: (experimental) JSONPath expression to indicate where to inject the error data. May also be the special value DISCARD, which will cause the error data to be discarded. Default: $

        :stability: experimental
        '''
        props = CatchProps(errors=errors, result_path=result_path)

        return typing.cast("Parallel", jsii.invoke(self, "addCatch", [handler, props]))

    @jsii.member(jsii_name="addRetry")
    def add_retry(
        self,
        *,
        backoff_rate: typing.Optional[jsii.Number] = None,
        errors: typing.Optional[typing.List[builtins.str]] = None,
        interval: typing.Optional[_Duration_070aa057] = None,
        max_attempts: typing.Optional[jsii.Number] = None,
    ) -> "Parallel":
        '''(experimental) Add retry configuration for this state.

        This controls if and how the execution will be retried if a particular
        error occurs.

        :param backoff_rate: (experimental) Multiplication for how much longer the wait interval gets on every retry. Default: 2
        :param errors: (experimental) Errors to retry. A list of error strings to retry, which can be either predefined errors (for example Errors.NoChoiceMatched) or a self-defined error. Default: All errors
        :param interval: (experimental) How many seconds to wait initially before retrying. Default: Duration.seconds(1)
        :param max_attempts: (experimental) How many times to retry this particular error. May be 0 to disable retry for specific errors (in case you have a catch-all retry policy). Default: 3

        :stability: experimental
        '''
        props = RetryProps(
            backoff_rate=backoff_rate,
            errors=errors,
            interval=interval,
            max_attempts=max_attempts,
        )

        return typing.cast("Parallel", jsii.invoke(self, "addRetry", [props]))

    @jsii.member(jsii_name="branch")
    def branch(self, *branches: IChainable) -> "Parallel":
        '''(experimental) Define one or more branches to run in parallel.

        :param branches: -

        :stability: experimental
        '''
        return typing.cast("Parallel", jsii.invoke(self, "branch", [*branches]))

    @jsii.member(jsii_name="next")
    def next(self, next: IChainable) -> Chain:
        '''(experimental) Continue normal execution with the given state.

        :param next: -

        :stability: experimental
        '''
        return typing.cast(Chain, jsii.invoke(self, "next", [next]))

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        '''(experimental) Return the Amazon States Language object for this state.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toStateJson", []))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validate this state.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List[INextable]:
        '''(experimental) Continuable states of this Chainable.

        :stability: experimental
        '''
        return typing.cast(typing.List[INextable], jsii.get(self, "endStates"))


@jsii.implements(INextable)
class Pass(State, metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_stepfunctions.Pass"):
    '''(experimental) Define a Pass in the state machine.

    A Pass state can be used to transform the current exeuction's state.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        comment: typing.Optional[builtins.str] = None,
        input_path: typing.Optional[builtins.str] = None,
        output_path: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        result: typing.Optional[Result] = None,
        result_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param comment: (experimental) An optional description for this state. Default: No comment
        :param input_path: (experimental) JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: $
        :param output_path: (experimental) JSONPath expression to select part of the state to be the output to this state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: $
        :param parameters: (experimental) Parameters pass a collection of key-value pairs, either static values or JSONPath expressions that select from the input. Default: No parameters
        :param result: (experimental) If given, treat as the result of this operation. Can be used to inject or replace the current execution state. Default: No injected result
        :param result_path: (experimental) JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: $

        :stability: experimental
        '''
        props = PassProps(
            comment=comment,
            input_path=input_path,
            output_path=output_path,
            parameters=parameters,
            result=result,
            result_path=result_path,
        )

        jsii.create(Pass, self, [scope, id, props])

    @jsii.member(jsii_name="next")
    def next(self, next: IChainable) -> Chain:
        '''(experimental) Continue normal execution with the given state.

        :param next: -

        :stability: experimental
        '''
        return typing.cast(Chain, jsii.invoke(self, "next", [next]))

    @jsii.member(jsii_name="toStateJson")
    def to_state_json(self) -> typing.Mapping[typing.Any, typing.Any]:
        '''(experimental) Return the Amazon States Language object for this state.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toStateJson", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List[INextable]:
        '''(experimental) Continuable states of this Chainable.

        :stability: experimental
        '''
        return typing.cast(typing.List[INextable], jsii.get(self, "endStates"))


__all__ = [
    "Activity",
    "ActivityProps",
    "AfterwardsOptions",
    "CatchProps",
    "CfnActivity",
    "CfnActivityProps",
    "CfnStateMachine",
    "CfnStateMachineProps",
    "Chain",
    "Choice",
    "ChoiceProps",
    "Condition",
    "Context",
    "CustomState",
    "CustomStateProps",
    "Data",
    "Errors",
    "Fail",
    "FailProps",
    "FieldUtils",
    "FindStateOptions",
    "IActivity",
    "IChainable",
    "INextable",
    "IStateMachine",
    "IStepFunctionsTask",
    "InputType",
    "IntegrationPattern",
    "JsonPath",
    "LogLevel",
    "LogOptions",
    "Map",
    "MapProps",
    "Parallel",
    "ParallelProps",
    "Pass",
    "PassProps",
    "Result",
    "RetryProps",
    "ServiceIntegrationPattern",
    "SingleStateOptions",
    "State",
    "StateGraph",
    "StateMachine",
    "StateMachineFragment",
    "StateMachineProps",
    "StateMachineType",
    "StateProps",
    "StateTransitionMetric",
    "StepFunctionsTaskConfig",
    "Succeed",
    "SucceedProps",
    "Task",
    "TaskInput",
    "TaskMetricsConfig",
    "TaskProps",
    "TaskStateBase",
    "TaskStateBaseProps",
    "Wait",
    "WaitProps",
    "WaitTime",
]

publication.publish()
