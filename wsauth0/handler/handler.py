import json
import os

import boto3

connections_table = boto3.resource('dynamodb', region_name='ap-northeast-1').Table(os.getenv('CONNECTIONS_TABLE_NAME'))


def connect_handler(event, context):
    connection_id = event["requestContext"]["connectionId"]

    join_member(connection_id)

    return {
        "statusCode": 200
    }


def disconnect_handler(event, context):
    connection_id = event["requestContext"]["connectionId"]

    leave_member(connection_id)

    return {
        "statusCode": 200
    }


def send_message_handler(event, context):
    members = get_members()
    apigw = get_apigw_management_client(event)

    data = json.loads(event['body'])['data']

    for member in members:
        try:
            apigw.post_to_connection(
                ConnectionId=member['connection_id'],
                Data=json.dumps({
                    "message": data['message']
                })
            )
        except Exception as e:
            print(e)

    return {
        "statusCode": 200
    }


def join_member(connection_id):
    connections_table.put_item(
        Item={
            'connection_id': connection_id,
        }
    )


def leave_member(connection_id):
    connections_table.delete_item(
        Key={
            'connection_id': connection_id,
        }
    )


def get_members():
    return connections_table.scan()['Items']


def get_apigw_management_client(event):
    domain = event["requestContext"]["domainName"]
    stage = event["requestContext"]["stage"]

    return boto3.client('apigatewaymanagementapi', endpoint_url=f'https://{domain}/{stage}')
