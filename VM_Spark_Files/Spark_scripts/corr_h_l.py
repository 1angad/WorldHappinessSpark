from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.stat import Correlation
import pandas as pd

# Initialize Spark session
spark = SparkSession.builder.appName("MultipleCorrelations").getOrCreate()

# Read the data
df = spark.read.csv('/home/Muhammed/WorldHappiness2021.csv', header=True, inferSchema=True)

# Specify the columns of interest and remove rows with any nulls in these columns
columns_of_interest = ["Ladder score", "Logged GDP per capita", "Social support", "Healthy life expectancy", "Freedom to make life choices", "Generosity", "Perceptions of corruption"]
df = df.dropna(subset=columns_of_interest)

# Use VectorAssembler to combine the selected columns into a single vector column
vectorAssembler = VectorAssembler(inputCols=columns_of_interest, outputCol="features")
df_vector = vectorAssembler.transform(df)

# Compute Pearson correlation matrix
correlation_matrix = Correlation.corr(df_vector, "features").collect()[0][0]

# Convert to Pandas DataFrame for easy handling and visualization
# The correlation matrix in Spark is a DenseMatrix, and we can access its values and convert them
correlation_df = pd.DataFrame(correlation_matrix.toArray(), index=columns_of_interest, columns=columns_of_interest)

# Round the correlation coefficients to 2 decimal places
correlation_df = correlation_df.round(2)

print("Correlation matrix:")
print(correlation_df)

# Save the Pandas DataFrame to a CSV file
correlation_df.to_csv('/home/Muhammed/total_correlation_matrix.csv')

# Stop Spark session
spark.stop()

