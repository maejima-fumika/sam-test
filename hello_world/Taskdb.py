class Taskdb:
    def __init__(self, dynamodb, table_name):
        self.db = dynamodb.Table(table_name)

    def execute_method(self, method, item):
        try:
            Id = int(item["Id"])
            Name = item["Name"]
        except:
            return 400, "required key does not exist"

        response = ""
        try:
            if method == "insert":
                response = self.insert_task(Id, Name)
            elif method == "get":
                response = self.get_task(Id)
            elif method == "scan":
                response = self.scan_task()
            elif method == "update":
                response = self.update_task(Id, Name)
            elif method == "delete":
                response = self.delete_task(Id)
            else:
                response = "method name does not fit"
                raise Exception
        except:
            return 400, response
        else:
            return 200, response

    def insert_task(self, Id, Name):
        response = self.db.put_item(
            Item={
                'Id': Id,
                'Name': Name
            }
        )
        return response

    def get_task(self, Id):
        response = self.db.get_item(Key={'Id': Id})
        return response["Item"]

    def scan_task(self):
        response = self.db.scan()
        return response["Items"]

    def update_task(self, Id, Name):
        response = self.db.update_item(
            Key={
                'Id': Id,
            },
            UpdateExpression="set #Name=:Name",
            ExpressionAttributeNames={
                '#Name': 'Name',
            },
            ExpressionAttributeValues={
                ':Name': Name
            },
            ReturnValues="UPDATED_NEW"
        )
        return response

    def delete_task(self, Id):
        response = self.db.delete_item(Key={'Id': Id})
        return response
