from flask import Flask, request, render_template
import csv

app = Flask(__name__)


# ---------- Load CSV every time ----------
def load_data():
    data = []
    with open("bus_routes.csv", newline="", encoding="latin-1") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


# ---------- Home ----------
@app.route("/")
def home():
    return render_template("index.html")


# ---------- Search ----------
@app.route("/search")
def search():

    # 🔥 latest CSV data every search
    data = load_data()

    q = request.args.get("q", "").lower().strip()

    if not q:
        return ""

    buses = {}

    # ---------- Filter buses ----------
    for row in data:

        bus_name = row.get("bus_name", "").lower()
        bus_number = row.get("bus_number", "").strip()
        stop = row.get("stop", "").lower()

        if q in stop or q in bus_name or q == bus_number:
            key = (row.get("bus_name", ""), row.get("bus_number", ""))

            if key not in buses:
                buses[key] = []

    if not buses:
        return "<p><b>No bus found</b></p>"

    result = ""

    # ---------- Full route table ----------
    for (bus, number) in buses.keys():

        result += f"<h3 style='color:#333;'>{bus} ({number})</h3>"

        result += """
        <table style="
        margin:auto;
        border-collapse:collapse;
        width:80%;
        background:white;
        box-shadow:0 2px 10px rgba(0,0,0,0.1);
        border-radius:8px;
        overflow:hidden;
        margin-bottom:30px;
        ">
        <tr style="background:#007BFF;color:white;">
            <th style="padding:12px;">Stop</th>
            <th style="padding:12px;">Time</th>
        </tr>
        """

        for r in data:
            if r.get("bus_name", "") == bus and r.get("bus_number", "") == number:

                stop_name = r.get("stop", "")
                time = r.get("time", "")

                # searched stop text mattum highlight
                if q in stop_name.lower():
                    result += f"""
                    <tr>
                        <td style="padding:10px;border:1px solid #ddd;">
                            <span style="background:yellow;font-weight:bold;">{stop_name}</span>
                        </td>
                        <td style="padding:10px;border:1px solid #ddd;">{time}</td>
                    </tr>
                    """
                else:
                    result += f"""
                    <tr>
                        <td style="padding:10px;border:1px solid #ddd;">{stop_name}</td>
                        <td style="padding:10px;border:1px solid #ddd;">{time}</td>
                    </tr>
                    """

        result += "</table>"

    return result


# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)