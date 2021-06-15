from fuzzywuzzy.fuzz import partial_ratio, ratio
import gc
from typing import List
from database import db, Repository, Package


gc.enable()


def get_all_repos() -> list:
    """
    O(n) when n is the amount of repos.\n
    Get the list of all the repos in the database (the sources.json file might have repos that aren't in the database)
    """
    return db.query(Repository).all()


def search_packages(package_name: str) -> list:
    """
    O(n*m) when n is the amount of repos and m is the amount of packages in each repo.\n
    Search for a package in the database and get a list of the most similar results.
    """
    packages = db.query(Package).filter(Package.name.ilike(f"%{package_name}%"))
    return [package.to_dict() for package in packages]
    results = []
    for repo in repos:
        for package in repo.packages:
            pratio = partial_ratio(package_name.lower(), package["name"].lower())
            rratio = ratio(package_name.lower(), package["name"].lower())
            package["repo name"] = repo.name
            if rratio >= 85 or pratio >= 85:
                result = {
                    "package": package,
                    "ratio": rratio
                    # I may say that I also add whatever is "similar" (as partial_ratio checks the similarity between the most similar substring),
                    # I still specify it's rratio so I don't get irrelevant stuff at the top
                }
                results.append(result)
            else:
                pratio = partial_ratio(package_name.lower(), package["package"].lower())
                rratio = ratio(package_name.lower(), package["package"].lower())
                if rratio >= 75 or pratio >= 85:
                    result = {
                        "package": package,
                        "ratio": rratio
                    }
                    results.append(result)

    _sort(results)  # I am not using `binary_search` with inserts because this one should be slightly faster in theory (and since this function is incredibly slow (almost 7 seconds for the website to return an answer) I want it to be as fast as it can be)

    results = [result["package"] for result in results]
    return results


def binary_search(l: List[dict], x: dict) -> int:
    """
    O(log(n)) when n is the size of `l`.\n
    Parameters:\n
    • l -> List[dict]: Represents a list of dictionaries\n
    • x -> dict: A dictionary you wish to add to the list\n\n
    This is just binary search. It returns the index of where you should add x to l
    """
    if len(l) == 0:
        return 0
    first, last = 0, 0
    while first <= last:
        mid = first + (last - first) // 2
        if l[mid]["ratio"] == x["ratio"]:
            return mid
        elif l[mid]["ratio"] > x["ratio"]:
            last = mid - 1
        else:
            first = mid + 1
    return last


def _sort(l: List[dict]) -> None:
    """
    O(n*log(n)) when n is the size of `l`.\n
    Parameters:\n
    • l -> List[dict]: Represents a list of dictionaries\n\n
    Returns `None`, sorts the list. I don't use it anymore as sorting the list as I search is faster
    """
    if len(l) <= 1:
        return
    right, left = l[ : len(l) // 2], l[len(l) // 2 : ]
    _sort(right)
    _sort(left)

    i, j, k = 0, 0, 0

    while i < len(right) and j < len(left):
        if right[i]["ratio"] < left[j]["ratio"]:
            l[k] = left[j]
            j += 1
        else:
            l[k] = right[i]
            i += 1
        k += 1
    
    for i in range(i, len(right)):
        l[k] = right[i]
        k += 1
    for i in range(j, len(left)):
        l[k] = left[j]
        k += 1
