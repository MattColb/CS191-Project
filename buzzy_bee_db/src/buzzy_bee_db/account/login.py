import boto3
from .account_response import AccountResponse

ddb_client = boto3.client("dynamodb")

def login_account(username:str, hashed_password:str, ddb_table_name:str):
    """
    Takes in username, hashed_password, and table name 
    
    Returns user_id:str, success:bool, message:str
    """

    response = ddb_client.query(
        TableName=ddb_table_name,
        IndexName="username-index",
        KeyConditionExpression='username = :username',
        ExpressionAttributeValues={
            ':username': {'S': username}
        }
    )
    if response["Count"] != 1:
        return AccountResponse(user_id=None, success=False, message="There was an error in the username or password")
    if response["Items"][0]["password"]["S"] != hashed_password:
        return AccountResponse(user_id=None, success=False, message="There was an error in the username or password")

    user_id = response["Items"][0]["user_id"]["S"]

    return AccountResponse(user_id=user_id, success=True, message=None)