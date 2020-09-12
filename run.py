from instahelper_app import create_app
from instahelper_app.models import db

app = create_app()

def init_db():
    db.init_app(app)
    db.app = app
    db.create_all()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
