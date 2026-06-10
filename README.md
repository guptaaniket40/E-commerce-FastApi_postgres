# E-Commerce API

A FastAPI-based E-Commerce Backend built using a modular company-style architecture with PostgreSQL, JWT Authentication, AWS S3, CloudFront, Alembic, and Docker.

## Features

* User Authentication (Signup, Login, Refresh Token)
* Product Management (CRUD Operations)
* Cart Management
* Order & Checkout System
* Payment Module
* AWS S3 Image Upload
* CloudFront Image Delivery
* Alembic Database Migrations
* Docker & Docker Compose Support

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* JWT Authentication
* AWS S3
* AWS CloudFront
* Alembic
* Docker

## Docker Image

```bash
docker pull guptaaniket05/ecommerce-fastapi:latest
```

## Run Project

```bash
docker compose up --build
```

Run migrations:

```bash
docker exec -it ecommerce_app alembic upgrade head
```

## API Documentation

```text
http://localhost:8000/docs
```

## GitHub Repository

https://github.com/guptaaniket05/E-commerce-FastApi_postgres/tree/restructure-ecommerce-api
