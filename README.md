# World Happiness Report Analysis

This repository contains the code for analyzing the World Happiness Report datasets using Apache Spark.
The instructions on the main branch are for running Spark jobs straight from the VM while the other branch is for Databricks

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
   sudo apt install default-jdk -y
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
   * Open profile settings
   ```
   sudo nano ~/.bashrc
   ```
   * Add the following lines to the end of the file
   ```
   export SPARK_HOME=/opt/spark
   export PATH=$PATH:$SPARK_HOME/bin
   ```
   * Source your profile to apply the changes:
   ```
   source ~/.bashrc
   ```
### 8. Install Python Dependencies:
   ```
   sudo apt-get install python3-pip -y
   pip3 install pyspark
   ```
   
## Downloading and Running the Scripts
   * You will need Matplotlib installed to run some of the scripts
   ```
   pip3 install pandas matplotlib
   ```
### 1. Download the files from this repository and transfer them to the VM

### 2. Using FileZilla to transfer the files
   * Open FileZilla > File > Site Manager
   * Click new site
   * For protocol select SFTP - SSH ...
   * Port: 22
   * For the host: paste the Public IP address of your VM here
   * For Logon type: However you sign into the VM (I used Key)
   * User: Username of your VM
   * If you are using Key for Logon type, in the Key file section browse to where the key is located
   * Click connect
   * Move files from folders titles "Spark_scripts" and "Python_graph_scripts"
   * The files in the results folder is what you will get after running the scripts so do not move them to the VM
   * I separated the files into folders for convenience, but in the VM, make sure they are all in the same root directory
### 3. Run the Spark Scripts:
   * Each script may need to be run slightly differently
   * For corr_h_l.py:
   * Open the file using vim or another editor
   ```
   vim corr_h_l.py
   ```
   * You will need to change the paths to match your directories
   * Change the path df = spark.read.csv('/home/Muhammed/WorldHappiness2021.csv', header=True, inferSchema=True) to your own path (you may just need to change Muhammed to your VM username)
   * Change the path correlation_df.to_csv('/home/Muhammed/total_correlation_matrix.csv') to your own path
   * You can then run the script
   ```
   spark-submit corr_h_l.py
   ```
   * You should see the matrix in the terminal
   ```
   ls -l
   ```
   * You should now see a file called "total_correlation_matrix.csv"
   * Using FileZilla you can go to site manager and connect to the VM once again without having to input all the details again
   * You can then transfer the file to your local machine and view it

   * For exclusive_highest_lowest.py:
   * Once again you will have to open the file, find the two lines and change the path to match yours
   ```
   spark-submit exclusive_highest_lowest.py
   ```
   * You will have a file called "exclusive_countries_highest_lowest_ladder_score.csv" that you can transfer to your local machine and view

   * For finland_happiness.py:
   * Open the file and find the line: base_directory = '/home/Muhammed/'
   * Change the base directory to match your own where all the data is located (You may just need to change Muhammed to your VM username)
   ```
   spark-submit finland_happiness.py
   ```
   * You will now have a file called "finland_happiness_scores.csv"
   * You MUST concatenate this file before being able to use it to make a graph
   ```
   cat /home/{YourVMUsername}/finland_happiness_scores.csv/part-*.csv > /home/{YourVMUsername}/combined_finland_happiness_scores.csv
   ```
   ```
   python3 visualize_finland_happiness.py
   ```
  * You will now have a file called "finland_happiness.png" that can be transferred to your local machine and viewed
  * Note that in the concatenation of the file, the name of the csv file was changed. This may need to be done for some of the other python graphing scripts to match the correct .csv file they are reading from.

  * The rest of the Spark files can be run in the same way
  * spark-submit <name_of_file>.py
  * And for graphing: python3 <name_of_file>.py
  * One note about the Python_graph_scripts files: These files may use a different named .csv file than the one you created from running the spark scripts. You will need to concatenate the .csv files and name them to match the files that the python graph scripts are reading from.
  * If this is not done properly, you may get an error. This is because running the spark script creates a csv file that is split in multiple parts. It needs to be concatenated, however, when concatenating I may have changed the name of some of the files and then used them in the python graphing scripts. Just make sure the name of the concatenated file matches the name of the file used in the python graphing scripts.
