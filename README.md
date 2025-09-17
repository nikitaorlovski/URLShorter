# 🔗 URL Shortener Service

FastAPI-based URL shortening service with Redis caching and PostgreSQL persistence.

## 🚀 Features

- **URL Shortening**: Convert long URLs to short codes (7 characters)
- **Redirection**: Automatic redirects from short codes to original URLs
- **Click Statistics**: Track number of redirects for each URL
- **Redis Caching**: High-performance caching for frequently accessed URLs
- **RESTful API**: Full CRUD operations for URL management
- **Async Support**: Built with async/await for better performance

## 📦 API Endpoints

### Shortening Service (`/shorten`)
- `POST /shorten` - Create a new short URL
- `GET /shorten/{short_code}` - Get original URL (cached for 30s)
- `PUT /shorten/{short_code}` - Update existing URL
- `DELETE /shorten/{short_code}` - Delete URL
- `GET /shorten/{short_code}/stats` - Get URL statistics

### Redirection Service (`/`)
- `GET /{short_code}` - Redirect to original URL (302 redirect)

## 🛠️ Technologies Used

- **FastAPI** - Modern web framework
- **PostgreSQL** - Primary database
- **Redis** - Caching layer
- **SQLAlchemy** - Async ORM
- **Alembic** - Database migrations
- **Docker** - Containerization
- **Uvicorn** - ASGI server

## 🏗️ Architecture
