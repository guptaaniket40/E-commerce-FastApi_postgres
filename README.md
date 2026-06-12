# E-Commerce API

FastAPI-based E-Commerce Backend built with PostgreSQL, JWT Authentication, AWS S3, CloudFront, Alembic, and Docker.

## Features

* JWT Authentication
* Product Management (CRUD)
* Cart & Order Management
* Payment Module
* AWS S3 Image Upload
* CloudFront Integration
* Alembic Migrations
* Docker Support

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* JWT
* AWS S3 & CloudFront
* Alembic
* Docker

## Docker Image

```bash
docker pull guptaaniket05/ecommerce-fastapi:latest
```

## Run Project

```bash
docker run -d \
--name ecommerce_app \
--env-file .env \
-p 8000:8000 \
guptaaniket05/ecommerce-fastapi:latest
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

https://github.com/guptaaniket40/E-commerce-FastApi_postgres/tree/restructure-ecommerce-api
