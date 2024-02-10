import json
from openai_handler import respond_to_prompt


def save_transcript(conversation):
    title = respond_to_prompt(f"Summarize the following transcript in 3 words or less. Do not include punctuation: {conversation}")

    title = title.replace(".", "")
    title = title.replace(",", "")
    title = title.replace(" ", "_")
    title = title.lower()

    conversation.pop(0)

    with open(f"transcripts/{title}.txt", 'w') as transcript:
        transcript.write(json.dumps(conversation, indent=3))
    transcript.close()