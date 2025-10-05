import boto3
import os

AWS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

if not AWS_KEY or not AWS_SECRET or not AWS_REGION:
    raise ValueError("Credenciais AWS (KEY, SECRET e REGION) não foram configuradas. Verifique o arquivo .env.")

dynamodb = boto3.resource(
    'dynamodb',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_KEY,
    aws_secret_access_key=AWS_SECRET
)

table = dynamodb.Table('artist_genius_traces')

def save_dynamo(payload):
    table = dynamodb.Table("artist_genius_traces")
    try:
        table.put_item(Item=payload)
        print(f"Transação {payload.get('transaction_id')} salva no DynamoDB.")
    except Exception as e:
        print(f"ERRO ao salvar a transação {payload.get('transaction_id')} no DynamoDB: {e}")