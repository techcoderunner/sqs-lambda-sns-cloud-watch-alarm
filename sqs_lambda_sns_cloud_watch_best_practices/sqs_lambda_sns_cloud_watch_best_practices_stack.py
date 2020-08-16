from aws_cdk import (
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_s3_notifications as aws_s3_notifications,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_cloudwatch as aws_cloudwatch,
    aws_cloudwatch_actions,
    aws_lambda_event_sources as event,
    core)

from aws_cdk.core import Duration


class SqsLambdaSnsCloudWatchBestPracticesStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        # Define aws lambda function
        my_lambda = _lambda.Function(self,"HelloHandler",
                            runtime=_lambda.Runtime.PYTHON_3_7,
                            handler="hello.handler",
                            code=_lambda.Code.asset('lambda'))

        # Define S3 bucket
        my_bucket = s3.Bucket(self,"ssl-s3-lambda-event-raw")

        queue_dlq = sqs.Queue(self
                            ,id='testQueueDLQ'
                            ,queue_name='testQueueDLQ'
                            ,data_key_reuse=Duration.minutes(1)
                            ,visibility_timeout=Duration.seconds(30)
                            ,retention_period=Duration.days(14)
                            ,receive_message_wait_time=Duration.seconds(20)
                            )

        queue = sqs.Queue(self
                            ,id='testQueue'
                            ,queue_name='testQueue'
                            ,data_key_reuse=Duration.minutes(1)
                            ,visibility_timeout=Duration.seconds(30)
                            ,retention_period=Duration.days(14)
                            ,receive_message_wait_time=Duration.seconds(20)
                            ,dead_letter_queue=sqs.DeadLetterQueue(max_receive_count=3,queue=queue_dlq)
                            )

        #Create S3 notification object which points to SQS.
        notification = aws_s3_notifications.SqsDestination(queue)
        filter1=s3.NotificationKeyFilter(prefix="home/")

        #Attach notificaton event to S3 bucket.
        my_bucket.add_event_notification(s3.EventType.OBJECT_CREATED,notification,filter1)

        #create SNS Topic
        topic = sns.Topic(self
                            ,id='testSns'
                            ,display_name='testSns'
                            ,topic_name='testSns')

        subscription = sns.Subscription(self
                                        ,id='testSubscription'
                                        ,topic=topic
                                        ,endpoint='londhesachin6@gmail.com'
                                        ,protocol=sns.SubscriptionProtocol.EMAIL)

        #Create cloud watch alarm
        metric = queue_dlq.metric('ApproximateNumberOfMessagesVisible')

        alarm=aws_cloudwatch.Alarm(self
                        ,id='testAlarm'
                        ,metric=metric
                        ,evaluation_periods=1
                        ,threshold=1
                        ,alarm_description='testAlarm'
                        ,alarm_name='testAlarm'
                        ,statistic='sum'
                        ,comparison_operator=aws_cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD
                        ,treat_missing_data=aws_cloudwatch.TreatMissingData.MISSING
                        ,period=Duration.minutes(1)
                        )
        
        alarm.add_alarm_action(aws_cloudwatch_actions.SnsAction(topic))

        my_lambda.add_event_source(event.SqsEventSource(queue,batch_size=1))

        
        
        
