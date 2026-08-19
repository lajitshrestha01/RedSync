"""creating prompt for the system"""

def get_system_prompt(state): 
    return f"""
            You are a Reddit Content Os. your goal is {state.instruction}
            #Current State: 
            Draft: {state.draft}
            
            #Rules: 
            1.If the draft is None, use the create_draft tool to write it. 
            2.If the draft already exists, Do not call any tools. Just reply with the word "Done"
"""
