# API Reference

## Authentication
All API endpoints (except `/token` and `/health`) require a JWT Bearer token.

### POST `/token`
Obtain an access token.
- **Parameters (Form Data):**
  - `username`: User's username.
  - `password`: User's password.
- **Response:**
  ```json
  {
    "access_token": "...",
    "token_type": "bearer"
  }
  ```

---

## Agent Operations

### POST `/agent/execute`
Submit a task for the agent to execute autonomously.
- **Parameters (Query):**
  - `task_description`: The high-level goal for the agent.
- **Response:**
  ```json
  {
    "results": [
      {
        "task_id": "...",
        "status": "completed",
        "output": "...",
        "logs": ["..."]
      }
    ]
  }
  ```

---

## System

### GET `/health`
Check the health status of the API.
- **Response:** `{"status": "healthy", "version": "0.1.0"}`
