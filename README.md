MVT Django Project


==>Features

=>Authentication:
    Buyer Registration
    Seller Registration
    Login / Logout
    Role-based system (Buyer / Seller)

=>Seller Features:
    Seller can register with:
        Store Name
        Category selection
    Categories managed using:
        Category
        SubCategory
        ProductType


==>Tech Stack

=>Backend
    python (v: 3.14.4)
    Django (v: 6.0.4)

=>Databse
    PostgreSQL (v:18.3)
    psycopg2-binary (v: 2.9.12)

=>Image Processing
    pillow (v: 12.2.0)

=>Frontend
    HTML5
    CSS3
    Bootstrap


==>Setup Instructions
    git clone [<your-repo-url>](https://github.com/krusha2005/MVT_DEMO.git)
    cd MVT_DEMO
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver


==>Project Structure
    accounts → authentication (buyer/seller)
    products → category, product models
    cart → cart system
    orders → order system
    wishlist → wishlist feature
    core → homepage & common views


==>Upcoming Features
    Seller Dashboard
    Add Product
    Cart System
    Wishlist
    Order System