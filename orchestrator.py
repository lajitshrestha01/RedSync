import json
from llm import get_next_action
from tool import create_draft, search_subreddit, validate_result

class Orchestrator: 
    def run(self, state):
        max_steps = 10 
        for step in range(max_steps):
            result = get_next_action(state)
        
            actions =  {
                "create_draft" : create_draft, 
                "search_subreddit": search_subreddit, 
                "validate_result": validate_result,
            }
            
            # 1. If no tools are called, the agent is done
            if not result.tool_calls: 
                state.agent_status = "completed"
                break
            
            try:               
                # 2. Extract the tool call data from the API object
                tool_call = result.tool_calls[0]
                actions_name = tool_call.function.name
                arguments_string = tool_call.function.arguments
                
                # --- DEBUGGING BLOCK ---
                print(f"\n--- DEBUG INFO ---")
                print(f"Tool Requested: {actions_name}")
                print(f"Raw Arguments String: {repr(arguments_string)}")
                # -----------------------

                # 3. Parse the JSON string into a Python dictionary
                arguments_dict = json.loads(arguments_string)
                
                print(f"Parsed Dictionary Type: {type(arguments_dict)}")
                print(f"------------------\n")

                # 4. Execute the tool
                if actions_name in actions:
                    actions[actions_name](state, **arguments_dict)
            
            except Exception as e: 
                print(f"Tool execution failed with error: {e}")
                state.agent_status = "failed"
                break
            
        return state