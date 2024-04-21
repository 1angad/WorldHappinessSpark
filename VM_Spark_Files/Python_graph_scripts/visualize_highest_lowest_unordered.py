import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('/home/Muhammed/countries_highest_lowest_ladder_score.csv')

# Assuming your DataFrame 'df' has "Regional indicator", "Ladder score", and "Score Type"
# where "Score Type" indicates "Highest" or "Lowest"

# Filter out the highest and lowest scores into separate DataFrames
highest_scores = df[df['Score Type'] == 'Highest']
lowest_scores = df[df['Score Type'] == 'Lowest']

highest_scores['Ladder score'] = pd.to_numeric(highest_scores['Ladder score'])
lowest_scores['Ladder score'] = pd.to_numeric(lowest_scores['Ladder score'])

# Plotting
plt.figure(figsize=(14, 8))

# Set the width of the bars
bar_width = 0.35

# Set positions of the bars on the x-axis
r1 = range(len(highest_scores))
r2 = [x + bar_width for x in r1]

# Make the plot
plt.bar(r1, highest_scores['Ladder score'], color='r', width=bar_width, edgecolor='grey', label='Highest Score')
plt.bar(r2, lowest_scores['Ladder score'], color='b', width=bar_width, edgecolor='grey', label='Lowest Score')

# Add labels to the plot
plt.xlabel('Region', fontweight='bold', fontsize=15)
plt.ylabel('Ladder Score', fontweight='bold', fontsize=15)
plt.xticks([r + bar_width/2 for r in range(len(highest_scores))], highest_scores['Regional indicator'], rotation=45, ha='right')
plt.title('Highest and Lowest Happiness Scores by Region')
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()
plt.savefig('highest_lowest_unordered.png')
