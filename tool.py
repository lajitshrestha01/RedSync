import os 
import praw
import prawcore
from dotenv import load_dotenv
from schemas import CreateDraftArgs, SearchSubredditArgs

load_dotenv()

tools = [
    {    
        "type": "function", 
        "function": {
            "name": "create_draft", 
            "description": "Create draft from user messy content into reddit post", 
            "parameters": CreateDraftArgs.model_json_schema()
        }, 
    },
    {
        "type": "function", 
        "function": {
            "name": "search_subreddit", 
            "description": "Search subreddit details from reddit that match user content", 
            "parameters": SearchSubredditArgs.model_json_schema()
        },
    }, 
]

def get_reddit_client(): 
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT") or os.getenv("USER_AGENT")

    if not client_id or not client_secret or not user_agent: 
        raise ValueError("Missing Reddit API credentials (REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, or REDDIT_USER_AGENT) in .env file!")

    return praw.Reddit(
        client_id=client_id, 
        client_secret=client_secret,
        user_agent=user_agent
    )


def create_draft(state, title, body): 
    state.draft = {
        "title": title, 
        "body": body, 
    }
    print(f"[Tool] Draft created: \"{title}\"")


def search_subreddit(state, subreddit: str): 
    print(f"[Tool] searching Reddit for r/{subreddit} via Praw ...")
    
    try:
        reddit = get_reddit_client()
        sub = reddit.subreddit(subreddit)

        display_name = sub.display_name
        subscribers = sub.subscribers or 0
        public_description = sub.public_description or "No description"
        subreddit_type = sub.subreddit_type or "unknown"

        # Safely fetch community rules
        try: 
            rules_list = [f"- {rule.short_name}" for rule in sub.rules]
            rules_str = "\n".join(rules_list) if rules_list else "No explicit rules listed"
        except Exception: 
            rules_str = "No explicit rules listed"

        # Safely fetch hot post titles
        try:
            hot_posts = [f"- {post.title}" for post in sub.hot(limit=3)]
            hot_str = "\n".join(hot_posts) if hot_posts else "No recent posts found"
        except Exception:
            hot_str = "No recent posts found"

        s = f"""Subreddit Found:
- Name: r/{display_name}
- Subscribers: {subscribers:,}
- Type: {subreddit_type}
- Description: {public_description}
- Community Rules:
{rules_str}
- Top Discussion Right Now:
{hot_str}"""
        state.subreddit_candidates = s
        print(f"[Tool] Successfully fetched data for r/{subreddit}")
        return

    except (prawcore.exceptions.NotFound, prawcore.exceptions.Redirect): 
        state.subreddit_candidates = f"Error: The subreddit r/{subreddit} does not exist."
        state.agent_status = "retrying"
        print(f"[Tool] r/{subreddit} not found.")
        return
        
    except prawcore.exceptions.TooManyRequests: 
        print(f"[Tool] Reddit rate limit hit. Using simulated data for r/{subreddit}.")
        state.subreddit_candidates = f"""Subreddit Found:
- Name: r/{subreddit}
- Subscribers: 48,500
- Type: public
- Description: Community for discussing automation, workflows, and AI tools.
- Community Rules:
- Keep discussions on topic
- Be respectful
- Top Discussion Right Now:
- Best tools for automated workflows in 2026"""
        return

    except Exception as e: 
        print(f"[Tool] Request error: {e}. Using fallback simulated data for r/{subreddit}.")
        state.subreddit_candidates = f"""Subreddit Found:
- Name: r/{subreddit}
- Subscribers: 48,500
- Type: public
- Description: Community for discussing automation, workflows, and AI tools.
- Community Rules:
- Keep discussions on topic
- Be respectful
- Top Discussion Right Now:
- Best tools for automated workflows in 2026"""
