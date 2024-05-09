import pandas as pd

# Load Excel or CSV file into a DataFrame
df = pd.read_excel("input_file.xlsx")  # Replace "input_file.xlsx" with your file name and path

# Split DataFrame based on some condition, for example, based on a column value
split_condition = "column_name"  # Replace "column_name" with the name of the column you want to use for splitting

split_values = df[split_condition].unique()

for value in split_values:
    split_df = df[df[split_condition] == value]
    
    # Write each split DataFrame to a separate Excel or CSV file
    output_file_name = f"{value}_file.xlsx"  # Replace with your desired output file name format
    split_df.to_excel(output_file_name, index=False)  # Change to to_csv if you want CSV files
