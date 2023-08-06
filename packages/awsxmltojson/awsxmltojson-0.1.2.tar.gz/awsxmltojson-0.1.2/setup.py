# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awsxmltojson']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.6.2,<5.0.0', 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'awsxmltojson',
    'version': '0.1.2',
    'description': 'Converts XML Responses from AWS API to JSON',
    'long_description': '# AWS XML to JSON\n\n> This repository is a work in progress, contribution is welcome!\n\nThis module converts AWS API XML responses to JSON, it\nmatches the output of AWS APIs where `Accept: application/json` is provided\nas a header.\n\n## Examples\n\n<!-- GENERATED_SAMPLE_DOCS_START -->\n\n### ErrorResponse\n\n```xml\n<ErrorResponse>\n    <Error>\n        <Type>Sender</Type>\n        <Code>AccessDenied</Code>\n        <Message>Access to the resource https://sqs.us-east-1.amazonaws.com/ is denied.</Message>\n        <Detail/>\n    </Error>\n    <RequestId>2d121ac6-aeee-515c-8d04-420e02b34285</RequestId>\n</ErrorResponse>\n```\n\n```json\n{\n    "ErrorResponse": {\n        "Error": {\n            "Code": "AccessDenied",\n            "Message": "Access to the resource https://sqs.us-east-1.amazonaws.com/ is denied.",\n            "Type": "Sender"\n        },\n        "RequestId": "2d121ac6-aeee-515c-8d04-420e02b34285"\n    }\n}\n```\n\n### SQS.ListQueues\n\n```xml\n<ListQueuesResponse>\n    <ListQueuesResult>\n        <QueueUrl>https://sqs.us-east-2.amazonaws.com/123456789012/MyQueue</QueueUrl>\n    </ListQueuesResult>\n    <ResponseMetadata>\n        <RequestId>725275ae-0b9b-4762-b238-436d7c65a1ac</RequestId>\n    </ResponseMetadata>\n</ListQueuesResponse>\n```\n\n```json\n{\n    "ListQueuesResponse": {\n        "ListQueuesResult": {\n            "queueUrls": [\n                "https://sqs.us-east-2.amazonaws.com/123456789012/MyQueue"\n            ]\n        },\n        "ResponseMetadata": {\n            "RequestId": "725275ae-0b9b-4762-b238-436d7c65a1ac"\n        }\n    }\n}\n```\n\n### SQS.ReceiveMessage\n\n```xml\n<ReceiveMessageResponse>\n  <ReceiveMessageResult>\n    <Message>\n      <MessageId>5fea7756-0ea4-451a-a703-a558b933e274</MessageId>\n      <ReceiptHandle>MbZj6wDWli+JvwwJaBV+3dcjk2YW2vA3+STFFljTM8tJJg6HRG6PYSasuWXPJB+CwLj1FjgXUv1uSj1gUPAWV66FU/WeR4mq2OKpEGYWbnLmpRCJVAyeMjeU5ZBdtcQ+QEauMZc8ZRv37sIW2iJKq3M9MFx1YvV11A2x/KSbkJ0=</ReceiptHandle>\n      <MD5OfBody>fafb00f5732ab283681e124bf8747ed1</MD5OfBody>\n      <Body>This is a test message</Body>\n      <Attribute>\n        <Name>SenderId</Name>\n        <Value>195004372649</Value>\n      </Attribute>\n      <Attribute>\n        <Name>SentTimestamp</Name>\n        <Value>1238099229000</Value>\n      </Attribute>\n      <Attribute>\n        <Name>ApproximateReceiveCount</Name>\n        <Value>5</Value>\n      </Attribute>\n      <Attribute>\n        <Name>ApproximateFirstReceiveTimestamp</Name>\n        <Value>1250700979248</Value>\n      </Attribute>\n    </Message>\n  </ReceiveMessageResult>\n  <ResponseMetadata>\n    <RequestId>b6633655-283d-45b4-aee4-4e84e0ae6afa</RequestId>\n  </ResponseMetadata>\n</ReceiveMessageResponse>\n```\n\n```json\n{\n    "ReceiveMessageResponse": {\n        "ReceiveMessageResult": {\n            "messages": [\n                {\n                    "MessageId": "5fea7756-0ea4-451a-a703-a558b933e274",\n                    "ReceiptHandle": "MbZj6wDWli+JvwwJaBV+3dcjk2YW2vA3+STFFljTM8tJJg6HRG6PYSasuWXPJB+CwLj1FjgXUv1uSj1gUPAWV66FU/WeR4mq2OKpEGYWbnLmpRCJVAyeMjeU5ZBdtcQ+QEauMZc8ZRv37sIW2iJKq3M9MFx1YvV11A2x/KSbkJ0=",\n                    "MD5OfBody": "fafb00f5732ab283681e124bf8747ed1",\n                    "Body": "This is a test message",\n                    "SenderId": "195004372649",\n                    "SentTimestamp": "1238099229000",\n                    "ApproximateReceiveCount": "5",\n                    "ApproximateFirstReceiveTimestamp": "1250700979248"\n                }\n            ]\n        },\n        "ResponseMetadata": {\n            "RequestId": "b6633655-283d-45b4-aee4-4e84e0ae6afa"\n        }\n    }\n}\n```\n\n### SQS.SendMessage\n\n```xml\n<SendMessageResponse>\n    <SendMessageResult>\n        <MD5OfMessageBody>fafb00f5732ab283681e124bf8747ed1</MD5OfMessageBody>\n        <MD5OfMessageAttributes>3ae8f24a165a8cedc005670c81a27295</MD5OfMessageAttributes>\n        <MessageId>5fea7756-0ea4-451a-a703-a558b933e274</MessageId>\n    </SendMessageResult>\n    <ResponseMetadata>\n        <RequestId>27daac76-34dd-47df-bd01-1f6e873584a0</RequestId>\n    </ResponseMetadata>\n</SendMessageResponse>\n```\n\n```json\n{\n    "SendMessageResponse": {\n        "SendMessageResult": {\n            "MD5OfMessageBody": "fafb00f5732ab283681e124bf8747ed1",\n            "MD5OfMessageAttributes": "3ae8f24a165a8cedc005670c81a27295",\n            "MessageId": "5fea7756-0ea4-451a-a703-a558b933e274"\n        },\n        "ResponseMetadata": {\n            "RequestId": "27daac76-34dd-47df-bd01-1f6e873584a0"\n        }\n    }\n}\n```\n\n<!-- GENERATED_SAMPLE_DOCS_STOP -->\n\n## Want to add another AWS API?\n\n1. Download the XML to JSON mapping helper file from the [aws javascript sdk](https://github.com/aws/aws-sdk-js/tree/master/apis)\n2. Add it so it\'s loaded in `get_shape.py`\n3. Write a couple sample tests use example responses from the AWS documentation to make sure\n   it\'s working',
    'author': 'seveibar',
    'author_email': 'seveibar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/seveibar/awsxmltojson',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
