import os
import sqlite3
from datetime import datetime
import secrets
from pathlib import Path
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


# ==========================================
# APP
# ==========================================

app = Flask(__name__)

SECRET_FILE = Path("secret.key")

if SECRET_FILE.exists():
    SECRET_KEY = SECRET_FILE.read_text().strip()
else:
    SECRET_KEY = secrets.token_hex(32)
    SECRET_FILE.write_text(SECRET_KEY)

app.secret_key = SECRET_KEY

DB = "ai_zone.db"


# ==========================================
# DATABASE
# ==========================================

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


# ==========================================
# 50 AI TOOLS
# ==========================================

TOOLS = [

    # ======================================
    # AI ASSISTANT — 10
    # ======================================

    (
        "ChatGPT",
        "chatgpt",
        "AI Assistant",
        "🤖",
        "AI assistant for learning, writing, brainstorming, research and coding."
    ),

    (
        "Google Gemini",
        "google-gemini",
        "AI Assistant",
        "✨",
        "AI assistant for questions, writing, research and creative tasks."
    ),

    (
        "Microsoft Copilot",
        "microsoft-copilot",
        "AI Assistant",
        "🪟",
        "AI assistant for productivity, writing, research and everyday tasks."
    ),

    (
        "Claude",
        "claude",
        "AI Assistant",
        "🧠",
        "AI assistant for writing, analysis, learning and coding."
    ),

    (
        "Perplexity",
        "perplexity",
        "AI Assistant",
        "🔎",
        "AI-powered search and research assistant."
    ),

    (
        "DeepSeek",
        "deepseek",
        "AI Assistant",
        "🐋",
        "AI assistant for reasoning, coding and general tasks."
    ),

    (
        "Grok",
        "grok",
        "AI Assistant",
        "⚡",
        "AI assistant for conversation, information and creative tasks."
    ),

    (
        "Poe",
        "poe",
        "AI Assistant",
        "💬",
        "Platform for interacting with different AI assistants."
    ),

    (
        "Character AI",
        "character-ai",
        "AI Assistant",
        "🎭",
        "Conversational AI characters and creative conversations."
    ),

    (
        "Hugging Face",
        "hugging-face",
        "AI Assistant",
        "🤗",
        "Platform for AI models, datasets and machine learning tools."
    ),


    # ======================================
    # DESIGN — 8
    # ======================================

    (
        "Canva",
        "canva",
        "Design",
        "🎨",
        "Create social media graphics, presentations, posters and visual content."
    ),

    (
        "Adobe Express",
        "adobe-express",
        "Design",
        "🖌️",
        "Create graphics, social posts, videos and visual content."
    ),

    (
        "Figma",
        "figma",
        "Design",
        "🖼️",
        "Collaborative interface and graphic design platform."
    ),

    (
        "Pixlr",
        "pixlr",
        "Design",
        "📷",
        "Online photo editing and image design tool."
    ),

    (
        "Photopea",
        "photopea",
        "Design",
        "🖼️",
        "Browser-based image editor for creative projects."
    ),

    (
        "Remove.bg",
        "remove-bg",
        "Design",
        "✂️",
        "Remove image backgrounds automatically."
    ),

    (
        "Leonardo AI",
        "leonardo-ai",
        "Design",
        "🧑‍🎨",
        "AI-powered image generation and creative design platform."
    ),

    (
        "Ideogram",
        "ideogram",
        "Design",
        "💡",
        "AI image generation tool for creative visual content."
    ),


    # ======================================
    # VIDEO — 8
    # ======================================

    (
        "CapCut",
        "capcut",
        "Video",
        "🎬",
        "Video editing tool for Reels, Shorts and social media content."
    ),

    (
        "VEED",
        "veed",
        "Video",
        "🎥",
        "Online video editor for social media and content creation."
    ),

    (
        "InVideo",
        "invideo",
        "Video",
        "🎞️",
        "AI-assisted video creation and editing platform."
    ),

    (
        "Pictory",
        "pictory",
        "Video",
        "📹",
        "Create videos from scripts, articles and other content."
    ),

    (
        "Descript",
        "descript",
        "Video",
        "🎙️",
        "Edit video and audio using text-based editing tools."
    ),

    (
        "Runway",
        "runway",
        "Video",
        "🚀",
        "AI-powered creative tools for video generation and editing."
    ),

    (
        "Lumen5",
        "lumen5",
        "Video",
        "💡",
        "Create social videos from text and other content."
    ),

    (
        "Synthesia",
        "synthesia",
        "Video",
        "🧑‍💻",
        "AI video creation platform with virtual presenters."
    ),


    # ======================================
    # WRITING — 6
    # ======================================

    (
        "Grammarly",
        "grammarly",
        "Writing",
        "✍️",
        "Writing assistant for grammar, spelling, clarity and style."
    ),

    (
        "QuillBot",
        "quillbot",
        "Writing",
        "📝",
        "Writing and text editing assistant."
    ),

    (
        "Jasper",
        "jasper",
        "Writing",
        "📝",
        "AI-powered content creation and writing platform."
    ),

    (
        "Writesonic",
        "writesonic",
        "Writing",
        "✏️",
        "AI tools for writing, content creation and marketing."
    ),

    (
        "Rytr",
        "rytr",
        "Writing",
        "🖊️",
        "AI writing assistant for creating different types of content."
    ),

    (
        "Wordtune",
        "wordtune",
        "Writing",
        "🔤",
        "Writing and rewriting assistant for clearer communication."
    ),


    # ======================================
    # CODING — 8
    # ======================================

    (
        "GitHub",
        "github",
        "Coding",
        "💻",
        "Code hosting, collaboration and software development platform."
    ),

    (
        "GitHub Copilot",
        "github-copilot",
        "Coding",
        "🤖",
        "AI coding assistant for developers."
    ),

    (
        "CodePen",
        "codepen",
        "Coding",
        "👨‍💻",
        "Online editor for HTML, CSS and JavaScript projects."
    ),

    (
        "Replit",
        "replit",
        "Coding",
        "🧑‍💻",
        "Online development environment for building and running projects."
    ),

    (
        "Cursor",
        "cursor",
        "Coding",
        "⌨️",
        "AI-assisted code editor for software development."
    ),

    (
        "Stack Overflow",
        "stack-overflow",
        "Coding",
        "📚",
        "Developer community for programming questions and answers."
    ),

    (
        "JSFiddle",
        "jsfiddle",
        "Coding",
        "🧪",
        "Online playground for HTML, CSS and JavaScript."
    ),

    (
        "W3Schools",
        "w3schools",
        "Coding",
        "🌐",
        "Learning resources and practice for web development."
    ),


    # ======================================
    # SOCIAL MEDIA — 5
    # ======================================

    (
        "Buffer",
        "buffer",
        "Social Media",
        "📅",
        "Social media publishing and content management tool."
    ),

    (
        "Hootsuite",
        "hootsuite",
        "Social Media",
        "📣",
        "Social media management and publishing platform."
    ),

    (
        "Later",
        "later",
        "Social Media",
        "📱",
        "Social media scheduling and content planning platform."
    ),

    (
        "Metricool",
        "metricool",
        "Social Media",
        "📊",
        "Social media analytics, planning and management platform."
    ),

    (
        "Publer",
        "publer",
        "Social Media",
        "🚀",
        "Social media scheduling and content management tool."
    ),


    # ======================================
    # PRODUCTIVITY — 5
    # ======================================

    (
        "Notion",
        "notion",
        "Productivity",
        "📒",
        "Workspace for notes, planning, documentation and productivity."
    ),

    (
        "Trello",
        "trello",
        "Productivity",
        "📋",
        "Visual project management and task organization tool."
    ),

    (
        "ClickUp",
        "clickup",
        "Productivity",
        "✅",
        "Project management and productivity platform."
    ),

    (
        "Evernote",
        "evernote",
        "Productivity",
        "🗒️",
        "Note-taking and organization platform."
    ),

    (
        "Google Keep",
        "google-keep",
        "Productivity",
        "📌",
        "Simple note-taking, lists and reminders tool."
    )
]


