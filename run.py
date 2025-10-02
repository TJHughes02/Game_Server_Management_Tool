from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
    print("Invocation of the Machine Spirit complete. The sacred cogs turn and the datastream flows.")

if __name__ == '__main__':
    app.run(debug=True)
