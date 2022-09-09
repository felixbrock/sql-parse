from flask import Flask, request
import sqlfluff
import base64
import json

app = Flask(__name__)

# todo - add security

@app.route("/sql", methods=['POST'])
def parseSQL():
    queryParameters = request.args
    body = request.json

    sql = base64toUTF8(body['sql'])

    dbtQueryParamKey = 'is_dbt'

    if dbtQueryParamKey in queryParameters and queryParameters[dbtQueryParamKey] == 'true':
        parsedSQL = sqlfluff.parse(sql, queryParameters['dialect'], './dbt.sqlfluff')
    else:
        parsedSQL = sqlfluff.parse(sql, queryParameters['dialect'], './.sqlfluff')

    # todo - This is just a workaround. In previous versions a dict object was returned rather than a JSON string (to be avoided in the future).
    # This led to receiving a modified object on the client side which was automatically alphabetically ordered.
    # Since the order of the object has an impact on how the lineage is analyzed we have to go with this workaround for now.
    # Before developing the lineage analysis further this needs to be fixed.
    # return json.dumps(sortOD(parsedSQL))
    parsedSQLSorted = sortOD(parsedSQL)

    return json.dumps(parsedSQLSorted)
    
def sortOD(od):
    res = {}
    for k, v in sorted(od.items()):
        if isinstance(v, dict):
            res[k] = sortOD(v)
        elif isinstance(v, list):
            sortedElements = []
            for element in v:
                sortedElements.append(sortOD(element))
            res[k] = sortedElements
        else:
            res[k] = v
    return res

def base64toUTF8(base64String):
    base64Encoded = base64String.encode("UTF-8")
    base64BytesDecoded = base64.b64decode(base64Encoded)
    return base64BytesDecoded.decode('utf-8') 
