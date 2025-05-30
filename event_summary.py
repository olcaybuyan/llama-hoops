import json
import os
from typing import List
from utils_llm import load_prompt_file
from llama_api_client import LlamaAPIClient
from models.summary_length import SummaryLength
from models.transcription_segment import TranscriptionSegment

client = LlamaAPIClient(api_key=os.environ.get("LLAMA_API_KEY"))

def highlight_summary(transcripts: List[TranscriptionSegment], length=SummaryLength.SHORT) -> str:
    transcription_json = json.dumps([item.to_dict() for item in transcripts])
    base_prompt = load_prompt_file("prompts/event_summary_prompt.md")

    event_summary_xxl_prompt = load_prompt_file("prompts/event_summary_duration/event_summary_xxl_prompt.md")
    event_summary_long_prompt = load_prompt_file("prompts/event_summary_duration/event_summary_long_prompt.md")
    event_summary_medium_prompt = load_prompt_file("prompts/event_summary_duration/event_summary_medium_prompt.md")
    event_summary_short_prompt = load_prompt_file("prompts/event_summary_duration/event_summary_short_prompt.md")
    length_prompt = ""
    if length == SummaryLength.XXL:
        length_prompt = event_summary_xxl_prompt
    elif length == SummaryLength.LONG:
        length_prompt = event_summary_long_prompt
    elif length == SummaryLength.MEDIUM:
        length_prompt = event_summary_medium_prompt
    else:
        length_prompt = event_summary_short_prompt

    prompt = base_prompt.replace("{LENGTH_PROMPT}", length_prompt)
    completion = client.chat.completions.create(
        model="Llama-4-Maverick-17B-128E-Instruct-FP8",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": transcription_json
            }
        ],
        temperature=0.7
    )
    output = completion.completion_message.content.text
    return output

if __name__ == "__main__":
    from test_data.demo_transcript import demo_transcript
    result = highlight_summary(demo_transcript, SummaryLength.MEDIUM)
    print(f"Event Summary: {result}")
