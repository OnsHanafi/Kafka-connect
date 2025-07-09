from flask import Flask, jsonify
import os
import json

app = Flask(__name__)

# Define path to the output directory
output_dir = "../output_test"
Checkpoint_file = "checkpoint.txt"

### ___Checkpoint___ ### 
def save_checkpoint(filename):
    existing_checkpoints = read_checkpoint()
    existing_checkpoints.add(filename)
    try:
        with open(Checkpoint_file, 'w') as f:
             f.write('\n'.join(existing_checkpoints))
        print("##############################################################################")
        print(f"Checkpoint saved to {Checkpoint_file}")
        print(f"Checkpoint updated. Total files saved: {len(existing_checkpoints)}")
    except FileNotFoundError:
        return None
    
def read_checkpoint():
    try:
        with open(Checkpoint_file,"r") as f:
           return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set() 

# Endpoint to fetch all files in the directory
@app.route('/api/data', methods=['GET'])
def fetch_data():
    files = os.listdir(output_dir)
    data = []

    # Read the JSON files
    for filename in files:
        if filename.endswith(".json") and  filename not in read_checkpoint():
            with open(os.path.join(output_dir, filename), "r") as f:
                content = json.load(f)
                print("##############################################################################")
                print(f"Processing file: {filename}, content: {content}")
                # add file to checkpoint
                save_checkpoint(filename)
                data.append(content)

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
