# DocQue 🏥📄

DocQue is a full-stack document management and processing system built using a modern monolithic architecture. It integrates a FastAPI backend, a React frontend, and PostgreSQL, all orchestrated via Docker for seamless development and deployment.

---

## 🚀 Features

* 📄 Document handling and processing
* ⚡ FastAPI-powered backend APIs
* 🖥️ Modern React frontend (Vite + Tailwind CSS)
* 🗄️ PostgreSQL database integration
* 🐳 Fully containerized using Docker
* 🔍 Adminer for database inspection

---

## 🏗️ Architecture

```
DocQue/
│
├── backend/        # FastAPI application
├── frontend/       # React (Vite) application
├── docker-compose.yml
└── README.md
```

### Services

* **backend** → FastAPI app (port 8000)
* **frontend** → React app served via Nginx (port 4173)
* **db** → PostgreSQL (port 5432)
* **adminer** → DB UI (port 8080)

---

## ⚙️ Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* ReportLab (PDF generation)

### Frontend

* React 19
* Vite
* Tailwind CSS
* Axios

### DevOps

* Docker
* Docker Compose

---

## 🐳 Running the Project (Recommended)

### 1. Clone the repository

```bash
git clone https://github.com/<your-repo>/DocQue.git
cd DocQue
```

---

### 2. Setup environment variables

Create a `.env` file inside `backend/`:

```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db
DATABASE_URL=postgresql://your_user:your_password@db:5432/your_db
```

---

### 3. Build and start containers

```bash
docker-compose up --build
```

---

### 4. Access services

| Service  | URL                   |
| -------- | --------------------- |
| Frontend | http://localhost:4173 |
| Backend  | http://localhost:8000 |
| Adminer  | http://localhost:8080 |

---

## 🧪 Running Locally (Without Docker)

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🔗 API Configuration

The frontend uses:

```
VITE_API_BASE_URL=http://backend:8000
```

When running locally, update it to:

```
http://localhost:8000
```

---

## 🗄️ Database Access (Adminer)

* URL: http://localhost:8080
* System: PostgreSQL
* Server: db
* Username/Password: from `.env`

---

## 📦 Docker Services Overview

```yaml
db         → PostgreSQL database
backend    → FastAPI service
frontend   → React + Nginx
adminer    → DB management UI
```

---

## 🛠️ Development Notes

* Backend code is mounted via volume:

  ```
  ./backend/app:/app/app
  ```

  → Enables live reload during development

* Frontend is built at container build time using Vite

---

## 🚀 Future Improvements

* Authentication & authorization
* CI/CD pipeline
* Production deployment (Kubernetes / ECS)
* Logging & monitoring
* File storage (S3 / MinIO)

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Push and open a PR

---

## 📜 License

This project is licensed under the MIT License.

---