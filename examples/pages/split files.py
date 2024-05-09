import streamlit as st
import pandas as pd
import math

# Function to calculate file size
def get_file_size(file_path):
    file_info = st.file_uploader("Upload file", type=["xlsx", "csv"])
    if file_info is not None:
        return len(file_info.getvalue()), file_info.size
    else:
        return None, None

# Function to split DataFrame and write to files
def split_and_write_files(df, num_rows, file_size, num_files):
    if num_files is not None:
        size_per_file = math.ceil(num_rows / num_files)
        st.write(f"Splitting file into {num_files} files with approximately {size_per_file} rows each.")
        for i in range(num_files):
            start_index = i * size_per_file
            end_index = min((i + 1) * size_per_file, num_rows)
            split_df = df.iloc[start_index:end_index]
            split_df.to_excel(f"split_file_{i+1}.xlsx", index=False)
        st.write("Files split successfully.")
    elif file_size is not None:
        num_files = math.ceil(file_size / file_size_per_file)
        st.write(f"Splitting file into {num_files} files with approximately {file_size_per_file} rows each.")
        for i in range(num_files):
            start_index = i * file_size_per_file
            end_index = min((i + 1) * file_size_per_file, num_rows)
            split_df = df.iloc[start_index:end_index]
            split_df.to_excel(f"split_file_{i+1}.xlsx", index=False)
        st.write("Files split successfully.")

# Main function
def main():
    st.title("Split Excel or CSV File")

    # Upload file and display file info
    st.write("Upload your Excel or CSV file.")
    num_rows, file_size = get_file_size("input_file")
    if num_rows is not None and file_size is not None:
        st.write(f"Number of rows: {num_rows}")
        st.write(f"Size of file: {file_size} bytes")

    # Choose split method
    st.write("Choose how you want to split the file:")
    split_option = st.radio("Split by:", ("File Size", "Number of Files"))

    if split_option == "File Size":
        num_files = None
        file_size_per_file = st.slider("Choose size per file (rows):", min_value=1, max_value=num_rows)
    else:
        file_size_per_file = None
        num_files = st.slider("Choose number of files:", min_value=1, max_value=num_rows)

    # Split and write files
    if st.button("Split File"):
        if num_rows is not None:
            file_info = st.file_uploader("Upload file", type=["xlsx", "csv"])
            if file_info is not None:
                if file_info.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                    df = pd.read_excel(file_info)
                elif file_info.type == "text/csv":
                    df = pd.read_csv(file_info)
                split_and_write_files(df, num_rows, file_size, num_files)

if __name__ == "__main__":
    main()
