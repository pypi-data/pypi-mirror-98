'''
[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-codepipeline-slack

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-codepipeline-slack)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-codepipeline-slack/)
[![Mentioned in Awesome CDK](https://awesome.re/mentioned-badge.svg)](https://github.com/kolomied/awesome-cdk)

> Cdk component that provisions a #slack approval workflow and notification messages on codepipeline state changes

![Approval Workflow](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/packages/cdk-codepipeline-slack/assets/approval_workflow.png)

![Review Dialog](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/packages/cdk-codepipeline-slack/assets/review_dialog.png)

## Install

TypeScript/JavaScript:

```bash
npm install --save @cloudcomponents/cdk-codepipeline-slack
```

Python:

```bash
pip install cloudcomponents.cdk-codepipeline-slack
```

## How to use

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Construct, Stack, StackProps
from aws_cdk.aws_codecommit import Repository
from aws_cdk.aws_codepipeline import Pipeline, Artifact
from aws_cdk.aws_codepipeline_actions import CodeCommitSourceAction, CodeBuildAction
from aws_cdk.aws_codebuild import PipelineProject

from cloudcomponents.cdk_codepipeline_slack import SlackApprovalAction, SlackNotifier

class CodePipelineSlackApprovalStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        repository = Repository(self, "Repository",
            repository_name="MyRepositoryName"
        )

        source_artifact = Artifact()

        source_action = CodeCommitSourceAction(
            action_name="CodeCommit",
            repository=repository,
            output=source_artifact
        )

        project = PipelineProject(self, "MyProject")

        build_action = CodeBuildAction(
            action_name="CodeBuild",
            project=project,
            input=source_artifact
        )

        slack_bot_token = process.env.SLACK_BOT_TOKEN
        slack_signing_secret = process.env.SLACK_SIGNING_SECRET
        slack_channel = process.env.SLACK_CHANNEL_NAME

        approval_action = SlackApprovalAction(
            action_name="SlackApproval",
            slack_bot_token=slack_bot_token,
            slack_signing_secret=slack_signing_secret,
            slack_channel=slack_channel,
            external_entity_link="http://cloudcomponents.org",
            additional_information="Would you like to promote the build to production?"
        )

        pipeline = Pipeline(self, "MyPipeline",
            pipeline_name="MyPipeline",
            stages=[StageProps(
                stage_name="Source",
                actions=[source_action]
            ), StageProps(
                stage_name="Build",
                actions=[build_action]
            ), StageProps(
                stage_name="Approval",
                actions=[approval_action]
            )
            ]
        )

        SlackNotifier(self, "SlackNotifier",
            pipeline=pipeline,
            slack_bot_token=slack_bot_token,
            slack_signing_secret=slack_signing_secret,
            slack_channel=slack_channel
        )
```

## Slack App Settings

Create an app that’s just for your workspace

### OAuth & Permissions

Grant the `channels::history`-Scope to the Bot in your app and Add the Bot to the configured Slack-Channel

Select Permission Scopes:

![OAuth Scopes](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/packages/cdk-codepipeline-slack/assets/oauth_scope.png)

### Interactive Components

Enter the url of your api from the AWS Api Gateway and append `/slack/actions`:

![Interactive Components](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/packages/cdk-codepipeline-slack/assets/interactive_components.png)

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-codepipeline-slack/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-codepipeline-slack/LICENSE)
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

import aws_cdk.aws_codepipeline
import aws_cdk.aws_codepipeline_actions
import aws_cdk.aws_iam
import aws_cdk.aws_s3
import aws_cdk.core


@jsii.enum(jsii_type="@cloudcomponents/cdk-codepipeline-slack.ChannelTypes")
class ChannelTypes(enum.Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


class SlackApprovalAction(
    aws_cdk.aws_codepipeline_actions.Action,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudcomponents/cdk-codepipeline-slack.SlackApprovalAction",
):
    def __init__(
        self,
        *,
        slack_bot_token: builtins.str,
        slack_signing_secret: builtins.str,
        additional_information: typing.Optional[builtins.str] = None,
        external_entity_link: typing.Optional[builtins.str] = None,
        slack_bot_icon: typing.Optional[builtins.str] = None,
        slack_bot_name: typing.Optional[builtins.str] = None,
        slack_channel: typing.Optional[builtins.str] = None,
        slack_channel_id: typing.Optional[builtins.str] = None,
        slack_channel_types: typing.Optional[typing.List[ChannelTypes]] = None,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param slack_bot_token: -
        :param slack_signing_secret: -
        :param additional_information: -
        :param external_entity_link: -
        :param slack_bot_icon: -
        :param slack_bot_name: -
        :param slack_channel: -
        :param slack_channel_id: -
        :param slack_channel_types: -
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        '''
        props = SlackApprovalActionProps(
            slack_bot_token=slack_bot_token,
            slack_signing_secret=slack_signing_secret,
            additional_information=additional_information,
            external_entity_link=external_entity_link,
            slack_bot_icon=slack_bot_icon,
            slack_bot_name=slack_bot_name,
            slack_channel=slack_channel,
            slack_channel_id=slack_channel_id,
            slack_channel_types=slack_channel_types,
            action_name=action_name,
            run_order=run_order,
            variables_namespace=variables_namespace,
        )

        jsii.create(SlackApprovalAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(
        self,
        scope: aws_cdk.core.Construct,
        stage: aws_cdk.aws_codepipeline.IStage,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        role: aws_cdk.aws_iam.IRole,
    ) -> aws_cdk.aws_codepipeline.ActionConfig:
        '''(experimental) The method called when an Action is attached to a Pipeline.

        This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 
        '''
        options = aws_cdk.aws_codepipeline.ActionBindOptions(bucket=bucket, role=role)

        return typing.cast(aws_cdk.aws_codepipeline.ActionConfig, jsii.invoke(self, "bound", [scope, stage, options]))


@jsii.data_type(
    jsii_type="@cloudcomponents/cdk-codepipeline-slack.SlackApprovalActionProps",
    jsii_struct_bases=[aws_cdk.aws_codepipeline.CommonActionProps],
    name_mapping={
        "action_name": "actionName",
        "run_order": "runOrder",
        "variables_namespace": "variablesNamespace",
        "slack_bot_token": "slackBotToken",
        "slack_signing_secret": "slackSigningSecret",
        "additional_information": "additionalInformation",
        "external_entity_link": "externalEntityLink",
        "slack_bot_icon": "slackBotIcon",
        "slack_bot_name": "slackBotName",
        "slack_channel": "slackChannel",
        "slack_channel_id": "slackChannelId",
        "slack_channel_types": "slackChannelTypes",
    },
)
class SlackApprovalActionProps(aws_cdk.aws_codepipeline.CommonActionProps):
    def __init__(
        self,
        *,
        action_name: builtins.str,
        run_order: typing.Optional[jsii.Number] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
        slack_bot_token: builtins.str,
        slack_signing_secret: builtins.str,
        additional_information: typing.Optional[builtins.str] = None,
        external_entity_link: typing.Optional[builtins.str] = None,
        slack_bot_icon: typing.Optional[builtins.str] = None,
        slack_bot_name: typing.Optional[builtins.str] = None,
        slack_channel: typing.Optional[builtins.str] = None,
        slack_channel_id: typing.Optional[builtins.str] = None,
        slack_channel_types: typing.Optional[typing.List[ChannelTypes]] = None,
    ) -> None:
        '''
        :param action_name: The physical, human-readable name of the Action. Note that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param variables_namespace: The name of the namespace to use for variables emitted by this action. Default: - a name will be generated, based on the stage and action names, if any of the action's variables were referenced - otherwise, no namespace will be set
        :param slack_bot_token: -
        :param slack_signing_secret: -
        :param additional_information: -
        :param external_entity_link: -
        :param slack_bot_icon: -
        :param slack_bot_name: -
        :param slack_channel: -
        :param slack_channel_id: -
        :param slack_channel_types: -
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action_name": action_name,
            "slack_bot_token": slack_bot_token,
            "slack_signing_secret": slack_signing_secret,
        }
        if run_order is not None:
            self._values["run_order"] = run_order
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace
        if additional_information is not None:
            self._values["additional_information"] = additional_information
        if external_entity_link is not None:
            self._values["external_entity_link"] = external_entity_link
        if slack_bot_icon is not None:
            self._values["slack_bot_icon"] = slack_bot_icon
        if slack_bot_name is not None:
            self._values["slack_bot_name"] = slack_bot_name
        if slack_channel is not None:
            self._values["slack_channel"] = slack_channel
        if slack_channel_id is not None:
            self._values["slack_channel_id"] = slack_channel_id
        if slack_channel_types is not None:
            self._values["slack_channel_types"] = slack_channel_types

    @builtins.property
    def action_name(self) -> builtins.str:
        '''The physical, human-readable name of the Action.

        Note that Action names must be unique within a single Stage.
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''The runOrder property for this Action.

        RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        :default: 1

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''The name of the namespace to use for variables emitted by this action.

        :default:

        - a name will be generated, based on the stage and action names,
        if any of the action's variables were referenced - otherwise,
        no namespace will be set
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slack_bot_token(self) -> builtins.str:
        result = self._values.get("slack_bot_token")
        assert result is not None, "Required property 'slack_bot_token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slack_signing_secret(self) -> builtins.str:
        result = self._values.get("slack_signing_secret")
        assert result is not None, "Required property 'slack_signing_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_information(self) -> typing.Optional[builtins.str]:
        result = self._values.get("additional_information")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_entity_link(self) -> typing.Optional[builtins.str]:
        result = self._values.get("external_entity_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slack_bot_icon(self) -> typing.Optional[builtins.str]:
        result = self._values.get("slack_bot_icon")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slack_bot_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("slack_bot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slack_channel(self) -> typing.Optional[builtins.str]:
        result = self._values.get("slack_channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slack_channel_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("slack_channel_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slack_channel_types(self) -> typing.Optional[typing.List[ChannelTypes]]:
        result = self._values.get("slack_channel_types")
        return typing.cast(typing.Optional[typing.List[ChannelTypes]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SlackApprovalActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SlackNotifier(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudcomponents/cdk-codepipeline-slack.SlackNotifier",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        pipeline: aws_cdk.aws_codepipeline.IPipeline,
        slack_bot_token: builtins.str,
        slack_signing_secret: builtins.str,
        slack_bot_icon: typing.Optional[builtins.str] = None,
        slack_bot_name: typing.Optional[builtins.str] = None,
        slack_channel: typing.Optional[builtins.str] = None,
        slack_channel_id: typing.Optional[builtins.str] = None,
        slack_channel_types: typing.Optional[typing.List[ChannelTypes]] = None,
        stage_names: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param pipeline: -
        :param slack_bot_token: -
        :param slack_signing_secret: -
        :param slack_bot_icon: -
        :param slack_bot_name: -
        :param slack_channel: -
        :param slack_channel_id: -
        :param slack_channel_types: -
        :param stage_names: -
        '''
        props = SlackNotifierProps(
            pipeline=pipeline,
            slack_bot_token=slack_bot_token,
            slack_signing_secret=slack_signing_secret,
            slack_bot_icon=slack_bot_icon,
            slack_bot_name=slack_bot_name,
            slack_channel=slack_channel,
            slack_channel_id=slack_channel_id,
            slack_channel_types=slack_channel_types,
            stage_names=stage_names,
        )

        jsii.create(SlackNotifier, self, [scope, id, props])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="environment")
    def _environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "environment"))

    @_environment.setter
    def _environment(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        jsii.set(self, "environment", value)


@jsii.data_type(
    jsii_type="@cloudcomponents/cdk-codepipeline-slack.SlackNotifierProps",
    jsii_struct_bases=[],
    name_mapping={
        "pipeline": "pipeline",
        "slack_bot_token": "slackBotToken",
        "slack_signing_secret": "slackSigningSecret",
        "slack_bot_icon": "slackBotIcon",
        "slack_bot_name": "slackBotName",
        "slack_channel": "slackChannel",
        "slack_channel_id": "slackChannelId",
        "slack_channel_types": "slackChannelTypes",
        "stage_names": "stageNames",
    },
)
class SlackNotifierProps:
    def __init__(
        self,
        *,
        pipeline: aws_cdk.aws_codepipeline.IPipeline,
        slack_bot_token: builtins.str,
        slack_signing_secret: builtins.str,
        slack_bot_icon: typing.Optional[builtins.str] = None,
        slack_bot_name: typing.Optional[builtins.str] = None,
        slack_channel: typing.Optional[builtins.str] = None,
        slack_channel_id: typing.Optional[builtins.str] = None,
        slack_channel_types: typing.Optional[typing.List[ChannelTypes]] = None,
        stage_names: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        '''
        :param pipeline: -
        :param slack_bot_token: -
        :param slack_signing_secret: -
        :param slack_bot_icon: -
        :param slack_bot_name: -
        :param slack_channel: -
        :param slack_channel_id: -
        :param slack_channel_types: -
        :param stage_names: -
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "pipeline": pipeline,
            "slack_bot_token": slack_bot_token,
            "slack_signing_secret": slack_signing_secret,
        }
        if slack_bot_icon is not None:
            self._values["slack_bot_icon"] = slack_bot_icon
        if slack_bot_name is not None:
            self._values["slack_bot_name"] = slack_bot_name
        if slack_channel is not None:
            self._values["slack_channel"] = slack_channel
        if slack_channel_id is not None:
            self._values["slack_channel_id"] = slack_channel_id
        if slack_channel_types is not None:
            self._values["slack_channel_types"] = slack_channel_types
        if stage_names is not None:
            self._values["stage_names"] = stage_names

    @builtins.property
    def pipeline(self) -> aws_cdk.aws_codepipeline.IPipeline:
        result = self._values.get("pipeline")
        assert result is not None, "Required property 'pipeline' is missing"
        return typing.cast(aws_cdk.aws_codepipeline.IPipeline, result)

    @builtins.property
    def slack_bot_token(self) -> builtins.str:
        result = self._values.get("slack_bot_token")
        assert result is not None, "Required property 'slack_bot_token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slack_signing_secret(self) -> builtins.str:
        result = self._values.get("slack_signing_secret")
        assert result is not None, "Required property 'slack_signing_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slack_bot_icon(self) -> typing.Optional[builtins.str]:
        result = self._values.get("slack_bot_icon")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slack_bot_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("slack_bot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slack_channel(self) -> typing.Optional[builtins.str]:
        result = self._values.get("slack_channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slack_channel_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("slack_channel_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slack_channel_types(self) -> typing.Optional[typing.List[ChannelTypes]]:
        result = self._values.get("slack_channel_types")
        return typing.cast(typing.Optional[typing.List[ChannelTypes]], result)

    @builtins.property
    def stage_names(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("stage_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SlackNotifierProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ChannelTypes",
    "SlackApprovalAction",
    "SlackApprovalActionProps",
    "SlackNotifier",
    "SlackNotifierProps",
]

publication.publish()
