from flask import Flask

app = Flask(__name__)

@app.get("/")
def home():
    return "Hello from Jenkins CI/CD!\n"
@app.get("/health")
def health():
    return "OK\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
