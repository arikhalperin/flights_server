import requests

from app.main.queries.BookingDetails import BookingDetails
from app.main.queries.CancelBookingDetails import CancelBookingDetails


def get_luis_result(query):
    payload = {"subscription-key": "8a5f7767dcef412d8ad42190b25166ea",
               "verbose": False,
               "show-all-intents": True,
               "log": False,
               "query": query
               }

    url = "https://westus.api.cognitive.microsoft.com/luis/prediction/v3.0/apps/8cff3032-986b-445c-bbc3-389d76c32ca7/" \
          "slots/production/predict"

    result = requests.get(url, params=payload)

 #   print(result.json())

    result = result.json()

    print(f"LUIS result:{result}")

    if result["prediction"]["topIntent"] == "BookFlight":
        origin = None
        destination = None
        capacity = None
        date = None
        user_id = None

        data = result["prediction"]["entities"]
        print(data)

        if "From" in data:
            fromAirportStruct = data["From"]
            airport_cell = fromAirportStruct[0]
            origin = airport_cell["Airport"][0][0]

        if "To" in data:
            toAirportStruct = data["To"]
            airport_cell = toAirportStruct[0]
            destination = airport_cell["Airport"][0][0]

        else:
            if "Airport" in data:
                airport_cell = data["Airport"]
                destination = airport_cell[0][0]

        if "Capacity" in data:
            capacity = int(data["Capacity"][0])

        if "datetimeV2" in data:
            dateStruct = data["datetimeV2"]
            date_cell = dateStruct[0]
            date = date_cell["values"][0]["timex"]

        if "User ID" in data:
            user_id = data["User ID"][0]

        print(origin, destination, capacity, date, user_id)

        b = BookingDetails(origin=origin, destination=destination, capacity=capacity, travel_date=date, user_id=user_id)
        return b

    if result["prediction"]["topIntent"] == "CancelBooking":
        destination = None
        date = None
        user_id = None

        data = result["prediction"]["entities"]
        print(data)

        if "Airport" in data:
            destination = data["Airport"][0][0]

        if "datetimeV2" in data:
            dateStruct = data["datetimeV2"]
            date_cell = dateStruct[0]
            date = date_cell["values"][0]["timex"]

        if "User ID" in data:
            user_id = data["User ID"][0]

        print(destination, date, user_id)

        b = CancelBookingDetails(destination=destination, travel_date=date, user_id=user_id)
        return b

    if result["prediction"]["topIntent"] == "EditBooking":
        destination = None
        capacity = None
        date = None
        user_id = None

        data = result["prediction"]["entities"]
        print(data)

        if "Airport" in data:
            destination = data["Airport"][0][0]

        if "Capacity" in data:
            capacity = data["Capacity"][0]

        if "datetimeV2" in data:
            dateStruct = data["datetimeV2"]
            date_cell = dateStruct[0]
            date = date_cell["values"][0]["timex"]

        if "User ID" in data:
            user_id = data["User ID"][0]

        print(destination, capacity, date, user_id)

        b = BookingDetails(destination=destination, capacity=capacity, travel_date=date, user_id=user_id)
        return b


