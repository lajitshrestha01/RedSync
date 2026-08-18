from fake_llm import get_next_action
from tool import create_draft, search_subreddit, validate_result

class Orchestrator: 
    def run(self, state):
        max_steps =10 
        for step in range(max_steps):
            result = get_next_action(state)
        
            actions =  {
            "create_draft" : create_draft, 
            "search_subreddit": search_subreddit, 
            "validate_result": validate_result,

            }
            
            if result['action'] == "finish":
                if(state.draft is not None and state.subreddit_candidates is not None and state.validate_result is not None):
                    state.agent_status = "completed"
                    break
            
                            
            if result['action'] not in actions:
                raise KeyError(f"Action {result['action']} does not exists")
            
            try: 
                actions[result["action"]](state)
            
            except Exception as e: 
                print(f"Tool {result['action']} failed with error as {e}")
                state.agent_status = "failed"
                break
            
        return state