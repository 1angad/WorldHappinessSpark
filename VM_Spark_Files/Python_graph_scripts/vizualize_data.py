import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('/home/Muhammed/combined_regional_happiness.csv')

# Visualize the data
plt.figure(figsize=(12, 8))
bars = plt.bar(df['Regional indicator'], df['average_happiness'])
plt.xlabel('Regional Indicator')
plt.ylabel('Average Happiness')
plt.title('Average Happiness by Regional Indicator')
plt.xticks(rotation=45, ha="right")  # Rotate for readability and adjust alignment

# Increase the gap in the x-axis between bars for readability
plt.gcf().subplots_adjust(bottom=0.15)

plt.savefig('regional_happiness2021.png')

