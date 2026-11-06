# Smart Parking Management & Demand Analytics Platform

A web-based parking management application developed using Python Django and SQLite to manage parking slots, vehicle entry and exit, reservations, parking history, and revenue analytics.

## Overview

Smart Parking Management & Demand Analytics Platform helps simplify daily parking operations through a centralized web application.

The system allows administrators to manage parking slots, track vehicle movements, check slot availability, handle reservations, and maintain parking records.

It also calculates parking fees automatically and provides charts to understand daily revenue and parking slot usage.

## Key Features

- **Dashboard:** Displays parking statistics and important information.
- **Parking Slot Management:** Add and manage parking slots.
- **Vehicle Entry:** Record vehicle details during entry.
- **Vehicle Exit:** Update parking records when vehicles leave.
- **Slot Availability:** Track available and occupied parking slots.
- **Parking Reservations:** Manage parking bookings.
- **Parking History:** View previous parking records with search and filters.
- **Parking Fee Calculation:** Automatically calculate fees based on parking duration.
- **Revenue Analytics:** View parking revenue details.
- **Daily Revenue Chart:** Display daily revenue using Chart.js.
- **Parking Usage Chart:** Visualize parking slot usage.
- **Django Admin:** Manage application records through the admin panel.

## Parking Management Workflow

The application follows this basic parking process:

```text
Dashboard
    |
    v
Parking Slot Management
    |
    v
Check Slot Availability
    |
    v
Vehicle Entry
    |
    v
Parking Slot Allocation
    |
    v
Vehicle Parking
    |
    v
Vehicle Exit
    |
    v
Parking Fee Calculation
    |
    v
Parking History
    |
    v
Revenue Analytics
```

## System Architecture

The application follows a three-tier architecture.

| Layer | Technologies | Purpose |
|---|---|---|
| Presentation | HTML, CSS, Bootstrap, JavaScript, Chart.js | User interface and charts |
| Application | Python, Django | Backend logic and application functionality |
| Database | SQLite | Store and manage application data |

**Database Integration:** Django ORM

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | Django |
| Frontend | HTML, CSS, JavaScript |
| UI Framework | Bootstrap |
| Database | SQLite |
| Data Visualization | Chart.js |
| Version Control | Git and GitHub |
| Deployment | Render |

## Project Structure

```text
Smart-Parking-Management/
│
├── manage.py
├── requirements.txt
├── db.sqlite3
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── parking/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
└── README.md
```

*Note: The structure shown above is illustrative. Refer to the actual repository for the complete file structure.*

## Installation and Setup

Follow these steps to run the project on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/SaiKiranGandham/Smart-Parking-Management.git
```

### 2. Open the Project Folder

```bash
cd Smart-Parking-Management
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply Database Migrations

```bash
python manage.py migrate
```

### 7. Run the Application

```bash
python manage.py runserver
```

Open your browser and visit:

http://127.0.0.1:8000/

## Live Application

**Live Demo:**  
https://smart-parking-management-django-sai.onrender.com/

**GitHub Repository:**  
https://github.com/SaiKiranGandham/Smart-Parking-Management

## Project Role and Contributions

**Role: Full Stack Developer**

- Developed the application using Python and Django.
- Created web pages using HTML, CSS, Bootstrap, and JavaScript.
- Implemented backend functionality using Django.
- Managed application data using SQLite and Django ORM.
- Developed parking slot and vehicle management features.
- Implemented vehicle entry and exit functionality.
- Added parking reservations and history management.
- Implemented automatic parking fee calculation.
- Created revenue and parking usage charts using Chart.js.
- Deployed the application using Render.

## Future Enhancements

- QR code-based vehicle entry and exit.
- Online parking fee payments.
- Real-time parking availability.
- AI-based parking demand prediction.
- Mobile application support.
- Advanced parking reports and analytics.

## Author

**Sai Kiran Gandham**

B.Tech – Computer Science and Engineering (AI & ML)  
Sreenidhi Institute of Science and Technology, Hyderabad.

- GitHub: https://github.com/SaiKiranGandham
- LinkedIn: https://linkedin.com/in/sai-kiran-gandham-84a0b3248
- Portfolio: https://sai-kiran-portfolio-one.vercel.app/

---

*Smart Parking Management & Demand Analytics Platform – Making Parking Management Simple, Efficient, and Organized.*
