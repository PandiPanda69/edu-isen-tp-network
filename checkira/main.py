from flask import Flask

app = Flask(__name__)

@app.route("/")
def ping():
    return "ok"

def main():
    print("hello")
    app.run()


if __name__ == '__main__':
    main()
