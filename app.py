from flask import Flask, render_template, redirect, url_for, request, flash
from config import Config
from models import db, User, Job
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

    if Job.query.count() == 0:
        sample_jobs = [
            Job(
                title="Python Backend Developer",
                company="TechNova Solutions",
                location="Bangalore, India",
                salary="₹6-8 LPA",
                description="Looking for a Python developer with Flask experience and REST API knowledge."
            ),
            Job(
                title="Data Analyst Intern",
                company="DataSphere Analytics",
                location="Remote",
                salary="₹15,000/month",
                description="Work with datasets, perform data cleaning and build visual dashboards."
            ),
            Job(
                title="Machine Learning Engineer",
                company="AI Vision Labs",
                location="Hyderabad, India",
                salary="₹10-14 LPA",
                description="Build predictive ML models and optimize AI pipelines."
            ),
            Job(
                title="Frontend Developer",
                company="BrightWeb Technologies",
                location="Mumbai, India",
                salary="₹5-7 LPA",
                description="Develop responsive UI using React and Bootstrap."
            )
        ]

        db.session.bulk_save_objects(sample_jobs)
        db.session.commit()

@app.route("/")
def index():
    jobs = Job.query.all()
    return render_template("index.html", jobs=jobs)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username")).first()
        if user and check_password_hash(user.password, request.form.get("password")):
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("Invalid credentials")
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/post_job", methods=["GET", "POST"])
@login_required
def post_job():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        job = Job(title=title, description=description)
        db.session.add(job)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("post_job.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)