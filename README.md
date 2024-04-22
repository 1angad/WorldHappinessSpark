# World Happiness Report Analysis

This repository contains the code for analyzing the World Happiness Report datasets using Apache Spark.

## Setting Up Spark on Azure VM
### 1. Create an Azure VM
   * Log in to the [Azure portal](https://azure.microsoft.com/en-us/get-started/azure-portal)
   * Click on "Virtual machines" then click "Create"
   * Select desired options for your VM then click "Review + create" to provision the VM
### 2. Connect to the Azure VM:
   * Once the VM is created, connect to it using SSH
### 3. Update the System Packages:
   ```
   sudo apt update
   ```
### 4. Install Java Development Kit:
   ```
   sudo apt install default-jre default-jdk
   ```
### 5. Download and Extract Spark
   ```
   wget https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz
   tar -xzvf spark-3.5.1-bin-hadoop3.tgz
   ```
### 6. Move Spark Directory to /opt
   ```
   sudo mv spark-3.5.1-bin-hadoop3 /opt/spark
   ```
### 7. Set Environment Variables:
   ```
   export SPARK_HOME=/opt/spark
   export PATH=$PATH:$SPARK_HOME/bin
   ```
### 8. Install Python Dependencies:
   ```
   sudo apt-get install python3-pip -y
   pip3 install pyspark
   ```

## Cloning the Repository and Running the Script
### 1. Clone the Repository
   ```
   git clone git@github.com:1angad/WorldHappinessSpark.git
   ```
### 2. Navigate to the Repository
   ```
   cd WorldHappinessSpark
   ```
### 3. Run the Python Script:
   ```
   python3 <script-name>.py
   ```
