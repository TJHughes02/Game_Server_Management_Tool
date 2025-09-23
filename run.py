from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
    print("Machine Spirit Awake and Vigilant. Praise the Omnissiah!")

if __name__ == '__main__':
    app.run(debug=True)
