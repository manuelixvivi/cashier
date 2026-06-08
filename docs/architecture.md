# POS AI Backend - Architecture Documentation

## Overview
Enterprise-grade Point of Sale system with AI Chatbot capabilities, built with Flask and MongoDB.

## Architecture Patterns

### 1. Repository Pattern
- **Location**: `app/*/repository.py`
- **Purpose**: Abstract data access layer
- **Benefits**: Easy to swap database, testable, DRY

### 2. Service Layer Pattern
- **Location**: `app/*/service.py`
- **Purpose**: Business logic encapsulation
- **Benefits**: Reusable, testable, separation of concerns

### 3. App Factory Pattern
- **Location**: `app.py`
- **Purpose**: Create Flask app instances with different configurations
- **Benefits**: Testing flexibility, multiple instances

### 4. Blueprint Structure
- **Location**: `app/*/routes.py`
- **Purpose**: Modular route organization
- **Benefits**: Scalable, maintainable

## Data Flow
```
Request -> Routes -> Service -> Repository -> MongoDB
                    |
                    v
              Validation (Schema)
```

## Tech Stack
- **Backend**: Flask 3.x
- **Database**: MongoDB 7.x
- **Cache/Queue**: Redis + Celery
- **Auth**: JWT (Flask-JWT-Extended)
- **AI**: Groq API (Gemma) + Offline Regex Engine
- **Forecasting**: Prophet + Moving Average

## Deployment Options
1. Docker Compose (Recommended)
2. CasaOS
3. Ubuntu Server
4. Windows (Development)
