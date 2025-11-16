from app import create_app, db
from app.utils import start_server

# change this to the ID of the server you want to test
SERVER_ID = 1

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        print(f"[test] Calling start_server({SERVER_ID})")
        start_server(SERVER_ID)
        print(f"[test] Done start_server({SERVER_ID})")
