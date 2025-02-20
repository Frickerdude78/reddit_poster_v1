import os
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import praw

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Reddit Poster API",
    description="API for creating Reddit posts",
    version="1.0.0"
)

class RedditPost(BaseModel):
    subreddit: str
    title: str
    text: Optional[str] = ""

# Initialize Reddit API client
def get_reddit_client():
    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/post")
async def create_post(post: RedditPost):
    """Create a new Reddit post"""
    try:
        # Submit the post
        reddit = get_reddit_client()
        subreddit = reddit.subreddit(post.subreddit)
        submission = subreddit.submit(post.title, selftext=post.text)

        return {
            "message": "Post created successfully!",
            "submission_url": submission.url
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
