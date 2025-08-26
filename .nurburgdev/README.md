---
title: "Design and implement an scalable URL shortener"
tags:
  - mysql
summary: "URL shorteners take any URL and generates a short key for it. This short key can be used to redirect users to the specified long URL. This is extremely useful for marketting on twitter bluesky and other social network. In this challenge you will be implementing few core APIs required for a scalable URL shortener"
---

## Problem Statement

You are tasked with implementing a scalable URL shortener service. URL shorteners are essential tools for social media marketing, analytics tracking, and creating user-friendly links.

### API Requirements

Your implementation must provide the following API endpoints:

#### 1. POST /short-key
Generate a random short key for a given URL.

**Sample Request:**
```json
POST /short-key
Content-Type: application/json

{
  "url": "https://example.com"
}
```

**Sample Response:**
```json
HTTP 200 OK
Content-Type: application/json

{
  "short_key": "abc123",
  "original_url": "https://example.com"
}
```

#### 2. POST /short-key/custom
Create a custom short key for a given URL.

**Sample Request:**
```json
POST /short-key/custom
Content-Type: application/json

{
  "url": "https://google.com",
  "custom_key": "mylink"
}
```

**Sample Response:**
```json
HTTP 200 OK
Content-Type: application/json

{
  "short_key": "mylink",
  "original_url": "https://google.com"
}
```

#### 3. GET /short-key/{short_key}
Redirect or retrieve URL by short key.

**Sample Request:**
```
GET /short-key/abc123
```

**Sample Response (Redirect):**
```
HTTP 302 Found
Location: https://example.com
```

**Sample Response (Data):**
```json
HTTP 200 OK
Content-Type: application/json

{
  "short_key": "abc123",
  "original_url": "https://example.com"
}
```

## Development Setup

### FastAPI Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Setup**
   ```bash
   cp .env.dev .env
   ```

3. **Run Development Server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Database Services

### Database Initialization
If you need to initialize your database schema, you can use the `init.sql` file:
- Edit `init.sql` to add your database schema, tables, and indexes
- Run the SQL file against your database to set up the initial structure

### MySQL
- **Host**: py-url-shortenermysql
- **Port**: 3306
- **Database**: mysql
- **User**: root
- **Password**: mysql

## Development Workflow

1. Make your changes to the code
2. Test locally using the development server
3. Ensure all tests pass
4. Deploy using the production configuration

## Production Deployment

The application uses `.env.prod` for production environment variables with Kubernetes service names for database connections.