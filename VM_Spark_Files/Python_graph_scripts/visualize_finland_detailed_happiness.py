import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('/home/Muhammed/combined_finland_happiness_detailed_scores.csv')

# Convert to numeric and sort by year
convert_columns = ["Ladder score", "Logged GDP per capita", "Social support"]
df[convert_columns] = df[convert_columns].apply(pd.to_numeric, errors='coerce')
df.sort_values('Year', inplace=True)

# Plotting the graph
plt.figure(figsize=(12, 8))
plt.plot(df['Year'], df['Ladder score'], marker='o', linestyle='-', label='Ladder Score')
plt.plot(df['Year'], df['Logged GDP per capita'], marker='o', linestyle='-', label='Logged GDP per capita')
plt.plot(df['Year'], df['Social support'], marker='o', linestyle='-', label='Social Support')

# Adding titles and labels
plt.title('Trend of Happiness and Related Metrics for Finland')
plt.xlabel('Year')
plt.ylabel('Values')
plt.legend()

# Displaying the grid
plt.grid(True)

plt.savefig('finland_detailed_happiness.png')

# Show the plot
plt.show()

