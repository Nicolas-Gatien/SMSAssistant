
def convert_context_to_transcript(user_name, assistant_name, context):
    transcript = ""
    for message in context:
        if message["role"] == "user":
            transcript += f"{user_name}: {message['content']}\n"
        if message["role"] == "assistant":
            transcript += f"{assistant_name}: {message['content']}\n"

    return transcript


def fabricate_transcript_abstraction_prompt(context):
    transcript = convert_context_to_transcript("Nicolas", "Muse", context)
    prompt = f"""
    {transcript}
    What 5 high-level abstractions can you make about the individual people in the above transcript?
    Make abstractions about the specific individuals. (ex: "1. Nicolas is an aspiring adventurer because...")
    Do not combine the abstractions into a "both" statement. (bad ex: "1. Both Nicolas & Muse...")
    """
    return prompt
