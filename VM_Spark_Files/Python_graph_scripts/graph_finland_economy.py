import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('/home/Muhammed/combined_finland_happiness_detailed_scores.csv')

# Convert 'Ladder score' to numeric, errors='coerce' will set invalid parsing to NaN
df['Logged GDP per capita'] = pd.to_numeric(df['Logged GDP per capita'], errors='coerce')

# Ensure the data is sorted by year
df.sort_values('Year', inplace=True)

# Plotting the line graph
plt.figure(figsize=(10, 6))
plt.plot(df['Year'], df['Logged GDP per capita'], marker='o', linestyle='-', color='b')

# Adding titles and labels
plt.title('Trend of Logged GDP per capita for Finland')
plt.xlabel('Year')
plt.ylabel('Logged GDP per capita')

# Displaying the grid
plt.grid(True)

# Save the plot to a png file
plt.savefig('finland_economy.png')

# Show the plot
plt.show()
