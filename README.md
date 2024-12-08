# EventAPI

EventAPI is a Django-based application that allows users to register, create events, and purchase event tickets. The application includes features for authentication, role-based access (Admin/User), and token-based authorization.

---

## Table of Contents
1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
    - [Creating a Superuser](#creating-a-superuser)
    - [Starting the Server](#starting-the-server)
    - [API Endpoints](#api-endpoints)
5. [SQL Query](#sql-query)
6. [Contributing](#contributing)
7. [License](#license)

---

## Features
- **Role-based Access Control**: Separate roles for Admin and User.
- **Event Management**: Admin can create and manage events.
- **Ticket Purchase**: Users can purchase tickets for events.
- **Token-based Authentication**: Secure access with JWT tokens.
- **Database Support**: PostgreSQL for data storage.

---

## Requirements
- **Python 3.8+**
- **Django 4.0+**
- **PostgreSQL**
- **Postman or similar API testing tool**

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone git@github.com:pawarJai/EventAPI.git
   cd EventAPI



2.**Create a Virtual Environment
->python3 -m venv venv

3. **Activate the Virtual Environment
Linux/Mac:
->source venv/bin/activate
Windows:
->venv\Scripts\activate

4.**Install Dependencies
->pip install -r requirements.txt

5. **Set Up PostgreSQL Database**
   - **Database Name**: `event`
   - **User**: `django_user`
   - **Password**: `root`
   - **Host**: `localhost`
   - **Port**: `5432`

6. **Apply Migrations
->python manage.py makemigrations
->python manage.py migrate

7. **Create a Superuser
->python manage.py createsuperuser

8. **Start the Django Server
->python manage.py runserver

9. **Login via Postman to Generate an Access Token
API Endpoint: http://127.0.0.1:8000/api/user/login/
Method: POST
Sample Body:{
    "email":"admin@gmail.com",
    "password":"1234"
}

10. **Add Users
API Endpoint:http://127.0.0.1:8000/api/user/register/
Method: POST
Sample Body:{
    "username": "jaypawar",
    "first_name": "jay",
    "last_name": "pawar",
    "email": "jaypawar@gmail.com",
    "role": "User",
    "password": "12345678"
}

11.**Add an Event (Admin Only)
API Endpoint:http://127.0.0.1:8000/api/events/
Header: Authorization: Bearer <token>
Method: POST
Sample Body: {
    "name": "Music Fest1",
    "date": "2024-12-21",
    "total_tickets": 500,
    "tickets_sold": 250
}

12. **Purchase Tickets (User Only)
API Endpoint: http://127.0.0.1:8000/api/tickets/1/purchase/
Method: POST
Header: Authorization: Bearer <token>
Sample Body:{
    "quantity": 4
}

13.**SQL Query
Write a custom SQL query to fetch the total tickets sold for all events along with event details. The query should optimize for large datasets and return the top 3 events by tickets sold.

SQL script:SELECT 
    id, name, date, total_tickets, tickets_sold 
FROM 
    events_event 
ORDER BY 
    tickets_sold DESC 
LIMIT 3;


