import os
import boto3
from boto3.dynamodb.conditions import Key
from pydantic import BaseModel


class User(BaseModel):
    pk: str  # user
    sk: str  # sid
    password: str
    username: str
    # model_config = ConfigDict(from_attributes=True)


class Aws:
    def __init__(self):
        table_name = "ill-ruby-firefly-gownCyclicDB"
        try:
            # 创建一个 DynamoDB 资源
            dynamodb = boto3.resource(
                "dynamodb",
                region_name=os.environ.get("AWS_REGION"),
                aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
                aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
            )
            self.db = dynamodb.Table(table_name)
        except:
            config = {}
            with open("local.txt", "r") as file:
                for line in file:
                    if line.startswith("export "):
                        var_name, var_value = line[len("export ") :].split("=", 1)
                        config[var_name] = var_value.replace("\n", "").strip('"')
            # 创建一个DynamoDB资源
            dynamodb = boto3.resource(
                "dynamodb",
                region_name=config.get("AWS_REGION", ""),
                aws_access_key_id=config.get("AWS_ACCESS_KEY_ID", ""),
                aws_secret_access_key=config.get("AWS_SECRET_ACCESS_KEY", ""),
                aws_session_token=config.get("AWS_SESSION_TOKEN", ""),
            ).Table(table_name)
            self.db = dynamodb

        # print(self.db.key_schema)＃主排序鍵

    def create_user(self, user: User):
        check = self.check_item(pk=user.pk, sk=user.sk)
        if check is None:
            try:
                self.db.put_item(Item=user.model_dump())
                return "success"
            except Exception as e:
                return e
        else:
            return "already exsist"

    def scan_all(self):
        response = self.db.scan()
        return response["Items"]

    def check_item(self, pk=None, sk=None):
        try:
            if pk and sk:  # check one
                response = self.db.query(KeyConditionExpression=Key("pk").eq(pk) & Key("sk").eq(sk))
                return response["Items"][0]
            elif pk:  # check all type
                response = self.db.query(KeyConditionExpression=Key("pk").eq(pk))
                return response["Items"]
            else:  # test db
                key = Key("pk").eq("user") & Key("sk").eq("0096c029")
                self.db.query(KeyConditionExpression=key)
        except Exception as e:  # test db
            print(e)
            return None

    def delete_user(self, pk, sk):
        response = self.db.delete_item(Key={"pk": pk, "sk": sk})
        # 如果操作成功，response 中会包含删除成功的信息
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return "success"
        else:
            return "Item deletion failed."


try:
    aws = Aws()
    aws.check_item()
except Exception as e:
    print(e)
    input("！！！簽證過期了！！！")
