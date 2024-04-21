from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Initialize Spark session
spark = SparkSession.builder.appName("MyApp").getOrCreate()

# Read the data
df = spark.read.csv('/home/Muhammed/WorldHappiness2021.csv', header=True, inferSchema=True)

# Aggregate data
regional_happiness2021 = df.groupBy("Regional indicator") \
                           .agg(F.avg("Ladder score").alias("average_happiness"))

# Display the result
regional_happiness2021.show()

# Write the aggregated data to a new CSV file
regional_happiness2021.write.csv('/home/Muhammed/regional_happiness2021.csv', header=True, mode="overwrite")

# Stop Spark session
spark.stop()

