from flask import Flask, render_template, abort, redirect
from functions import get_all_repos, search_packages, search_harder
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


@app.route("/<packages>")
def wrong_website(packages: str):
    """
    Redirect to the Cydia repo in case somebody thought this is the repo
    """
    if packages.lower().startswith("packages") or packages.lower().startswith("release"):
        packages = packages.lower().capitalize()
        return redirect(f"https://spartacusdev.github.io/{packages}")
    abort(404)


@app.route("/api/search/<package_name>")
def search(package_name: str):
    """
    Search packages
    """
    package_name = package_name.replace("%20", " ")
    return {
        "data": search_packages(package_name)
    }

@app.route("/api/search_harder/<package_name>")
def find_more_results(package_name: str):
    """
    Search packages, but show more results (slower)
    """
    package_name = package_name.replace("%20", " ")
    return {
        "data": search_harder(package_name)
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
