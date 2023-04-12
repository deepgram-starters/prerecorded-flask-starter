import json
from flask import Flask, jsonify, request, abort, make_response
from deepgram import Deepgram
import os
from dotenv import load_dotenv
load_dotenv()

app =   Flask(__name__, static_folder='./build', static_url_path='/')

@app.route('/', methods = ['GET'])
def index():
	return app.send_static_file('index.html')

deepgram = Deepgram(os.getenv("deepgram_api_key"))

@app.route('/api', methods = ['POST'])
async def transcribe():
	form = request.form
	files = request.files
	url = form.get('url')
	features = form.get('features')
	model = form.get('model')
	version = form.get('version')
	tier = form.get('tier')

	dgFeatures = json.loads(features)
	dgRequest = None

	try:
		if url and url.startswith("https://res.cloudinary.com/deepgram"):
			dgRequest = { 
				"url": url 
			}

		if 'file' in files:
			file = files.get('file')
			dgRequest = {
				"mimetype": file.mimetype,
				"buffer": file.stream.read()
			}
		
		dgFeatures["model"] = model;
		
		if version:
			dgFeatures["version"] = version;
		
		if model == "whisper":
			dgFeatures["tier"] = tier;

		if not dgRequest:
			raise Exception("Error: You need to choose a file to transcribe your own audio.")

		transcription = await deepgram.transcription.prerecorded(dgRequest, dgFeatures)

		return jsonify({
			"model": model,
			"version": version,
			"tier": tier,
			"dgFeatures": dgFeatures,
			"transcription": transcription,
		})
	except Exception as error:
		return json_abort(error)

def json_abort(message):
	print(message)
	return abort(make_response(jsonify(err=str(message)), 500))

if __name__=='__main__':
	app.run(debug=True)
