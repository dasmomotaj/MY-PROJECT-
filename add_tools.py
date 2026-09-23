import sqlite3

DB = "ai_zone.db"

tools = [
    (
        "ChatGPT",
        "chatgpt",
        "AI Assistant",
        "🤖",
        "AI assistant for writing, learning, brainstorming, coding and everyday tasks."
    ),
    (
        "Canva",
        "canva",
        "Design",
        "🎨",
        "Create social media graphics, presentations, posters and other visual content."
    ),
    (
        "CapCut",
        "capcut",
        "Video",
        "🎬",
        "Create and edit short-form videos with templates and AI-powered features."
    ),
    (
        "Grammarly",
        "grammarly",
        "Writing",
        "✍️",
        "Writing assistant for grammar, clarity and style."
    ),
    (
        "GitHub",
        "github",
        "Coding",
        "💻",
        "Platform for hosting, collaborating on and managing software projects."
    ),
    (
        "Notion",
        "notion",
        "Productivity",
        "📒",
        "Workspace for notes, documents, planning and organizing projects."
    ),
    (
        "Adobe Express",
        "adobe-express",
        "Design",
        "🖌️",
        "Create social posts, graphics, videos and other visual content."
    ),
    (
        "VEED",
        "veed",
        "Video",
        "🎥",
        "Online video editor with tools for creating and editing social content."
    ),
    (
        "QuillBot",
        "quillbot",
        "Writing",
        "📝",
        "Writing and paraphrasing tools for improving and rewriting text."
    ),
    (
        "CodePen",
        "codepen",
        "Coding",
        "👨‍💻",
        "Online environment for experimenting with HTML, CSS and JavaScript."
    ),
]

conn = sqlite3.connect(DB)
cur = conn.cursor()

for name, slug, category, icon, description in tools:

    existing = cur.execute(
        "SELECT id FROM tools WHERE slug = ?",
        (slug,)
    ).fetchone()

    if existing:
        print(f"⏭️ Already exists: {name}")
    else:
        cur.execute(
            """
            INSERT INTO tools
            (name, slug, category, icon, description, affiliate_url, clicks)
            VALUES (?, ?, ?, ?, ?, '#', 0)
            """,
            (
                name,
                slug,
                category,
                icon,
                description
            )
        )

        print(f"✅ Added: {name}")

conn.commit()

count = cur.execute(
    "SELECT COUNT(*) FROM tools"
).fetchone()[0]

conn.close()

print()
print(f"🎉 Total tools in database: {count}")
import sqlite3

DB_NAME = "ai_zone.db"

tools = [
    (
        "ChatGPT",
        "chatgpt",
        "AI Assistant",
        "🤖",
        "Writing, learning, brainstorming এবং coding-এর জন্য AI assistant."
    ),
    (
        "Canva",
        "canva",
        "Design",
        "🎨",
        "Social media graphics, presentations এবং visual content তৈরির জন্য."
    ),
    (
        "CapCut",
        "capcut",
        "Video",
        "🎬",
        "Reels, Shorts এবং educational video editing-এর জন্য."
    ),
    (
        "Grammarly",
        "grammarly",
        "Writing",
        "✍️",
        "Grammar, spelling এবং writing উন্নত করার জন্য."
    ),
    (
        "GitHub",
        "github",
        "Coding",
        "💻",
        "Code hosting এবং web development project-এর জন্য."
    ),
    (
        "Notion",
        "notion",
        "Productivity",
        "📒",
        "Notes, planning এবং productivity management-এর জন্য."
    ),
    (
        "Adobe Express",
        "adobe-express",
        "Design",
        "🖌️",
        "Graphics এবং social media content তৈরির জন্য."
    ),
    (
        "VEED",
        "veed",
        "Video",
        "🎥",
        "Online video editing এবং content creation-এর জন্য."
    ),
    (
        "QuillBot",
        "quillbot",
        "Writing",
        "📝",
        "Writing এবং text editing-এর জন্য."
    ),
    (
        "CodePen",
        "codepen",
        "Coding",
        "👨‍💻",
        "HTML, CSS এবং JavaScript practice করার জন্য."
    )
]

con = sqlite3.connect(DB_NAME)
cur = con.cursor()

for tool in tools:
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

print("✅ 10 AI Tools successfully added!")
