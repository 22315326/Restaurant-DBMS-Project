# Restaurant Management System (DBMS Project) 🍔

**Course:** CMPE344 - Database Management Systems and Programming II  
**Instructor:** Prof. Dr. Melike Şah Direkoğlu  
**Term:** Fall 2025-2026  

## 👥 Group Members
* **[İsim Soyisim 1]** (Student ID)
* **[İsim Soyisim 2]** (Student ID)
* **[İsim Soyisim 3]** (Student ID)

---

## 📖 Project Overview
This project is a cloud-based **Restaurant Database Management System** designed to digitize and streamline restaurant operations. The system allows authorized users (Admins, Waiters) to manage menu items, track tables, and process customer orders in real-time.

The application is built using **Python (Streamlit)** for the frontend and **Supabase (PostgreSQL)** for the cloud database backend, ensuring secure and accessible data management.

## 🚀 Features
* **🔐 User Authentication:** Secure login system for staff members.
* **📋 Menu Management:** Add, delete, and view menu items with categories and prices.
* **🛒 Order Processing:**
    * Select specific restaurant tables.
    * Add items to a shopping cart.
    * Calculate total amounts automatically.
    * Submit orders to the database.
* **📊 Order Tracking:** View active and past orders with details.
* **☁️ Cloud Architecture:** Fully hosted on Supabase (PostgreSQL).

## 🛠️ Technology Stack
* **Language:** Python 3.9+
* **GUI Framework:** Streamlit
* **Database:** PostgreSQL (via Supabase)
* **Libraries:** `supabase`, `pandas`, `streamlit`

## 🗄️ Database Schema
The database consists of the following key tables:
1.  **Users:** Stores staff credentials and roles.
2.  **Roles:** Defines user permissions (Admin, Waiter, Kitchen).
3.  **MenuItems:** Stores food/beverage details and prices.
4.  **Categories:** Categorizes menu items (Main Course, Desserts, etc.).
5.  **RestaurantTables:** Manages physical tables in the restaurant.
6.  **Orders:** Stores order headers (Date, Table, Waiter, Status).
7.  **OrderDetails:** Stores specific items within an order (Many-to-Many relationship).

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/YourUsername/Restaurant-DBMS-Project.git](https://github.com/YourUsername/Restaurant-DBMS-Project.git)
cd Restaurant-DBMS-Project