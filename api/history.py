@app.route('/api/history')
def api_history():
    conn = sqlite3.connect("sensor_data.db")
    c = conn.cursor()
    # Query the most recent 100 records (adjust as needed)
    c.execute("SELECT timestamp, temperature, pH, EC, water_level, status FROM sensor_data ORDER BY timestamp DESC LIMIT 100")
    rows = c.fetchall()
    conn.close()
    # Format records as a list of dictionaries.
    data = []
    for row in rows:
        rec = {
            "timestamp": row[0],
            "temperature": row[1],
            "pH": row[2],
            "EC": row[3],
            "water_level": row[4],
            "status": row[5]
        }
        data.append(rec)
    return jsonify(data)
