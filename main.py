from state import AgentState
from orchestrator import Orchestrator

state = AgentState(
    user_input="Planning to buy some cat toys for my cat",
    instruction="change this into reddit content and explain how happy was my sister",
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
print(f"revisions count: {len(state.revision_history)}")
for rev in state.revision_history:
    print(f"  - Version {rev['version']} [{rev['status']}]: {rev['feedback']}")
