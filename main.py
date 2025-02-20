import os
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
import praw

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Reddit Poster API",
    description="API for creating Reddit posts",
    version="1.0.0"
)

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
async def create_post(
    subreddit: str = Form(...),
    title: str = Form(...),
    text: Optional[str] = Form(default="")
):
    """Create a new Reddit post
    
    Args:
        subreddit: Name of the subreddit to post to
        title: Title of the post
        text: Content of the post in Markdown format (optional)
    """
    try:
        # Validate inputs
        if not subreddit or not title:
            return JSONResponse(
                status_code=400,
                content={"error": "Subreddit and title are required"}
            )

        # Clean up the text content
        text = text.strip() if text else ""

        # Submit the post
        reddit = get_reddit_client()
        subreddit = reddit.subreddit(subreddit)
        
        try:
            submission = subreddit.submit(title, selftext=text)
            return {
                "message": "Post created successfully!",
                "submission_url": submission.url
            }
        except praw.exceptions.RedditAPIException as e:
            error_messages = [f"{error.error_type}: {error.message}" for error in e.items]
            return JSONResponse(
                status_code=400,
                content={"error": "Reddit API Error", "details": error_messages}
            )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "details": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
