from openai import OpenAI
from config.settings import OPENAI

OPENAI = OpenAI(api_key=OPENAI)


def make_api_call(messages, model="gpt-3.5-turbo", max_tokens=100):
    response = OPENAI.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=max_tokens
    )
    return response.choices[0].message


def embed(text):
    response = OPENAI.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )

    return response.data[0].embedding


def get_response(context):
    message = make_api_call(context)
    context.append({"role": "assistant", "content": message.content})
    return message.content


def respond_to_prompt(prompt, max_tokens=500):
    context = [{"role": "system", "content": prompt}]
    message = make_api_call(context, max_tokens=max_tokens)
    return message.content
