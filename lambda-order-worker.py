import boto3, json, os
from datetime import datetime
from botocore.exceptions import ClientError

ddb = boto3.client("dynamodb")
DDB_TABLE = os.environ["DDB_TABLE"]

def log(level, msg, **fields):
    print(json.dumps({"ts": datetime.utcnow().isoformat()+"Z", "level": level, "message": msg, **fields}, ensure_ascii=False))

def pk(order_id: str) -> str:
    return f"ORDER#{order_id}"

def put_status(order_id: str, status: str, **extras):
    item = {
        "pk": {"S": pk(order_id)},
        "order_id": {"S": order_id},
        "status": {"S": status},
        "updated_at": {"S": datetime.utcnow().isoformat()+"Z"},
    }
    for k, v in extras.items():
        item[k] = {"S": str(v)}

    ddb.put_item(TableName=DDB_TABLE, Item=item)

def put_if_not_exists(order_id: str, status: str, **extras):
    # Idempotence: only insert if pk does not exist
    item = {
        "pk": {"S": pk(order_id)},
        "order_id": {"S": order_id},
        "status": {"S": status},
        "updated_at": {"S": datetime.utcnow().isoformat()+"Z"},
    }
    for k, v in extras.items():
        item[k] = {"S": str(v)}

    ddb.put_item(
        TableName=DDB_TABLE,
        Item=item,
        ConditionExpression="attribute_not_exists(pk)"
    )

def lambda_handler(event, context):
    for rec in event["Records"]:
        body = json.loads(rec["body"])
        order = body["order"]
        meta = body["meta"]

        order_id = order.get("order_id", "UNKNOWN")
        ok = meta.get("validation_ok", False)
        reason = meta.get("validation_reason", "unknown")

        # If invalid: write REJECTED then raise to force retry -> DLQ
        if not ok:
            put_status(order_id, "REJECTED", reason=reason)
            log("ERROR", "Order rejected (will go to DLQ after retries)", order_id=order_id, reason=reason)
            raise Exception(f"Order rejected: {reason}")

        # Valid order: idempotent insert
        try:
            put_if_not_exists(order_id, "PROCESSED", amount=order.get("amount"), currency=order.get("currency"))
            log("INFO", "Order processed", order_id=order_id)
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                # Duplicate
                put_status(order_id, "DUPLICATE")
                log("WARN", "Duplicate order ignored", order_id=order_id)
            else:
                log("ERROR", "DynamoDB error", order_id=order_id, error=str(e))
                raise

    return {"status": "OK"}
