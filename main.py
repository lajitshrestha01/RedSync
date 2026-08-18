from state import AgentState
from orchestrator import Orchestrator

test_1 = AgentState(
    user_input = "I build an n8n automation that saves me 10 hours every week.", 
    instruction = "Trun this into an authentic reddit post"
)

orchestrator_test = Orchestrator()
result = orchestrator_test.run(test_1)

print(result)
print(test_1.subreddit_candidates)
print(f"validate result: {result.validate_result}")
print(test_1.agent_status)
