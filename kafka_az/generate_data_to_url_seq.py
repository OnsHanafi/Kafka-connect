from flask import Flask, jsonify
import pandas as pd

app = Flask('__name__')

# Load the CSV data when the application starts
csv_file = 'shopping_trends.csv'  # Replace with the path to your CSV file

# Define a generator function to yield rows one by one
def read_csv_sequentially(csv_file):
    for chunk in pd.read_csv(csv_file, chunksize=1):
        yield chunk.to_dict(orient='records')[0]

data_generator = read_csv_sequentially(csv_file)

@app.route('/api/data', methods=['GET'])
def get_sequential_data():
    try:
        # Get the next row from the generator
        json_data = next(data_generator)
        return jsonify(json_data)
    except StopIteration:
        return "No more data available"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
