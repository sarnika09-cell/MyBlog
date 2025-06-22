import sqlite3

# Define your database file name
DATABASE_FILE = 'blog_forum.db'

def init_database():
    conn = None
    try:
        # Connect to the SQLite database. If the file doesn't exist, it will be created.
        conn = sqlite3.connect(DATABASE_FILE)
        # Set row_factory to sqlite3.Row for dictionary-like access to rows
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # --- SQL for creating the Users table ---
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                -- password TEXT NOT NULL, -- Keep this commented for now if not doing user auth yet
                email TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        print("Users table checked/created.")

        # --- Insert some initial users (for testing comments) ---
        # INSERT OR IGNORE will only insert if the username doesn't already exist
        cursor.execute("INSERT OR IGNORE INTO Users (username, email) VALUES (?, ?);", ('Alice', 'alice@example.com'))
        cursor.execute("INSERT OR IGNORE INTO Users (username, email) VALUES (?, ?);", ('Bob', 'bob@example.com'))
        cursor.execute("INSERT OR IGNORE INTO Users (username, email) VALUES (?, ?);", ('Charlie', 'charlie@example.com'))
        print("Initial users added (if not existing).")

        # --- SQL for creating the Posts table ---
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Posts (
                post_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE
            );
        ''')
        print("Posts table checked/created.")

        # --- SQL for creating the Comments table ---
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Comments (
                comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES Posts (post_id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE
            );
        ''')
        print("Comments table checked/created.")

        # --- Optional: Add some initial posts (for testing) ---
        # Example: Check if 'First Post' exists and add it if not, using an existing user_id
        # You'll need to know a user_id from your Users table (e.g., 1 for Alice)
        # If your Users table is empty, create a user first before adding posts
        # cursor.execute("""
        #     INSERT INTO Posts (user_id, title, content)
        #     SELECT 1, 'Welcome to My Blog', 'This is the very first post on our new blog platform!'
        #     WHERE NOT EXISTS(SELECT 1 FROM Posts WHERE title = 'Welcome to My Blog');
        # """)
        # cursor.execute("""
        #     INSERT INTO Posts (user_id, title, content)
        #     SELECT 2, 'Thoughts on Flask Development', 'Flask makes web development so much fun. Loving the Jinja2 templates!'
        #     WHERE NOT EXISTS(SELECT 1 FROM Posts WHERE title = 'Thoughts on Flask Development');
        # """)
        # print("Initial posts added (if not existing).")

        conn.commit() # Save all changes
        print(f"Database '{DATABASE_FILE}' initialized/updated successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close() # Always close the connection

# To run this script and initialize your database
if __name__ == '__main__':
    init_database()