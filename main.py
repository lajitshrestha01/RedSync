from state import AgentState
from orchestrator import Orchestrator

test_1 = AgentState(
    user_input = "i automated my job, something that took, 20 hours for posting in platform like realtor weekly, i used n8n, caputre image, ai generate descrptio and automate the posting", 
    instruction = "Turn this into a long, detailed Reddit post. If the user provided specific tools and how much money they saved, include them. Do not make them up if they are missing")

orchestrator_test = Orchestrator()
result = orchestrator_test.run(test_1)

print(result)
print(test_1.subreddit_candidates)
print(f"validate result: {result.validation_result}")
print(test_1.agent_status)
