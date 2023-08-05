# cdk-watchful

![Release](https://github.com/eladb/cdk-watchful/workflows/Release/badge.svg)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cdk-watchful/)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/cdk-watchful)

> Watching your CDK back since 2019

Watchful is an [AWS CDK](https://github.com/awslabs/aws-cdk) construct library that makes it easy
to monitor CDK apps. It automatically synthesizes alarms and dashboards for supported AWS resources.

**TypeScript:**

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_watchful import Watchful

wf = Watchful(self, "watchful")
wf.watch_dynamo_table("My Cute Little Table", my_table)
wf.watch_lambda_function("My Function", my_function)
wf.watch_api_gateway("My REST API", my_rest_api)
```

**Python:**

```python
from cdk_watchful import Watchful

wf = Watchful(self, 'watchful')
wf.watch_dynamo_table('My Cute Little Table', my_table)
wf.watch_lambda_function('My Function', my_function)
wf.watch_api_gateway('My REST API', my_rest_api)
```

And...

![](https://raw.githubusercontent.com/eladb/cdk-watchful/master/example/sample.png)

## Install

TypeScript/JavaScript:

```console
$ npm install cdk-watchful
```

Python:

```console
$ pip install cdk-watchful
```

## Initialize

To get started, just define a `Watchful` construct in your CDK app (code is in
TypeScript, but python will work too). You can initialize using an email address, SQS arn or both:

**TypeScript:**

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_watchful import Watchful
import aws_cdk.aws_sns as sns
import aws_cdk.aws_sqs as sqs

alarm_sqs = sqs.Queue.from_queue_arn(self, "AlarmQueue", "arn:aws:sqs:us-east-1:444455556666:alarm-queue")
alarm_sns = sns.Topic.from_topic_arn(self, "AlarmTopic", "arn:aws:sns:us-east-2:444455556666:MyTopic")

wf = Watchful(self, "watchful",
    alarm_email="your@email.com",
    alarm_sqs=alarm_sqs,
    alarm_sns=alarm_sns
)
```

**Python:**

```python
from cdk_watchful import Watchful

alarm_sqs = sqs.Queue.from_queue_arn(self, 'AlarmQueue', 'arn:aws:sqs:us-east-1:444455556666:alarm-queue')
alarm_sns = sns.Topic.from_topic_arn(self, 'AlarmTopic', 'arn:aws:sns:us-east-2:444455556666:MyTopic')

wf = Watchful(
  self,
  'watchful',
  alarm_email='your@amil.com',
  alarm_sqs=alarm_sqs,
  alarm_sns=alarm_sns
```

## Add Resources

Watchful manages a central dashboard and configures default alarming for:

* Amazon DynamoDB: `watchful.watchDynamoTable`
* AWS Lambda: `watchful.watchLambdaFunction`
* Amazon API Gateway: `watchful.watchApiGateway`
* [Request yours](https://github.com/eladb/cdk-watchful/issues/new)

## Watching Scopes

Watchful can also watch complete CDK construct scopes. It will automatically
discover all watchable resources within that scope (recursively), add them
to your dashboard and configure alarms for them.

**TypeScript:**

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
wf.watch_scope(storage_layer)
```

**Python:**

```python
wf.watch_scope(storage_layer)
```

## API Reference

See [API.md](./API.md).

## Example

See a more complete [example](https://github.com/eladb/cdk-watchful/blob/master/example/index.ts).

## Contributing

Contributions of all kinds are welcome and celebrated. Raise an issue, submit a PR, do the right thing.

To set up a dev environment:

1. Clone this repo
2. `yarn`

Development workflow (change code and run tests automatically):

```shell
yarn test:watch
```

Build (like CI):

```shell
yarn build
```

Release new versions:

```shell
yarn bump
```

And then publish as a PR.

## License

[Apache 2.0](https://github.com/eladb/cdk-watchful/blob/master/LICENSE)
