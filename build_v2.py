from pathlib import Path

files = {

"app.py": r'''
import os
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
''',

"templates/base.html": r'''
<!DOCTYPE html>
<html lang="bn">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<meta name="description"
content="AI Zone বাংলা - AI, Technology এবং Digital Skills শেখার platform">

<title>{% block title %}AI Zone বাংলা{% endblock %}</title>

<link rel="stylesheet"
href="{{ url_for('static', filename='style.css') }}">

</head>

<body>

<header class="navbar">

<a class="logo" href="/">
🤖 AI Zone বাংলা
</a>

<button class="menu-btn"
onclick="toggleMenu()">☰</button>

<nav id="navMenu">

<a href="/">🏠 Home</a>
<a href="/tools">🤖 Tools</a>
<a href="/tutorials">📚 Tutorials</a>
<a href="/blog">📰 Blog</a>
<a href="/services">🛠️ Services</a>

{% if session.get("user_id") %}
<a href="/profile">👤 Profile</a>
<a href="/logout">Logout</a>
{% else %}
<a href="/login">Login</a>
<a href="/register">Register</a>
{% endif %}

<a href="/contact">📩 Contact</a>

<button class="theme-btn"
onclick="toggleTheme()">🌙</button>

</nav>

</header>

{% with messages = get_flashed_messages(with_categories=true) %}

{% if messages %}

<div class="flash-container">

{% for category, message in messages %}

<div class="flash {{ category }}">
{{ message }}
</div>

{% endfor %}

</div>

{% endif %}

{% endwith %}

<main>

{% block content %}
{% endblock %}

</main>

<footer>

<h3>🤖 AI Zone বাংলা</h3>

<p>
AI • Technology • Web Development • Social Media
</p>

<p>
<a href="/monetization">💰 Monetization</a>
</p>

<p>© 2026 AI Zone বাংলা</p>

</footer>

<script src="{{ url_for('static', filename='script.js') }}"></script>

</body>

</html>
''',

"templates/index.html": r'''
{% extends "base.html" %}

{% block title %}AI Zone বাংলা{% endblock %}

{% block content %}

<section class="hero">

<div class="hero-content">

<span class="badge">
🚀 Learn AI in Bangla
</span>

<h1>
AI শিখুন<br>
<span>সহজ বাংলায়</span>
</h1>

<p>
AI Tools, ChatGPT, Web Development এবং
Social Media সম্পর্কে সহজভাবে শেখার জন্য
AI Zone বাংলায় স্বাগতম।
</p>

<div class="buttons">

<a class="btn primary"
href="/tools">
🤖 AI Tools
</a>

<a class="btn secondary"
href="/tutorials">
📚 Tutorials
</a>

</div>

</div>

</section>

<section class="section">

<h2>AI Zone বাংলায় কী পাবেন?</h2>

<div class="cards">

<div class="card">
<div class="icon">🤖</div>
<h3>AI Tools</h3>
<p>Useful AI tools এবং তাদের ব্যবহার সম্পর্কে জানুন।</p>
</div>

<div class="card">
<div class="icon">📚</div>
<h3>Tutorials</h3>
<p>একদম শুরু থেকে সহজ বাংলায় শেখার resources.</p>
</div>

<div class="card">
<div class="icon">📰</div>
<h3>Blog</h3>
<p>AI ও technology নিয়ে সহজ বাংলা articles.</p>
</div>

<div class="card">
<div class="icon">🛠️</div>
<h3>Services</h3>
<p>Digital এবং AI-based service ideas.</p>
</div>

</div>

</section>

<section class="cta">

<h2>🚀 আজ থেকেই শেখা শুরু করুন</h2>

<p>
প্রথমে শেখা, তারপর audience তৈরি,
তারপর বৈধ monetization।
</p>

<a class="btn primary"
href="/tools">
Explore Tools
</a>

</section>

{% endblock %}
''',

"templates/tools.html": r'''
{% extends "base.html" %}

{% block title %}AI Tools{% endblock %}

{% block content %}

<section class="page-header">

<h1>🤖 AI Tools</h1>

<p>AI tools খুঁজুন এবং ব্যবহার সম্পর্কে জানুন</p>

</section>

<section class="section">

<form class="search-box" method="GET">

<input
type="search"
name="q"
value="{{ search }}"
placeholder="🔍 Tool খুঁজুন...">

<button type="submit">
Search
</button>

</form>

<div class="category-row">

<a href="/tools">All</a>

{% for category in categories %}

<a href="/tools?category={{ category['category'] }}">
{{ category['category'] }}
</a>

{% endfor %}

</div>

<div class="cards">

{% for tool in tools %}

<div class="card">

<div class="icon">
{{ tool['icon'] }}
</div>

<h3>
{{ tool['name'] }}
</h3>

<p>
{{ tool['description'] }}
</p>

<span class="tag">
{{ tool['category'] }}
</span>

<br>

<a class="btn primary"
href="/tool/{{ tool['slug'] }}">
Details →
</a>

</div>

{% else %}

<p>কোনো tool পাওয়া যায়নি।</p>

{% endfor %}

</div>

</section>

{% endblock %}
''',

"templates/tool.html": r'''
{% extends "base.html" %}

{% block title %}{{ tool['name'] }}{% endblock %}

{% block content %}

<section class="page-header">

<h1>
{{ tool['icon'] }}
{{ tool['name'] }}
</h1>

<p>
{{ tool['category'] }}
</p>

</section>

<section class="section">

<div class="about-box">

<h2>
{{ tool['icon'] }} {{ tool['name'] }}
</h2>

<p>
{{ tool['description'] }}
</p>

<div class="rating">

⭐ Average:
{% if rating['average'] %}
{{ "%.1f"|format(rating['average']) }}/5
{% else %}
No rating yet
{% endif %}

</div>

<div class="notice">

💡 Educational information:
AI Zone বাংলা এই tool-এর ব্যবহার সম্পর্কে
শিক্ষামূলক information প্রদান করছে।

</div>

<a class="btn primary"
href="/go/{{ tool['slug'] }}">
Visit Tool →
</a>

{% if session.get("user_id") %}

<form method="POST"
action="/favorite/{{ tool['id'] }}"
style="margin-top:15px;">

<button type="submit">

{% if favorite %}
❤️ Remove Favorite
{% else %}
🤍 Add Favorite
{% endif %}

</button>

</form>

<h3 style="margin-top:30px;">
⭐ আপনার Rating
</h3>

<form method="POST"
action="/rate/{{ tool['id'] }}"
class="rating-form">

<select name="rating">

<option value="5">⭐⭐⭐⭐⭐</option>
<option value="4">⭐⭐⭐⭐</option>
<option value="3">⭐⭐⭐</option>
<option value="2">⭐⭐</option>
<option value="1">⭐</option>

</select>

<button type="submit">
Save Rating
</button>

</form>

{% else %}

<p style="margin-top:20px;">
Rating/Favorite ব্যবহার করতে
<a href="/login">Login</a> করুন।
</p>

{% endif %}

</div>

</section>

{% endblock %}
''',

"templates/register.html": r'''
{% extends "base.html" %}

{% block title %}Register{% endblock %}

{% block content %}

<section class="page-header">
<h1>👤 Register</h1>
</section>

<section class="section">

<div class="auth-box">

<form method="POST">

<input
name="username"
placeholder="Username"
required>

<input
type="email"
name="email"
placeholder="Email"
required>

<input
type="password"
name="password"
placeholder="Password - minimum 6 characters"
required>

<button type="submit">
Create Account
</button>

</form>

<p>
Already registered?
<a href="/login">Login</a>
</p>

</div>

</section>

{% endblock %}
''',

"templates/login.html": r'''
{% extends "base.html" %}

{% block title %}Login{% endblock %}

{% block content %}

<section class="page-header">
<h1>🔐 Login</h1>
</section>

<section class="section">

<div class="auth-box">

<form method="POST">

<input
type="email"
name="email"
placeholder="Email"
required>

<input
type="password"
name="password"
placeholder="Password"
required>

<button type="submit">
Login
</button>

</form>

<p>
No account?
<a href="/register">Register</a>
</p>

</div>

</section>

{% endblock %}
''',

"templates/profile.html": r'''
{% extends "base.html" %}

{% block title %}Profile{% endblock %}

{% block content %}

<section class="page-header">

<h1>👤 {{ session['username'] }}</h1>

<p>Your AI Zone বাংলা profile</p>

</section>

<section class="section">

<h2>❤️ Favorite Tools</h2>

<div class="cards">

{% for tool in favorites %}

<div class="card">

<div class="icon">
{{ tool['icon'] }}
</div>

<h3>
{{ tool['name'] }}
</h3>

<p>
{{ tool['description'] }}
</p>

<a class="btn primary"
href="/tool/{{ tool['slug'] }}">
Open
</a>

</div>

{% else %}

<p>
এখনো কোনো favorite tool নেই।
</p>

{% endfor %}

</div>

</section>

{% endblock %}
''',

"templates/tutorials.html": r'''
{% extends "base.html" %}

{% block title %}Tutorials{% endblock %}

{% block content %}

<section class="page-header">

<h1>📚 Tutorials</h1>

<p>শুরু থেকে শেখার সহজ resources</p>

</section>

<section class="section">

<div class="cards">

<div class="card">
<div class="icon">🐍</div>
<h3>Python</h3>
<p>Python basics এবং ছোট project.</p>
</div>

<div class="card">
<div class="icon">🌐</div>
<h3>HTML & CSS</h3>
<p>Website structure এবং design.</p>
</div>

<div class="card">
<div class="icon">🔥</div>
<h3>Flask</h3>
<p>Python দিয়ে web application.</p>
</div>

<div class="card">
<div class="icon">🐙</div>
<h3>GitHub</h3>
<p>Project version control এবং publishing.</p>
</div>

<div class="card">
<div class="icon">📱</div>
<h3>Termux</h3>
<p>Android-এ coding environment.</p>
</div>

<div class="card">
<div class="icon">🤖</div>
<h3>AI Learning</h3>
<p>AI দিয়ে productivity বাড়ানোর workflow.</p>
</div>

</div>

</section>

{% endblock %}
''',

"templates/social.html": r'''
{% extends "base.html" %}

{% block title %}Social Media{% endblock %}

{% block content %}

<section class="page-header">

<h1>📱 Social Media</h1>

<p>Content creation ideas</p>

</section>

<section class="section">

<div class="cards">

<div class="card">
<div class="icon">📘</div>
<h3>Facebook</h3>
<p>Educational posts এবং Reels.</p>
</div>

<div class="card">
<div class="icon">📸</div>
<h3>Instagram</h3>
<p>Reels এবং carousel content.</p>
</div>

<div class="card">
<div class="icon">🎬</div>
<h3>Short Video</h3>
<p>Short-form educational content.</p>
</div>

</div>

</section>

{% endblock %}
''',

"templates/blog.html": r'''
{% extends "base.html" %}

{% block title %}Blog{% endblock %}

{% block content %}

<section class="page-header">

<h1>📰 AI Zone বাংলা Blog</h1>

<p>AI ও Technology নিয়ে সহজ বাংলা articles</p>

</section>

<section class="section">

{% for post in posts %}

<div class="card blog-card">

<h2>{{ post['title'] }}</h2>

<p>
{{ post['content'] }}
</p>

<small>
{{ post['created_at'] }}
</small>

</div>

{% else %}

<div class="card">

<h3>🚀 প্রথম Blog শীঘ্রই আসছে</h3>

<p>
Admin dashboard থেকে Blog post তৈরি করা যাবে।
</p>

</div>

{% endfor %}

</section>

{% endblock %}
''',

"templates/services.html": r'''
{% extends "base.html" %}

{% block title %}Services{% endblock %}

{% block content %}

<section class="page-header">

<h1>🛠️ Services</h1>

<p>AI এবং Digital service ideas</p>

</section>

<section class="section">

<div class="cards">

<div class="card">
<div class="icon">🎨</div>
<h3>Social Media Design</h3>
<p>Social media visual content তৈরি।</p>
</div>

<div class="card">
<div class="icon">✍️</div>
<h3>AI Content</h3>
<p>Caption, script এবং content তৈরি।</p>
</div>

<div class="card">
<div class="icon">🌐</div>
<h3>Website Setup</h3>
<p>Basic website development service.</p>
</div>

</div>

</section>

{% endblock %}
''',

"templates/about.html": r'''
{% extends "base.html" %}

{% block title %}About{% endblock %}

{% block content %}

<section class="page-header">

<h1>ℹ️ AI Zone বাংলা</h1>

<p>AI ও Technology শেখার learning project</p>

</section>

<section class="section">

<div class="about-box">

<h2>আমাদের লক্ষ্য</h2>

<p>
AI, Web Development এবং Digital Technology
সহজ বাংলায় শেখার সুযোগ তৈরি করা।
</p>

<p>
এই project Python, Flask, SQLite,
HTML, CSS এবং JavaScript দিয়ে তৈরি।
</p>

</div>

</section>

{% endblock %}
''',

"templates/monetization.html": r'''
{% extends "base.html" %}

{% block title %}Monetization{% endblock %}

{% block content %}

<section class="page-header">

<h1>💰 Monetization</h1>

<p>ভবিষ্যতে income তৈরির সম্ভাব্য পথ</p>

</section>

<section class="section">

<div class="cards">

<div class="card">
<div class="icon">🔗</div>
<h3>Affiliate Marketing</h3>
<p>
Approved affiliate programs-এর referral
commission-এর মাধ্যমে income-এর সুযোগ।
</p>
</div>

<div class="card">
<div class="icon">📢</div>
<h3>Advertising</h3>
<p>
ভবিষ্যতে website traffic তৈরি হলে
advertising options দেখা যেতে পারে।
</p>
</div>

<div class="card">
<div class="icon">🤝</div>
<h3>Sponsored Content</h3>
<p>
Relevant brands-এর সাথে paid collaboration.
</p>
</div>

<div class="card">
<div class="icon">🛠️</div>
<h3>Services</h3>
<p>
AI content, design এবং website services.
</p>
</div>

</div>

<div class="notice">

⚠️ Income guaranteed নয়।
Affiliate program-এর নিজের approval এবং terms থাকে।

</div>

</section>

{% endblock %}
''',

"templates/contact.html": r'''
{% extends "base.html" %}

{% block title %}Contact{% endblock %}

{% block content %}

<section class="page-header">

<h1>📩 Contact</h1>

<p>আপনার message পাঠান</p>

</section>

<section class="section">

<div class="auth-box">

{% if message %}

<div class="flash success">
{{ message }}
</div>

{% endif %}

<form method="POST">

<input
type="text"
name="name"
placeholder="আপনার নাম"
required>

<input
type="email"
name="email"
placeholder="আপনার Email"
required>

<textarea
name="message"
placeholder="আপনার Message"
rows="6"
required></textarea>

<button type="submit">
Send Message 🚀
</button>

</form>

</div>

</section>

{% endblock %}
''',

"templates/admin_login.html": r'''
{% extends "base.html" %}

{% block title %}Admin Login{% endblock %}

{% block content %}

<section class="page-header">

<h1>🔐 Admin Login</h1>

<p>Private administrator area</p>

</section>

<section class="section">

<div class="auth-box">

<form method="POST">

<input
type="password"
name="password"
placeholder="Admin Password"
required>

<button type="submit">
Login
</button>

</form>

</div>

</section>

{% endblock %}
''',

"templates/admin.html": r'''
{% extends "base.html" %}

{% block title %}Admin Dashboard{% endblock %}

{% block content %}

<section class="page-header">

<h1>📊 Admin Dashboard</h1>

<p>
<a href="/admin/logout">Logout</a>
</p>

</section>

<section class="section">

<div class="stats">

<div>
<strong>{{ users }}</strong>
<span>Users</span>
</div>

<div>
<strong>{{ visits }}</strong>
<span>Page Visits</span>
</div>

<div>
<strong>{{ messages }}</strong>
<span>Messages</span>
</div>

</div>


<h2 style="margin-top:50px;">
🔗 Affiliate Clicks
</h2>

<div class="cards">

{% for tool in clicks %}

<div class="card">

<h3>
{{ tool['name'] }}
</h3>

<p>
Clicks: <strong>{{ tool['clicks'] }}</strong>
</p>

</div>

{% endfor %}

</div>


<h2 style="margin-top:50px;">
📰 Create Blog Post
</h2>

<div class="auth-box">

<form method="POST"
action="/admin/blog">

<input
name="title"
placeholder="Blog Title"
required>

<textarea
name="content"
rows="8"
placeholder="Blog content"
required></textarea>

<button type="submit">
Publish Blog
</button>

</form>

</div>


<h2 style="margin-top:50px;">
📩 Recent Messages
</h2>

{% for message in recent_messages %}

<div class="card"
style="margin-top:15px;">

<h3>
{{ message['name'] }}
</h3>

<p>
{{ message['email'] }}
</p>

<p>
{{ message['message'] }}
</p>

<small>
{{ message['created_at'] }}
</small>

</div>

{% else %}

<p>কোনো message নেই।</p>

{% endfor %}

</section>

{% endblock %}
'''
}


