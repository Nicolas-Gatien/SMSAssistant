from datetime import datetime
from config.settings import CONVERSATION_TIMEOUT
from openai_handler import get_response, respond_to_prompt, embed
from transcript_handler import save_transcript
from prompt_factory import fabricate_transcript_abstraction_prompt
from numpy import dot
from numpy.linalg import norm



with open("config/persona.txt", 'r') as file:
    PERSONA = file.read()

context = [{"role": "system", "content": PERSONA}]
last_message_time = datetime.now()


class Memory:
    def __init__(self, timestamp, importance, text):
        self.timestamp = timestamp  # DECAY IS CURRENTLY CALCULATED FOR EVERY SINGLE MEMORY
        self.importance = importance
        self.text = text
        self.meaning = embed(text)
        self.relevance = 0

    def __lt__(self, other):
        return self.relevance < other.relevance


memory_stream = []


def get_abstractions(context):
    abstractions_string = respond_to_prompt(fabricate_transcript_abstraction_prompt(context), 500)
    abstractions = abstractions_string.split('\n')

    for x, abstract in enumerate(abstractions):
        if abstract == "":
            abstractions.pop(x)
            continue

        abstractions[x] = abstract[3:]

    return abstractions


def get_relevant_memories(text_query):
    query = embed(text_query)

    for memory in memory_stream:
        cos_sim = dot(memory.meaning, query) / (norm(memory.meaning) * norm(query))
        memory.relevance = cos_sim

    memory_stream.sort(reverse=True)
    print(memory_stream[0].text)


def save_memories(context):
    abstractions = get_abstractions(context)

    for abstract in abstractions:
        memory_stream.append(Memory(datetime.now(), 5, abstract))

    for memory in memory_stream:
        print(f"{memory.timestamp}: {memory.text}")


def generate_response(prompt):
    global context, last_message_time

    time_since_last_message = datetime.now() - last_message_time
    if time_since_last_message.total_seconds() > CONVERSATION_TIMEOUT and len(context) > 1:
        context = reset_conversation(context)

    context.append({"role": "user", "content": prompt})
    response = get_response(context)

    last_message_time = datetime.now()

    return response


def reset_conversation(context):
    save_transcript(context)
    save_memories(context)
    print("Reset Conversation")

    return [{"role": "system", "content": PERSONA}]


while True:
    get_relevant_memories("Mole")
    print(generate_response(input("User: ")))

