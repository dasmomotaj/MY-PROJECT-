import os
import sqlite3
import importlib

print("\n======================================")
print("   AI ZONE বাংলা - PROJECT TEST")
print("======================================\n")

passed = 0
failed = 0

def test(name, condition):
    global passed, failed
    if condition:
        print(f"✅ PASS  | {name}")
        passed += 1
    else:
        print(f"❌ FAIL  | {name}")
        failed += 1

# 1. Files
required_files = [
    "app.py",
    "templates/base.html",
    "templates/index.html",
    "templates/tools.html",
    "templates/tutorials.html",
    "templates/blog.html",
    "templates/services.html",
    "templates/about.html",
    "templates/contact.html",
    "templates/login.html",
    "templates/register.html",
    "templates/profile.html",
    "templates/admin_login.html",
    "templates/admin.html",
    "static/style.css",
    "static/script.js",
]

print("📁 FILE TEST")
for file in required_files:
    test(file, os.path.exists(file))

# 2. App import
print("\n🐍 FLASK TEST")

try:
    app_module = importlib.import_module("app")
    app = app_module.app
    test("Flask app import", True)
except Exception as e:
    test("Flask app import", False)
    print("   Error:", e)
    print("\n❌ Flask app load failed. Fix the error above first.")
    raise SystemExit

# 3. Database
print("\n🗄️ DATABASE TEST")

db_file = "ai_zone.db"

test("Database exists", os.path.exists(db_file))

if os.path.exists(db_file):
    try:
        conn = sqlite3.connect(db_file)
        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }

        required_tables = {
            "users",
            "tools",
            "favorites",
            "ratings",
            "messages",
            "blog",
            "visits",
        }

        for table in sorted(required_tables):
            test(f"Table: {table}", table in tables)

        conn.close()

    except Exception as e:
        test("SQLite database readable", False)
        print("   Error:", e)

# 4. Flask routes
print("\n🌐 ROUTE TEST")

routes = [
    "/",
    "/tools",
    "/tutorials",
    "/social",
    "/blog",
    "/services",
    "/about",
    "/contact",
    "/login",
    "/register",
    "/profile",
    "/admin/login",
    "/admin",
]

with app.test_client() as client:
    for route in routes:
        try:
            response = client.get(route, follow_redirects=False)

            # 200 = page works
            # 302 = login protection/redirect works
            ok = response.status_code in (200, 302)

            test(
                f"{route} [{response.status_code}]",
                ok
            )

        except Exception as e:
            test(route, False)
            print("   Error:", e)

# 5. Registration test
print("\n👤 USER SYSTEM TEST")

test_username = "test_user_az"
test_email = "test@aizone.local"
test_password = "TestPassword123!"

try:
    with app.test_client() as client:

        response = client.post(
            "/register",
            data={
                "username": test_username,
                "email": test_email,
                "password": test_password,
            },
            follow_redirects=False,
        )

        # 200/302 both can indicate the route processed
        test(
            "Registration route processed",
            response.status_code in (200, 302)
        )

except Exception as e:
    test("Registration system", False)
    print("   Error:", e)

# 6. Database user check
try:
    conn = sqlite3.connect(db_file)
    row = conn.execute(
        "SELECT username, email FROM users WHERE username=?",
        (test_username,)
    ).fetchone()

    test("Test user saved in database", row is not None)

    conn.close()

except Exception as e:
    test("User database check", False)
    print("   Error:", e)

# 7. Admin environment
print("\n🔐 ADMIN TEST")

admin_password = os.environ.get("AI_ZONE_ADMIN_PASSWORD")

test(
    "AI_ZONE_ADMIN_PASSWORD is set",
    bool(admin_password)
)

# 8. Affiliate tools
print("\n🔗 AFFILIATE TRACKING TEST")

try:
    conn = sqlite3.connect(db_file)

    tool = conn.execute(
        "SELECT slug, clicks FROM tools LIMIT 1"
    ).fetchone()

    test("Tools exist in database", tool is not None)

    if tool:
        slug = tool[0]

        with app.test_client() as client:
            response = client.get(
                f"/go/{slug}",
                follow_redirects=False
            )

            test(
                f"Affiliate route /go/{slug}",
                response.status_code in (200, 302)
            )

    conn.close()

except Exception as e:
    test("Affiliate tracking", False)
    print("   Error:", e)

# 9. Analytics
print("\n📊 ANALYTICS TEST")

try:
    conn = sqlite3.connect(db_file)

    visit_count = conn.execute(
        "SELECT COUNT(*) FROM visits"
    ).fetchone()[0]

    test(
        "Analytics visits table working",
        visit_count >= 0
    )

    conn.close()

except Exception as e:
    test("Analytics system", False)
    print("   Error:", e)

# Summary
print("\n======================================")
print("             TEST SUMMARY")
print("======================================")

print(f"✅ Passed : {passed}")
print(f"❌ Failed : {failed}")

if failed == 0:
    print("\n🎉 ALL TESTS PASSED!")
    print("AI Zone বাংলা project is ready for the next stage.")
else:
    print("\n⚠️ কিছু test failed.")
    print("উপরের ❌ FAIL লাইনগুলো দেখো।")

print("\n======================================\n")
