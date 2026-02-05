# SIEM Project (Django + Elasticsearch + Kibana)

A simple SIEM (Security Information and Event Management) system that logs user authentication events from Django to Elasticsearch and visualizes them in Kibana.

## 🏗 Architecture
- **Django**: Web application & authentication provider.
- **Elasticsearch**: Aggregates logs.
- **Kibana**: Dashboard for log analysis.

## 🚀 Quick Start (Fresh Laptop)

### Prerequisites
1.  **Docker & Docker Compose** installed.
2.  **Python 3.10+** installed.
3.  **Git** installed.

### 1. Backend Infrastructure (Docker)
Start the database and dashboard first.
```bash
# From the project root (where docker-compose.yml is)
docker-compose up -d
```
- **Elasticsearch**: [http://localhost:9200](http://localhost:9200)
- **Kibana**: [http://localhost:5601](http://localhost:5601)

### 2. Django Application
Open a new terminal configuration for the app.

```bash
# 1. Navigate to project source
cd siem_project

# 2. Create Virtual Environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Migrate Database
python manage.py migrate

# 5. Create Admin User
python manage.py createsuperuser

# 6. Run Server
python manage.py runserver
```
App URL: [http://localhost:8000](http://localhost:8000)

## 📊 Using the System
1.  **Generate Logs**: Go to [http://localhost:8000/login/](http://localhost:8000/login/) and log in/out or fail a login.
2.  **View Logs**: Go to [http://localhost:5601](http://localhost:5601).
    - Navigate to **Discover**.
    - Create a Data View for `django-audit-logs*`.
    - Explore your events.

## 🔄 Restarting After Reboot

If you restart your computer, follow these steps to get everything running again:

### 1. Start Infrastructure (Docker)
Open a terminal in the project folder and run:
```bash
docker-compose up -d
```
*Wait ~30 seconds for Elasticsearch and Kibana to initialize.*

### 2. Start Django App
Open a terminal in `siem_project/` and run:
```bash
source venv/bin/activate  # Activate the existing virtual environment
python manage.py runserver
```

