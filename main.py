from flask import Flask, render_template, abort, request
from functions import get_all_repos, search_packages
from database import db, Repository, LastUpdate
import os
from datetime import date

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
repos = get_all_repos()
backend_finished = False


@app.route("/")
def home():
    """
    Homepage ¯\_(ツ)_/¯
    """
    return render_template("home.html")


@app.route("/documentation")
def api_documentaion():
    """
    Documentation page ¯\_(ツ)_/¯
    """
    global backend_finished
    if backend_finished:
        status = "Database was updated today"
        status_color = "green"
    else:
        last_update = db.query(LastUpdate).first()
        status = "Database has never been updated" if last_update is None else f"Database has last been updated on {last_update.update_date}"
        status_color = "red"
    return render_template("api_documentation.html", repositories=repos, status=status, status_color=status_color)


@app.route("/api/search/<package_name>")
def search(package_name: str):
    """
    Search packages
    """
    global backend_finished
    package_name = package_name.replace("%20", " ")
    last_update = db.query(LastUpdate).first()
    return {
        "status": "Database has been updated today" if backend_finished else "Database has never been updated" if last_update is None else f"Database has last been updated on {last_update.update_date}",
        "data": search_packages(package_name)
    }

@app.route(f"/api/<repo>")
def get_repo(repo: str):
    """
    Get all packages from a certain repo
    """
    global repos, backend_finished
    for i in repos:
        if i.lower() == repo.lower():
            break
    else:
        abort(404)

    last_update = db.query(LastUpdate).first()

    return {
        "status": "Database has been updated today" if backend_finished else "Database has never been updated" if last_update is None else f"Database has last been updated on {last_update.update_date}",
        "data": db.query(Repository).filter(Repository.name.ilike(repo.lower())).first().packages
    }


@app.route("/api/finished", methods=["POST"])
def finished():
    """
    This for the backend
    """
    global backend_finished
    if request.headers["User-Agent"] == os.getenv("BACKEND"):
        backend_finished = True
        update = f"{date.today()}"
        last_update = db.query(LastUpdate).first()
        if last_update is None:
            last_update = LastUpdate(title="Last Update", update_date=update)
            db.add(last_update)
        else:
            last_update.update_date = update
        db.commit()
    
    return {"finished": backend_finished}


if __name__ == "__main__":
    app.run()
