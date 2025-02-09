# Ticketing System

A robust and scalable ticketing system built with Django and Django REST Framework (DRF). This system allows users to create and manage support tickets, with threaded conversations for each ticket. It includes user authentication, role-based access control, and API documentation.

---

## Features

- **User Authentication**: JWT-based authentication for secure API access
- **Ticket Management**:
  - Create, read, update, and delete tickets
  - Set ticket status (Open, Pending, Closed) and priority (Low, Medium, High)
- **Conversation Threads**:
  - Threaded messages for each ticket
  - Automatic admin response tagging
- **Role-Based Access Control**:
  - Regular users can manage their own tickets
  - Admins/Agents can manage all tickets
- **API Documentation**:
  - Swagger UI for interactive API exploration
  - ReDoc for clean API documentation

---

## API Endpoints

### Authentication
- `POST /api/v1/accounts/register/` - Register new user
- `POST /api/v1/accounts/login/` - Login and get JWT tokens
- `GET /api/v1/accounts/me/` - Get current user profile

### Tickets
- `GET /api/v1/tickets/` - List all tickets
- `POST /api/v1/tickets/` - Create new ticket
- `GET /api/v1/tickets/{id}/` - Retrieve ticket details
- `PATCH /api/v1/tickets/{id}/` - Update ticket
- `DELETE /api/v1/tickets/{id}/` - Delete ticket

### Messages
- `GET /api/v1/tickets/{ticket_id}/messages/` - List all messages for a ticket
- `POST /api/v1/tickets/{ticket_id}/messages/` - Create new message

### Admin (Staff Only)
- `GET /api/v1/accounts/users/` - List all users

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL (or SQLite for development)
- pipenv (recommended)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/amiiirm8/ticketing-system.git
   cd ticketing-system