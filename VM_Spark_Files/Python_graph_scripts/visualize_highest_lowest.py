import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('/home/Muhammed/countries_highest_lowest_ladder_score.csv')

# Assuming your DataFrame 'df' has the following columns:
# "Regional indicator", "Country name", "Ladder score", and "Score Type"
# where "Score Type" distinguishes between "Highest" and "Lowest"

# Filter out the highest and lowest scores into separate DataFrames
highest_scores = df[df['Score Type'] == 'Highest']
lowest_scores = df[df['Score Type'] == 'Lowest']

# Ensure the order of regions is consistent for plotting
regions = highest_scores['Regional indicator'].unique()
highest_scores = highest_scores.set_index('Regional indicator').reindex(index=regions).reset_index()
lowest_scores = lowest_scores.set_index('Regional indicator').reindex(index=regions).reset_index()

# Plotting
plt.figure(figsize=(14, 8))

# Set the width of the bars
bar_width = 0.35

# Set the positions of the bars on the x-axis
r1 = range(len(highest_scores))
r2 = [x + bar_width for x in r1]

# Make the plot
plt.bar(r1, highest_scores['Ladder score'], color='b', width=bar_width, edgecolor='grey', label='Highest Score')
plt.bar(r2, lowest_scores['Ladder score'], color='r', width=bar_width, edgecolor='grey', label='Lowest Score')

# Add labels to the plot
plt.xlabel('Region', fontweight='bold', fontsize=15)
plt.ylabel('Ladder Score', fontweight='bold', fontsize=15)
plt.xticks([r + bar_width/2 for r in range(len(highest_scores))], highest_scores['Regional indicator'], rotation=45, ha='right')
plt.title('Highest and Lowest Happiness Scores by Region')
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()
plt.savefig('highest_lowest.png')
