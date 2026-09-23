from pathlib import Path

# -------------------------
# app.py
# -------------------------
Path("app.py").write_text(r'''
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DB = "ai_zone.db"

def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    con.commit()
    con.close()

init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/tools")
def tools():
    return render_template("tools.html")


@app.route("/tool/<name>")
def tool_details(name):
    tools = {
        "chatgpt": {
            "name": "ChatGPT",
            "icon": "🤖",
            "category": "AI Assistant",
            "description": "Writing, learning, brainstorming, coding এবং productivity-এর জন্য AI assistant."
        },
        "design": {
            "name": "AI Design Tools",
            "icon": "🎨",
            "category": "Design",
            "description": "Social media graphics এবং visual content তৈরির জন্য AI design workflow."
        },
        "video": {
            "name": "AI Video Tools",
            "icon": "🎬",
            "category": "Video",
            "description": "Short video, Reel এবং educational content তৈরির workflow."
        }
    }

    tool = tools.get(name.lower())

    if not tool:
        return "Tool not found", 404

    return render_template("tool.html", tool=tool, slug=name)


@app.route("/go/<name>")
def affiliate_redirect(name):

    # এখানে পরে নিজের approved affiliate link বসাবে
    affiliate_links = {
        "chatgpt": "#",
        "design": "#",
        "video": "#"
    }

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute(
        "INSERT INTO clicks (tool) VALUES (?)",
        (name,)
    )

    con.commit()
    con.close()

    link = affiliate_links.get(name, "#")

    if link == "#":
        return redirect(url_for("tools"))

    return redirect(link)


@app.route("/tutorials")
def tutorials():
    return render_template("tutorials.html")


@app.route("/social")
def social():
    return render_template("social.html")


@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route("/services")
def services():
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

        name = request.form.get("name")
        email = request.form.get("email")
        user_message = request.form.get("message")

        con = sqlite3.connect(DB)
        cur = con.cursor()

        cur.execute(
            "INSERT INTO messages (name,email,message) VALUES (?,?,?)",
            (name, email, user_message)
        )

        con.commit()
        con.close()

        message = "ধন্যবাদ! আপনার message সংরক্ষণ করা হয়েছে।"

    return render_template("contact.html", message=message)


@app.route("/admin")
def admin():

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
        SELECT tool, COUNT(*)
        FROM clicks
        GROUP BY tool
        ORDER BY COUNT(*) DESC
    """)

    clicks = cur.fetchall()

    cur.execute("""
        SELECT name,email,message,created_at
        FROM messages
        ORDER BY id DESC
    """)

    messages = cur.fetchall()

    con.close()

    return render_template(
        "admin.html",
        clicks=clicks,
        messages=messages
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
''', encoding="utf-8")


# -------------------------
# base.html
# -------------------------
Path("templates/base.html").write_text(r'''
<!DOCTYPE html>
<html lang="bn">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<meta name="description"
content="AI Zone বাংলা - AI Tools, Tutorials, Social Media এবং Digital Skills">

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
<a href="/tools">🤖 AI Tools</a>
<a href="/tutorials">📚 Tutorials</a>
<a href="/blog">📰 Blog</a>
<a href="/services">🛠️ Services</a>
<a href="/about">ℹ️ About</a>
<a href="/contact">📩 Contact</a>

<button class="theme-btn"
onclick="toggleTheme()">🌙</button>

</nav>

</header>

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
''', encoding="utf-8")


