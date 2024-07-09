#!/usr/bin/python3
import requests
from requests.exceptions import Timeout
from os import getenv
import re
"""Logic for text processing, flashcard creation"""

API_TOKEN = getenv("HUGGINGFACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def query(payload):
	"""
	Sends a POST request to the Hugging Face API with the provided payload.

	Args:
	payload (dict): Dictionary containing the data to be sent to the API.
		Expected keys: 'inputs' (string containing the text and instructions).

	Returns:
	dict: The JSON response from the API, or None if an error occurs.

	Raises:
	requests.exceptions.RequestException: For other network or request-related errors.
	"""
	try:
		response = requests.post(API_URL, headers=headers, json=payload)
		return response.json()
	except Timeout:
		print("Error: Network timeout occurred")
		return None
	except requests.exceptions.RequestException as e:
		print(f"Error: Request failed with {e}")
		return None


instructions = "generate question(Q) and answer(A) pair from the text above"


def main(text):
	text = text.replace('\n', ' ')
	text = text.replace('  ', ' ')
	output = query({
		'inputs': f"{text}. {instructions}",
		})

	if not output:
		print("Error: No output received from API")
		return {}
	
	print(output)
	questions= re.findall("\sQ:(.*)\?", output[0]['generated_text'])
	answers= re.findall("\sA:(.*)\.",  output[0]['generated_text'])

	if len(questions) != len(answers):
		print("Warning: Mismatched number of questions and answers")
		return {}
	
	dict_= {}
	for i in range(len(questions)):
		try:
			dict_[questions[i]]= answers[i]
		except Exception:
			pass
	return dict_