# ==========================================
# DATABASE INITIALIZATION
# ==========================================

def init_db():

    con = db()
    cur = con.cursor()

    # USERS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # TOOLS
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

    # FAVORITES
    cur.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tool_id INTEGER NOT NULL,
            UNIQUE(user_id, tool_id)
        )
    """)

    # RATINGS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tool_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            UNIQUE(user_id, tool_id)
        )
    """)

    # MESSAGES
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # BLOG
    cur.execute("""
        CREATE TABLE IF NOT EXISTS blog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # VISITS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # --------------------------------------
    # Remove old placeholder tools
    # --------------------------------------

    old_slugs = (
        "design",
        "video",
        "writing",
        "coding"
    )

    placeholders = cur.execute(
        """
        SELECT id
        FROM tools
        WHERE slug IN (?, ?, ?, ?)
        """,
        old_slugs
    ).fetchall()

    for row in placeholders:
        cur.execute(
            "DELETE FROM favorites WHERE tool_id = ?",
            (row["id"],)
        )

        cur.execute(
            "DELETE FROM ratings WHERE tool_id = ?",
            (row["id"],)
        )

    cur.execute(
        """
        DELETE FROM tools
        WHERE slug IN (?, ?, ?, ?)
        """,
        old_slugs
    )

    # --------------------------------------
    # Insert 50 tools
    # --------------------------------------

    for tool in TOOLS:

        cur.execute(
            """
            INSERT OR IGNORE INTO tools
            (name, slug, category, icon, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            tool
        )

    con.commit()
    con.close()


# Initialize database when app starts
init_db()


# ==========================================
# LOGIN REQUIRED
# ==========================================

def login_required(view):

    @wraps(view)
    def wrapped(*args, **kwargs):

        if "user_id" not in session:

            flash(
                "এই page ব্যবহার করতে Login করুন।",
                "warning"
            )

            return redirect(url_for("login"))

        return view(*args, **kwargs)

    return wrapped


# ==========================================
# ADMIN REQUIRED
# ==========================================

def admin_required(view):

    @wraps(view)
    def wrapped(*args, **kwargs):

        if not session.get("admin"):

            flash(
                "Admin access required.",
                "warning"
            )

            return redirect(url_for("admin_login"))

        return view(*args, **kwargs)

    return wrapped


# ==========================================
# ANALYTICS
# ==========================================

def track(page):

    con = db()

    con.execute(
        "INSERT INTO visits (page) VALUES (?)",
        (page,)
    )

    con.commit()
    con.close()


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    track("/")

    return render_template("index.html")


# ==========================================
# TOOLS
# ==========================================

@app.route("/tools")
def tools():

    track("/tools")

    category = request.args.get(
        "category",
        ""
    ).strip()

    search = request.args.get(
        "q",
        ""
    ).strip()

    con = db()

    if search:

        rows = con.execute(
            """
            SELECT *
            FROM tools
            WHERE name LIKE ?
               OR category LIKE ?
               OR description LIKE ?
            ORDER BY name
            """,
            (
                f"%{search}%",
                f"%{search}%",
                f"%{search}%"
            )
        ).fetchall()

    elif category:

        rows = con.execute(
            """
            SELECT *
            FROM tools
            WHERE category = ?
            ORDER BY name
            """,
            (category,)
        ).fetchall()

    else:

        rows = con.execute(
            """
            SELECT *
            FROM tools
            ORDER BY name
            """
        ).fetchall()

    categories = con.execute(
        """
        SELECT DISTINCT category
        FROM tools
        ORDER BY category
        """
    ).fetchall()

    con.close()

    return render_template(
        "tools.html",
        tools=rows,
        categories=categories,
        search=search,
        selected_category=category
    )


# ==========================================
# TOOL DETAILS
# ==========================================

@app.route("/tool/<slug>")
def tool_details(slug):

    con = db()

    tool = con.execute(
        """
        SELECT *
        FROM tools
        WHERE slug = ?
        """,
        (slug,)
    ).fetchone()

    if not tool:

        con.close()

        return "Tool not found", 404

    rating = con.execute(
        """
        SELECT
            AVG(rating) AS average,
            COUNT(*) AS total
        FROM ratings
        WHERE tool_id = ?
        """,
        (tool["id"],)
    ).fetchone()

    favorite = False

    if "user_id" in session:

        favorite = con.execute(
            """
            SELECT id
            FROM favorites
            WHERE user_id = ?
              AND tool_id = ?
            """,
            (
                session["user_id"],
                tool["id"]
            )
        ).fetchone() is not None

    con.close()

    return render_template(
        "tool.html",
        tool=tool,
        rating=rating,
        favorite=favorite
    )


# ==========================================
# TOOL / AFFILIATE REDIRECT
# ==========================================

@app.route("/go/<slug>")
def affiliate_redirect(slug):

    con = db()

    tool = con.execute(
        """
        SELECT *
        FROM tools
        WHERE slug = ?
        """,
        (slug,)
    ).fetchone()

    if not tool:

        con.close()

        return redirect(url_for("tools"))

    con.execute(
        """
        UPDATE tools
        SET clicks = clicks + 1
        WHERE id = ?
        """,
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

        return redirect(
            url_for(
                "tool_details",
                slug=slug
            )
        )

    return redirect(link)


# ==========================================
# FAVORITE
# ==========================================

@app.route(
    "/favorite/<int:tool_id>",
    methods=["POST"]
)
@login_required
def favorite(tool_id):

    con = db()

    exists = con.execute(
        """
        SELECT id
        FROM favorites
        WHERE user_id = ?
          AND tool_id = ?
        """,
        (
            session["user_id"],
            tool_id
        )
    ).fetchone()

    if exists:

        con.execute(
            """
            DELETE FROM favorites
            WHERE id = ?
            """,
            (exists["id"],)
        )

    else:

        con.execute(
            """
            INSERT OR IGNORE INTO favorites
            (user_id, tool_id)
            VALUES (?, ?)
            """,
            (
                session["user_id"],
                tool_id
            )
        )

    con.commit()
    con.close()

    return redirect(
        request.referrer or url_for("tools")
    )


# ==========================================
# RATING
# ==========================================

@app.route(
    "/rate/<int:tool_id>",
    methods=["POST"]
)
@login_required
def rate(tool_id):

    try:

        rating = int(
            request.form.get(
                "rating",
                0
            )
        )

    except (ValueError, TypeError):

        rating = 0

    if rating not in range(1, 6):

        flash(
            "Rating 1 থেকে 5-এর মধ্যে দিন।",
            "warning"
        )

        return redirect(
            request.referrer or url_for("tools")
        )

    con = db()

    con.execute(
        """
        INSERT INTO ratings
        (user_id, tool_id, rating)
        VALUES (?, ?, ?)

        ON CONFLICT(user_id, tool_id)
        DO UPDATE SET rating = excluded.rating
        """,
        (
            session["user_id"],
            tool_id,
            rating
        )
    )

    con.commit()
    con.close()

    flash(
        "আপনার rating save হয়েছে ⭐",
        "success"
    )

    return redirect(
        request.referrer or url_for("tools")
    )


# ==========================================
# REGISTER
# ==========================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        if len(username) < 3 or len(password) < 6:

            flash(
                "Username কমপক্ষে 3 এবং password কমপক্ষে 6 characters হতে হবে।",
                "warning"
            )

            return render_template(
                "register.html"
            )

        if not email:

            flash(
                "Email দিন।",
                "warning"
            )

            return render_template(
                "register.html"
            )

        con = db()

        try:

            con.execute(
                """
                INSERT INTO users
                (username, email, password)
                VALUES (?, ?, ?)
                """,
                (
                    username,
                    email,
                    generate_password_hash(password)
                )
            )

            con.commit()

        except sqlite3.IntegrityError:

            con.close()

            flash(
                "Username বা Email আগে থেকেই ব্যবহার হয়েছে।",
                "warning"
            )

            return render_template(
                "register.html"
            )

        con.close()

        flash(
            "Registration সফল হয়েছে। এখন Login করুন।",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


# ==========================================
# LOGIN
# ==========================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        con = db()

        user = con.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        con.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session.clear()

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(
                url_for("home")
            )

        flash(
            "Email অথবা password সঠিক নয়।",
            "warning"
        )

    return render_template(
        "login.html"
    )


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# ==========================================
# PROFILE
# ==========================================

@app.route("/profile")
@login_required
def profile():

    con = db()

    favorites = con.execute(
        """
        SELECT tools.*
        FROM favorites
        JOIN tools
          ON tools.id = favorites.tool_id
        WHERE favorites.user_id = ?
        ORDER BY tools.name
        """,
        (session["user_id"],)
    ).fetchall()

    con.close()

    return render_template(
        "profile.html",
        favorites=favorites
    )


# ==========================================
# TUTORIALS
# ==========================================

@app.route("/tutorials")
def tutorials():

    track("/tutorials")

    return render_template(
        "tutorials.html"
    )


# ==========================================
# SOCIAL
# ==========================================

@app.route("/social")
def social():

    track("/social")

    return render_template(
        "social.html"
    )


# ==========================================
# BLOG
# ==========================================

@app.route("/blog")
def blog():

    track("/blog")

    con = db()

    posts = con.execute(
        """
        SELECT *
        FROM blog
        ORDER BY id DESC
        """
    ).fetchall()

    con.close()

    return render_template(
        "blog.html",
        posts=posts
    )


# ==========================================
# SERVICES
# ==========================================

@app.route("/services")
def services():

    track("/services")

    return render_template(
        "services.html"
    )


# ==========================================
# MONETIZATION
# ==========================================

@app.route("/monetization")
def monetization():

    track("/monetization")

    return render_template(
        "monetization.html"
    )


# ==========================================
# ABOUT
# ==========================================

@app.route("/about")
def about():

    track("/about")

    return render_template(
        "about.html"
    )


# ==========================================
# CONTACT
# ==========================================

@app.route(
    "/contact",
    methods=["GET", "POST"]
)
def contact():

    message = None

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        user_message = request.form.get(
            "message",
            ""
        ).strip()

        if name and email and user_message:

            con = db()

            con.execute(
                """
                INSERT INTO messages
                (name, email, message)
                VALUES (?, ?, ?)
                """,
                (
                    name,
                    email,
                    user_message
                )
            )

            con.commit()
            con.close()

            message = (
                "ধন্যবাদ! আপনার message গ্রহণ করা হয়েছে।"
            )

        else:

            message = (
                "সবগুলো field পূরণ করুন।"
            )

    return render_template(
        "contact.html",
        message=message
    )


# ==========================================
# ADMIN LOGIN
# ==========================================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def admin_login():

    if request.method == "POST":

        password = request.form.get(
            "password",
            ""
        )

        admin_password = os.environ.get(
            "AI_ZONE_ADMIN_PASSWORD"
        )

        if not admin_password:

            flash(
                "AI_ZONE_ADMIN_PASSWORD সেট করা হয়নি।",
                "warning"
            )

            return render_template(
                "admin_login.html"
            )

        if secrets.compare_digest(
            password,
            admin_password
        ):

            session.clear()

            session["admin"] = True

            return redirect(
                url_for("admin_dashboard")
            )

        flash(
            "Admin password সঠিক নয়।",
            "warning"
        )

    return render_template(
        "admin_login.html"
    )


# ==========================================
# ADMIN LOGOUT
# ==========================================

@app.route("/admin/logout")
def admin_logout():

    session.pop(
        "admin",
        None
    )

    return redirect(
        url_for("home")
    )


# ==========================================
# ADMIN DASHBOARD
# ==========================================

@app.route("/admin")
@admin_required
def admin_dashboard():

    con = db()

    users = con.execute(
        """
        SELECT COUNT(*) AS total
        FROM users
        """
    ).fetchone()["total"]

    visits = con.execute(
        """
        SELECT COUNT(*) AS total
        FROM visits
        """
    ).fetchone()["total"]

    messages = con.execute(
        """
        SELECT COUNT(*) AS total
        FROM messages
        """
    ).fetchone()["total"]

    tool_count = con.execute(
        """
        SELECT COUNT(*) AS total
        FROM tools
        """
    ).fetchone()["total"]

    clicks = con.execute(
        """
        SELECT name, clicks
        FROM tools
        ORDER BY clicks DESC
        """
    ).fetchall()

    recent_messages = con.execute(
        """
        SELECT *
        FROM messages
        ORDER BY id DESC
        LIMIT 10
        """
    ).fetchall()

    con.close()

    return render_template(
        "admin.html",
        users=users,
        visits=visits,
        messages=messages,
        tool_count=tool_count,
        clicks=clicks,
        recent_messages=recent_messages
    )


# ==========================================
# ADMIN TOOLS
# ==========================================

@app.route("/admin/tools")
@admin_required
def admin_tools():

    con = db()

    tools = con.execute(
        """
        SELECT *
        FROM tools
        ORDER BY name
        """
    ).fetchall()

    con.close()

    return render_template(
        "admin_tools.html",
        tools=tools
    )


# ==========================================
# ADMIN DELETE TOOL
@app.route("/admin/tools/delete/<int:tool_id>", methods=["POST"])
@admin_required
def admin_delete_tool(tool_id):

    con = db()

    tool = con.execute(
        "SELECT name FROM tools WHERE id=?",
        (tool_id,)
    ).fetchone()

    if not tool:
        con.close()
        flash("Tool পাওয়া যায়নি।", "warning")
        return redirect(url_for("admin_tools"))

    backup_file = "ai_zone_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".db"
    backup_con = sqlite3.connect(backup_file)
    con.backup(backup_con)
    backup_con.close()

    con.execute(
        "DELETE FROM tools WHERE id=?",
        (tool_id,)
    )

    con.commit()
    con.close()

    flash(f"🗑️ {tool['name']} মুছে ফেলা হয়েছে।", "success")

    return redirect(url_for("admin_tools"))


# ADMIN EDIT TOOL
@app.route("/admin/tools/edit/<int:tool_id>", methods=["GET", "POST"])
@admin_required
def admin_edit_tool(tool_id):

    con = db()

    tool = con.execute(
        "SELECT * FROM tools WHERE id=?",
        (tool_id,)
    ).fetchone()

    if not tool:
        con.close()
        flash("Tool পাওয়া যায়নি।", "warning")
        return redirect(url_for("admin_tools"))

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        slug = request.form.get("slug", "").strip().lower()
        category = request.form.get("category", "").strip()
        icon = request.form.get("icon", "🤖").strip()
        description = request.form.get("description", "").strip()
        affiliate_url = request.form.get("affiliate_url", "").strip()

        if not name or not slug or not category or not description:
            con.close()
            flash("Name, Slug, Category এবং Description পূরণ করুন।", "warning")
            return redirect(url_for("admin_edit_tool", tool_id=tool_id))

        if not affiliate_url:
            affiliate_url = "#"

        try:
            con.execute(
                """
                UPDATE tools
                SET name=?,
                    slug=?,
                    category=?,
                    icon=?,
                    description=?,
                    affiliate_url=?
                WHERE id=?
                """,
                (
                    name,
                    slug,
                    category,
                    icon,
                    description,
                    affiliate_url,
                    tool_id
                )
            )

            con.commit()
            flash("✅ Tool সফলভাবে আপডেট হয়েছে।", "success")

        except sqlite3.IntegrityError:
            flash("❌ এই Name বা Slug অন্য Tool-এ আগে থেকেই আছে।", "warning")

        finally:
            con.close()

        return redirect(url_for("admin_tools"))

    con.close()

    return render_template(
        "admin_edit_tool.html",
        tool=tool
    )


# ADMIN ADD TOOL
@app.route("/admin/tools/add", methods=["GET", "POST"])
@admin_required
def admin_add_tool():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        slug = request.form.get("slug", "").strip().lower()
        category = request.form.get("category", "").strip()
        icon = request.form.get("icon", "🤖").strip()
        description = request.form.get("description", "").strip()
        affiliate_url = request.form.get("affiliate_url", "").strip()

        if not name or not slug or not category or not description:
            flash("Name, Slug, Category এবং Description পূরণ করুন।", "warning")
            return redirect(url_for("admin_add_tool"))

        if not affiliate_url:
            affiliate_url = "#"

        con = db()

        try:
            con.execute(
                """
                INSERT INTO tools
                (name, slug, category, icon, description, affiliate_url)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (name, slug, category, icon, description, affiliate_url)
            )
            con.commit()
            flash("✅ নতুন Tool সফলভাবে যোগ হয়েছে।", "success")

        except sqlite3.IntegrityError:
            flash("❌ এই Name বা Slug আগে থেকেই আছে।", "warning")

        finally:
            con.close()

        return redirect(url_for("admin_tools"))

    return render_template("admin_add_tool.html")


# ADMIN BLOG
# ==========================================

@app.route(
    "/admin/blog",
    methods=["POST"]
)
@admin_required
def admin_blog():

    title = request.form.get(
        "title",
        ""
    ).strip()

    content = request.form.get(
        "content",
        ""
    ).strip()

    if title and content:

        con = db()

        con.execute(
            """
            INSERT INTO blog
            (title, content)
            VALUES (?, ?)
            """,
            (
                title,
                content
            )
        )

        con.commit()
        con.close()

        flash(
            "Blog post তৈরি হয়েছে।",
            "success"
        )

    return redirect(
        url_for("admin_dashboard")
    )


# ==========================================
# ROBOTS.TXT
# ==========================================

@app.route("/robots.txt")
def robots():

    return (
        "User-agent: *\n"
        "Allow: /\n\n"
        "Sitemap: /sitemap.xml\n"
    ), 200, {
        "Content-Type": "text/plain"
    }


# ==========================================
# SITEMAP
# ==========================================

@app.route("/sitemap.xml")
def sitemap():

    pages = [
        "/",
        "/tools",
        "/tutorials",
        "/social",
        "/blog",
        "/services",
        "/monetization",
        "/about",
        "/contact"
    ]

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    for page in pages:

        xml.append(
            f"<url><loc>{page}</loc></url>"
        )

    xml.append("</urlset>")

    return "\n".join(xml), 200, {
        "Content-Type": "application/xml"
    }


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    # Automatically add/update AI tools
    try:
        import add_tools
        add_tools.main()
    except Exception as e:
        print("Tool loader warning:", e)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
