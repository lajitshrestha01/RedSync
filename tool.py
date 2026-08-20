from schemas import CreateDraftArgs, SearchSubredditArgs
tools = [
    
    {    
    "type": "function", 
    "function": {
        "name" : "create_draft", 
        "description": "Create draft from user messy content into reddit post", 
        "parameters": CreateDraftArgs.model_json_schema()
    }, 
    },
    
    {
        "type": "function", 
        "function": {
        "name": "search_subreddit", 
        "description": "Search sub_reddit from reddit that match user content", 
        "parameters": SearchSubredditArgs.model_json_schema()
        
    },
    }, 

]

def create_draft(state, title, body): 
    state.draft = {
        "title" : title, 
        "body": body, 
    }

def search_subreddit(state, subreddit): 
    state.subreddit_candidates = [subreddit]
    

    
