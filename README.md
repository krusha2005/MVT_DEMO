
 # MVT_DEMO project

Project Overview: MVT_demo
- MVT_DEMO is a multi-vendor e-commerce web application built using Django MVT architecture with separate Admin, Seller, and Buyer dashboards.  

## Key Highlights:

- Dual Roles: Users can register as either a Seller (to manage stores, products, stock, and de-listing) or a Buyer (to browse, shop, and place orders).

- Dashboard Management:
  - Admin Dashboard: Manage buyers, sellers, products, and platform activity.
  - Seller Dashboard: Manage products, stock, orders, and product de-listing.
  - Buyer Dashboard: View profile details, status and order history.

- Smart Inventory: Products are organized using a structured hierarchy:
  Category ➔ Sub-Category ➔ Product Type.

- Essential Features: Includes Search, Filters, Wishlist, Cart, Checkout, Order Management, and Bestseller product sections.


## 📋 Prerequisites
Ensure you have the following installed before starting:

- **Git**

- **Python** 3.14.4  (for local setup)

- **PostgreSQL** 18.3  (for local setup)

- **Docker & Docker Desktop** (for Docker setup)

## 🐳 Docker Installation Guide
If you do not have Docker installed, you can install it quickly using your terminal:

###  macOS (using Homebrew)
```bash
brew install --cask docker
```

-**Note:** This installs Docker Desktop. Once installed, open your Applications folder and launch Docker to start the background engine.

### 🐧 Linux (Ubuntu/Debian)

```bash
# Update packages and install Docker + Docker Compose
sudo apt update
sudo apt install docker.io docker-compose-v2 -y


# Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker
```


## ⚙️ Environment Configuration (.env)

Before running the project in either local or Docker mode, you need to configure your environment variables. Create a file named .env in the root directory of your project:

```bash
touch .env
```

Add the following environment configuration inside .env:

```bash
# Common configurations
SECRET_KEY=your_django_secret_key_here
DEBUG=True

# Database Configuration
DB_NAME=marketplace_db
DB_USER=postgres
DB_PASSWORD=your_secure_password

# --- IF RUNNING LOCALLY ---
# DB_HOST=localhost
# DB_PORT=5432

# --- IF RUNNING WITH DOCKER ---
DB_HOST=db
DB_PORT=5432

```

- 💡 **Note** : When switching between **Docker** and **Local**, make sure to toggle (comment/uncomment) the correct DB_HOST in your .env file. Docker uses db as the host, while local running uses localhost.

# 🐳 Option A: Running with Docker (Recommended)

Using Docker allows you to start the web server and database instantly without installing PostgreSQL or Python locally.

## 1. Build and Run the Containers

This command builds your container images and starts both the Web server (Django) and Database (Postgres) services.

```bash
docker compose up --build
```

The web application will be accessible at **http://127.0.0.1:8001**

## 2. Apply Database Migrations (Run in a new terminal window)

```bash
docker compose exec web python manage.py migrate
```

## 3. Create a Superuser / Admin Account

```bash
docker compose exec web python manage.py createsuperuser
```

## 4. Stop the Containers

To safely stop and spin down your Docker services:

```bash
docker compose down
```

# 💻 Option B: Running Locally (Without Docker)
Follow these steps if you want to run the project directly on your physical machine.


### Project SetUp (macOS / Linux)
Follow these steps precisely to get the project running on your local machine.

## 1. Clone & Set Up Directory


- **git clone** https://github.com/krusha2005/MVT_DEMO.git
- cd MVT_DEMO


## 2. Set Up Virtual Environment

# Create the environment
```bash
python3 -m venv venv
```

# Activate it
```bash
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```


## 4. Database Setup (PostgreSQL)
- PostgreSQL Setup (macOS / Linux)


### 4.1. Download & Install
#### for macOS

```bash
    brew install postgresql@18
```
#### for linux

```bash
    sudo apt update
    sudo apt install postgresql-18
```


### 4.2. Start the Database Service
(Your database needs to be "awake" to accept connections from Django.)

#### macOS: 

```bash
brew services start postgresql@18
```

#### Linux:
```bash
 sudo systemctl start postgresql
 ```


### 4.3. Access the PostgreSQL Terminal (psql)

## Log in as the default 'postgres' user

```bash
sudo -u postgres psql
```


###  SQL Command Cheat Sheet

Once you are inside the psql shell (you will see a `postgres=#` prompt), you can copy and run these commands:

- List all Databases: 
   \l

- Create your Project DB:
CREATE DATABASE marketplace_db;

- Connect to your DB:
\c marketplace_db

- List all Tables (after migrating):
\dt

- See Table Structure:
\d table_name

- Run a Select Query (Don't forget the semicolon!):
SELECT * FROM accounts_user;

- Exit PostgreSQL:
\q

#### Important: After creating the database, open MVT_demo/settings.py and update the DATABASES section with your PostgreSQL USER and PASSWORD.


## 5. Django Commands (Syncing everything)


### 1. Apply the changes to the PostgreSQL tables
```bash
python3 manage.py migrate
```

### 2. Create an admin user to see the data
```bash
python3 manage.py createsuperuser
```

### 3. Start the project
```bash
python3 manage.py runserver
```
The local server will be running at **http://127.0.0.1:8000**


## 📂 Project Structure & Module Flow:

```
MVT_DEMO/
├── accounts/           #  Authentication & Profiles
│   └── Logic: Custom User roles (Buyer/Seller), Registration   Login.
|
├── products/           #  Inventory Management
│   └── Logic: 3-Tier Hierarchy (Category -> SubCategory -> ProductType) & Product CRUD.\
|
├── core/               #  Homepage & Global Views
│   └── Logic: Landing page & Smart Location-Based filtering logic.
|
├── cart/               #  Shopping Cart
│   └── Logic: Temporary storage for items selected for purchase.
|
├── wishlist/           #  Saved Items
│   └── Logic: Allows buyers to save products for later.
|
├── orders/             #  Order Management
│   └── Logic: Checkout process, Order history, and Tracking.
|
├── media/              #  Static Uploads (Product Images)
|
└── templates/          #  Global UI Components (Navbar, Footer, Base)
```