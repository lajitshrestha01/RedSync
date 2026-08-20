from enum import Enum
from dataclasses import dataclass

class FailureType(Enum): 
    TRANSIENT = "transient"
    CORRECTABLE = "correctable"
    USER_INPUT_REQUIRED = "user_input_required"
    UNRECOVERABLE = "unrecoverable"
    


@dataclass
class Failure: 
    type: FailureType
    reason: str
    retryable: bool 

MAX_RETRIES = 3

    
def handle_failure(failure: Failure, state) -> str: 
    failure_key = (failure.type, getattr(state, "current_action", None))
    
    if failure_key == getattr(state, "last_failure_reason", None): 
        state.failure_streak = getattr(state, "failure_streak", 0) + 1
    else: 
        state.failure_streak = 1
    
    state.last_failure_reason = failure.reason
    state.validation_result = failure.reason
    
    if failure.retryable and state.failure_streak >= MAX_RETRIES: 
        state.agent_status = "user_input_needed"
        state.validation_result = (
            f"Stuck after {state.failure_streak} attempts: {failure.reason}"
        )
        return "pause"
        
    if failure.type in (FailureType.TRANSIENT, FailureType.CORRECTABLE): 
        state.agent_status = "retrying"
        state.validation_result = failure.reason
        return "continue"
        
    
    if failure.type == FailureType.USER_INPUT_REQUIRED: 
        state.agent_status = "user_input_needed"
        state.validation_result = failure.reason
        return "pause"
    
    #Unrecoverable 
    state.agent_status = "Failed"
    state.validation_result = failure.reason
    return "stop"