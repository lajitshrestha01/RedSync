from state import AgentState
from orchestrator import Orchestrator

state = AgentState(
    user_input="I want to learn about AI Agents. Can you check if the subreddit 'AI_Agents' is a good place to start?",
    instruction="Use the search_subreddit tool to find 'AI_Agents'. Then write a very short draft telling me how many subscribers it has.",
    draft=None,
    subreddit_candidates=None,
    validation_result="",
    agent_status="initialized"
)

orchestrator_test = Orchestrator()
result = orchestrator_test.run(state)

print(result)
print(f"validate result: {result.validation_result}")
print(f"subreddit: {state.subreddit_candidates}")
print(f"agent status: {state.agent_status}")
