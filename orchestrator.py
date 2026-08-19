import json
from llm import get_next_action
from tool import create_draft, search_subreddit
from validators import evaluate_draft

class Orchestrator: 
    ACTIONS =  {
                    "create_draft" : create_draft, 
                    "search_subreddit": search_subreddit,
    }
    VALIDATORS = {
        "create_draft": lambda state: evaluate_draft(state.user_input, state.draft["body"])
    }
    
                
    def run(self, state):
        max_steps = 10 
        for step in range(max_steps):
            result = get_next_action(state)
        
            
            # 1. If no tools are called, the agent is done
            if not result.tool_calls: 
                state.agent_status = "completed"
                break
            
                           
            # 2. Extract the tool call data from the API object
            tool_call = result.tool_calls[0]
            actions_name = tool_call.function.name
            arguments_string = tool_call.function.arguments
                
            # --- DEBUGGING BLOCK ---
            print(f"\n--- DEBUG INFO ---")
            print(f"Tool Requested: {actions_name}")
            print(f"Raw Arguments String: {repr(arguments_string)}")
                # -----------------------
            
            try:
            # 3. Parse the JSON string into a Python dictionary
                arguments_dict = json.loads(arguments_string)
            
            except json.JSONDecodeError as e: 
                print(f"Bad Json from llm : {e}")
                state.validation_result = f"Your last tool call had invalid json arguments: {e}" 
                continue 

            # 4. Execute the tool
            if actions_name not in self.ACTIONS:
                state.validation_result = f"Unkwon tool: {actions_name}"
                continue
                
            try: 
                self.ACTIONS[actions_name](state, **arguments_dict)
            
            except Exception as e: 
                print(f"Tool execution failed with error: {e}")
                state.agent_status = "failed"
                break
            
            validator = self.VALIDATORS.get(actions_name)
            if validator: 
                val_result = validator(state)
                print(f"Validation Result : {val_result}")
                
                if not val_result.get("is_valid", True): 
                    state.validation_result = val_result.get("reason")
                    state.draft = None
                    print("Draft rehected! forcing LLM to retry")
            
                else: 
                    state.validation_result = "Passed"
            else: 
                state.agent_status = "max_steps_reached"
            
        return state