# AWS XML to JSON

> This repository is a work in progress, contribution is welcome!

This module converts AWS API XML responses to JSON, it
matches the output of AWS APIs where `Accept: application/json` is provided
as a header.

## Examples

<!-- GENERATED_SAMPLE_DOCS_START -->

### ErrorResponse

```xml
<ErrorResponse>
    <Error>
        <Type>Sender</Type>
        <Code>AccessDenied</Code>
        <Message>Access to the resource https://sqs.us-east-1.amazonaws.com/ is denied.</Message>
        <Detail/>
    </Error>
    <RequestId>2d121ac6-aeee-515c-8d04-420e02b34285</RequestId>
</ErrorResponse>
```

```json
{
    "ErrorResponse": {
        "Error": {
            "Code": "AccessDenied",
            "Message": "Access to the resource https://sqs.us-east-1.amazonaws.com/ is denied.",
            "Type": "Sender"
        },
        "RequestId": "2d121ac6-aeee-515c-8d04-420e02b34285"
    }
}
```

### SQS.ListQueues

```xml
<ListQueuesResponse>
    <ListQueuesResult>
        <QueueUrl>https://sqs.us-east-2.amazonaws.com/123456789012/MyQueue</QueueUrl>
    </ListQueuesResult>
    <ResponseMetadata>
        <RequestId>725275ae-0b9b-4762-b238-436d7c65a1ac</RequestId>
    </ResponseMetadata>
</ListQueuesResponse>
```

```json
{
    "ListQueuesResponse": {
        "ListQueuesResult": {
            "queueUrls": [
                "https://sqs.us-east-2.amazonaws.com/123456789012/MyQueue"
            ]
        },
        "ResponseMetadata": {
            "RequestId": "725275ae-0b9b-4762-b238-436d7c65a1ac"
        }
    }
}
```

### SQS.ReceiveMessage

```xml
<ReceiveMessageResponse>
  <ReceiveMessageResult>
    <Message>
      <MessageId>5fea7756-0ea4-451a-a703-a558b933e274</MessageId>
      <ReceiptHandle>MbZj6wDWli+JvwwJaBV+3dcjk2YW2vA3+STFFljTM8tJJg6HRG6PYSasuWXPJB+CwLj1FjgXUv1uSj1gUPAWV66FU/WeR4mq2OKpEGYWbnLmpRCJVAyeMjeU5ZBdtcQ+QEauMZc8ZRv37sIW2iJKq3M9MFx1YvV11A2x/KSbkJ0=</ReceiptHandle>
      <MD5OfBody>fafb00f5732ab283681e124bf8747ed1</MD5OfBody>
      <Body>This is a test message</Body>
      <Attribute>
        <Name>SenderId</Name>
        <Value>195004372649</Value>
      </Attribute>
      <Attribute>
        <Name>SentTimestamp</Name>
        <Value>1238099229000</Value>
      </Attribute>
      <Attribute>
        <Name>ApproximateReceiveCount</Name>
        <Value>5</Value>
      </Attribute>
      <Attribute>
        <Name>ApproximateFirstReceiveTimestamp</Name>
        <Value>1250700979248</Value>
      </Attribute>
    </Message>
  </ReceiveMessageResult>
  <ResponseMetadata>
    <RequestId>b6633655-283d-45b4-aee4-4e84e0ae6afa</RequestId>
  </ResponseMetadata>
</ReceiveMessageResponse>
```

```json
{
    "ReceiveMessageResponse": {
        "ReceiveMessageResult": {
            "messages": [
                {
                    "Message": {
                        "MessageId": "5fea7756-0ea4-451a-a703-a558b933e274",
                        "ReceiptHandle": "MbZj6wDWli+JvwwJaBV+3dcjk2YW2vA3+STFFljTM8tJJg6HRG6PYSasuWXPJB+CwLj1FjgXUv1uSj1gUPAWV66FU/WeR4mq2OKpEGYWbnLmpRCJVAyeMjeU5ZBdtcQ+QEauMZc8ZRv37sIW2iJKq3M9MFx1YvV11A2x/KSbkJ0=",
                        "MD5OfBody": "fafb00f5732ab283681e124bf8747ed1",
                        "Body": "This is a test message",
                        "SenderId": "195004372649",
                        "SentTimestamp": "1238099229000",
                        "ApproximateReceiveCount": "5",
                        "ApproximateFirstReceiveTimestamp": "1250700979248"
                    }
                }
            ]
        },
        "ResponseMetadata": {
            "RequestId": "b6633655-283d-45b4-aee4-4e84e0ae6afa"
        }
    }
}
```

### SQS.SendMessage

```xml
<SendMessageResponse>
    <SendMessageResult>
        <MD5OfMessageBody>fafb00f5732ab283681e124bf8747ed1</MD5OfMessageBody>
        <MD5OfMessageAttributes>3ae8f24a165a8cedc005670c81a27295</MD5OfMessageAttributes>
        <MessageId>5fea7756-0ea4-451a-a703-a558b933e274</MessageId>
    </SendMessageResult>
    <ResponseMetadata>
        <RequestId>27daac76-34dd-47df-bd01-1f6e873584a0</RequestId>
    </ResponseMetadata>
</SendMessageResponse>
```

```json
{
    "SendMessageResponse": {
        "SendMessageResult": {
            "MD5OfMessageBody": "fafb00f5732ab283681e124bf8747ed1",
            "MD5OfMessageAttributes": "3ae8f24a165a8cedc005670c81a27295",
            "MessageId": "5fea7756-0ea4-451a-a703-a558b933e274"
        },
        "ResponseMetadata": {
            "RequestId": "27daac76-34dd-47df-bd01-1f6e873584a0"
        }
    }
}
```

<!-- GENERATED_SAMPLE_DOCS_STOP -->

## Want to add another AWS API?

1. Download the XML to JSON mapping helper file from the [aws javascript sdk](https://github.com/aws/aws-sdk-js/tree/master/apis)
2. Add it so it's loaded in `get_shape.py`
3. Write a couple sample tests use example responses from the AWS documentation to make sure
   it's working