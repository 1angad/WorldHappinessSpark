from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.stat import Correlation
import pandas as pd

# Initialize Spark session
spark = SparkSession.builder.appName("LowestScoresCorrelation").getOrCreate()

# Read the data
df = spark.read.csv('/home/Muhammed/countries_highest_lowest_ladder_score.csv', header=True, inferSchema=True)

# Filter for countries with the lowest scores
lowest_scores_df = df.filter(df['Score Type'] == 'Lowest')

# Remove rows with any null values in the columns of interest
columns_of_interest = ["Ladder score", "Logged GDP per capita", "Social support", "Healthy life expectancy", "Freedom to make life choices", "Generosity", "Perceptions of corruption"]
lowest_scores_df = lowest_scores_df.dropna(subset=columns_of_interest)

# Use VectorAssembler to combine the selected columns into a single vector column
vectorAssembler = VectorAssembler(inputCols=columns_of_interest, outputCol="features")
df_vector = vectorAssembler.transform(lowest_scores_df)

# Compute Pearson correlation matrix
correlation_matrix = Correlation.corr(df_vector, "features").collect()[0][0]

# Convert to Pandas DataFrame for easy handling and visualization
correlation_df = pd.DataFrame(correlation_matrix.toArray(), index=columns_of_interest, columns=columns_of_interest)

# Round the correlation coefficients to 2 decimal places
correlation_df = correlation_df.round(2)

print("Correlation matrix for countries with the lowest scores:")
print(correlation_df)

# Save the Pandas DataFrame to a CSV file
correlation_df.to_csv('/home/Muhammed/lowest_scores_correlation_matrix.csv')

# Stop Spark session
spark.stop()