# -------------------------
# tools.html
# -------------------------
Path("templates/tools.html").write_text(r'''
{% extends "base.html" %}

{% block title %}AI Tools{% endblock %}

{% block content %}

<section class="page-header">

<h1>🤖 AI Tools</h1>

<p>
Useful AI tools এবং তাদের ব্যবহার সম্পর্কে জানুন
</p>

</section>

<section class="section">

<div class="search-box">

<input
id="toolSearch"
type="search"
placeholder="🔍 AI Tool খুঁজুন..."
onkeyup="searchCards('toolSearch','toolCard')">

</div>

<div class="cards">

<div class="card toolCard">

<div class="icon">🤖</div>

<h3>ChatGPT</h3>

<p>
Writing, learning, coding এবং brainstorming-এর জন্য AI assistant.
</p>

<span class="tag">AI Assistant</span>

<br>

<a class="btn primary"
href="/tool/chatgpt">
Details →
</a>

</div>


<div class="card toolCard">

<div class="icon">🎨</div>

<h3>AI Design Tools</h3>

<p>
Social media graphics ও visual content তৈরি করুন।
</p>

<span class="tag">Design</span>

<br>

<a class="btn primary"
href="/tool/design">
Details →
</a>

</div>


<div class="card toolCard">

<div class="icon">🎬</div>

<h3>AI Video Tools</h3>

<p>
Reels, Shorts এবং educational video তৈরির workflow.
</p>

<span class="tag">Video</span>

<br>

<a class="btn primary"
href="/tool/video">
Details →
</a>

</div>

</div>

</section>

{% endblock %}
''', encoding="utf-8")


# -------------------------
# tool.html
# -------------------------
Path("templates/tool.html").write_text(r'''
{% extends "base.html" %}

{% block title %}{{ tool.name }}{% endblock %}

{% block content %}

<section class="page-header">

<h1>
{{ tool.icon }} {{ tool.name }}
</h1>

<p>{{ tool.category }}</p>

</section>

<section class="section">

<div class="about-box">

<h2>{{ tool.icon }} {{ tool.name }}</h2>

<p>
{{ tool.description }}
</p>

<div class="notice">

💡 AI Zone বাংলা এই tool সম্পর্কে
শিক্ষামূলক তথ্য ও ব্যবহারবিধি প্রদান করছে।

</div>

<a class="btn primary"
href="/go/{{ slug }}">
Visit Tool →
</a>

</div>

</section>

{% endblock %}
''', encoding="utf-8")


# -------------------------
# blog.html
# -------------------------
Path("templates/blog.html").write_text(r'''
{% extends "base.html" %}

{% block title %}Blog{% endblock %}

{% block content %}

<section class="page-header">

<h1>📰 AI Zone বাংলা Blog</h1>

<p>AI ও Technology সম্পর্কে সহজ বাংলা লেখা</p>

</section>

<section class="section">

<div class="cards">

<div class="card">

<div class="icon">🤖</div>

<h3>ChatGPT কী?</h3>

<p>
ChatGPT কীভাবে শেখা ও productivity-তে ব্যবহার করা যায়
তা সহজভাবে জানুন।
</p>

</div>


<div class="card">

<div class="icon">🎨</div>

<h3>AI দিয়ে Design</h3>

<p>
Social media content-এর জন্য AI design workflow সম্পর্কে জানুন।
</p>

</div>


<div class="card">

<div class="icon">🎬</div>

<h3>AI দিয়ে Video</h3>

<p>
Short educational video তৈরির basic workflow শিখুন।
</p>

</div>

</div>

</section>

{% endblock %}
''', encoding="utf-8")


# -------------------------
# services.html
# -------------------------
Path("templates/services.html").write_text(r'''
{% extends "base.html" %}

{% block title %}Services{% endblock %}

{% block content %}

<section class="page-header">

<h1>🛠️ Our Services</h1>

<p>Digital এবং AI-based service ideas</p>

</section>

<section class="section">

<div class="cards">

<div class="card">

<div class="icon">🎨</div>

<h3>Social Media Design</h3>

<p>
Facebook এবং Instagram-এর জন্য visual content তৈরি।
</p>

</div>


<div class="card">

<div class="icon">✍️</div>

<h3>AI Content</h3>

<p>
Caption, script এবং educational content তৈরির service.
</p>

</div>


<div class="card">

<div class="icon">🌐</div>

<h3>Website Setup</h3>

<p>
ছোট personal বা learning website তৈরির basic service.
</p>

</div>

</div>

</section>

{% endblock %}
''', encoding="utf-8")


