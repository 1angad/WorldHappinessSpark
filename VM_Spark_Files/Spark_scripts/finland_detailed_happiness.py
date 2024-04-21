from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, col

# Initialize Spark session
spark = SparkSession.builder.appName("FinlandTrendAnalysis").getOrCreate()

# List of years for which you have data
years = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2023]  # Extend or modify this list according to your actual data

# Base directory where the CSV files are stored
base_directory = '/home/Muhammed/'

# Empty DataFrame to hold all the data for Finland
finland_data_df = None

for year in years:
    # Construct the file path
    file_path = f'{base_directory}WorldHappiness{year}.csv'
    
    # Read the data for the year
    df = spark.read.csv(file_path, header=True, inferSchema=True)
    
    # Filter for Finland and select relevant columns
    finland_df = df.filter(col("Country name") == "Finland") \
                   .select("Country name", "Ladder score", "Logged GDP per capita", "Social support", "Healthy life expectancy") \
                   .withColumn("Year", lit(year))
    
    # Append the data for this year to the main DataFrame
    if finland_data_df is None:
        finland_data_df = finland_df
    else:
        finland_data_df = finland_data_df.union(finland_df)

# Once all data is combined, you can save it to a CSV for visualization
output_path = f'{base_directory}finland_happiness_detailed_scores.csv'
finland_data_df.write.csv(output_path, header=True, mode="overwrite")

# Stop Spark session
spark.stop()

