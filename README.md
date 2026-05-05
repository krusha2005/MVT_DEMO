
MVT_DEMO project

🛒 Project Overview: MVT_demo
MVT_demo is a multi-vendor e-commerce platform (like Amazon) built with Django. It features a unique dual-role system and location-based sorting to connect local buyers and sellers.

🔑 Key Highlights:
Dual Roles: Users register as either a Seller (to manage stores and inventory) or a Buyer (to shop and browse).

Smart Inventory: Products are organized by Category ➔ Sub-Category ➔ Product Type.

Location-First Logic: If a Buyer and Seller are in the same city/state, those products appear at the top of the feed automatically.

Essential Features: Includes Search, Filters, Wishlist, Cart, and "Bestseller" tags.


📋 Prerequisites
Ensure you have the following installed before starting:

Python 3.14.4

PostgreSQL 18.3

Git


Getting Started (macOS / Linux)
Follow these steps precisely to get the project running on your local machine.

1. Clone the Project
    git clone https://github.com/krusha2005/MVT_DEMO.git
    cd MVT_DEMO


2. Set Up Virtual Environment
    # Create the environment
    python3 -m venv venv

    # Activate it
    source venv/bin/activate


3. Install Dependencies
    pip install --upgrade pip
    pip install -r requirements.txt


4. Database Setup (PostgreSQL)

=>PostgreSQL Setup (macOS / Linux)


4.1. Download & Install
=>for macOS
    brew install postgresql@18

=>for linux
    sudo apt update
    sudo apt install postgresql-18


4.2. Start the Database Service
(Your database needs to be "awake" to accept connections from Django.)

macOS: brew services start postgresql@18

Linux: sudo systemctl start postgresql


4.3. Access the PostgreSQL Terminal (psql)

# Log in as the default 'postgres' user
sudo -u postgres psql


🔍 SQL Command Cheat Sheet
Once you are inside the psql shell (you will see a postgres=# prompt), use these commands:

    List all Databases --> \l
    Create your Project DB --> CREATE DATABASE mvt_demo_db;
    Connect to your DB --> \c mvt_demo_db
    List all Tables (after migrating) --> \dt
    See Table Structure --> \d table_name
    Run a Select Query --> SELECT * FROM accounts_user; (Don't forget the ;)
    Exit PostgreSQL --> \q

-->Important: After creating the database, open MVT_demo/settings.py and update the DATABASES section with your PostgreSQL USER and PASSWORD.


5.Django Commands (Syncing everything)

# 1. Create the migration files (blueprints)
python3 manage.py makemigrations

# 2. Apply the changes to the PostgreSQL tables
python3 manage.py migrate

# 3. Create an admin user to see the data
python3 manage.py createsuperuser

# 4. Start the project
python3 manage.py runserver  (Navigate to http://127.0.0.1:8000 in your browser.)


Project Structure & Module Flow:

MVT_DEMO/
├── accounts/           #  Authentication & Profiles
│   └── Logic: Custom User roles (Buyer/Seller), Registration, & Login.
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