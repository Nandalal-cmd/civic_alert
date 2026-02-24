# CivicAlert

CivicAlert is a professional infrastructure management platform that allows citizens to report municipal issues and track them in real-time. Municipal administrators can manage these reports, assign priority, and update statuses.

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- MySQL Server
- Virtual Environment (recommended)

### Installation
1.  **Clone the project** to your local machine.
2.  **Set up the environment**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    pip install django mysqlclient
    ```
3.  **Database Configuration**:
    - Create a database in MySQL named `civic_alert_pro`.
    - Update `DATABASES` settings in `civicalert_project/settings.py` with your MySQL credentials.
4.  **Applied Migrations**:
    ```bash
    python manage.py migrate
    ```
5.  **Run the Server**:
    ```bash
    python manage.py runserver
    ```

---

## 🛠 Tools & Resources

-   **Backend Framework**: [Django 6.0](https://www.djangoproject.com/) (Python)
-   **Database**: [MySQL](https://www.mysql.com/) (Professional relational schema)
-   **Frontend Styling**: [Tailwind CSS](https://tailwindcss.com/)
-   **Mapping**: [Leaflet.js](https://leafletjs.com/) with OpenStreetMap data
-   **Icons**: Standard emoji and Lucide-like icons for simplicity and performance.

---

## 🔒 Security Implementation

The project implements several layers of security to protect data and user privacy:

1.  **Authentication & Authorization**:
    - Secure login system for Citizens and Staff.
    - `is_staff` check for all administrative actions (Admin Dashboard).
2.  **CSRF Protection**: Standard Django Cross-Site Request Forgery protection on all POST requests.
3.  **Password Security**: Industry-standard PBKDF2 hashing for all user passwords.
4.  **Database Security**:
    - **Mapped Schema**: Application models are manually mapped to a professional SQL schema (`pro_relational_schema.sql`) using `db_table` and `db_column` to ensure strict structure.
    - **Foreign Key Constraints**: Strict `ON DELETE CASCADE` and `ON DELETE SET NULL` constraints to prevent orphaned data.
    - **ORM Layer**: Prevents SQL Injection by using Django's abstracted database interaction.
5.  **Data Integrity**: Duplicate detection logic in the Citizen Dashboard prevents spam and duplicate reporting.

---

## 🏗 Project Architecture

-   **`complaints`**: The main application containing models, views, and templates.
-   **`civicalert_project`**: Project configuration and settings.
-   **`media/`**: Stores uploaded images for complaints.
-   **Map Logic**: Integrated directly into `dashboard.html` (Citizen) and `admin_dashboard.html` (Admin) using Leaflet.js.

---

## ⬆️ Future Upgrades

To upgrade or add features:
1.  **New Models**: Add to `complaints/models.py` and map them to SQL tables using `class Meta: db_table = '...'`.
2.  **Migrations**: Use `python manage.py makemigrations` and `migrate` to keep Django's state in sync.
3.  **Frontend**: The project uses a CDN for Tailwind CSS for easy prototyping. For production, consider a build step.
