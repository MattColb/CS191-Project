import uuid
import boto3
from .account_response import AccountResponse

ddb_client = boto3.client("dynamodb")

def register_account(username:str, hashed_password:str, email_address:str, ddb_table_name:str):
    """
    Takes in username, hashed_password, email address, and table name

    Returns: UserID, successful, error_message    
    """
    
    response = ddb_client.query(
        TableName=ddb_table_name,
        IndexName="username-index",
        KeyConditionExpression='username = :username',
        ExpressionAttributeValues={
            ':username': {'S': username}
        }
    )

    if response["Count"] > 0:
        return AccountResponse(success=False, message="That account already exists", user_id=None)
    
    user_id = str(uuid.uuid4())
    
    ddb_client.put_item(TableName=ddb_table_name, Item = {
        "user_id":{"S":user_id},
        "username":{"S":username},
        "password":{"S":hashed_password},
        "email":{"S":email_address},
        "sub_users":{"L":[]}
    })

    return AccountResponse(success=True, user_id=user_id, message=None)
