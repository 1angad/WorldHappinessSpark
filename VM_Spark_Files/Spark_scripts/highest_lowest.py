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
highest_ladder_score = df.filter(F.col("rank_asc") == 1).withColumn("Score Type", F.lit("Highest"))
lowest_ladder_score = df.filter(F.col("rank_desc") == 1).withColumn("Score Type", F.lit("Lowest"))

# Combine highest and lowest ladder score countries into one DataFrame
combined_highest_lowest = highest_ladder_score.unionByName(lowest_ladder_score)

# Optionally, you can select specific columns to display or write to CSV if you want a clearer view.
# For example, to select and rename certain columns, you might do something like this:
# combined_select = combined.select("Regional indicator", "Country name", "Ladder score", "Score Type")

# Optionally, write the combined data to a new CSV
combined_highest_lowest.write.csv('/home/Muhammed/countries_highest_lowest_ladder_score_full.csv', header=True, mode="overwrite")

# Stop Spark session
spark.stop()

