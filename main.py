from state import AgentState
from orchestrator import Orchestrator

state = AgentState(
    user_input="i build this automation scripts that automate linkedin scraping and send connection request to the user i want.  ",
    instruction="List the tools I used and my boss's rection. Give me long from content that explain how i use the tool and suprise my boss",
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
