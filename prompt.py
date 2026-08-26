"""creating prompt for the system"""

def get_system_prompt(state): 
    history_str = ""
    if state.revision_history:
        history_items = []
        for r in state.revision_history:
            history_items.append(f"- Version {r['version']} Rejection Feedback: \"{r['feedback']}\"")
        history_str = "\n# Previous Revisions & Critique:\n" + "\n".join(history_items) + "\n"

    feedback_str = f"\n- Latest User Feedback to address: {state.human_feedback}" if state.human_feedback else ""

    return f"""You are a Reddit Content OS. Your goal is: {state.instruction}

# Current State:
- Subreddit Information: {state.subreddit_candidates if state.subreddit_candidates else "Not searched yet"}
- Draft: {state.draft}
- Validation Feedback: {state.validation_result}{feedback_str}
{history_str}
# Rules:
1. If Subreddit Information is "Not searched yet", call the `search_subreddit` tool first.
2. Once Subreddit Information is available and Draft is None, use `create_draft` to write the post using the retrieved information.
3. If revising, carefully follow the user's feedback and avoid repeating mistakes noted in previous revisions.
4. If the draft already exists, validation feedback is "Passed", and there is no pending feedback, do not call any tools. Just reply with "Done".
"""

def evaluate_draft_prompt(): 
    return """
          You are a strict quality assurance judge. Your job is to compare a user's original thought and instructions
          with a generated Reddit draft. 
          
          Rules: 
          1. The draft Must Not invent any personal experiences, tools, or facts not mentioned in the original thought or retrieved facts.
          2. Placeholders like [insert text] are considered Failures. 
          
          You must output a JSON object with exactly three keys: 
          - "is_valid" : boolean (true if it passes, false if it fails)
          - "reason" : string (a short explanation of why it passed or failed)
          - "has_hallucination": boolean (true if response deviates from source/instruction with false facts)          
"""

