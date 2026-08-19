tools = [
    
    {    
    "type": "function", 
    "function": {
        "name" : "create_draft", 
        "description": "Create draft from user messy content into reddit post", 
        "parameters": {
            "type": "object", 
            "properties": {
                "title" : {
                    "type": "string", 
                    "description": "Title of reddit content e.g how i create a agent under 24 hours",     
                }, 
                "body": {
                    "type" : "string",
                    "description": "A reddit content from messy thought of user "

                },   
            }, 
            "required": ["title", "body"]
            
        }
    }
    }, 
    
    {
        "type": "function", 
        "function": {
        "name": "search_subreddit", 
        "description": "Search sub_reddit from reddit that match user content", 
        "parameters": {
            "type": "object", 
            "properties": {
                "subreddit": {
                    "type": "string", 
                    "description": "An sub_reddit like r/AI_agent, r/entrepreneur"
                }, 
            }, 
            "required": ["subreddit"],
        }
    }
        
    }

]

def create_draft(state, title, body): 
    state.draft = {
        "title" : title, 
        "body": body, 
    }

def search_subreddit(state, subreddit): 
    state.subreddit_candidates = [subreddit]
    
def validate_result(state):
    state.validate_result = {
        "title": "validated", 
        "body": "Test validated"
    }
    
