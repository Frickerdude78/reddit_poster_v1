# Reddit Poster API

A FastAPI application that creates Reddit posts through a simple API interface. Built for deployment on Coolify.

## Features

- Create Reddit posts via API
- FastAPI with automatic OpenAPI documentation
- Docker containerization
- Built for Coolify deployment

## Prerequisites

- Reddit Account
- Reddit App (create one at [Reddit App Preferences](https://www.reddit.com/prefs/apps))
- Docker (if running locally)
- Coolify instance (for deployment)

### Creating a Reddit App

1. Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
2. Click "create another app..."
3. Fill in the details:
   - Name: your app name
   - Type: select "script"
   - Description: brief description of your app
   - About URL: optional
   - Redirect URI: optional for script apps
4. Click "create app"
5. Note down your credentials:
   - Client ID: the string under your app name
   - Client Secret: the "secret" field

## Environment Variables

Copy `.env.example` to `.env` and fill in your Reddit API credentials:

```env
REDDIT_CLIENT_ID=your_client_id_here        # The string under your app name
REDDIT_CLIENT_SECRET=your_client_secret_here # The "secret" field from your app
REDDIT_USER_AGENT=your_user_agent_here      # Example: "MyBot/1.0 by YourUsername"
REDDIT_USERNAME=your_reddit_username        # Your Reddit username
REDDIT_PASSWORD=your_reddit_password        # Your Reddit password
```

Note: For REDDIT_USER_AGENT, it's recommended to use a unique identifier that includes your username and app version to help Reddit track API usage.

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn main:app --reload
```

## Docker

Build and run locally:

```bash
docker build -t reddit-poster .
docker run -p 8000:8000 --env-file .env reddit-poster
```

## Coolify Deployment

1. Push this repository to GitHub
2. In Coolify dashboard:
   - Create a new service
   - Select this repository
   - Set build configuration to use Dockerfile
   - Add the environment variables
   - Deploy

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /post` - Create a Reddit post
- `GET /docs` - Interactive API documentation

### Create Post Example

```bash
curl -X POST http://your-domain/post \
  -H "Content-Type: application/json" \
  -d '{
    "subreddit": "test",
    "title": "Test Post",
    "text": "Hello Reddit!"
  }'
```

## License

MIT
