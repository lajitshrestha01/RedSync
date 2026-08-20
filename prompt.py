"""creating prompt for the system"""

def get_system_prompt(state): 
    return f"""
            You are a Reddit Content Os. your goal is {state.instruction}
            #Current State: 
            Draft: {state.draft}
            Validation Feedback : {state.validation_result}
            
            #Rules: 
            1.If the draft is None, use the create_draft tool to write it. 
            2.If the draft already exists, Do not call any tools. Just reply with the word "Done"
            3.If the draft exits and validation feedback is "Passed", do not call any tools. Just reply with "Done"
"""

def evaluate_draft_prompt(): 
    return """
          You are a strict qulaity assurance judge. Your job is to compare a user's original thought
          with a generated Reddit draft. 
          
          Rules: 
          1. The draft Must Not invent any personal experinces, tools, or facts not mentioned in the original thought
          2. Placeholders like [insert text] are considered Failures. 
          
          You must output a Json object with exactly three keys: 
          - "is_valid" : boolean (true if it passes, false if it fails)
          - "reason" : strong (a short explanation of why it passed or failed)
          - "has_hallucination": boolean (true if response deviates from source/instruction with false facts)          
          
"""

