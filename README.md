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

## 📂 Project Structure

keep-notes-backend/
│── app/
│ ├── index.py
│ ├── run_server.py
│ ├── db/
│ │ ├── database.py
| ├── managers
| | ├──users.py
│ ├── schemas/ # Pydantic models
│ │ ├── note.py
│ │ ├── register.py
│ │ ├── token.py
│ ├── services/ # Business logic layer
│ │ ├── user_service.py
│ │ ├── note_service.py
│ ├── tests/ # Unit tests
│ │ ├── test_users.py
│ │ ├── test_notes.py
│── requirements.txt
│── README.md
│── .env