# Write files
for filename, content in files.items():

    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        content.strip() + "\n",
        encoding="utf-8"
    )


# CSS
Path("static").mkdir(exist_ok=True)

Path("static/style.css").write_text(r'''
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --bg: #0f172a;
    --card: #1e293b;
    --nav: #111827;
    --text: #ffffff;
    --muted: #cbd5e1;
    --border: #334155;
    --primary: #2563eb;
    --accent: #60a5fa;
}

body.light {
    --bg: #f1f5f9;
    --card: #ffffff;
    --nav: #ffffff;
    --text: #0f172a;
    --muted: #475569;
    --border: #cbd5e1;
}

body {
    font-family: Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    transition: 0.3s;
}

a {
    color: var(--accent);
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 6%;
    background: var(--nav);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.logo {
    color: var(--text);
    text-decoration: none;
    font-size: 21px;
    font-weight: bold;
}

nav {
    display: flex;
    align-items: center;
    gap: 13px;
}

nav a {
    color: var(--muted);
    text-decoration: none;
    font-size: 14px;
}

nav a:hover {
    color: var(--accent);
}

.menu-btn {
    display: none;
    background: transparent;
    color: var(--text);
    border: 0;
    font-size: 26px;
}

.theme-btn {
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 8px;
    padding: 6px 10px;
    cursor: pointer;
}

.hero {
    min-height: 75vh;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 70px 20px;
    background:
        radial-gradient(circle at top, #1e3a8a, #0f172a 65%);
}

.hero-content {
    max-width: 800px;
}

.badge {
    display: inline-block;
    padding: 8px 15px;
    border-radius: 50px;
    background: #1e293b;
    color: #93c5fd;
}

.hero h1 {
    font-size: clamp(42px, 9vw, 75px);
    line-height: 1.1;
    margin: 20px 0;
}

.hero h1 span {
    color: var(--accent);
}

.hero p {
    color: #cbd5e1;
    font-size: 18px;
    max-width: 700px;
    margin: auto;
}

.buttons {
    margin-top: 30px;
}

.btn {
    display: inline-block;
    padding: 12px 20px;
    margin: 5px;
    border-radius: 10px;
    text-decoration: none;
    font-weight: bold;
}

.primary {
    background: var(--primary);
    color: white;
}

.secondary {
    background: #334155;
    color: white;
}

.section {
    max-width: 1100px;
    margin: auto;
    padding: 70px 20px;
}

.section > h2 {
    text-align: center;
    margin-bottom: 35px;
}

.cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.card {
    background: var(--card);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid var(--border);
    transition: 0.2s;
}

.card:hover {
    transform: translateY(-4px);
    border-color: var(--accent);
}

.icon {
    font-size: 38px;
    margin-bottom: 12px;
}

.card p {
    color: var(--muted);
}

.tag {
    display: inline-block;
    margin-top: 14px;
    padding: 4px 9px;
    background: #1d4ed8;
    color: white;
    border-radius: 20px;
    font-size: 12px;
}

.page-header {
    text-align: center;
    padding: 65px 20px;
    background: var(--nav);
}

.page-header h1 {
    font-size: 40px;
}

.page-header p {
    color: var(--muted);
}

.search-box {
    display: flex;
    max-width: 700px;
    margin: 0 auto 25px;
    gap: 10px;
}

input,
textarea,
select {
    width: 100%;
    padding: 14px;
    border: 1px solid var(--border);
    border-radius: 10px;
    background: var(--bg);
    color: var(--text);
    font-size: 16px;
}

button {
    padding: 13px 18px;
    border: none;
    border-radius: 10px;
    background: var(--primary);
    color: white;
    font-weight: bold;
    cursor: pointer;
}

.category-row {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
    margin-bottom: 30px;
}

.category-row a {
    text-decoration: none;
    padding: 8px 13px;
    border: 1px solid var(--border);
    border-radius: 20px;
}

.auth-box {
    max-width: 600px;
    margin: auto;
    background: var(--card);
    padding: 30px;
    border-radius: 18px;
    border: 1px solid var(--border);
}

.auth-box form {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-bottom: 15px;
}

.about-box {
    max-width: 800px;
    margin: auto;
    background: var(--card);
    padding: 35px;
    border-radius: 18px;
    border: 1px solid var(--border);
}

.about-box p {
    color: var(--muted);
    margin-top: 15px;
}

.notice {
    margin: 25px 0;
    padding: 18px;
    background: rgba(37,99,235,.15);
    border: 1px solid #2563eb;
    border-radius: 12px;
    color: var(--muted);
}

.rating {
    margin-top: 20px;
    font-weight: bold;
}

.rating-form {
    display: flex;
    gap: 10px;
    margin-top: 12px;
}

.cta {
    text-align: center;
    padding: 70px 20px;
    background: var(--card);
}

.cta p {
    color: var(--muted);
    margin: 12px 0 20px;
}

.flash-container {
    max-width: 900px;
    margin: 15px auto;
    padding: 0 20px;
}

.flash {
    padding: 13px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.flash.success {
    background: #14532d;
    color: #bbf7d0;
}

.flash.warning {
    background: #78350f;
    color: #fed7aa;
}

.flash.info {
    background: #1e3a8a;
    color: #bfdbfe;
}

.stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
}

.stats div {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 25px;
    text-align: center;
}

.stats strong {
    display: block;
    font-size: 30px;
}

.stats span {
    color: var(--muted);
}

.blog-card {
    margin-bottom: 18px;
}

.blog-card h2 {
    margin-bottom: 10px;
}

footer {
    text-align: center;
    padding: 35px 20px;
    background: #020617;
    color: #94a3b8;
}

footer p {
    margin-top: 7px;
}

@media (max-width: 800px) {

    .navbar {
        flex-wrap: wrap;
    }

    .menu-btn {
        display: block;
    }

    nav {
        display: none;
        width: 100%;
        flex-direction: column;
        padding-top: 15px;
    }

    nav.show {
        display: flex;
    }

    .cards {
        grid-template-columns: 1fr;
    }

    .stats {
        grid-template-columns: 1fr;
    }

    .search-box {
        flex-direction: column;
    }

    .hero {
        min-height: 65vh;
    }

    .hero h1 {
        font-size: 46px;
    }
}
'''.strip() + "\n", encoding="utf-8")


