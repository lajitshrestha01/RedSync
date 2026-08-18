def create_draft(state): 
    state.draft = {
        "title" : "I build an n8n automation that saves me 10 hours every week", 
        "body": "Test draft"
    }

def search_subreddit(state): 
    state.subreddit_candidates = ["r/saas", "r/AI_agent"]
    
def validate_result(state):
    state.validate_result = {
        "title": "validated", 
        "body": "Test validated"
    }
    
