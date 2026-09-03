from state import AgentState

def test_agent_state_initialization(): 
    # Arrange and act 
    state = AgentState(user_input="learn python", instruction="Draft a post")
    #2 assert 
    assert state.agent_status == "initialized"
    assert state.failure_streak == 0
    assert state.revision_history == []
    