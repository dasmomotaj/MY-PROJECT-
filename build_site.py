from pathlib import Path

files = {
"app.py": r'''
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tools")
def tools():
    return render_template("tools.html")

@app.route("/tutorials")
def tutorials():
    return render_template("tutorials.html")

@app.route("/social")
def social():
    return render_template("social.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    message = None
    if request.method == "POST":
        name = request.form.get("name", "বন্ধু")
        message = f"ধন্যবাদ {name}! আপনার বার্তা গ্রহণ করা হয়েছে।"
    return render_template("contact.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
''',

"templates/base.html": r'''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="AI Zone বাংলা - AI, Web Development ও Social Media শেখার প্ল্যাটফর্ম">
    <title>{% block title %}AI Zone বাংলা{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>

<body>

<header class="navbar">
    <a class="logo" href="/">🤖 AI Zone বাংলা</a>

    <button class="menu-btn" onclick="toggleMenu()">☰</button>

    <nav id="navMenu">
        <a href="/">🏠 Home</a>
        <a href="/tools">🤖 AI Tools</a>
        <a href="/tutorials">📚 Tutorials</a>
        <a href="/social">📱 Social Media</a>
        <a href="/about">ℹ️ About</a>
        <a href="/contact">📩 Contact</a>
        <button class="theme-btn" onclick="toggleTheme()">🌙</button>
    </nav>
</header>

<main>
{% block content %}{% endblock %}
</main>

<footer>
    <h3>🤖 AI Zone বাংলা</h3>
    <p>AI • Technology • Web Development • Social Media</p>
    <p>© 2026 AI Zone বাংলা</p>
</footer>

<script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
''',

"templates/index.html": r'''
{% extends "base.html" %}

{% block title %}Home - AI Zone বাংলা{% endblock %}

{% block content %}

<section class="hero">
    <div class="hero-content">
        <span class="badge">🚀 Learn AI in Bangla</span>

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
            <a class="btn primary" href="/tools">🤖 AI Tools</a>
            <a class="btn secondary" href="/tutorials">📚 Tutorials</a>
        </div>
    </div>
</section>

<section class="section">
    <h2>আমরা কী শেখাই?</h2>

    <div class="cards">

        <div class="card">
            <div class="icon">🤖</div>
            <h3>AI Tools</h3>
            <p>AI tools কীভাবে ব্যবহার করতে হয় তা সহজভাবে শিখুন।</p>
        </div>

        <div class="card">
            <div class="icon">💻</div>
            <h3>Web Development</h3>
            <p>HTML, CSS, Python এবং Flask দিয়ে Web App তৈরি শিখুন।</p>
        </div>

        <div class="card">
            <div class="icon">📱</div>
            <h3>Social Media</h3>
            <p>Facebook, Instagram ও Short Video content সম্পর্কে জানুন।</p>
        </div>

        <div class="card">
            <div class="icon">💡</div>
            <h3>Digital Skills</h3>
            <p>নতুন digital skills শেখার সহজ resources খুঁজে নিন।</p>
        </div>

    </div>
</section>

<section class="cta">
    <h2>🚀 আজ থেকেই শেখা শুরু করুন</h2>
    <p>AI এবং Technology-কে সহজ বাংলায় বুঝুন।</p>
    <a class="btn primary" href="/tools">Explore AI Tools</a>
</section>

{% endblock %}
''',

"templates/tools.html": r'''
{% extends "base.html" %}

{% block title %}AI Tools - AI Zone বাংলা{% endblock %}

{% block content %}

<section class="page-header">
    <h1>🤖 AI Tools</h1>
    <p>আপনার কাজ সহজ করার জন্য AI tools</p>
</section>

<section class="section">

<div class="search-box">
    <input id="toolSearch"
           type="search"
           placeholder="🔍 AI Tool খুঁজুন..."
           onkeyup="searchCards('toolSearch','toolCard')">
</div>

<div class="cards">

<div class="card toolCard">
    <div class="icon">💬</div>
    <h3>ChatGPT</h3>
    <p>Writing, learning, brainstorming এবং coding-এর জন্য AI assistant.</p>
    <span class="tag">AI Assistant</span>
</div>

<div class="card toolCard">
    <div class="icon">🎨</div>
    <h3>Design AI</h3>
    <p>Social media graphics এবং visual content তৈরির workflow.</p>
    <span class="tag">Design</span>
</div>

<div class="card toolCard">
    <div class="icon">🎬</div>
    <h3>AI Video</h3>
    <p>Reels, Shorts এবং educational video তৈরির জন্য AI workflow.</p>
    <span class="tag">Video</span>
</div>

<div class="card toolCard">
    <div class="icon">✍️</div>
    <h3>AI Writing</h3>
    <p>Caption, script, article এবং content ideas তৈরি করুন।</p>
    <span class="tag">Writing</span>
</div>

<div class="card toolCard">
    <div class="icon">💻</div>
    <h3>AI Coding</h3>
    <p>Code শেখা, debugging এবং project planning-এ AI ব্যবহার করুন।</p>
    <span class="tag">Coding</span>
</div>

<div class="card toolCard">
    <div class="icon">🎙️</div>
    <h3>AI Voice</h3>
    <p>Educational এবং social media content-এর voice workflow শিখুন।</p>
    <span class="tag">Audio</span>
</div>

</div>
</section>

{% endblock %}
''',

"templates/tutorials.html": r'''
{% extends "base.html" %}

{% block title %}Tutorials - AI Zone বাংলা{% endblock %}

{% block content %}

<section class="page-header">
    <h1>📚 Tutorials</h1>
    <p>একদম শুরু থেকে শেখার সহজ tutorial</p>
</section>

<section class="section">

<div class="search-box">
    <input id="tutorialSearch"
           type="search"
           placeholder="🔍 Tutorial খুঁজুন..."
           onkeyup="searchCards('tutorialSearch','tutorialCard')">
</div>

<div class="cards">

<div class="card tutorialCard">
    <div class="icon">🐍</div>
    <h3>Python</h3>
    <p>Python basic থেকে ছোট project তৈরি করা শিখুন।</p>
</div>

<div class="card tutorialCard">
    <div class="icon">🌐</div>
    <h3>HTML & CSS</h3>
    <p>Website-এর structure এবং design তৈরি করতে শিখুন।</p>
</div>

<div class="card tutorialCard">
    <div class="icon">🔥</div>
    <h3>Flask</h3>
    <p>Python দিয়ে Web Application তৈরি করা শিখুন।</p>
</div>

<div class="card tutorialCard">
    <div class="icon">🐙</div>
    <h3>GitHub</h3>
    <p>Project save, version control এবং GitHub ব্যবহার শিখুন।</p>
</div>

<div class="card tutorialCard">
    <div class="icon">📱</div>
    <h3>Termux</h3>
    <p>Android ফোনে coding environment তৈরি করার basics শিখুন।</p>
</div>

<div class="card tutorialCard">
    <div class="icon">🤖</div>
    <h3>AI Learning</h3>
    <p>AI দিয়ে শেখা এবং productivity বাড়ানোর workflow শিখুন।</p>
</div>

</div>
</section>

{% endblock %}
''',

"templates/social.html": r'''
{% extends "base.html" %}

{% block title %}Social Media - AI Zone বাংলা{% endblock %}

{% block content %}

<section class="page-header">
    <h1>📱 Social Media</h1>
    <p>Digital content তৈরির সহজ ideas</p>
</section>

<section class="section">

<div class="cards">

<div class="card">
    <div class="icon">📘</div>
    <h3>Facebook</h3>
    <p>Educational post, Reel এবং AI-related content পরিকল্পনা করুন।</p>
</div>

<div class="card">
    <div class="icon">📸</div>
    <h3>Instagram</h3>
    <p>Reels, carousel এবং visual content-এর ideas তৈরি করুন।</p>
</div>

<div class="card">
    <div class="icon">🎵</div>
    <h3>Short Video</h3>
    <p>Short-form educational content-এর script ও storyboard তৈরি করুন।</p>
</div>

<div class="card">
    <div class="icon">📅</div>
    <h3>Content Calendar</h3>
    <p>নিয়মিত social media content পরিকল্পনা করার system তৈরি করুন।</p>
</div>

</div>
</section>

<section class="cta">
    <h2>💡 Content Idea</h2>
    <p>একটি AI tool নিয়ে ছোট tutorial Reel তৈরি করুন।</p>
</section>

{% endblock %}
''',

"templates/about.html": r'''
{% extends "base.html" %}

{% block title %}About - AI Zone বাংলা{% endblock %}

{% block content %}

<section class="page-header">
    <h1>ℹ️ AI Zone বাংলা</h1>
    <p>AI ও Technology শেখার একটি learning project</p>
</section>

<section class="section">

<div class="about-box">
    <h2>আমাদের লক্ষ্য</h2>

    <p>
        AI Zone বাংলা-এর লক্ষ্য হলো AI, Web Development
        এবং Digital Technology-এর বিষয়গুলো সহজ বাংলায়
        শেখার সুযোগ তৈরি করা।
    </p>

    <p>
        এই website Python, Flask, HTML, CSS এবং JavaScript
        ব্যবহার করে তৈরি করা হয়েছে।
    </p>

    <div class="stats">
        <div>
            <strong>🤖</strong>
            <span>AI</span>
        </div>

        <div>
            <strong>💻</strong>
            <span>Coding</span>
        </div>

        <div>
            <strong>📱</strong>
            <span>Social</span>
        </div>
    </div>
</div>

</section>

{% endblock %}
''',

"templates/contact.html": r'''
{% extends "base.html" %}

{% block title %}Contact - AI Zone বাংলা{% endblock %}

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
''',

"static/style.css": r'''
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
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
    gap: 14px;
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
    padding: 13px 22px;
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

.btn:hover {
    transform: translateY(-2px);
}

.section {
    max-width: 1100px;
    margin: auto;
    padding: 70px 20px;
}

.section > h2 {
    text-align: center;
    margin-bottom: 35px;
    font-size: 32px;
}

.cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.card {
    background: var(--card);
    padding: 28px 22px;
    border-radius: 18px;
    border: 1px solid var(--border);
    transition: 0.2s;
}

.card:hover {
    transform: translateY(-5px);
    border-color: var(--accent);
}

.icon {
    font-size: 38px;
    margin-bottom: 12px;
}

.card h3 {
    margin-bottom: 10px;
}

.card p {
    color: var(--muted);
}

.tag {
    display: inline-block;
    margin-top: 15px;
    padding: 5px 10px;
    border-radius: 20px;
    background: #1d4ed8;
    color: white;
    font-size: 12px;
}

.page-header {
    text-align: center;
    padding: 70px 20px;
    background: var(--nav);
}

.page-header h1 {
    font-size: 42px;
    margin-bottom: 10px;
}

.page-header p {
    color: var(--muted);
}

.search-box {
    max-width: 650px;
    margin: 0 auto 35px;
}

.search-box input {
    width: 100%;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid var(--border);
    background: var(--card);
    color: var(--text);
    font-size: 16px;
}

.about-box,
.contact-box {
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

.stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin-top: 30px;
}

.stats div {
    text-align: center;
    padding: 20px;
    background: var(--bg);
    border-radius: 12px;
}

.stats strong {
    display: block;
    font-size: 30px;
}

.stats span {
    color: var(--muted);
}

form {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

input,
textarea {
    width: 100%;
    padding: 14px;
    border: 1px solid var(--border);
    border-radius: 10px;
    background: var(--bg);
    color: var(--text);
    font-size: 16px;
}

textarea {
    resize: vertical;
}

button[type="submit"] {
    padding: 14px;
    border: none;
    border-radius: 10px;
    background: var(--primary);
    color: white;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
}

.success {
    background: #14532d;
    color: #bbf7d0;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
}

.cta {
    text-align: center;
    padding: 70px 20px;
    background: var(--card);
}

.cta p {
    color: var(--muted);
    margin: 10px 0 20px;
}

footer {
    text-align: center;
    padding: 35px 20px;
    background: #020617;
    color: #94a3b8;
}

footer p {
    margin-top: 5px;
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

    .hero {
        min-height: 65vh;
    }

    .page-header h1 {
        font-size: 34px;
    }
}
''',

"static/script.js": r'''
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

function searchCards(inputId, cardClass) {
    const input = document.getElementById(inputId);
    const cards = document.getElementsByClassName(cardClass);

    if (!input) return;

    const query = input.value.toLowerCase();

    for (let card of cards) {
        const text = card.innerText.toLowerCase();

        if (text.includes(query)) {
            card.style.display = "";
        } else {
            card.style.display = "none";
        }
    }
}

window.addEventListener("DOMContentLoaded", function() {
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "light") {
        document.body.classList.add("light");
    }
});
'''
}

for filename, content in files.items():
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

print("✅ AI Zone বাংলা complete website তৈরি হয়েছে!")
print("📁 Files:", len(files))
print("🚀 এখন চালান: python app.py")
