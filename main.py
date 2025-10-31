from flask import Flask, render_template
from flask_login import LoginManager, login_required, current_user
from submod.auth import auth_bp, User, load_user_by_id, init_db  # noqa: F401
from submod.kubctl import Kubctl, Internal  # noqa: F401
import dotenv

dotenv.load_dotenv()
app = Flask(__name__,static_folder='static', static_url_path='/static')
app.secret_key = "secret"

# setup login manager
login_manager = LoginManager(app)
login_manager.user_loader(load_user_by_id)
login_manager.login_view = "auth.login"


# register blueprint
app.register_blueprint(auth_bp)

# init database
with app.app_context():
    init_db()

@app.route("/protected")
@login_required
def protected():
    return render_template("protected/home.html", name=current_user.username)

@app.route("/protected/podmanage")
@login_required
def podmanage():
    return render_template("protected/podman.html", files=Internal.listdir("example"))


if __name__ == "__main__":
    app.run(debug=True)
