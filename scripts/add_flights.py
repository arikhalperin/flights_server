from app import create_app, db, Flight
import datetime

app = create_app('local')
app_context = app.app_context()
app_context.push()

departure = datetime.datetime(year=2021, month=1, day=1, hour=17, minute=0, second=0)
landing = departure + datetime.timedelta(hours=5)
for i in range(1, 30):
    flight_added = Flight(source="london", destination="new york",
                            landing=landing, departure=departure, capacity=300)
    db.session.add(flight_added)
    departure = departure + datetime.timedelta(days=2)
    landing = landing + datetime.timedelta(days=2)
db.session.commit()
db.session.flush()
app_context.pop()
