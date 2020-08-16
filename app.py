#!/usr/bin/env python3

from aws_cdk import core

from sqs_lambda_sns_cloud_watch_best_practices.sqs_lambda_sns_cloud_watch_best_practices_stack import SqsLambdaSnsCloudWatchBestPracticesStack


app = core.App()
SqsLambdaSnsCloudWatchBestPracticesStack(app, "sqs-lambda-sns-cloud-watch-best-practices",env={'region': 'ap-south-1'})

app.synth()
