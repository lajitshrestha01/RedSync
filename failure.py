from enum import Enum
from dataclasses import dataclass
from state import AgentState

class FailureType(Enum): 
    TRANSIENT = "transient"
    CORRECTABLE = "correctable"
    USER_INPUT_REQUIRED = "user_input_required"
    UNRECOVERABLE = "unrecoverable"

class Action(str, Enum):
    CONTINUE = "continue"
    PAUSE = "pause"
    STOP = "stop"

@dataclass
class Failure: 
    type: FailureType
    reason: str
    retryable: bool = True

MAX_RETRIES = 3


def classify_and_decide(failure: Failure, current_streak: int) -> tuple[Action, int]:
    """
    Pure policy function: Decides the action based on failure type, retryability, and streak count.
    Does not mutate state.
    """
    # 1. Breach of maximum retry limit
    if failure.retryable and current_streak >= MAX_RETRIES:
        return Action.STOP, current_streak

    # 2. Non-retryable or explicitly unrecoverable failures
    if failure.type == FailureType.UNRECOVERABLE or not failure.retryable:
        return Action.STOP, current_streak

    # 3. Failures requiring user intervention
    if failure.type == FailureType.USER_INPUT_REQUIRED:
        return Action.PAUSE, current_streak

    # 4. Correctable or transient failures
    if failure.type in (FailureType.TRANSIENT, FailureType.CORRECTABLE):
        return Action.CONTINUE, current_streak

    return Action.STOP, current_streak


def handle_failure(failure: Failure, state) -> Action: 
    """
    State updater function: Tracks failure streak accurately and mutates agent state based on policy decision.
    """
    # Compare against previous failure key (failure.type, action)
    failure_key = (failure.type, getattr(state, "current_action", None))
    last_key = getattr(state, "last_failure_key", None)
    
    if failure_key == last_key: 
        state.failure_streak = getattr(state, "failure_streak", 0) + 1
    else: 
        state.failure_streak = 1
    
    state.last_failure_key = failure_key
    state.last_failure_reason = failure.reason
    
    # Decide next action using pure policy function
    action, streak = classify_and_decide(failure, state.failure_streak)
    
    if action == Action.STOP:
        state.agent_status = "unrecoverable"
        if failure.retryable and streak >= MAX_RETRIES:
            state.validation_result = (
                f"Unrecoverable error: Exceeded max retries ({streak}/{MAX_RETRIES}): {failure.reason}"
            )
        else:
            state.validation_result = failure.reason
        return action

    if action == Action.PAUSE:
        state.agent_status = "user_input_needed"
        state.validation_result = failure.reason
        return action

    if action == Action.CONTINUE:
        state.agent_status = "retrying"
        state.validation_result = failure.reason
        return action

    return action

def map_validation_to_failure(validator_output: dict, state: AgentState) -> Failure: 
    reason = validator_output.get("reason", "validation failed")
    
    if validator_output.get("has_hallucination", False): 
        return Failure(
            type=FailureType.USER_INPUT_REQUIRED, 
            reason=reason,
            retryable=False
        )
        
    return Failure(
        type=FailureType.CORRECTABLE, 
        reason=reason,
        retryable=True
            
    )
    