import os
from pathlib import Path
import sqlite3
import secrets
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Secret automatically generated and saved locally.
SECRET_FILE = Path("secret.key")

if SECRET_FILE.exists():
    SECRET_KEY = SECRET_FILE.read_text().strip()
else:
    SECRET_KEY = secrets.token_hex(32)
    SECRET_FILE.write_text(SECRET_KEY)

app.secret_key = SECRET_KEY

DB = "ai_zone.db"


def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    con = db()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            icon TEXT NOT NULL,
            description TEXT NOT NULL,
            affiliate_url TEXT DEFAULT '#',
            clicks INTEGER DEFAULT 0
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tool_id INTEGER NOT NULL,
            UNIQUE(user_id, tool_id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tool_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            UNIQUE(user_id, tool_id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS blog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    tools = [
        (
            "ChatGPT",
            "chatgpt",
            "AI Assistant",
            "🤖",
            "Writing, learning, brainstorming এবং coding-এর জন্য AI assistant."
        ),
        (
            "AI Design Tools",
            "design",
            "Design",
            "🎨",
            "Social media graphics এবং visual content তৈরির workflow."
        ),
        (
            "AI Video Tools",
            "video",
            "Video",
            "🎬",
            "Reels, Shorts এবং educational video তৈরির workflow."
        ),
        (
            "AI Writing Tools",
            "writing",
            "Writing",
            "✍️",
            "Caption, script, article এবং content ideas তৈরির workflow."
        ),
        (
            "AI Coding Tools",
            "coding",
            "Coding",
            "💻",
            "Coding শেখা, debugging এবং project planning-এর জন্য tools."
        )
    ]

    for tool in tools:
        cur.execute("""
            INSERT OR IGNORE INTO tools
            (name, slug, category, icon, description)
            VALUES (?, ?, ?, ?, ?)
        """, tool)

    con.commit()
    con.close()


init_db()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("এই page ব্যবহার করতে Login করুন।", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin"):
            flash("Admin access required.", "warning")
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)
    return wrapped


def track(page):
    con = db()
    con.execute("INSERT INTO visits (page) VALUES (?)", (page,))
    con.commit()
    con.close()


@app.route("/")
def home():
    track("/")
    return render_template("index.html")


@app.route("/tools")
def tools():
    track("/tools")
    category = request.args.get("category", "")
    search = request.args.get("q", "")

    con = db()

    if search:
        rows = con.execute("""
            SELECT * FROM tools
            WHERE name LIKE ? OR category LIKE ? OR description LIKE ?
            ORDER BY name
        """, (f"%{search}%", f"%{search}%", f"%{search}%")).fetchall()

    elif category:
        rows = con.execute("""
            SELECT * FROM tools
            WHERE category = ?
            ORDER BY name
        """, (category,)).fetchall()

    else:
        rows = con.execute(
            "SELECT * FROM tools ORDER BY name"
        ).fetchall()

    categories = con.execute(
        "SELECT DISTINCT category FROM tools ORDER BY category"
    ).fetchall()

    con.close()

    return render_template(
        "tools.html",
        tools=rows,
        categories=categories,
        search=search,
        selected_category=category
    )


@app.route("/tool/<slug>")
def tool_details(slug):
    con = db()

    tool = con.execute(
        "SELECT * FROM tools WHERE slug = ?",
        (slug,)
    ).fetchone()

    if not tool:
        con.close()
        return "Tool not found", 404

    rating = con.execute("""
        SELECT AVG(rating) AS average, COUNT(*) AS total
        FROM ratings
        WHERE tool_id = ?
    """, (tool["id"],)).fetchone()

    favorite = False

    if "user_id" in session:
        favorite = con.execute("""
            SELECT id FROM favorites
            WHERE user_id = ? AND tool_id = ?
        """, (session["user_id"], tool["id"])).fetchone() is not None

    con.close()

    return render_template(
        "tool.html",
        tool=tool,
        rating=rating,
        favorite=favorite
    )


@app.route("/go/<slug>")
def affiliate_redirect(slug):
    con = db()

    tool = con.execute(
        "SELECT * FROM tools WHERE slug = ?",
        (slug,)
    ).fetchone()

    if not tool:
        con.close()
        return redirect(url_for("tools"))

    con.execute(
        "UPDATE tools SET clicks = clicks + 1 WHERE id = ?",
        (tool["id"],)
    )

    con.commit()

    link = tool["affiliate_url"]

    con.close()

    if not link or link == "#":
        flash(
            "এই tool-এর official/approved link এখনো যোগ করা হয়নি।",
            "info"
        )
        return redirect(url_for("tool_details", slug=slug))

    return redirect(link)


@app.route("/favorite/<int:tool_id>", methods=["POST"])
@login_required
def favorite(tool_id):
    con = db()

    exists = con.execute("""
        SELECT id FROM favorites
        WHERE user_id = ? AND tool_id = ?
    """, (session["user_id"], tool_id)).fetchone()

    if exists:
        con.execute(
            "DELETE FROM favorites WHERE id = ?",
            (exists["id"],)
        )
    else:
        con.execute("""
            INSERT OR IGNORE INTO favorites(user_id, tool_id)
            VALUES (?, ?)
        """, (session["user_id"], tool_id))

    con.commit()
    con.close()

    return redirect(request.referrer or url_for("tools"))


@app.route("/rate/<int:tool_id>", methods=["POST"])
@login_required
def rate(tool_id):
    try:
        rating = int(request.form.get("rating", 0))
    except ValueError:
        rating = 0

    if rating not in range(1, 6):
        flash("Rating 1 থেকে 5-এর মধ্যে দিন।", "warning")
        return redirect(request.referrer or url_for("tools"))

    con = db()

    con.execute("""
        INSERT INTO ratings(user_id, tool_id, rating)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, tool_id)
        DO UPDATE SET rating=excluded.rating
    """, (session["user_id"], tool_id, rating))

    con.commit()
    con.close()

    flash("আপনার rating save হয়েছে ⭐", "success")

    return redirect(request.referrer or url_for("tools"))


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if len(username) < 3 or len(password) < 6:
            flash(
                "Username কমপক্ষে 3 এবং password কমপক্ষে 6 characters হতে হবে।",
                "warning"
            )
            return render_template("register.html")

        con = db()

        try:
            con.execute("""
                INSERT INTO users(username, email, password)
                VALUES (?, ?, ?)
            """, (
                username,
                email,
                generate_password_hash(password)
            ))

            con.commit()

        except sqlite3.IntegrityError:
            con.close()
            flash("Username বা Email আগে থেকেই ব্যবহার হয়েছে।", "warning")
            return render_template("register.html")

        con.close()

        flash("Registration সফল হয়েছে। এখন Login করুন।", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        con = db()

        user = con.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        con.close()

        if user and check_password_hash(user["password"], password):

            session.clear()

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(url_for("home"))

        flash("Email অথবা password সঠিক নয়।", "warning")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/profile")
@login_required
def profile():

    con = db()

    favorites = con.execute("""
        SELECT tools.*
        FROM favorites
        JOIN tools ON tools.id = favorites.tool_id
        WHERE favorites.user_id = ?
        ORDER BY tools.name
    """, (session["user_id"],)).fetchall()

    con.close()

    return render_template(
        "profile.html",
        favorites=favorites
    )


@app.route("/tutorials")
def tutorials():
    track("/tutorials")
    return render_template("tutorials.html")


@app.route("/social")
def social():
    track("/social")
    return render_template("social.html")


@app.route("/blog")
def blog():
    track("/blog")

    con = db()
    posts = con.execute(
        "SELECT * FROM blog ORDER BY id DESC"
    ).fetchall()
    con.close()

    return render_template("blog.html", posts=posts)


@app.route("/services")
def services():
    track("/services")
    return render_template("services.html")


@app.route("/monetization")
def monetization():
    return render_template("monetization.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():

    message = None

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        user_message = request.form.get("message", "").strip()

        if name and email and user_message:

            con = db()

            con.execute("""
                INSERT INTO messages(name, email, message)
                VALUES (?, ?, ?)
            """, (name, email, user_message))

            con.commit()
            con.close()

            message = "ধন্যবাদ! আপনার message গ্রহণ করা হয়েছে।"

    return render_template(
        "contact.html",
        message=message
    )


# -------------------------
# ADMIN
# -------------------------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        password = request.form.get("password", "")

        admin_password = os.environ.get("AI_ZONE_ADMIN_PASSWORD")

        if not admin_password:
            flash(
                "AI_ZONE_ADMIN_PASSWORD সেট করা হয়নি।",
                "warning"
            )
            return render_template("admin_login.html")

        if secrets.compare_digest(password, admin_password):

            session.clear()
            session["admin"] = True

            return redirect(url_for("admin_dashboard"))

        flash("Admin password সঠিক নয়।", "warning")

    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("home"))


@app.route("/admin")
@admin_required
def admin_dashboard():

    con = db()

    users = con.execute(
        "SELECT COUNT(*) AS total FROM users"
    ).fetchone()["total"]

    visits = con.execute(
        "SELECT COUNT(*) AS total FROM visits"
    ).fetchone()["total"]

    messages = con.execute(
        "SELECT COUNT(*) AS total FROM messages"
    ).fetchone()["total"]

    clicks = con.execute("""
        SELECT name, clicks
        FROM tools
        ORDER BY clicks DESC
    """).fetchall()

    recent_messages = con.execute("""
        SELECT *
        FROM messages
        ORDER BY id DESC
        LIMIT 10
    """).fetchall()

    con.close()

    return render_template(
        "admin.html",
        users=users,
        visits=visits,
        messages=messages,
        clicks=clicks,
        recent_messages=recent_messages
    )


@app.route("/admin/blog", methods=["POST"])
@admin_required
def admin_blog():

    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if title and content:

        con = db()

        con.execute("""
            INSERT INTO blog(title, content)
            VALUES (?, ?)
        """, (title, content))

        con.commit()
        con.close()

        flash("Blog post তৈরি হয়েছে।", "success")

    return redirect(url_for("admin_dashboard"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
