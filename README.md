# 📝 Keep Notes API (FastAPI + MySQL + JWT)

A scalable backend API for a **Keep Notes** application built using **FastAPI**, **SQLAlchemy (MySQL)**, and **JWT authentication**.  
This project follows a modular and production-ready folder structure for easy future expansion (microservices, additional modules, etc.).

---

## 🚀 Features
- User Registration & Login with **hashed passwords**
- JWT-based Authentication
- CRUD APIs for Notes (Create, Read, Update, Delete)
- MySQL integration via SQLAlchemy ORM
- Scalable project structure (services, schemas, routes separated)
- Environment-based configuration

---
## **Create Virtual Environment & Install Dependencies**
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

pip install -r requirements.txt

## **Setup Environment Variables**
DATABASE_URL=mysql+pymysql://<db_user>:<db_password>@localhost:3306/keepnotes \n
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

## Run Database Migrations 
CREATE DATABASE keepnotes;
python -m app.db.database

## Start FastAPI Server
cd app
python run_server

