import sys, os
sys.path.insert(0, r"D:\Meu Portfolio e HUB")
os.chdir(r"D:\Meu Portfolio e HUB")
from app import create_app
app = create_app()
with app.test_client() as c:
    for route in ["/about", "/planner", "/projects", "/skills"]:
        r = c.get(route, follow_redirects=True)
        print(route, r.status_code)
