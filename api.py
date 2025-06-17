from flask import Flask, request, jsonify
from jyotisha.panchangam.spatio_temporal import City
from jyotisha.panchangam.daily import DailyPanchanga

app = Flask(__name__)

@app.route('/api/panchangam', methods=['GET'])
def panchangam_api():
    # Get date parameters from the URL query string
    year_str = request.args.get('year')
    month_str = request.args.get('month')
    day_str = request.args.get('day')

    # Validate the input
    if not all([year_str, month_str, day_str]):
        return jsonify({"error": "Missing required parameters. Please provide year, month, and day."}), 400

    try:
        year, month, day = int(year_str), int(month_str), int(day_str)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid date parameters. Year, month, and day must be integers."}), 400

    # Perform the Panchangam calculation
    chennai = City('Chennai', '13.0827 N', '80.2707 E', 'Asia/Kolkata')
    panchanga = DailyPanchanga(city=chennai, year=year, month=month, day=day)
    panchanga.compute()

    # Build a structured dictionary with the results
    response_data = {
        "input_data": {
            "city": chennai.name,
            "year": year,
            "month": month,
            "day": day
        },
        "sunrise": panchanga.sunrise.get_hour_str() if panchanga.sunrise else None,
        "sunset": panchanga.sunset.get_hour_str() if panchanga.sunset else None,
        "tithi_at_sunrise": panchanga.tithis_with_ends[0].name.replace('_', ' '),
        "nakshatra_at_sunrise": panchanga.nakshatras_with_ends[0].name.replace('_', ' '),
        "yoga_at_sunrise": panchanga.yogas_with_ends[0].name.replace('_', ' '),
    }

    # Return the dictionary as a JSON response
    return jsonify(response_data)
