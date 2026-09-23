from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>My First Web App</title>
    </head>
    <body>
        <h1>🚀 Hello from My Web App!</h1>
        <p>আমি Termux + Python + Flask দিয়ে এই App তৈরি করেছি।</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

