from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    test_user = User(
        display_name = "TestUser",
        email = "testuser@gmail.com",
        #password = "password123",
        is_owner = False
    )
    test_user.set_pass("password123")
    db.session.add(test_user)
    db.session.commit()
    print("The Machine Spirit hums in solemn approval, Tech-Priest anointed. Praise the Omnissiah!")