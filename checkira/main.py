from flask import Flask, render_template
import config
import check
import ports

app = Flask(__name__)
cfg = {}


@app.route("/")
def index():
    network_state = {}
    for g in cfg["groups"]:
        network_state[g] = ports.check_project_ports(cfg["groups"][g])

    return render_template("index.html", groups=cfg["groups"], checks=network_state)


@app.route("/check/<string:group>", methods = [ "POST" ])
def check_group(group):
    if group not in cfg["groups"]:
       return "Invalid group", 404 
 
    try:
        check.check_project(cfg=cfg["groups"][group])
    except Exception as ex:
        return str(ex), 500
 
    return "Pass.", 200


def main():
    global cfg

    cfg = config.load_config()
    app.run()


if __name__ == '__main__':
    main()
