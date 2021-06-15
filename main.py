from flask import Flask, render_template, abort
from functions import get_all_repos, search_packages
from database import db, Repository

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
repos = get_all_repos()


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
    return render_template("api_documentation.html", repositories=[{"name": repo.name, "url": f"https://spartacusdev.herokuapp.com/api/{repo.name.replace(' ', '%20')}"} for repo in repos])


@app.route("/api/search/<package_name>")
def search(package_name: str):
    """
    Search packages
    """
    package_name = package_name.replace("%20", " ")
    return {
        "data": search_packages(package_name)
    }

@app.route(f"/api/<repo>")
def get_repo(repo: str):
    """
    Get all packages from a certain repo
    """
    repo = repo.replace("%20", " ")
    repo = db.query(Repository).filter(Repository.name.ilike(repo)).first()
    if repo is None:
        abort(404)
    return {
        "data": [package.to_dict() for package in repo.packages]
    }



if __name__ == "__main__":
    app.run()
