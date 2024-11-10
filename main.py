from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the dataset once, when the server starts
file_path = r"D:\Sankiiiiii\PROJECT\Sem7th\compressed_data.csv"
df = pd.read_csv(file_path, low_memory=False)
df['name'] = df['name'].str.strip().str.lower()  # Normalize dataset names

def find_cheapest_substitute(medicine_name):
    # Normalize input medicine name
    medicine_name = medicine_name.strip().lower()
    
    # Check if the medicine exists in the dataset
    if medicine_name not in df['name'].values:
        return f"{medicine_name} not found in the dataset."

    # Get the row corresponding to the input medicine
    medicine_row = df[df['name'] == medicine_name].iloc[0]
    cost = medicine_row.get('Cost', None)
    
    # Gather substitutes and their costs
    substitutes = []
    for i in range(5):  # Up to 5 substitutes
        substitute_name = medicine_row.get(f'substitute{i}', None)
        if pd.notna(substitute_name):
            substitute_name = substitute_name.strip().lower()
            substitute_row = df[df['name'] == substitute_name]
            if not substitute_row.empty:
                substitute_cost = substitute_row['Cost'].values[0]
                substitutes.append((substitute_name, substitute_cost))
    
    # Find the cheapest substitute
    if not substitutes:
        return f"No substitutes found for {medicine_name}."
    
    cheapest_substitute = min(substitutes, key=lambda x: x[1])
    
    return {
        "message": f"The cheapest substitute for {medicine_name} is {cheapest_substitute[0]} at a cost of {cheapest_substitute[1]:.2f}.",
        "original_cost": cost,
        "cheapest_substitute": {
            "name": cheapest_substitute[0],
            "cost": cheapest_substitute[1]
        }
    }

@app.route('/get_cheapest_substitute', methods=['POST'])
def get_cheapest_substitute():
    # Get medicine name from the JSON request body
    data = request.get_json()
    medicine_name = data.get('medicine_name')
    
    if not medicine_name:
        return jsonify({"error": "Please provide a medicine name."}), 400
    
    result = find_cheapest_substitute(medicine_name)
    
    # Return JSON response
    if isinstance(result, str):
        return jsonify({"message": result}), 404  # Return not found if it's an error message
    else:
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
