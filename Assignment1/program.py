from flask import Flask, request, jsonify
import rocksdb
import uuid
import subprocess

app = Flask(__name__) # root path

@app.route("/api/v1/scripts/<id>", methods = ['GET'])
def call_script(id):
    try:
        db = rocksdb.DB("assignment1.db", rocksdb.Options(create_if_missing = True))
        script = db.get(str.encode(id))
        if script:
            response = subprocess.check_output(["python3.6", "-c", script])
            return response, 201
        else:
            return "Script not found in DB", HttpResponse(status = 404)
    except subprocess.CalledProcessError as e:
            return "Error occurred"

@app.route("/api/v1/scripts", methods = ['POST'])
def save_script():
    db = rocksdb.DB("assignment1.db", rocksdb.Options(create_if_missing = True))
    id = str(uuid.uuid4())
    script = request.files['data']
    db.put(str.encode(id), script.read())
    return jsonify({"script-id": id})




if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)