# JavaScript
Path("static/script.js").write_text(r'''
function toggleMenu() {
    const menu = document.getElementById("navMenu");

    if (menu) {
        menu.classList.toggle("show");
    }
}

function toggleTheme() {

    document.body.classList.toggle("light");

    if (document.body.classList.contains("light")) {
        localStorage.setItem("theme", "light");
    } else {
        localStorage.setItem("theme", "dark");
    }
}

window.addEventListener("DOMContentLoaded", function() {

    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "light") {
        document.body.classList.add("light");
    }

});
'''.strip() + "\n", encoding="utf-8")


# Git ignore
Path(".gitignore").write_text(r'''
__pycache__/
*.pyc
ai_zone.db
secret.key
.env
'''.strip() + "\n", encoding="utf-8")


print()
print("======================================")
print("🚀 AI Zone বাংলা v2 তৈরি হয়েছে!")
print("======================================")
print("✅ Secure user login/register")
print("✅ Server-side sessions")
print("✅ Admin password protection")
print("✅ SQLite database")
print("✅ AI Tools + search")
print("✅ Category filter")
print("✅ Favorites")
print("✅ Ratings")
print("✅ Blog system")
print("✅ Contact database")
print("✅ Affiliate click tracking")
print("✅ Analytics")
print("✅ Dark/Light mode")
print("✅ Mobile responsive")
print("✅ GitHub-safe .gitignore")
print()
print("Next:")
print("python app.py")
print("======================================")
