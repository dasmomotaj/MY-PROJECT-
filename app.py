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
        name = request.form.get("name")
        message = f"ধন্যবাদ {name}! আপনার বার্তা গ্রহণ করা হয়েছে।"

    return render_template("contact.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
