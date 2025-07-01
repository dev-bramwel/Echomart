
# 🛒 Echomart MVP

Echomart is a simplified e-commerce platform built with Django and React. It is designed to demonstrate clean backend/frontend separation, dynamic product management, user accounts, and real-time payment integration via M-PESA or Flutterwave.

---

## 📁 Project Structure

```
echomart/
├── backend/       # Django project: APIs, business logic, DB models
├── frontend/      # React project: UI components, pages, API integration
└── docs/          # Project proposal, mockups, screenshots
```

---

## 🧠 Team Roles & Responsibilities

| Name     | Role                     | Responsibilities |
|----------|--------------------------|------------------|
| Bramwel  | Backend Lead / Architect | Django setup, M-PESA integration, architecture |
| Masira   | Backend Developer        | Vendor/product/cart logic |
| Eddie    | Frontend Developer       | React UI, routing, integration |
| Xvira    | Frontend Developer       | React UI, search/product detail |
| Ryan     | UI/UX Designer           | Figma design, visual review |

---

## ⚙️ Local Development Setup

### 🔧 Backend (Django)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 🌐 Frontend (React)
```bash
cd frontend
npm install
npm start
```

React runs on [http://localhost:3000](http://localhost:3000)  
Django runs on [http://localhost:8000](http://localhost:8000)

> Make sure to enable CORS in your Django settings to allow requests from the frontend.

---

## 🔌 API Endpoints (Sample)

- `/api/categories/` – List of categories
- `/api/products/?featured=true` – Featured products
- `/api/promotions/` – Homepage banners

---

## 🚀 Deployment Plan

- **Frontend**: Vercel / Netlify
- **Backend**: Render / Railway / VPS
- `.env` files for secure key management

---

## 📜 License

This project is for educational and prototyping purposes only.
