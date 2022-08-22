import json
import sqlfluff
import base64

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    request = event

    queryParameters = request['queryStringParameters']
    body = json.loads(request['body']) if isinstance(request['body'], str) else request['body']

    sql = base64toUTF8(body['sql'])

    dialectQueryParamKey = 'dialect'

    if not dialectQueryParamKey in queryParameters:
        return {
        "statusCode": 400,
        "body": 'Missing dialect query parameter',
    }

    isDbtQueryParamKey = 'isDbt'

    # if isDbtQueryParamKey in queryParameters and queryParameters[isDbtQueryParamKey] == 'true':
    parsedSQL = sqlfluff.parse(sql, queryParameters[dialectQueryParamKey], './.sqlfluff')
    # else:
        # parsedSQL = sqlfluff.parse(sql, queryParameters[dialectQueryParamKey])
            
    return {
        "statusCode": 200,
        "body": json.dumps(parsedSQL),
    }

def base64toUTF8(base64String):
    base64Encoded = base64String.encode("UTF-8")
    base64BytesDecoded = base64.b64decode(base64Encoded)
    return base64BytesDecoded.decode('utf-8') 

    


