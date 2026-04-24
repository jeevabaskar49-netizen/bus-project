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

    data = load_data()

    q = request.args.get("q", "").lower().strip()

    if not q:
        return ""

    buses = {}

    # ---------- Filter ----------
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

    # 🔥 Bus count
    result += f"<h2 style='text-align:center;'>{len(buses)} Bus Found 🚍</h2>"

    # ---------- Build UI ----------
    for (bus, number) in buses.keys():

        result += f"""
        <div style="
        background:white;
        padding:20px;
        margin:20px auto;
        width:85%;
        border-radius:12px;
        box-shadow:0 5px 15px rgba(0,0,0,0.2);
        ">

        <h3 style='color:#007BFF;margin-bottom:10px;'>{bus} ({number})</h3>
        """

        result += """
        <table style="
        margin:auto;
        border-collapse:collapse;
        width:80%;
        background:white;
        border-radius:8px;
        overflow:hidden;
        margin-bottom:20px;
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

                if q in stop_name.lower():
                    result += f"""
                    <tr style="transition:0.3s;">
                        <td style="padding:10px;border:1px solid #ddd;">
                            <span style="background:yellow;font-weight:bold;">{stop_name}</span>
                        </td>
                        <td style="padding:10px;border:1px solid #ddd;">{time}</td>
                    </tr>
                    """
                else:
                    result += f"""
                    <tr style="transition:0.3s;">
                        <td style="padding:10px;border:1px solid #ddd;">{stop_name}</td>
                        <td style="padding:10px;border:1px solid #ddd;">{time}</td>
                    </tr>
                    """

        result += "</table></div>"   # ✅ correct indent

    return result


# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)