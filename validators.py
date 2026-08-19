import os 
import json
from openai import OpenAI
from dotenv import load_dotenv
from prompt import evaluate_draft_prompt

load_dotenv()

api_key = os.getenv("CEREBRAS_API_KEY")
base_url = os.getenv("BASE_URL")

client = OpenAI(api_key=api_key, base_url=base_url)

def evaluate_draft(user_input, draft_body):
    #1.  provide the deteministic ruels to the llm
    system_prompt = evaluate_draft_prompt()
    user_message = f"Original Thought: {user_input} \n\nDraft: {draft_body}"
    
    response = client.chat.completions.create(
        model="gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt}, 
            {"role": "user", "content": user_message}
        ], 
        response_format={"type": "json_object"}
    )
    
    result_text = response.choices[0].message.content
    return json.loads(result_text)

