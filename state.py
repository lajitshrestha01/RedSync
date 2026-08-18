from dataclasses import dataclass 

@dataclass
class AgentState: 
    user_input: str 
    instruction: str
    draft : dict | None = None 
    subreddit_candidates: list[str] | None = None 
    validate_result: dict | None = None 
    agent_status: str = "initialized"