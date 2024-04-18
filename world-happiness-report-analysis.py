# Databricks notebook source
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# COMMAND ----------

spark = SparkSession.builder \
    .appName("HappinessAnalysis") \
    .getOrCreate()

# COMMAND ----------

# MAGIC %md
# MAGIC ###Load Datasets
# MAGIC Load datasets for 2021 - 2024 World Happiness Reports

# COMMAND ----------

df_2024 = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("datasets/2024.csv")
df_2023 = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("datasets/2023.csv")
df_2022 = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("datasets/2022.csv")
df_2021 = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("datasets/2021.csv")
df_2018 = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("datasets/2018.csv")
df_2019 = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("datasets/2019.csv")
df_2020 = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("datasets/2020.csv")
df_2017 = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("datasets/2017.csv")

# COMMAND ----------


# Alter dataset columns for consistency
regional_indicator_data = df_2021.select("Country name", "Regional indicator")

df_2022 = df_2022.withColumnRenamed("Country", "Country name")
df_2022 = df_2022.withColumnRenamed("Happiness score", "Ladder score")
df_2022 = df_2022.withColumnRenamed("Explained by: GDP per capita", "Explained by: Log GDP per capita")
df_2022 = df_2022.withColumnRenamed("Dystopia (1.83) + residual", "Dystopia + residual")

df_2022 = df_2022.join(regional_indicator_data, on="Country name", how="left")
df_2023 = df_2023.join(regional_indicator_data, on="Country name", how="left")
df_2024 = df_2024.join(regional_indicator_data, on="Country name", how="left")

# COMMAND ----------

# MAGIC %md
# MAGIC ###Average of Happiness Scores from 2021-2024

# COMMAND ----------

common_columns = set(df_2017.columns) & set(df_2018.columns) & set(df_2019.columns) & set(df_2020.columns) & set(df_2021.columns) & set(df_2022.columns) & set(df_2023.columns) & set(df_2024.columns)

df_2017_common = df_2017.select(*common_columns)
df_2018_common = df_2018.select(*common_columns)
df_2019_common = df_2019.select(*common_columns)
df_2020_common = df_2020.select(*common_columns)
df_2021_common = df_2021.select(*common_columns)
df_2022_common = df_2022.select(*common_columns)
df_2023_common = df_2023.select(*common_columns)
df_2024_common = df_2024.select(*common_columns)

all_data = df_2017_common.union(df_2018_common).union(df_2019_common).union(df_2020_common).union(df_2021_common).union(df_2022_common).union(df_2023_common).union(df_2024_common)
all_data = all_data.withColumn("Country name", F.when(all_data["Country name"] == "Russia", "Russian Federation").otherwise(all_data["Country name"]))

country_happiness = all_data.groupBy("Country name").agg(F.avg("Ladder score").alias("Average Happiness Score"))

country_happiness.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ###Extent to which each of the six factors affected the overall happiness score based on region

# COMMAND ----------

common_columns = set(df_2021.columns) & set(df_2022.columns) & set(df_2023.columns) & set(df_2024.columns)

df_2021_common = df_2021.select(*common_columns)
df_2022_common = df_2022.select(*common_columns)
df_2023_common = df_2023.select(*common_columns)
df_2024_common = df_2024.select(*common_columns)

df_all_years = df_2021_common.union(df_2022_common).union(df_2023_common).union(df_2024_common)

# Calculate the factors for all years
df_factors_all_years = df_all_years.groupBy("Regional indicator").agg(
    F.avg("Explained by: Log GDP per capita").alias("Avg GDP Per Capita"),
    F.avg("Explained by: Social support").alias("Avg Social Support"),
    F.avg("Explained by: Healthy life expectancy").alias("Avg Healthy Life Expectancy"),
    F.avg("Explained by: Freedom to make life choices").alias("Avg Freedom to Make Life Choices"),
    F.avg("Explained by: Generosity").alias("Avg Generosity"),
    F.avg("Explained by: Perceptions of corruption").alias("Avg Perceptions of Corruption"),
    F.avg("Dystopia + residual").alias("Avg Dystopia + Residual")
)

# Calculate the total happiness score for all years
df_factors_all_years = df_factors_all_years.withColumn(
    "Total Happiness Score",
    F.col("Avg GDP Per Capita") +
    F.col("Avg Social Support") +
    F.col("Avg Healthy Life Expectancy") +
    F.col("Avg Freedom to Make Life Choices") +
    F.col("Avg Generosity") +
    F.col("Avg Perceptions of Corruption") +
    F.col("Avg Dystopia + Residual")
)

# Calculate the percentage contribution of each factor to the total happiness score for all years
df_factors_all_years_percentage = df_factors_all_years.select(
    "Regional indicator",
    (F.col("Avg GDP Per Capita") / F.col("Total Happiness Score") * 100).alias("GDP Per Capita"),
    (F.col("Avg Social Support") / F.col("Total Happiness Score") * 100).alias("Social Support"),
    (F.col("Avg Healthy Life Expectancy") / F.col("Total Happiness Score") * 100).alias("Healthy Life Expectancy"),
    (F.col("Avg Freedom to Make Life Choices") / F.col("Total Happiness Score") * 100).alias("Freedom to Make Life Choices"),
    (F.col("Avg Generosity") / F.col("Total Happiness Score") * 100).alias("Generosity"),
    (F.col("Avg Perceptions of Corruption") / F.col("Total Happiness Score") * 100).alias("Perceptions of Corruption"),
    (F.col("Avg Dystopia + Residual") / F.col("Total Happiness Score") * 100).alias("Dystopia + Residual")
)

df_factors_all_years_percentage.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ###Calculating the Highest and Lowest Happiness Score by Region

# COMMAND ----------

def highest_lowest_by_region(df, year):
    grouped_df = df.groupBy("Regional indicator")
    
    # Find the country with the highest and lowest happiness score within each region
    highest_happiness = grouped_df.agg(F.max("Ladder score").alias("Highest Happiness Score"))
    lowest_happiness = grouped_df.agg(F.min("Ladder score").alias("Lowest Happiness Score"))
    
    highest_df = highest_happiness.join(df, (highest_happiness["Regional indicator"] == df["Regional indicator"]) & (highest_happiness["Highest Happiness Score"] == df["Ladder score"]), "inner").select(highest_happiness["Regional indicator"], "Country name", "Highest Happiness Score")

    lowest_df = lowest_happiness.join(df, (lowest_happiness["Regional indicator"] == df["Regional indicator"]) & (lowest_happiness["Lowest Happiness Score"] == df["Ladder score"]), "inner").select(lowest_happiness["Regional indicator"], "Country name", "Lowest Happiness Score")

    highest_df.show()
    lowest_df.show()
    
print("2021")
highest_lowest_by_region(df_2021, 2021)
print("2022")
highest_lowest_by_region(df_2022, 2022)
print("2023")
highest_lowest_by_region(df_2023, 2023)
print("2024")
highest_lowest_by_region(df_2024, 2024)

# COMMAND ----------

# MAGIC %md
# MAGIC
