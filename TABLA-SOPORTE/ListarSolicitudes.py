import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TABLA-SOPORTE')

def lambda_handler(event, context):
    response = table.scan()
    return {
        'statusCode': 200,
        'body': response['Items']
    }