from flask import Flask, jsonify
import pandas as pd
import random  # Import the random module
app = Flask('__name__')

# Load the CSV data when the application starts
csv_file = 'shopping_trends.csv'  # Replace with the path to your CSV file
data = pd.read_csv(csv_file)

@app.route('/api/data', methods=['GET'])

def get_random_data():
    # Select a random row from the data
    random_row = data.sample(n=1)

    # Convert the selected row to JSON
    json_data = random_row.to_dict(orient='records')[0]

    return jsonify(json_data)

if __name__ == '__main__':
    #app.run(port=50001)
    #app.run() # This is when you want to access the app from your local machine
    app.run(host='0.0.0.0') # this is when we want to allow connection from outside the local machine.
