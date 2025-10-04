import boto3
import os

aws_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")

dynamodb = boto3.resource(
    'dynamodb',
    region_name='sa-east-1',
    aws_access_key_id=aws_key,
    aws_secret_access_key=aws_secret
)

table = dynamodb.Table('Musicas')

def save_dynamo(payload):
    table = dynamodb.Table("Musicas")
    try:
        table.put_item(Item=payload)
        print(f"Transação {payload.get('transaction_id')} salva no DynamoDB.")
    except Exception as e:
        print(f"ERRO ao salvar a transação {payload.get('transaction_id')} no DynamoDB: {e}")