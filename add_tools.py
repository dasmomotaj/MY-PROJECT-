import sqlite3

DB = "ai_zone.db"

def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    # Tools table না থাকলে তৈরি করবে
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

    # Existing ChatGPT row update
    cur.execute("""
        UPDATE tools
        SET name=?, slug=?, category=?, icon=?, description=?, affiliate_url=?
        WHERE slug=?
    """, (
        "ChatGPT",
        "chatgpt",
        "AI Assistant",
        "🤖",
        "Writing, learning, brainstorming এবং coding-এর জন্য AI assistant.",
        "https://chatgpt.com/",
        "chatgpt"
    ))

    # Existing placeholder rowsকে real tools করা
    replacements = [
        (
            "design",
            "Canva",
            "canva",
            "Design",
            "🎨",
            "Social media design, poster, presentation এবং visual content তৈরির tool.",
            "https://www.canva.com/"
        ),
        (
            "video",
            "CapCut",
            "capcut",
            "Video",
            "🎬",
            "Short video, Reels, Shorts এবং social media video editing-এর tool.",
            "https://www.capcut.com/"
        ),
        (
            "writing",
            "Grammarly",
            "grammarly",
            "Writing",
            "✍️",
            "Writing, grammar এবং English content improve করার tool.",
            "https://www.grammarly.com/"
        ),
        (
            "coding",
            "GitHub",
            "github",
            "Coding",
            "💻",
            "Code hosting, Git এবং software development-এর platform.",
            "https://github.com/"
        )
    ]

    for old_slug, name, slug, category, icon, description, url in replacements:
        cur.execute("""
            UPDATE tools
            SET name=?, slug=?, category=?, icon=?, description=?, affiliate_url=?
            WHERE slug=?
        """, (
            name,
            slug,
            category,
            icon,
            description,
            url,
            old_slug
        ))

    # আরও 45টি tool
    tools = [
        (
            "Notion",
            "notion",
            "Productivity",
            "📝",
            "Notes, database, planning এবং productivity-এর জন্য জনপ্রিয় workspace.",
            "https://www.notion.so/"
        ),
        (
            "Adobe Express",
            "adobe-express",
            "Design",
            "✨",
            "Social posts, graphics এবং দ্রুত visual content তৈরির tool.",
            "https://www.adobe.com/express/"
        ),
        (
            "VEED",
            "veed",
            "Video",
            "🎥",
            "Online video editing, subtitles এবং social media video তৈরির tool.",
            "https://www.veed.io/"
        ),
        (
            "QuillBot",
            "quillbot",
            "Writing",
            "🖊️",
            "Paraphrasing, grammar এবং writing improvement-এর tool.",
            "https://quillbot.com/"
        ),
        (
            "CodePen",
            "codepen",
            "Coding",
            "🧑‍💻",
            "HTML, CSS এবং JavaScript practice ও sharing-এর platform.",
            "https://codepen.io/"
        ),
        (
            "Claude",
            "claude",
            "AI Assistant",
            "🧠",
            "Writing, analysis, learning এবং coding-এর AI assistant.",
            "https://claude.ai/"
        ),
        (
            "Google Gemini",
            "gemini",
            "AI Assistant",
            "✨",
            "Google-এর AI assistant; writing, research এবং brainstorming-এর জন্য.",
            "https://gemini.google.com/"
        ),
        (
            "Microsoft Copilot",
            "copilot",
            "AI Assistant",
            "🤖",
            "AI assistant এবং productivity কাজের জন্য Microsoft-এর tool.",
            "https://copilot.microsoft.com/"
        ),
        (
            "Perplexity",
            "perplexity",
            "Research",
            "🔎",
            "AI-powered search এবং research-এর জন্য tool.",
            "https://www.perplexity.ai/"
        ),
        (
            "DeepSeek",
            "deepseek",
            "AI Assistant",
            "🐋",
            "AI chat, reasoning এবং coding-এর জন্য AI platform.",
            "https://www.deepseek.com/"
        ),
        (
            "Grok",
            "grok",
            "AI Assistant",
            "⚡",
            "AI chat, প্রশ্নোত্তর এবং content ideas-এর জন্য tool.",
            "https://grok.com/"
        ),
        (
            "Poe",
            "poe",
            "AI Assistant",
            "💬",
            "বিভিন্ন AI model ও chatbot ব্যবহারের platform.",
            "https://poe.com/"
        ),
        (
            "Hugging Face",
            "hugging-face",
            "AI Development",
            "🤗",
            "AI models, datasets এবং machine learning resources-এর platform.",
            "https://huggingface.co/"
        ),
        (
            "Leonardo AI",
            "leonardo-ai",
            "Image Generation",
            "🖼️",
            "AI image এবং creative visual তৈরির tool.",
            "https://leonardo.ai/"
        ),
        (
            "Ideogram",
            "ideogram",
            "Image Generation",
            "🎨",
            "AI-generated images এবং text-based visual তৈরির tool.",
            "https://ideogram.ai/"
        ),
        (
            "Midjourney",
            "midjourney",
            "Image Generation",
            "🌌",
            "AI image এবং creative artwork তৈরির platform.",
            "https://www.midjourney.com/"
        ),
        (
            "Runway",
            "runway",
            "AI Video",
            "🎞️",
            "AI video generation এবং creative video editing-এর platform.",
            "https://runwayml.com/"
        ),
        (
            "Pika",
            "pika",
            "AI Video",
            "🎬",
            "AI দিয়ে creative video এবং visual effects তৈরির tool.",
            "https://pika.art/"
        ),
        (
            "Synthesia",
            "synthesia",
            "AI Video",
            "🧑‍🏫",
            "AI avatar ও presentation video তৈরির platform.",
            "https://www.synthesia.io/"
        ),
        (
            "ElevenLabs",
            "elevenlabs",
            "AI Voice",
            "🎙️",
            "AI voice generation এবং audio tools-এর platform.",
            "https://elevenlabs.io/"
        ),
        (
            "Descript",
            "descript",
            "Video",
            "🎧",
            "Video, audio এবং transcript editing-এর tool.",
            "https://www.descript.com/"
        ),
        (
            "Gamma",
            "gamma",
            "Presentation",
            "📊",
            "AI দিয়ে presentation, document এবং webpage তৈরির tool.",
            "https://gamma.app/"
        ),
        (
            "Tome",
            "tome",
            "Presentation",
            "📖",
            "AI-powered presentation এবং storytelling-এর platform.",
            "https://tome.app/"
        ),
        (
            "Beautiful.ai",
            "beautiful-ai",
            "Presentation",
            "📑",
            "দ্রুত professional presentation তৈরির tool.",
            "https://www.beautiful.ai/"
        ),
        (
            "Framer",
            "framer",
            "Web Design",
            "🌐",
            "Website design এবং publishing-এর modern platform.",
            "https://www.framer.com/"
        ),
        (
            "Cursor",
            "cursor",
            "Coding",
            "⌨️",
            "AI-assisted coding এবং software development-এর editor.",
            "https://www.cursor.com/"
        ),
        (
            "Replit",
            "replit",
            "Coding",
            "💻",
            "Browser থেকেই coding এবং app development করার platform.",
            "https://replit.com/"
        ),
        (
            "Bolt",
            "bolt",
            "Coding",
            "⚡",
            "AI দিয়ে web application তৈরি ও prototype করার tool.",
            "https://bolt.new/"
        ),
        (
            "Lovable",
            "lovable",
            "Coding",
            "💜",
            "AI দিয়ে website এবং web application তৈরির platform.",
            "https://lovable.dev/"
        ),
        (
            "v0",
            "v0",
            "Coding",
            "🧩",
            "AI দিয়ে UI এবং web interface তৈরি করার tool.",
            "https://v0.dev/"
        ),
        (
            "Figma",
            "figma",
            "Design",
            "🖌️",
            "UI/UX design, prototype এবং collaborative design-এর platform.",
            "https://www.figma.com/"
        ),
        (
            "Miro",
            "miro",
            "Productivity",
            "🗺️",
            "Online whiteboard, planning এবং brainstorming-এর platform.",
            "https://miro.com/"
        ),
        (
            "Zapier",
            "zapier",
            "Automation",
            "⚙️",
            "বিভিন্ন app-এর মধ্যে workflow automation করার platform.",
            "https://zapier.com/"
        ),
        (
            "Make",
            "make",
            "Automation",
            "🔧",
            "Visual workflow এবং automation তৈরির platform.",
            "https://www.make.com/"
        ),
        (
            "n8n",
            "n8n",
            "Automation",
            "🔄",
            "Workflow automation এবং app integration-এর platform.",
            "https://n8n.io/"
        ),
        (
            "Airtable",
            "airtable",
            "Productivity",
            "🗃️",
            "Database, project management এবং workflow management-এর platform.",
            "https://www.airtable.com/"
        ),
        (
            "Otter.ai",
            "otter-ai",
            "AI Productivity",
            "🦦",
            "Meeting transcription এবং notes তৈরির AI tool.",
            "https://otter.ai/"
        ),
        (
            "NotebookLM",
            "notebooklm",
            "Research",
            "📚",
            "Documents ও sources নিয়ে AI-powered research এবং learning tool.",
            "https://notebooklm.google/"
        ),
        (
            "Elicit",
            "elicit",
            "Research",
            "🔬",
            "Academic research এবং paper analysis-এর AI tool.",
            "https://elicit.com/"
        ),
        (
            "Consensus",
            "consensus",
            "Research",
            "📖",
            "Research paper এবং scientific information খোঁজার AI tool.",
            "https://consensus.app/"
        ),
        (
            "Suno",
            "suno",
            "AI Music",
            "🎵",
            "AI দিয়ে music ও creative audio তৈরি করার platform.",
            "https://suno.com/"
        ),
        (
            "Udio",
            "udio",
            "AI Music",
            "🎶",
            "AI-generated music তৈরির creative platform.",
            "https://udio.com/"
        ),
        (
            "Photoroom",
            "photoroom",
            "Image Editing",
            "📸",
            "Product photo এবং background editing-এর tool.",
            "https://www.photoroom.com/"
        ),
        (
            "Remove.bg",
            "remove-bg",
            "Image Editing",
            "✂️",
            "ছবির background দ্রুত remove করার tool.",
            "https://www.remove.bg/"
        ),
        (
            "Cleanup.pictures",
            "cleanup-pictures",
            "Image Editing",
            "🧹",
            "ছবি থেকে unwanted object remove করার image editing tool.",
            "https://cleanup.pictures/"
        )
    ]

    for tool in tools:
        cur.execute("""
            INSERT INTO tools
            (name, slug, category, icon, description, affiliate_url)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                slug=excluded.slug,
                category=excluded.category,
                icon=excluded.icon,
                description=excluded.description,
                affiliate_url=excluded.affiliate_url
        """, tool)

    # Update official website links for existing tools
    official_links = {
        "Buffer": "https://buffer.com/",
        "Canva": "https://www.canva.com/",
        "CapCut": "https://www.capcut.com/",
        "Character AI": "https://character.ai/",
        "ClickUp": "https://clickup.com/",
        "Evernote": "https://evernote.com/",
        "GitHub": "https://github.com/",
        "GitHub Copilot": "https://github.com/features/copilot",
        "Google Keep": "https://keep.google.com/",
        "Grammarly": "https://www.grammarly.com/",
        "Hootsuite": "https://www.hootsuite.com/",
        "InVideo": "https://invideo.io/",
        "JSFiddle": "https://jsfiddle.net/",
        "Jasper": "https://www.jasper.ai/",
        "Later": "https://later.com/",
        "Lumen5": "https://lumen5.com/",
        "Metricool": "https://metricool.com/",
        "Photopea": "https://www.photopea.com/",
        "Pictory": "https://pictory.ai/",
        "Pixlr": "https://pixlr.com/",
        "Publer": "https://publer.io/",
        "Rytr": "https://rytr.me/",
        "Stack Overflow": "https://stackoverflow.com/",
        "Trello": "https://trello.com/",
        "W3Schools": "https://www.w3schools.com/",
        "Wordtune": "https://www.wordtune.com/",
        "Writesonic": "https://writesonic.com/"
    }

    for name, url in official_links.items():
        cur.execute(
            "UPDATE tools SET affiliate_url=? WHERE name=?",
            (url, name)
        )

    con.commit()

    total = cur.execute(
        "SELECT COUNT(*) FROM tools"
    ).fetchone()[0]

    con.close()

    print("====================================")
    print("✅ AI Zone বাংলা tools update complete!")
    print(f"🤖 Total tools in database: {total}")
    print("====================================")


if __name__ == "__main__":
    main()
