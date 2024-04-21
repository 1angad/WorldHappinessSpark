from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Initialize Spark session
spark = SparkSession.builder.appName("MyApp").getOrCreate()

# Read the data
df = spark.read.csv('/home/Muhammed/WorldHappiness2021.csv', header=True, inferSchema=True)

# Define a window partitioned by "Regional indicator", ordered by "Ladder score"
windowSpec = Window.partitionBy("Regional indicator").orderBy("Ladder score")

# Add rank columns for highest and lowest ladder score
df = df.withColumn("rank_asc", F.rank().over(windowSpec)) \
       .withColumn("rank_desc", F.rank().over(windowSpec.orderBy(F.col("Ladder score").desc())))

# Filter for the countries with the highest and lowest ladder score in their region
highest_ladder_score = df.filter(F.col("rank_asc") == 1).select("Country name", "Regional indicator", "Ladder score").withColumnRenamed("Ladder score", "Highest Ladder Score")
lowest_ladder_score = df.filter(F.col("rank_desc") == 1).select("Country name", "Regional indicator", "Ladder score").withColumnRenamed("Ladder score", "Lowest Ladder Score")

# Join the highest and lowest ladder scores on "Regional indicator"
combined = highest_ladder_score.join(lowest_ladder_score, "Regional indicator")\
                               .select(highest_ladder_score["Regional indicator"],
                                       F.col("Country name").alias("Country with Highest Score"),
                                       "Highest Ladder Score",
                                       lowest_ladder_score["Country name"].alias("Country with Lowest Score"),
                                       "Lowest Ladder Score")

# Display the result
combined.show()

# Optionally, write the result to a new CSV
combined.write.csv('/home/Muhammed/exclusive_countries_highest_lowest_ladder_score.csv', header=True, mode="overwrite")

# Stop Spark session
spark.stop()

