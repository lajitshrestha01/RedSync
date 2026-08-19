from pydantic import BaseModel, Field

class CreateDraftArgs(BaseModel):
    title : str = Field(description="Title of reddit content")
    body : str = Field(description="content for reddit")
    
    

class SearchSubredditArgs(BaseModel): 
    subreddit : list[str] | None = None
    

class ValidatorArgs(BaseModel):
    is_valid: bool = Field(description="check whether the draft is valid or new informatio is created")
    reason: str = Field(description="why this is valid")


