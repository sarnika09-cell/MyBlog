# MyBlog - A Simple Flask Blog Application

## Overview
This is a basic blogging platform built using the Flask web framework in Python and SQLite for the database. It allows users to create, view, edit, and delete blog posts, as well as add, edit, and delete comments on those posts.

## Features
* **Post Management:** Create, Read, Update, Delete (CRUD) operations for blog posts.
* **Comment System:** Users can add, edit, and delete comments on individual posts.
* **SQLite Database:** Simple, file-based database for easy setup.
* **Basic Styling:** Clean and readable user interface.

## Technologies Used
Flask: Python web framework.

SQLite: Database.

HTML/CSS: Frontend structure and styling.
**Python 3.x**

**Setup Instructions**

Follow these steps to get the project up and running on your local machine.

 1. Clone the repository

git clone [https://github.com/](https://github.com/)

2. Create and activate a virtual environment
It's highly recommended to use a virtual environment to manage dependencies.

Bash

python3 -m venv .venv
source .venv/bin/activate
(On Windows, use .\.venv\Scripts\activate)

3. Install dependencies
Bash

pip install Flask
pip install gunicorn # Optional, for production deployment later

4. Initialize the database
This will create the blog_forum.db file and set up the necessary tables (Users, Posts, Comments) and add some initial users.

Bash

python init_db.py
5. Run the Flask application
Set the Flask app environment variable and then run the application.

Bash

export FLASK_APP=app.py
export FLASK_ENV=development # For development mode with auto-reloading
flask run
(On Windows, use set FLASK_APP=app.py and set FLASK_ENV=development)

The application will typically run at http://127.0.0.1:5000/ in your browser.

Usage
Home Page: View all posts.
Create New Post: Add new blog entries.
View Post & Comments: Click on a post to see its full content and manage comments.
Edit/Delete: Modify or remove existing posts and comments.

License
Distributed under the MIT License. See LICENSE for more information.

Contact
If you have any questions, feel free to reach out:
GitHub: @sarnika09-cell
Email: sarnikapullimula09@gmail.com
 







