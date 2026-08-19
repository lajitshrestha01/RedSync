import os
from dotenv import load_dotenv
from openai import OpenAI
from prompt import get_system_prompt
from tool import tools

load_dotenv()

api_key = os.getenv("CEREBRAS_API_KEY")
base_url = os.getenv("BASE_URL")

if not api_key or not base_url: 
    print("Either api_key or base_url is missing in .env")
    exit()
    
client = OpenAI(api_key=api_key, base_url=base_url)


try:
    def get_next_action(state): 
        system_prompt = get_system_prompt(state)
        user_message = state.user_input
        
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
                ],
            model="gemma-4-31b",
            tools=tools, 
            tool_choice="auto"
            )
        
        return response.choices[0].message
        
        
        
except Exception as e:
    print(f"An error occurred: {e}")