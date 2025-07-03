# 🛒 Echomart MVP

Echomart is a simplified e-commerce platform built with Django and React. It is designed to demonstrate clean backend/frontend separation, dynamic product management, user accounts, and real-time payment integration via M-PESA or Flutterwave.

---

## 📁 Project Structure

```
echomart/
├── backend/                    # Django project: APIs, business logic, DB models
│   ├── accounts/              # User authentication and profile management
│   ├── config/                # Django settings and main configuration
│   ├── orders/                # Order management and processing
│   ├── payments/              # Payment processing (M-PESA, Flutterwave)
│   ├── products/              # Product catalog and management
│   ├── vendors/               # Vendor/seller management
│   ├── templates/             # HTML templates
│   ├── manage.py              # Django management script
│   └── db.sqlite3             # SQLite database (development)
├── frontend/                   # React project: UI components, pages, API integration
│   ├── public/                # Static assets
│   ├── src/                   # React source code
│   │   ├── Components/        # Reusable UI components
│   │   ├── App.js             # Main app component
│   │   └── index.js           # Entry point
│   └── package.json           # Node.js dependencies
├── vite-frontend/             # Alternative Vite-based React frontend
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 🧠 Team Roles & Responsibilities

| Name    | Role                     | Responsibilities                               |
| ------- | ------------------------ | ---------------------------------------------- |
| Bramwel | Backend Lead / Architect | Django setup, M-PESA integration, architecture |
| Masira  | Backend Developer        | Vendor/product/cart logic                      |
| Eddie   | Frontend Developer       | React UI, routing, integration                 |
| Xvira   | Frontend Developer       | React UI, search/product detail                |
| Ryan    | UI/UX Designer           | Figma design, visual review                    |

---

## 🚀 Getting Started - New Team Member Setup

### � Prerequisites

- Python 3.9+ installed
- Node.js 16+ and npm installed
- Git installed

### 🔧 Initial Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/echomart.git
   cd echomart
   ```

2. **Create and activate a virtual environment:**

   **On Windows:**

   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

   **On macOS/Linux:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   ```bash
   cd backend
   python manage.py migrate
   python manage.py createsuperuser  # Optional: Create admin user
   ```

5. **Install frontend dependencies:**
   ```bash
   cd ../frontend
   npm install
   ```

### 🏃‍♂️ Running the Development Servers

**Terminal 1 - Backend (Django):**

```bash
cd backend
python manage.py runserver
```

Backend will run on [http://localhost:8000](http://localhost:8000)

**Terminal 2 - Frontend (React):**

```bash
cd frontend
npm start
```

Frontend will run on [http://localhost:3000](http://localhost:3000)

### 🔧 Environment Variables

Create a `.env` file in the backend directory:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 📝 Common Commands

**Backend:**

```bash
# Make migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Start development server
python manage.py runserver
```

**Frontend:**

```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

### 🛠️ Development Workflow

1. **Before starting work:**

   ```bash
   git pull origin main
   # Activate virtual environment
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # macOS/Linux
   ```

2. **Create a feature branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes and commit:**

   ```bash
   git add .
   git commit -m "Add your descriptive commit message"
   ```

4. **Push and create a pull request:**
   ```bash
   git push origin feature/your-feature-name
   ```

### 🐛 Troubleshooting

**Common Issues:**

1. **Virtual environment not activated:**

   - Make sure you see `(venv)` in your terminal prompt
   - Re-activate with `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)

2. **Module not found errors:**

   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt` again

3. **Database errors:**

   - Delete `db.sqlite3` file and run migrations again
   - `python manage.py migrate`

4. **Port already in use:**

   - Kill existing processes or use different ports
   - `python manage.py runserver 8001`

5. **CORS issues:**
   - Check that `corsheaders` is installed and configured in settings.py
   - Ensure frontend URL is in `CORS_ALLOWED_ORIGINS`

### 🧪 Testing

**Backend Tests:**

```bash
cd backend
python manage.py test
```

**Frontend Tests:**

```bash
cd frontend
npm test
```

### 📝 Contributing

1. **Code Style:**

   - Follow PEP 8 for Python code
   - Use ESLint for JavaScript/React code
   - Add docstrings to functions and classes

2. **Commit Messages:**

   - Use descriptive commit messages
   - Follow format: `type: description`
   - Examples: `feat: add user authentication`, `fix: resolve CORS issue`

3. **Pull Requests:**
   - Create feature branches from `main`
   - Write descriptive PR descriptions
   - Request code review before merging

### 🔧 Technology Stack

**Backend:**

- Django 5.2.3
- Django REST Framework
- SQLite (development) / PostgreSQL (production)
- Django CORS Headers

**Frontend:**

- React 19.1.0
- React Router DOM
- Tailwind CSS
- Axios for API calls

**Development Tools:**

- Git for version control
- Virtual environments for Python
- npm for JavaScript package management

---

## ⚙️ Local Development Setup

---

## 🔌 API Endpoints

### Authentication

- `POST /api/auth/register/` – User registration
- `POST /api/auth/login/` – User login
- `POST /api/auth/logout/` – User logout
- `GET /api/auth/profile/` – User profile

### Products

- `GET /api/products/` – List all products
- `GET /api/products/?featured=true` – Featured products
- `GET /api/products/{id}/` – Product details
- `POST /api/products/` – Create product (vendors only)

### Categories

- `GET /api/categories/` – List of categories
- `GET /api/categories/{id}/products/` – Products by category

### Orders

- `POST /api/orders/` – Create order
- `GET /api/orders/` – User's orders
- `GET /api/orders/{id}/` – Order details

### Payments

- `POST /api/payments/mpesa/` – M-PESA payment
- `POST /api/payments/flutterwave/` – Flutterwave payment
- `GET /api/payments/{id}/status/` – Payment status

### Vendors

- `GET /api/vendors/` – List vendors
- `GET /api/vendors/{id}/products/` – Vendor products

### Utilities

- `GET /api/promotions/` – Homepage banners
- `GET /ping/` – Health check

---

## 🚀 Deployment Plan

- **Frontend**: Vercel / Netlify
- **Backend**: Render / Railway / VPS
- `.env` files for secure key management

---

## 📜 License

This project is for educational and prototyping purposes only.
