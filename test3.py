import pandas as pd

# List of functions and datasets
functions = ["cost", "time"]
set_datasets = ["d1", "d2", "d3"]

# Placeholder function to simulate the FCA algorithm
def run_fca_algorithm(dataset, metric):
    # Simulate some computation and return a result
    import random
    return random.uniform(10, 100)

# Initialize a dictionary to store data for each function
data_dict = {f: [] for f in functions}

for f in functions:
    for d in set_datasets:
        # Simulate the FCA algorithm execution
        result = run_fca_algorithm(d, f)
        
        # Store the result in the data dictionary
        data_dict[f].append({
            "dataset": d,
            "FCA": result
        })

# Create a new Excel writer object
with pd.ExcelWriter('results/metrics.xlsx', engine='openpyxl') as writer:
    for f in functions:
        # Convert the data to a DataFrame
        df = pd.DataFrame(data_dict[f])
        
        # Write the DataFrame to an Excel sheet
        df.to_excel(writer, sheet_name=f, index=False)

print("Excel file created successfully.")
