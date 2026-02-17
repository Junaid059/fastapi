# Social Media API

A FastAPI-based social media backend API that provides user authentication, posts, comments, follows, voting, feed generation, and real-time chat functionality.

![System Architecture](social.drawio.png)

## Features

- **User Authentication** - Register, login with JWT token-based authentication
- **Posts** - Create, read, update, delete posts
- **Comments** - Add comments to posts
- **Votes** - Like/unlike posts
- **Follow System** - Follow and unfollow users
- **Feed** - Personalized feed based on followed users and random posts
- **Search** - Search functionality for users and posts
- **Real-time Chat** - WebSocket-based messaging between users

## Tech Stack

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **JWT** - Authentication tokens
- **WebSockets** - Real-time communication

## Project Structure

```
app/
├── main.py              # Application entry point
├── database.py          # Database configuration
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── utils.py             # Utility functions
├── connection_manager.py # WebSocket connection manager
└── routers/
    ├── auth.py          # Authentication endpoints
    ├── users.py         # User management
    ├── posts.py         # Post CRUD operations
    ├── comments.py      # Comment operations
    ├── votes.py         # Voting system
    ├── follow.py        # Follow/unfollow
    ├── feed.py          # User feed
    ├── search.py        # Search functionality
    ├── chat.py          # Real-time chat
    └── Oauth.py         # OAuth2 token handling
```

## Database Models

| Model | Description |
|-------|-------------|
| User | User accounts with email, password, role |
| Post | User posts with title, content |
| Comment | Comments on posts |
| Votes | Post likes |
| Follow | User follow relationships |
| Message | Chat messages between users |

## API Endpoints

### Authentication
- `POST /login` - Login and get JWT token
- `POST /users` - Register new user

### Posts
- `GET /posts` - Get all posts
- `POST /posts` - Create a post
- `GET /posts/{id}` - Get specific post
- `PUT /posts/{id}` - Update post
- `DELETE /posts/{id}` - Delete post

### Comments
- `POST /comments` - Add comment
- `GET /comments/{post_id}` - Get comments for a post

### Votes
- `POST /vote` - Vote on a post

### Follow
- `POST /follow` - Follow a user
- `DELETE /follow/{id}` - Unfollow a user

### Feed
- `GET /feed` - Get personalized feed

### Search
- `GET /search` - Search users and posts

### Chat
- `WebSocket /chat/ws/{token}` - Real-time chat connection
- `GET /chat/history/{user_id}` - Get chat history with a user
- `GET /chat/conversations` - Get list of conversations
- `GET /chat/unread/count` - Get unread message count

## Real-time Chat System

The chat system allows two users to send and receive messages in real-time using WebSockets.

### How it Works

1. **Connect** - User connects to WebSocket with their JWT token
2. **Send Message** - Send JSON with receiver_id and content
3. **Receive Message** - Messages are delivered instantly if user is online
4. **Persistence** - All messages are saved to database

### WebSocket Connection

```
ws://localhost:8000/chat/ws/{jwt_token}
```

### Message Format

**Send a message:**
```json
{
    "type": "message",
    "receiver_id": 2,
    "content": "Hello!"
}
```

**Receive a message:**
```json
{
    "type": "message",
    "message_id": 1,
    "sender_id": 1,
    "receiver_id": 2,
    "content": "Hello!",
    "created_at": "2026-02-16T10:00:00",
    "sender_email": "user@example.com"
}
```

**Typing indicator:**
```json
{
    "type": "typing",
    "receiver_id": 2
}
```

**Mark as read:**
```json
{
    "type": "read",
    "message_id": 5
}
```

**Check online status:**
```json
{
    "type": "online_status",
    "user_id": 2
}
```

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables** in `.env`
   ```
   DATABASE_URL=postgresql://user:password@localhost/dbname
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

3. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access API docs**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Testing Chat

1. Login to get JWT token
2. Connect to WebSocket: `ws://localhost:8000/chat/ws/{token}`
3. Send message to another user
4. The recipient receives the message in real-time if connected
