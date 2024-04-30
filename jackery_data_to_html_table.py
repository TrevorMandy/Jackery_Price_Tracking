from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    # Connect to the SQLite database
    conn = sqlite3.connect('jackery_prices.db')
    c = conn.cursor()
    
    # Fetch data from the database
    c.execute("SELECT * FROM product_prices")
    data = c.fetchall()
    
    # Close the database connection
    conn.close()
    
    # Render the HTML template with the data
    return render_template('jackery_prices_table.html', data=data)

#if __name__ == '__main__':
#    app.run(debug=True)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
