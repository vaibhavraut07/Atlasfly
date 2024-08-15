from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd
from datetime import datetime, timedelta  # Import datetime module
import os  # Import os module for environment variables

app = Flask(__name__)
model = pickle.load(open("flight_rf.pkl", "rb"))
# This is final commit

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        current_date = datetime.now().strftime("%Y-%m-%dT%H:%M")
        depart_date = request.form["Dep_Time"]
        min_arrival_date = (datetime.fromisoformat(depart_date) + timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M")

        # Date_of_Journey
        date_dep = request.form["Dep_Time"]
        Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)

        # Departure
        Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)

        # Arrival
        date_arr = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)

        # Duration
        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)

        # Total Stops
        Total_stops = int(request.form["stops"])

        # Airline
        airline = request.form['airline']
        Jet_Airways = IndiGo = Air_India = Multiple_carriers = SpiceJet = Vistara = GoAir = Multiple_carriers_Premium_economy = Jet_Airways_Business = Vistara_Premium_economy = Trujet = 0

        if airline == 'Jet Airways':
            Jet_Airways = 1
        elif airline == 'IndiGo':
            IndiGo = 1
        elif airline == 'Air India':
            Air_India = 1
        elif airline == 'Multiple carriers':
            Multiple_carriers = 1
        elif airline == 'SpiceJet':
            SpiceJet = 1
        elif airline == 'Vistara':
            Vistara = 1
        elif airline == 'GoAir':
            GoAir = 1
        elif airline == 'Multiple carriers Premium economy':
            Multiple_carriers_Premium_economy = 1
        elif airline == 'Jet Airways Business':
            Jet_Airways_Business = 1
        elif airline == 'Vistara Premium economy':
            Vistara_Premium_economy = 1
        elif airline == 'Trujet':
            Trujet = 1

        # Source
        s_Delhi = s_Kolkata = s_Mumbai = s_Chennai = 0
        Source = request.form["Source"]
        if Source == 'Delhi':
            s_Delhi = 1
        elif Source == 'Kolkata':
            s_Kolkata = 1
        elif Source == 'Mumbai':
            s_Mumbai = 1
        elif Source == 'Chennai':
            s_Chennai = 1

        # Destination
        d_Cochin = d_Delhi = d_New_Delhi = d_Hyderabad = d_Kolkata = 0
        Destination = request.form["Destination"]
        if Destination == 'Cochin':
            d_Cochin = 1
        elif Destination == 'Delhi':
            d_Delhi = 1
        elif Destination == 'New_Delhi':
            d_New_Delhi = 1
        elif Destination == 'Hyderabad':
            d_Hyderabad = 1
        elif Destination == 'Kolkata':
            d_Kolkata = 1

        # Prediction
        prediction = model.predict([[
            Total_stops,
            Journey_day,
            Journey_month,
            Dep_hour,
            Dep_min,
            Arrival_hour,
            Arrival_min,
            dur_hour,
            dur_min,
            Air_India,
            GoAir,
            IndiGo,
            Jet_Airways,
            Jet_Airways_Business,
            Multiple_carriers,
            Multiple_carriers_Premium_economy,
            SpiceJet,
            Trujet,
            Vistara,
            Vistara_Premium_economy,
            s_Chennai,
            s_Delhi,
            s_Kolkata,
            s_Mumbai,
            d_Cochin,
            d_Delhi,
            d_Hyderabad,
            d_Kolkata,
            d_New_Delhi
        ]])

        departure_from = request.form.get("Source")
        arrival_at = request.form.get("Destination")
        depart_date = request.form.get("Dep_Time")
        arrival_date = request.form.get("Arrival_Time")
        stoppage = request.form.get("stops")
        company = request.form.get("airline")

        output = round(prediction[0])

        return render_template(
            "index.html",
            current_date=current_date,
            min_arrival_date=min_arrival_date,
            prediction_text="{amount}".format(amount=output),
            departure_from=departure_from,
            arrival_at=arrival_at,
            depart_date=depart_date,
            arrival_date=arrival_date,
            stoppage=stoppage,
            company=company
        )

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT environment variable or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)
