import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
# Replace 'data.csv' with the path to your actual CSV file
file_path = './results/stop_creteria.csv'
data = pd.read_csv(file_path)

# Plot the curves
plt.figure(figsize=(10, 6))

plt.plot(data['Iteraitons'], data['PSO'], marker='o', label='PSO')
plt.plot(data['Iteraitons'], data['CPSO'], marker='o', label='C-PSO')
plt.plot(data['Iteraitons'], data['CRO'], marker='o', label='CRO')

# Add labels, title, and legend
plt.xlabel('Iteraitons', fontsize=12)
plt.ylabel('Fitness', fontsize=12)
plt.legend()
plt.grid(True)

# Show the plot

# Save the figure as a PNG file
plt.savefig('./results/stop_creteria.png')

# Display the plot
plt.show()
