from dataclasses import dataclass 

@dataclass
class AgentState: 
    user_input: str 
    instruction: str
    draft: dict | None = None 
    subreddit_candidates: str | None = None 
    validation_result: str | None = None 
    agent_status: str = "initialized"
    failure_streak: int = 0
    last_failure_reason: str | None = None
    last_failure_key: tuple | None = None
    current_action: str | None = None