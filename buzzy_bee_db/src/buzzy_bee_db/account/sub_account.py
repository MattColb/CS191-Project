from buzzy_bee_db.account.account_response import SubAccountGetResponse, SubAccountResponse
import uuid
import boto3

ddb_client = boto3.client("dynamodb")

def get_sub_accounts(main_account_id, ddb_table_name):
    result = ddb_client.get_item(
        TableName=ddb_table_name,
        Key={
            "user_id":{"S":main_account_id}
        }
    )

    sub_users = result["Item"].get("sub_users", {})
    users = sub_users.get("L", [])

    if result['ResponseMetadata']['HTTPStatusCode'] == 200:
        return SubAccountGetResponse(users=users, success=True, message=None)

    return SubAccountGetResponse(users=None, success=False, message="Something went wrong when updating the table")

def create_sub_account(main_account_id, ddb_table_name, sub_account_name, sub_account_grade):
    sub_account_id = str(uuid.uuid4())
    sub_account = {"L":[
        {"M":{
            "user_id":{"S":sub_account_id},
            "name":{"S":sub_account_name},
            "grade":{"S":sub_account_grade}
        }}
    ]}

    result = ddb_client.update_item(
        TableName = ddb_table_name,
        Key = {
            "user_id":{"S":main_account_id},
        },
        UpdateExpression="SET sub_users = list_append(sub_users, :i)",
        ExpressionAttributeValues={
            ":i":sub_account
        }
    )

    if result['ResponseMetadata']['HTTPStatusCode'] == 200:
        return SubAccountResponse(sub_user_id=sub_account_id, success=True, message=None)

    return SubAccountResponse(sub_user_id=None, success=False, message="Something went wrong when updating the table")

def update_sub_account(main_account_id, ddb_table_name, sub_account_id, sub_account_new_name=None, sub_account_new_grade=None):
    result = ddb_client.get_item(
        TableName=ddb_table_name,
        Key={
            "user_id":{"S":main_account_id}
        }
    )

    sub_users = result["Item"].get("sub_users", {})
    sub_users = sub_users.get("L", [])

    for i in sub_users:
        if i["M"]["user_id"]["S"] == sub_account_id:
            i["M"]["name"]["S"] = i["M"]["name"]["S"] if sub_account_new_name == None else sub_account_new_name
            i["M"]["grade"]["S"] = i["M"]["grade"]["S"] if sub_account_new_grade == None else sub_account_new_grade

    result = ddb_client.update_item(
        TableName = ddb_table_name,
        Key = {
            "user_id":{"S":main_account_id},
        },
        UpdateExpression="SET sub_users = :i",
        ExpressionAttributeValues={
            ":i":{"L":sub_users}
        }
    )

    if result['ResponseMetadata']['HTTPStatusCode'] == 200:
        return SubAccountResponse(sub_user_id=None, success=True, message=None)

    return SubAccountResponse(sub_user_id=None, success=False, message="Something went wrong when updating the table")

def delete_sub_account(main_account_id, ddb_table_name, sub_account_id):
    result = ddb_client.get_item(
        TableName=ddb_table_name,
        Key={
            "user_id":{"S":main_account_id}
        }
    )

    sub_users = result["Item"].get("sub_users", {})
    sub_users = sub_users.get("L", [])

    new_sub_users = [i for i in sub_users if i["M"]["user_id"]["S"] != sub_account_id]

    result = ddb_client.update_item(
        TableName = ddb_table_name,
        Key = {
            "user_id":{"S":main_account_id},
        },
        UpdateExpression="SET sub_users = :i",
        ExpressionAttributeValues={
            ":i":{"L":new_sub_users}
        }
    )

    if result['ResponseMetadata']['HTTPStatusCode'] == 200:
        return SubAccountResponse(sub_user_id=None, success=True, message=None)

    return SubAccountResponse(sub_user_id=None, success=False, message="Something went wrong when updating the table")