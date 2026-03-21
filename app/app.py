from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask app is running on Azure 🚀"

@app.route("/health")
def health():
    return "OK", 200

# Only for local testing (Azure ignores this)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)