from flask import Flask
from flask import jsonify, request
from DOA import get_first_data,get_all_collection_data,insert_data,update_data
import numbers

try:
    app = Flask(__name__)
except Exception as err:
    print ("failed to start the application! ", err)

@app.route('/<api>', defaults={'name' : None, 'version': None}, methods = ['POST', 'GET'])
@app.route('/<api>/<name>', defaults={'version': None}, methods = ['POST', 'GET'])
@app.route('/<api>/<name>/<version>', methods = ['POST', 'GET'])
def get_first_api(api:str,name:str = None ,version:str = None):
    try:
        result, _ = get_first_data(api,name,version)
        return jsonify(result)
    except Exception as err:
        print (err)
        return handleException(err)

@app.route('/all/<api>' , methods = ['POST', 'GET'])
def get_all_data(api:str):
    try:
        result = get_all_collection_data(api)
        return jsonify(result)
    except Exception as err:
        print (err)
        return handleException(err)

@app.route('/override/<api>', defaults={'name' : 'default', 'version': '1'}, methods = ['POST', 'GET'])
@app.route('/override/<api>/<name>', defaults={'version': '1'}, methods = ['POST', 'GET'])
@app.route('/override/<api>/<name>/<version>', methods = ['POST', 'GET'])
def get_and_override(api:str,name:str,version:str):
    try:
        result, id = get_first_data(api,name,version)
        update_data(api,id,result)
        return jsonify(result)
    except Exception as err:
        print (err)
        return handleException(err)

@app.route('/add/<api>', defaults={'name' : 'default', 'version': '1'}, methods = ['POST'])
@app.route('/add/<api>/<name>', defaults={'version': '1'}, methods = ['POST'])
@app.route('/add/<api>/<name>/<version>', methods = ['POST'])
def insert_new(api:str,name:str,version:str):
    try:
        result = insert_data(api,name,version, request.data.decode("utf-8")) # remove the string of the body
        return jsonify(result)
    except Exception as err:
        print (err)
        return handleException(err)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path: str):
    if (path.__contains__('fake')):
        k = path.split('/')
        api = k[0]
        name = version = None
        if (k[1] != 'fake'):
            name = k[1]
            if (k[2] != 'fake'):
                version = k[2]
        return get_first_api(api, name, version)
    return handle_404(None)
    
@app.errorhandler(404)
def handle_404(e):
    # handle all other routes here
    return 'Unsupported route! use /<api>/<name>/<version>',404 

def handleException(err: Exception):
    responseCode = err.args[1] if len(err.args) > 1 and isinstance(err.args[1], numbers.Number) else 500
    return err.args[0], responseCode