# -------------------------
# monetization.html
# -------------------------
Path("templates/monetization.html").write_text(r'''
{% extends "base.html" %}

{% block title %}Monetization{% endblock %}

{% block content %}

<section class="page-header">

<h1>💰 Monetization</h1>

<p>AI Zone বাংলা থেকে ভবিষ্যতে আয়ের সম্ভাব্য পথ</p>

</section>

<section class="section">

<div class="cards">

<div class="card">

<div class="icon">🔗</div>

<h3>Affiliate Marketing</h3>

<p>
Approved affiliate programs-এর মাধ্যমে
referral commission পাওয়ার সুযোগ।
</p>

</div>


<div class="card">

<div class="icon">📢</div>

<h3>Advertising</h3>

<p>
Website traffic তৈরি হলে advertising
options বিবেচনা করা যায়।
</p>

</div>


<div class="card">

<div class="icon">🤝</div>

<h3>Sponsored Content</h3>

<p>
Audience তৈরি হলে relevant brands-এর
সাথে paid collaboration করা যেতে পারে।
</p>

</div>


<div class="card">

<div class="icon">🛠️</div>

<h3>Digital Services</h3>

<p>
AI content, design বা website-related
service দেওয়া যেতে পারে।
</p>

</div>

</div>

<div class="notice">

⚠️ Income guaranteed নয়। Affiliate program-এর
নিজস্ব terms ও approval requirements থাকে।

</div>

</section>

{% endblock %}
''', encoding="utf-8")


# -------------------------
# admin.html
# -------------------------
Path("templates/admin.html").write_text(r'''
{% extends "base.html" %}

{% block title %}Dashboard{% endblock %}

{% block content %}

<section class="page-header">

<h1>📊 Admin Dashboard</h1>

<p>Website activity</p>

</section>

<section class="section">

<h2>🔗 Tool Clicks</h2>

<div class="cards">

{% for tool,count in clicks %}

<div class="card">

<h3>{{ tool }}</h3>

<p>
Clicks: <strong>{{ count }}</strong>
</p>

</div>

{% else %}

<p>এখনো কোনো click নেই।</p>

{% endfor %}

</div>


<h2 style="margin-top:50px;">
📩 Messages
</h2>

{% for name,email,message,date in messages %}

<div class="card" style="margin-top:15px;">

<h3>{{ name }}</h3>

<p>{{ email }}</p>

<p>{{ message }}</p>

<small>{{ date }}</small>

</div>

{% else %}

<p>কোনো message নেই।</p>

{% endfor %}

</section>

{% endblock %}
''', encoding="utf-8")


# -------------------------
# contact.html
# -------------------------
Path("templates/contact.html").write_text(r'''
{% extends "base.html" %}

{% block title %}Contact{% endblock %}

{% block content %}

<section class="page-header">

<h1>📩 Contact</h1>

<p>আপনার message পাঠান</p>

</section>

<section class="section">

<div class="contact-box">

{% if message %}

<div class="success">
{{ message }}
</div>

{% endif %}

<form method="POST">

<input
type="text"
name="name"
placeholder="আপনার নাম"
required
>

<input
type="email"
name="email"
placeholder="আপনার Email"
required
>

<textarea
name="message"
placeholder="আপনার Message"
rows="6"
required
></textarea>

<button type="submit">
Send Message 🚀
</button>

</form>

</div>

</section>

{% endblock %}
''', encoding="utf-8")


# -------------------------
# CSS additions
# -------------------------
css = Path("static/style.css")

if css.exists():
    old = css.read_text(encoding="utf-8")
else:
    old = ""

extra_css = r'''

.notice {
    margin: 25px 0;
    padding: 18px;
    background: rgba(37,99,235,0.15);
    border: 1px solid #2563eb;
    border-radius: 12px;
    color: var(--muted);
}

.about-box .btn {
    margin-top: 20px;
}

small {
    color: var(--muted);
}
'''

css.write_text(old + extra_css, encoding="utf-8")


print()
print("===================================")
print("🚀 AI Zone বাংলা Monetization Upgrade")
print("===================================")
print("✅ Affiliate-ready tools")
print("✅ Click tracking")
print("✅ Blog")
print("✅ Services")
print("✅ Monetization page")
print("✅ Contact database")
print("✅ Admin dashboard")
print("✅ SQLite database")
print()
print("Run: python app.py")
print("===================================")
