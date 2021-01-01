from app import create_app, db

app = create_app('local')
app_context = app.app_context()
app_context.push()
db.drop_all()
db.create_all()

db.session.flush()
app_context.pop()