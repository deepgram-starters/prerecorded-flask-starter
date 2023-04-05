from flask import Flask, jsonify, request
app =   Flask(__name__, static_folder='./build', static_url_path='/')

@app.route('/api', methods = ['POST'])
def api_post():
    try:
        body = request.form
        file = request.files['file']
        print(body, file)
        dgRequest = {}

        return jsonify({})
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

@app.route('/', methods = ['GET'])
def index():
    return app.send_static_file('index.html')

if __name__=='__main__':
    app.run(debug=True)
