from flask import Flask, request
import sqlfluff
import base64

app = Flask(__name__)

# todo - add security

@app.route("/sql", methods=['POST'])
def parseSQL():
    queryParameters = request.args
    body = request.json

    sql = base64toUTF8(body['sql'])

    return sqlfluff.parse(sql, queryParameters['dialect'])
    


def base64toUTF8(base64String):
    base64Encoded = base64String.encode("UTF-8")
    base64BytesDecoded = base64.b64decode(base64Encoded)
    print(base64BytesDecoded)
    return base64BytesDecoded.decode('utf-8') 
