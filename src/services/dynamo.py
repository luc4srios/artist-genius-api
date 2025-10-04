import boto3
import os

AWS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")

if not AWS_KEY:
    raise ValueError("AWS_KEY não foi configurada")

if not AWS_SECRET:
    raise ValueError("AWS_SECRET não foi configurada")

dynamodb = boto3.resource(
    'dynamodb',
    region_name='sa-east-1',
    aws_access_key_id=AWS_KEY,
    aws_secret_access_key=AWS_SECRET
)

table = dynamodb.Table('Musicas')

def save_dynamo(payload):
    table = dynamodb.Table("Musicas")
    try:
        table.put_item(Item=payload)
        print(f"Transação {payload.get('transaction_id')} salva no DynamoDB.")
    except Exception as e:
        print(f"ERRO ao salvar a transação {payload.get('transaction_id')} no DynamoDB: {e}")