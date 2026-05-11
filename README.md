# Campus Exchange - Django Term Project

This is a full-stack Django web application designed for a university term project. It allows students to buy, sell, or exchange items within the campus. 

## Features (According to Grading Scheme)

- **Core Functionality**: Full CRUD operations for Items (Create, Read, Update, Delete). Uses Django MVT architecture.
- **Database Design**: Three main models: `User` (built-in), `Category`, `Item`, and `Comment`. Demonstrates use of Foreign Keys and constraints.
- **Frontend & UX**: Built with HTML, CSS, and Bootstrap 5 for a clean, responsive, and mobile-friendly user interface.
- **Advanced Features**:
  1. **Authentication System**: Full login/signup/logout implementation.
  2. **Authorization**: Only item owners can edit or delete their items.
  3. **Search & Filter**: Users can search for items by title/description or filter by category.
- **Code Quality**: Modular views, clean templates with template inheritance, and well-structured code.

## Setup Instructions

1. Ensure Python 3.10+ is installed on your system.
2. Open terminal in the project directory.
3. Activate the virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Run migrations: `python manage.py migrate`
5. Create a superuser (optional, for admin access): `python manage.py createsuperuser`
6. Start the development server: `python manage.py runserver`
7. Open `http://127.0.0.1:8000/` in your browser.

## Database Schema / Models

- **Category**: Classifies items (e.g., Electronics, Books).
- **Item**: The main product being sold/exchanged. Contains title, price, description, and an image field.
- **Comment**: Allows users to ask questions on an item page.
