from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

DEVELOPER = "@istgrehu"

# Desired output order
DESIRED_ORDER = [
    "Owner Name", "Father's Name", "Owner Serial No", "Model Name", "Maker Model",
    "Vehicle Class", "Fuel Type", "Fuel Norms", "Registered RTO", "Registration Date",
    "Insurance Company", "Insurance No", "Insurance Expiry", "Insurance Upto",
    "Fitness Upto", "Tax Upto", "PUC No", "PUC Upto",
    "Financier Name", "Address", "City Name", "Phone"
]


# -----------------------------------------------------------
# ⭐ WORKING VAHANX PARSER (Latest Layout)
# -----------------------------------------------------------
def get_vehicle_details(rc_number: str) -> dict:
    rc = rc_number.strip().upper()
    url = f"https://vahanx.in/rc-search/{rc}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        return {"error": f"Network error: {e}", "developer": DEVELOPER}

    # ⭐ New parser based on VahanX updated HTML
    def get_value(label):
        try:
            title_div = soup.find("div", class_="data-title", string=label)
            if not title_div:
                return None
            value_div = title_div.find_next_sibling("div", class_="data-value")
            if value_div:
                return value_div.get_text(strip=True)
            return None
        except:
            return None

    details = {
        "Owner Name": get_value("Owner Name"),
        "Father's Name": get_value("Father's Name"),
        "Owner Serial No": get_value("Owner Serial No"),
        "Model Name": get_value("Model Name"),
        "Maker Model": get_value("Maker Model"),
        "Vehicle Class": get_value("Vehicle Class"),
        "Fuel Type": get_value("Fuel Type"),
        "Fuel Norms": get_value("Fuel Norms"),
        "Registered RTO": get_value("Registered RTO"),
        "Registration Date": get_value("Registration Date"),
        "Insurance Company": get_value("Insurance Company"),
        "Insurance No": get_value("Insurance No"),
        "Insurance Expiry": get_value("Insurance Expiry"),
        "Insurance Upto": get_value("Insurance Upto"),
        "Fitness Upto": get_value("Fitness Upto"),
        "Tax Upto": get_value("Tax Upto"),
        "PUC No": get_value("PUC No"),
        "PUC Upto": get_value("PUC Upto"),
        "Financier Name": get_value("Financier Name"),
        "Address": get_value("Address"),
        "City Name": get_value("City Name"),
        "Phone": get_value("Phone"),
    }

    return details


# -----------------------------------------------------------
# ROUTES
# -----------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "🚗 Vehicle Info API is Live!",
        "developer": DEVELOPER
    })


@app.route("/lookup", methods=["GET"])
def lookup_vehicle():
    rc_number = request.args.get("rc")

    if not rc_number:
        return jsonify({
            "error": "Missing parameter: rc",
            "developer": DEVELOPER
        }), 400

    details = get_vehicle_details(rc_number)

    if "error" in details:
        details["developer"] = DEVELOPER
        return jsonify(details)

    ordered = OrderedDict()
    for key in DESIRED_ORDER:
        ordered[key] = details.get(key)

    ordered["developer"] = DEVELOPER

    return jsonify(ordered)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
