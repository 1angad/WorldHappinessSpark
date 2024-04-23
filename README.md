# World Happiness Report Analysis

This repository contains the code for analyzing the World Happiness Report datasets using Databricks. To run the code using an Azure VM, follow the instructions in the main branch's README.

## Setting Up Azure Databricks
### 1. Clone the Repository
  ```
   git clone git@github.com:1angad/WorldHappinessSpark.git
   git checkout analysis-kd
  ```
### 2. Azure Setup
  * Log in to the [Azure portal](https://azure.microsoft.com/en-us/get-started/azure-portal)
  * Click on "Create a resource" and search for "Azure Databricks"
  * Select desired options for the Azure Databricks workspace and click "Review + create" then "Create"
  * Launch the Workspace
### 3. Workspace Setup
* Navigate to "Compute" to create a new Cluster
* Select desired options for your cluster and click "Create compute"
### 4. Upload Datasets and Python script
* Navigate to "Workspace," select the three dots, and select "Import" to import the ```factor_influence_and_average_happiness.py``` script and create a new notebook
* Navigate to File > Upload data to DBFS and upload the dataset CSV files located in the 'datasets' folder of the repository
* Update the paths for loading the dataset to match the paths for the datasets uploaded in the Databricks File System
### 5. Running the Script
* At the top of the notebook, select Run all to run all cells
* Uncomment lines with "Display" function to view data visualizations
