# 🛒 Echomart MVP

Echomart is a simplified e-commerce platform built with Django and React. It is designed to demonstrate clean backend/frontend separation, dynamic product management, user accounts, and real-time payment integration via M-PESA or Flutterwave.

For the shared setup, development workflow, daily log template, contribution guide, and troubleshooting notes, see the [development documentation](docs/README.md).

---

## 📁 Project Structure

```
echomart/
├── backend/                    # Django project: APIs, business logic, DB models
│   ├── accounts/              # User authentication and profile management
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── signals.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── migrations/        # Database migrations
│   │   ├── tests/             # Unit tests
│   │   └── __pycache__/
│   ├── config/                # Django settings and main configuration
│   ├── orders/                # Order management and processing
│   ├── payments/              # Payment processing (M-PESA, Flutterwave)
│   ├── products/              # Product catalog and management
│   ├── vendors/               # Vendor/seller management
│   ├── templates/             # HTML templates
│   ├── manage.py              # Django management script
│   ├── db.sqlite3             # SQLite database (development)
│   ├── requirements.txt       # Backend Python dependencies
│   └── .gitignore             # Backend Git ignore rules
├── frontend/                   # Basic React project (legacy)
│   ├── public/                # Static assets
│   ├── src/                   # React source code
│   ├── package.json           # Node.js dependencies
│   ├── README.md              # Frontend documentation
│   └── .gitignore             # Frontend Git ignore rules
├── vite-frontend/             # Main Vite-based React frontend (active development)
│   ├── public/                # Static assets and favicon
│   ├── src/                   # React source code
│   │   ├── Components/        # Reusable UI components
│   │   │   └── Assets/        # Image assets and logos
│   │   └── main.jsx           # Entry point for React app
│   ├── index.html             # Main HTML template
│   ├── package.json           # Node.js dependencies and scripts
│   ├── vite.config.js         # Vite configuration
│   ├── eslint.config.js       # ESLint configuration
│   ├── README.md              # Vite frontend documentation
│   └── .gitignore             # Frontend Git ignore rules
├── requirements.txt           # Root Python dependencies
├── README.md                  # This file - main project documentation
└── .gitignore                 # Root Git ignore rules
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
   [git clone https://github.com/dev-bramwel/Echomart.git
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
   cd ../vite-frontend
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
cd vite-frontend
npm run dev
```

Frontend will run on [http://localhost:5173](http://localhost:5173)

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

### 🔄 Git Collaboration Guidelines

#### Pull Request & Review Process

**⚠️ IMPORTANT:** All merges to the `master` branch require at least **2 reviewers** before merging.

1. **Creating a Pull Request:**

   - Push your feature branch to GitHub
   - Create a Pull Request from your branch to `master`
   - Add a clear title and description of your changes
   - Request reviews from at least 2 team members

2. **Required Reviewers:**

   - At least one technical reviewer (Bramwel, Masira, Eddie, or Xvira)
   - GitHub Copilot suggestions (when available)
   - Any other team member familiar with the changed code

3. **Review Checklist:**
   - [ ] Code follows project style guidelines
   - [ ] All tests pass
   - [ ] No breaking changes to existing functionality
   - [ ] Documentation updated if needed
   - [ ] Security considerations addressed

#### Pulling Changes from GitHub

To stay up-to-date with the latest changes from any branch:

```bash
# Pull changes from the main branch
git pull origin main

# Pull changes from a specific feature branch
git pull origin feature/branch-name

# Pull changes from any branch (replace <branchName> with actual branch name)
git pull origin <branchName>
```

**Best Practices:**

- Always pull the latest changes before starting new work
- Pull frequently to avoid large merge conflicts
- Communicate with your team when working on related features

**Examples:**

```bash
# Pull latest backend changes
git pull origin backend/api-improvements

# Pull latest frontend changes
git pull origin frontend/ui-components

# Pull latest from development branch
git pull origin development
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
