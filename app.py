
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
