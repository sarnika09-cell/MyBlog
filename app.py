import sqlite3
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
# Add a secret key for session management (even if not fully used yet)
# IMPORTANT: Replace this with a strong, random key in a real application!
app.config['SECRET_KEY'] = 'a_very_secret_key_for_development' # Use secrets.token_hex(16) for real projects

DATABASE = 'blog_forum.db'

def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

# --- Main Index Page ---
@app.route('/')
def index():
    conn = get_db_connection()
    if not conn:
        return "<h1>Database Connection Error</h1><p>Could not connect to the database.</p>"
    
    # Fetch posts along with author username
    posts = conn.execute('''
        SELECT P.post_id, P.title, P.content, U.username AS author_username, P.created_at
        FROM Posts AS P
        JOIN Users AS U ON P.user_id = U.user_id
        ORDER BY P.created_at DESC;
    ''').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# --- Create New Post ---
@app.route('/new_post', methods=('GET', 'POST'))
def new_post():
    conn = get_db_connection()
    if not conn:
        return "<h1>Database Connection Error</h1><p>Could not connect to the database.</p>"

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id_str = request.form['user_id'] # Get user_id from form

        if not title or not content or not user_id_str:
            conn.close()
            return "<h1>Error: Title, Content, and Author are required!</h1>"

        try:
            user_id = int(user_id_str)
        except ValueError:
            conn.close()
            return "<h1>Error: User ID must be a number!</h1>"
        
        # Check if user_id exists
        existing_user = conn.execute("SELECT 1 FROM Users WHERE user_id = ?;", (user_id,)).fetchone()
        if not existing_user:
            conn.close()
            return "<h1>Error: Selected author does not exist!</h1>"

        try:
            conn.execute("INSERT INTO Posts (user_id, title, content) VALUES (?, ?, ?)",
                           (user_id, title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        except sqlite3.Error as e:
            conn.close()
            return f"<h1>Database Error: {e}</h1><p>Failed to create post. Please try again.</p>"
    
    # For GET request, fetch users to populate the dropdown
    users = conn.execute("SELECT user_id, username FROM Users;").fetchall()
    conn.close()
    return render_template('new_post.html', users=users)


# --- Edit Post ---
@app.route('/edit_post/<int:post_id>', methods=('GET', 'POST'))
def edit_post(post_id):
    conn = get_db_connection()
    if not conn:
        return "<h1>Database Connection Error</h1><p>Could not connect to the database.</p>"
    
    post = conn.execute("SELECT * FROM Posts WHERE post_id = ?", (post_id,)).fetchone()

    if post is None:
        conn.close()
        return "<h1>Post Not Found!</h1><p>The post you are trying to edit does not exist.</p>"

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title or not content:
            conn.close()
            return "<h1>Error: Title and Content are required!</h1>"

        try:
            conn.execute("UPDATE Posts SET title = ?, content = ? WHERE post_id = ?",
                           (title, content, post_id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        except sqlite3.Error as e:
            conn.close()
            return f"<h1>Database Error: {e}</h1><p>Failed to update post. Please try again.</p>"

    conn.close()
    return render_template('edit_post.html', post=post)

# --- Delete Post ---
@app.route('/delete_post/<int:post_id>', methods=('POST',))
def delete_post(post_id):
    conn = get_db_connection()
    if not conn:
        return "<h1>Database Connection Error</h1><p>Could not connect to the database.</p>"

    post = conn.execute("SELECT * FROM Posts WHERE post_id = ?", (post_id,)).fetchone()
    if post is None:
        conn.close()
        return "<h1>Post Not Found!</h1><p>The post you are trying to delete does not exist.</p>"

    try:
        conn.execute("DELETE FROM Posts WHERE post_id = ?", (post_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    except sqlite3.Error as e:
        conn.close()
        # This error might occur if there are issues with ON DELETE CASCADE
        return f"<h1>Database Error: {e}</h1><p>Failed to delete post. Please try again.</p>"


# --- New Route: View a Single Post and its Comments (post_detail.html) ---
@app.route('/post/<int:post_id>')
def post_detail(post_id):
    conn = get_db_connection()
    if not conn:
        return "<h1>Database Connection Error</h1><p>Could not connect to the database.</p>"

    # Fetch the specific post
    post = conn.execute('''
        SELECT P.post_id, P.title, P.content, U.username AS author_username, P.created_at
        FROM Posts AS P
        JOIN Users AS U ON P.user_id = U.user_id
        WHERE P.post_id = ?;
    ''', (post_id,)).fetchone()

    if post is None:
        conn.close()
        return "<h1>Post Not Found!</h1><p>The post you are looking for does not exist.</p>"

    # Fetch comments for this post
    comments = conn.execute('''
        SELECT C.comment_id, C.content, U.username AS commenter_username, C.created_at
        FROM Comments AS C
        JOIN Users AS U ON C.user_id = U.user_id
        WHERE C.post_id = ?
        ORDER BY C.created_at ASC;
    ''', (post_id,)).fetchall()

    # Fetch users for the 'add comment' form dropdown
    users = conn.execute("SELECT user_id, username FROM Users;").fetchall()

    conn.close()
    return render_template('post_detail.html', post=post, comments=comments, users=users)


# --- New Route: Add a Comment to a Post ---
@app.route('/post/<int:post_id>/add_comment', methods=('POST',))
def add_comment(post_id):
    conn = get_db_connection()
    if not conn:
        return "<h1>Database Connection Error</h1><p>Could not connect to the database.</p>"

    content = request.form['content']
    user_id_str = request.form['user_id'] # User ID for the comment author

    if not content or not user_id_str:
        conn.close()
        return f"<h1>Error: Comment content and author are required!</h1><p><a href='/post/{post_id}'>Go back</a></p>"

    try:
        user_id = int(user_id_str)
    except ValueError:
        conn.close()
        return f"<h1>Error: User ID must be a number!</h1><p><a href='/post/{post_id}'>Go back</a></p>"

    # Check if user_id exists
    existing_user = conn.execute("SELECT 1 FROM Users WHERE user_id = ?;", (user_id,)).fetchone()
    if not existing_user:
        conn.close()
        return f"<h1>Error: Comment author does not exist! Please select a valid author.</h1><p><a href='/post/{post_id}'>Go back</a></p>"

    try:
        conn.execute("INSERT INTO Comments (post_id, user_id, content) VALUES (?, ?, ?);",
                       (post_id, user_id, content))
        conn.commit()
        conn.close()
        return redirect(url_for('post_detail', post_id=post_id)) # Redirect back to the post detail
    except sqlite3.Error as e:
        conn.close()
        return f"<h1>Database Error: {e}</h1><p>Failed to add comment. Please try again.</p>"


# --- New Route: Edit a Comment ---
@app.route('/comment/<int:comment_id>/edit', methods=('GET', 'POST'))
def edit_comment(comment_id):
    conn = get_db_connection()
    if not conn:
        return "<h1>Database Connection Error</h1><p>Could not connect to the database.</p>"

    comment = conn.execute("SELECT * FROM Comments WHERE comment_id = ?", (comment_id,)).fetchone()

    if comment is None:
        conn.close()
        return "<h1>Comment Not Found!</h1><p>The comment you are trying to edit does not exist.</p>"

    if request.method == 'POST':
        content = request.form['content']

        if not content:
            conn.close()
            return f"<h1>Error: Comment content cannot be empty!</h1><p><a href='/comment/{comment_id}/edit'>Go back</a></p>"

        try:
            conn.execute("UPDATE Comments SET content = ? WHERE comment_id = ?", (content, comment_id))
            conn.commit()
            conn.close()
            # Redirect back to the post the comment belongs to
            return redirect(url_for('post_detail', post_id=comment['post_id']))
        except sqlite3.Error as e:
            conn.close()
            return f"<h1>Database Error: {e}</h1><p>Failed to update comment. Please try again.</p>"

    conn.close()
    return render_template('edit_comment.html', comment=comment)


# --- New Route: Delete a Comment ---
@app.route('/comment/<int:comment_id>/delete', methods=('POST',))
def delete_comment(comment_id):
    conn = get_db_connection()
    if not conn:
        return "<h1>Database Connection Error</h1><p>Could not connect to the database.</p>"

    # Get post_id to redirect back to the correct post detail page
    comment_info = conn.execute("SELECT post_id FROM Comments WHERE comment_id = ?", (comment_id,)).fetchone()

    if comment_info is None:
        conn.close()
        return "<h1>Comment Not Found!</h1><p>The comment you are trying to delete does not exist.</p>"

    try:
        conn.execute("DELETE FROM Comments WHERE comment_id = ?", (comment_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('post_detail', post_id=comment_info['post_id'])) # Redirect back to post detail
    except sqlite3.Error as e:
        conn.close()
        return f"<h1>Database Error: {e}</h1><p>Failed to delete comment. This might happen if there are complex constraints. Please try again.</p>"


if __name__ == '__main__':
    # Set debug=True for development. It auto-reloads and provides debug info.
    # Set debug=False for production.
    app.run(debug=True)