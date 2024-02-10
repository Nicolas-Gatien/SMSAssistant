from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
from config.settings import MY_PHONE, CONVERSATION_TIMEOUT
from openai_handler import get_response
from transcript_handler import save_transcript
import json
import os


APP = Flask(__name__)

PERSONA = ""
with open("config/persona.txt", 'r') as file:
    PERSONA = file.read()

context = [{"role": "system", "content": PERSONA}]
last_message_time = datetime.now()


@APP.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    global context, last_message_time

    time_since_last_message = datetime.now() - last_message_time
    if time_since_last_message.total_seconds() > CONVERSATION_TIMEOUT and len(context) > 1:
        save_transcript(context)
        context = [{"role": "system", "content": PERSONA}]
        print("reset convo")

    resp = MessagingResponse()
    message_sender = request.values.get("From")
    message_body = request.values.get("Body")

    if message_sender != MY_PHONE:
        resp.message("You are not authorized, message Nico for access.")
        return str(resp)

    context.append({"role": "user", "content": message_body})
    response = get_response(context)

    last_message_time = datetime.now()

    resp.message(response)
    return str(resp)


if __name__ == "__main__":
    APP.run(debug=True, port=5002)