def get_next_action(state): 
    if state.draft is None: 
        return{
            "action" : "create_draft", 
            "arguments": {}
        }
    
    elif state.subreddit_candidates is None: 
        return {
            "action": "search_subreddit", 
            "arguments": {}
        }
    elif state.validate_result is None: 
        return{
            "action": "validate_result", 
            "arguments": {}
        }
    else: 
        return {
            "action": "finish", 
            "arguements": {}
        }