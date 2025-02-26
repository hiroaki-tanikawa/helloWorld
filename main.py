from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return "Hello, this is a simple web server!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)