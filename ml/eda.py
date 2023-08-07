import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

# Load the dataset from the .txt file
file_path = './data/fire/NFDB_point_20220901.txt'
data = pd.read_csv(file_path, sep=',')

# Display basic information about the dataset
print(data.head())
print()
print(data.info())
print()
print(data.describe())
print()

# Replace missing values with NaN
data.replace({'': np.nan, ' ': np.nan}, inplace=True)  # Replace empty strings and spaces with NaN

# Create a string to store basic information
basic_info = ""

# Append basic information to the string
basic_info += "Head of the dataset:\n" + str(data.head()) + "\n\n"
basic_info += "Info of the dataset:\n" + str(data.info()) + "\n\n"
basic_info += "Description of the dataset:\n" + str(data.describe()) + "\n\n"
basic_info += "Missing values count:\n" + str(data.isnull().sum()) + "\n\n"

# Save the basic information to a text file
with open('./eda/eda.txt', 'a') as file:
    file.write(basic_info)

# Check for missing values
print('\nnull values:\n', data.isnull().sum())

# Create a histogram of fire sizes with a log-transformed y-axis
plt.figure(figsize=(10, 6))
n, bins, _ = plt.hist(data['SIZE_HA'], bins=50, alpha=0.6)
plt.yscale('log')  # Apply log scale to the y-axis
plt.xlabel('Fire Size (Hectares)')
plt.ylabel('Frequency (log scale)')
plt.title('Histogram of Fire Sizes (Log Transformed)')
plt.savefig('./eda/Histogram of Fire Sizes.png')
plt.show()

# Explore causes of fire
plt.figure(figsize=(12, 6))
cause_order = data['CAUSE'].value_counts().index
sns.countplot(data=data, x='CAUSE', order=cause_order)
plt.xticks(rotation=45, ha='right')
plt.xlabel('Fire Cause')
plt.yscale('log')  # Apply log scale to the y-axis
plt.ylabel('Count (log scale)')
plt.title('Distribution of Fire Causes (Log Transformed)')
plt.savefig('./eda/Distribution of Fire Causes.png')
plt.show()

# Filter out entries with year -999 and calculate total fire size in hectares over the years
filtered_data = data[data['YEAR'] != -999]
total_size_by_year = filtered_data.groupby('YEAR')['SIZE_HA'].sum()
# Create a line plot of total fire size over the years
plt.figure(figsize=(12, 6))
sns.lineplot(x=total_size_by_year.index, y=total_size_by_year.values)
plt.xlabel('Year')
plt.ylabel('Total Fire Size (Hectares)')
plt.title('Total Fire Size in HA Over the Years (Ignoring -999)')
plt.xticks(rotation=45)
plt.savefig('./eda/Total Fire Sizes in HA Over the Years.png')
plt.show()

# Create a pivot table of fire causes by month
pivot_table = data.pivot_table(index='CAUSE', columns='MONTH', aggfunc='size', fill_value=0)
# Create a heatmap of fire causes by month
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table, cmap='YlGnBu', annot=True, fmt='d')
plt.xlabel('Month')
plt.ylabel('Fire Cause')
plt.title('Fire Causes by Month')
plt.xticks(rotation=45)
plt.savefig('./eda/Fire Causes by Month.png')
plt.show()

# Create a heatmap of correlation between numeric variables
corr_matrix = data.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Heatmap')
plt.savefig('./eda/Correlation Heatmap.png')
plt.show()
