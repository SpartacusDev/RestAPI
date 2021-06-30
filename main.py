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


@app.route("/<repo_endpoint>")
def wrong_website(repo_endpoint: str):
    """
    Redirect to the Cydia repo in case somebody thought this is the repo
    """
    if repo_endpoint.lower().startswith("packages") or repo_endpoint.lower().startswith("release") or \
        repo_endpoint.lower().startswith("cydiaicon"):
        return redirect(f"https://spartacusdev.github.io/{repo_endpoint}")
    abort(404)


@app.route("/depictions/<depiction_endpoint>")
def redirect_to_depictions(depiction_endpoint: str):
    """
    Redirect to the Cydia repo in case somebody thought this is the repo
    """
    return redirect(f"https://spartacusdev.github.io/depictions/{depiction_endpoint}")


@app.route("/SileoDepictions/<depiction_endpoint>")
def redirect_to_sileo_depictions(depiction_endpoint: str):
    """
    Redirect to the Cydia repo in case somebody thought this is the repo
    """
    return redirect(f"https://spartacusdev.github.io/SileoDepictions/{depiction_endpoint}")


@app.route("/images/<image_endpoint>")
def redirect_to_images(image_endpoint: str):
    """
    Redirect to the Cydia repo in case somebody thought this is the repo
    """
    return redirect(f"https://spartacusdev.github.io/images/{image_endpoint}")


@app.route("/debs/<deb_endpoint>")
def redirect_to_dbs(deb_endpoint: str):
    """
    Redirect to the Cydia repo in case somebody thought this is the repo
    """
    return redirect(f"https://spartacusdev.github.io/debs/{deb_endpoint}")


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
