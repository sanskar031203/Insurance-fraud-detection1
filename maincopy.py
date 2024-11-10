from flask import Flask, request, jsonify
from reader import extract_invoice_details
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
    
    return cost,cheapest_substitute[1]
pdf_path = 'test.pdf'
medicine_name = extract_invoice_details()
result = find_cheapest_substitute(medicine_name)
oc = result[0]
cc = result[1]
diff = ((oc-cc)/oc)*100
th = 30
print(f"Original price : {oc}")
print(f"Alternate medicine price : {cc}")
print(f"Difference is : {diff} %")
if diff>th :
    print("Medicine bills are inflated")
print(oc)

