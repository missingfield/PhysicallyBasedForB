from pathlib import Path
from functools import cache
from typing import Any
from urllib.error import HTTPError
import urllib.request
import json

SCRIPT_DIR = Path(__file__).parent
BASE_URL = "https://api.physicallybased.info/"
CACHE_LOC = SCRIPT_DIR / "cached_data"
CACHE_LOC.mkdir(exist_ok=True)


DATA_REQUESTS = {
    "materials": BASE_URL + "materials",
    "lights": BASE_URL + "lightsources",
    "cameras": BASE_URL + "cameras",
}


def _request_data(path: str):
    """ TODO: handle 404 """
    with urllib.request.urlopen(path) as response:
        return json.loads(response.read())


def _cache_response(datatype: str, response: dict[str, Any]) -> Path:
    """ Write response from server to json file CACHE_LOC/datatype.json"""
    path = CACHE_LOC / f"{datatype}.json"
    print(f"Caching {datatype} to {path}")
    with open(path, "w") as cache_file:
        cache_file.write(json.dumps(response))


def run_update():
    """ Get data from api and cache if successful """
    new_cache_data = False
    for datatype, url in DATA_REQUESTS.items():
        print(f"Requesting {datatype}")
        try:
            data = _request_data(url)
            _cache_response(datatype, data)
            new_cache_data = True
        except HTTPError:
            print(f"Failed to get {datatype}, from url: {url}")
            continue
    # Loaders cache their returns so this is necessary
    if new_cache_data:
        load_cached_data.cache_clear()
        get_names.cache_clear()
        

@cache
def load_cached_data(datatype: str) -> list[dict[str, Any]]:
    cached_path = CACHE_LOC / f"{datatype}.json"
    with open(cached_path, "r") as cache_file:
        return json.loads(cache_file.read())


@cache
def get_names(datatype: str, category_prefix: bool = True):
    names = []
    data = load_cached_data(datatype)
    for item in data:
        categories = item.get("category")
        name =  item.get("name")
        if categories is None or not category_prefix:
            names.append(name)
        else:
            for category in categories:
                names.append(f"{category}/{name}")
    return sorted(names)


def get_data_by_name(datatype: str, name: str):
    """
    Get the data of datatype by matching name arg.
    name is processed 'name.split("/", 1)[-1]' to remove potential category prefix
    """
    # Remove category is preset
    name = name.split("/", 1)[-1]
    data = load_cached_data(datatype)
    for item in data:
        if item["name"] == name:
            return item
    return None


if __name__ == "__main__":
    #run_update()
    names = get_names("materials")
    test_name = "Metal/Brass"
    brass = get_data_by_name("materials", test_name)
    print(brass.keys())

