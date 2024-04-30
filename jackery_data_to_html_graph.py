from flask import Flask, render_template
import sqlite3
import json

app = Flask(__name__)

@app.route('/')
def display_prices():
    # Connect to the SQLite database
    conn = sqlite3.connect('jackery_prices.db')
    cursor = conn.cursor()

    # Fetch data from the database for date '2024-04-28'
    cursor.execute("SELECT * FROM product_prices WHERE Date = '2024-04-28'")
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Preprocess the data into JSON format
    json_data = []
    for row in data:
        product = {
            'Product Name': row[0],
            'Discounted Price': row[1],
            'Regular Price': row[2],
            'Date': row[3]
        }
        json_data.append(product)

    # Convert the data to JSON format
    json_string = json.dumps(json_data)

    # Render the HTML template and pass the JSON data
    return render_template('jackery_prices_graph.html', data=json_string)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
