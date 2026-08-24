import json
from llm import get_next_action
from tool import create_draft, search_subreddit
from validators import evaluate_draft
from failure import (
    Failure,
    FailureType,
    Action,
    handle_failure,
    map_validation_to_failure,
)

class Orchestrator: 
    ACTIONS = {
        "create_draft": create_draft, 
        "search_subreddit": search_subreddit,
    }

    VALIDATORS = {
        "create_draft": lambda state: evaluate_draft(
            state.user_input, 
            state.draft.get("body", "") if isinstance(state.draft, dict) else "", 
            context=state.subreddit_candidates
        ),
        "search_subreddit": lambda state: {
            "is_valid": not (isinstance(state.subreddit_candidates, str) and state.subreddit_candidates.startswith("Error:")),
            "reason": state.subreddit_candidates if (isinstance(state.subreddit_candidates, str) and state.subreddit_candidates.startswith("Error:")) else "Subreddit found successfully",
            "has_hallucination": False
        }
    }
    
    def run(self, state):
        max_steps = 10 
        for step in range(max_steps):
            result = get_next_action(state)
            
            # 1. Handle completion or text/clarification response when no tools are called
            if not result.tool_calls:
                if state.draft and state.validation_result == "Passed":
                    state.agent_status = "completed"
                    break
                
                # LLM responded with text (e.g. asking for missing details or clarifying)
                if result.content:
                    print(f"\n[Agent]: {result.content}\n")
                    user_clarification = input("Please provide the missing details (or type 'quit' to stop): ").strip()
                    if user_clarification.lower() == 'quit':
                        state.agent_status = "aborted"
                        break
                    state.user_input += f"\nAdditional details from user: {user_clarification}"
                    state.agent_status = "running"
                    state.failure_streak = 0
                    continue
                else:
                    failure = Failure(
                        type=FailureType.CORRECTABLE, 
                        reason="You responded without calling a tool. You must call search_subreddit or create_draft to proceed.", 
                        retryable=True
                    )
                    signal = handle_failure(failure, state)
                    if signal == Action.STOP: 
                        break
                    continue
            
            # 2. Extract tool call from LLM response
            tool_call = result.tool_calls[0]
            action_name = tool_call.function.name
            arguments_string = tool_call.function.arguments
                
            # --- DEBUGGING BLOCK ---
            print(f"\n--- DEBUG INFO (Step {step + 1}/{max_steps}) ---")
            print(f"Tool Requested: {action_name}")
            print(f"Raw Arguments: {repr(arguments_string)}")
            
            # 3. Parse JSON arguments with resilience
            try:
                arguments_dict = json.loads(arguments_string)
            except json.JSONDecodeError as e: 
                print(f"[Orchestrator] Bad JSON from LLM: {e}")
                failure = Failure(
                    type=FailureType.CORRECTABLE,
                    reason=f"Your last tool call had invalid JSON arguments: {e}",
                    retryable=True
                )
                signal = handle_failure(failure, state)
                if signal == Action.STOP:
                    break
                continue 

            # 4. Validate tool existence
            if action_name not in self.ACTIONS:
                failure = Failure(
                    type=FailureType.CORRECTABLE,
                    reason=f"Unknown tool '{action_name}'. Available tools: {list(self.ACTIONS.keys())}",
                    retryable=True
                )
                signal = handle_failure(failure, state)
                if signal == Action.STOP:
                    break
                continue
                
            # 5. Execute the requested tool
            try: 
                state.current_action = action_name
                self.ACTIONS[action_name](state, **arguments_dict)
            except Exception as e: 
                print(f"[Orchestrator] Tool execution failed with error: {e}")
                failure = Failure(
                    type=FailureType.UNRECOVERABLE,
                    reason=f"Tool execution error: {e}",
                    retryable=False
                )
                handle_failure(failure, state)
                break
            
            # 6. Run post-execution validator if registered
            validator = self.VALIDATORS.get(action_name)
            if validator: 
                val_result = validator(state)
                print(f"[Orchestrator] Validation Result: {val_result}")
                
                if not val_result.get("is_valid", True): 
                    if action_name == "create_draft":
                        state.draft = None  # Reset rejected draft
                    
                    failure = map_validation_to_failure(val_result, state)
                    signal = handle_failure(failure, state)
                    print(f"[Orchestrator] Action rejected (Signal: {signal.value}). Reason: {failure.reason}")
                    
                    if signal == Action.PAUSE or state.agent_status == "user_input_needed": 
                        print(f"[Orchestrator] The LLM needs clarification: {state.validation_result}")
                        user_correction = input("Please provide the missing details (or type 'quit' to stop): ")
                        
                        if user_correction.strip().lower() == 'quit': 
                            state.agent_status = "aborted"
                            break
                        state.user_input += f"\nAdditional Details from user: {user_correction.strip()}"
                        state.agent_status = "running"
                        state.failure_streak = 0
                        continue
                    
                    elif signal == Action.STOP: 
                        break
                    
                    elif signal == Action.CONTINUE:
                        continue
            
                else:
                    state.validation_result = "Passed"
                    state.failure_streak = 0
            else:
                state.validation_result = "Passed"
                state.failure_streak = 0
                
        return state