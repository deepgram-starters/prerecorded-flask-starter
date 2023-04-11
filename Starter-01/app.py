import json
from flask import Flask, jsonify, request, abort, make_response
from deepgram import Deepgram
import os
from dotenv import load_dotenv
load_dotenv()

app =   Flask(__name__, static_folder='./build', static_url_path='/')
deepgram = Deepgram(os.getenv("deepgram_api_key"))

@app.route('/api', methods = ['POST'])
def transcribe():
	body, files = request
	url, features, model, version, tier = body
	dgFeatures = json.loads(features)
	dgRequest

	try:
		if url and url.startswith("https://res.cloudinary.com/deepgram"):
			dgRequest = { 
				"url": url 
			}

		if files["file"]:
			file = files["file"]
			dgRequest = {
				"mimetype": file.mimetype,
				"buffer": file.stream.read()
			}

		if not dgRequest:
			raise Exception("Error: You need to choose a file to transcribe your own audio.")
		
		dgFeatures["model"] = model;
		
		if version:
			dgFeatures["version"] = version;
		
		if model == "whisper":
			dgFeatures["tier"] = tier;

		transcription = deepgram.transcription.prerecorded(dgRequest, dgFeatures)

		return jsonify({
			"model": model,
			"version": version,
			"tier": tier,
			"dgRequest": dgRequest,
			"dgFeatures": dgFeatures,
			"transcription": transcription,
		})
	except Exception as err:
		if err.message:
			abort(make_response(jsonify(err=err.message), 500))
		else:
			abort(make_response(jsonify(err=err), 500))

@app.route('/', methods = ['GET'])
def index():
	return app.send_static_file('index.html')

if __name__=='__main__':
	app.run(debug=True)
