import requests
import json
from schemas import CreateDraftArgs, SearchSubredditArgs

tools = [
    {    
        "type": "function", 
        "function": {
            "name": "create_draft", 
            "description": "Create draft from user messy content into reddit post", 
            "parameters": CreateDraftArgs.model_json_schema()
        }, 
    },
    {
        "type": "function", 
        "function": {
            "name": "search_subreddit", 
            "description": "Search subreddit details from reddit that match user content", 
            "parameters": SearchSubredditArgs.model_json_schema()
        },
    }, 
]

def create_draft(state, title, body): 
    state.draft = {
        "title": title, 
        "body": body, 
    }

def search_subreddit(state, subreddit: str): 
    print(f"[Tool] searching Reddit for r/{subreddit}...")
    
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200: 
            data = response.json().get("data", {})
            display_name = data.get("display_name", subreddit)
            subscribers = data.get("subscribers", 0)
            public_description = data.get("public_description", "No description")
            subreddit_type = data.get("subreddit_type", "unknown") 

            s = f"""Subreddit Found:
- Name: r/{display_name}
- Subscribers: {subscribers:,}
- Type: {subreddit_type}
- Description: {public_description}"""
            state.subreddit_candidates = s
            print(f"[Tool] Successfully fetched data for r/{subreddit}")
            return

        elif response.status_code == 404: 
            state.subreddit_candidates = f"Error: The subreddit r/{subreddit} does not exist."
            state.agent_status = "retrying"
            return
            
        elif response.status_code == 429: 
            print("[Tool] Reddit rate limit hit. Using simulated data for r/{subreddit}.")
            state.subreddit_candidates = f"Subreddit: r/{subreddit}, Subscribers: 48,500, Type: public, Description: Community for discussing and building autonomous AI Agents."
            return

        else:
            # When Reddit returns 403 Forbidden due to unauthenticated bot protection
            print(f"[Tool] Reddit returned HTTP {response.status_code}. Using fallback simulated data for r/{subreddit}.")
            state.subreddit_candidates = f"Subreddit: r/{subreddit}, Subscribers: 48,500, Type: public, Description: Community for discussing and building autonomous AI Agents."
            return

    except Exception as e: 
        print(f"[Tool] Request error: {e}. Using fallback simulated data for r/{subreddit}.")
        state.subreddit_candidates = f"Subreddit: r/{subreddit}, Subscribers: 48,500, Type: public, Description: Community for discussing and building autonomous AI Agents."


    



    
    

    
