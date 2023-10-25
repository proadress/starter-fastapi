import os
import boto3
from werkzeug.security import generate_password_hash, check_password_hash
from boto3.dynamodb.conditions import Key

table_name = "ill-ruby-firefly-gownCyclicDB"


def get_text():
    with open("local.txt", "r") as file:
        content = file.read()
    lines = content.split("\n")
    config = {}
    for line in lines:
        parts = line.split("=", 1)
        var_name = parts[0].replace("export ", "")  # 去除 "export " 前缀
        var_value = parts[1].strip('"')  # 去除引号
        config[var_name] = var_value
    return config


try:
    # 创建一个 DynamoDB 资源
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
    )
    db = dynamodb.Table(table_name)
except:
    keep_find = True
    while keep_find:
        config = get_text()
        # 创建一个DynamoDB资源
        dynamodb = boto3.resource(
            "dynamodb",
            region_name=config.get("AWS_REGION", ""),
            aws_access_key_id=config.get("AWS_ACCESS_KEY_ID", ""),
            aws_secret_access_key=config.get("AWS_SECRET_ACCESS_KEY", ""),
            aws_session_token=config.get("AWS_SESSION_TOKEN", ""),
        )
        try:
            db = dynamodb.Table(table_name)
            db.query(KeyConditionExpression=Key("pk").eq("y359032@gmail.com"))
            keep_find = False
        except:
            input("!!!psssword need to update!!!(press enter)")


def check_item(name, contant):
    key_condition_expression = Key(name).eq(contant)
    response = db.query(KeyConditionExpression=key_condition_expression)
    return response["Items"]


def create_account(email, password, name):
    response = check_item("pk", email)
    user = [item for item in response if item.get("sk") == "user"]
    if len(user) == 0:
        # 使用 Werkzeug 库对密码进行哈希处理
        hashed_password = generate_password_hash(password)
        # 创建新用户项
        new_user = {"pk": email, "sk": "user", "name": name, "password": hashed_password}
        # 将新用户项插入到 DynamoDB 表中
        db.put_item(Item=new_user)
        print("新用户已创建并存储到 DynamoDB 表中")
        return True
    return False


def login_account(email, password):
    response = check_item("pk", email)
    user = [item for item in response if item.get("sk") == "user"]
    if len(user) == 1:
        user = user[0]
        print(user)
        if "password" in user and check_password_hash(user["password"], password):
            print("用户已验证")
            return 1
        else:
            print("密码错误")
            return 2
    elif len(user) > 1:
        print("error")
        return 3
    else:
        print("电子邮件地址不存在")
        return 4


def scan_all():
    response = db.scan()
    return response["Items"]


def delete_items(items):
    for item in items:
        response = db.delete_item(Key={"pk": item["pk"], "sk": item["sk"]})
        # 如果操作成功，response 中会包含删除成功的信息
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print("deleted successfully")
            print(item)
        else:
            print("Item deletion failed.")
    print("no items to delete")


class User:
    def __init__(self, username, email, other_data=None):
        self.username = username
        self.email = email
        self.other_data = other_data
