# Deepgram Python Starter

This sample demonstrates interacting with the Deepgram API from Python. It uses the Deepgram Python SDK, and has a React companion application to interact with the Python integration.

## Sign-up to Deepgram

Before you start, it's essential to generate a Deepgram API key to use in this project. [Sign-up now for Deepgram](https://console.deepgram.com/signup).

## Quickstart

### Manual

Follow these steps to get started with this starter application.

#### Clone the repository

Go to GitHub and [clone the repository](https://github.com/deepgram-starters/deepgram-python-starters).

#### Install dependencies

Install the project dependencies in the `Starter 01` directory.

```bash
cd ./Starter-01
pip install -r requirements.txt
```

#### Edit the config file

Copy the text from `.env-sample` and create a new file called `.env`. Paste in the code and enter your API key you generated in the [Deepgram console](https://console.deepgram.com/).

```bash
port=3000
deepgram_api_key=api_key
```

#### Run the application

Once running, you can [access the application in your browser](http://localhost:5000/).

```bash
flask run --debug
```
