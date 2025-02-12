import boto3

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
        return None, False, "There was an error in the username or password"
    if response["Items"][0]["password"]["S"] != hashed_password:
        return None, False, "There was an error in the username or password"

    user_id = response["Items"][0]["user_id"]["S"]

    return user_id, True, None