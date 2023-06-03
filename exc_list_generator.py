import importlib.util
import inspect
import json
import pkgutil

import app
from app.exceptions import ExceptionDescribed

info = {}

def handle_module(m):
    members = inspect.getmembers(m)
    for member in members:
        if inspect.isclass(member[1]):
            if ExceptionDescribed in member[1].__bases__:
                print("class found", member[1])
                print(f"Class: {member[1].__name__}, Code: {member[1].code}, Status code: {member[1].status_code}, Description: {member[1].description}")
                class_info = {
                    member[1].code: {
                        "description": member[1].description
                    }
                }
                global info
                info = class_info | info
    if hasattr(m, "__path__"):
        for module in pkgutil.iter_modules(m.__path__):
            spec = module.module_finder.find_spec(module.name)
            m1 = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m1)
            handle_module(m1)


handle_module(app)

with open('app/static/exceptions.json', 'w') as file:
    print(json.dump(info, file, ensure_ascii=False))