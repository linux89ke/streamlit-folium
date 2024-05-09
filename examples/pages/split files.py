import pandas as pd
import math

# Function to calculate file size
def get_file_size(file_path):
    file_info = st.file_uploader("Upload file", type=["xlsx", "csv"])
    if file_info is not None:
        num_rows = len(file_info.getvalue())
        file_size = file_info.size
        return num_rows, file_size
    else:
        return None, None

# Function to split DataFrame and write to files
def split_and_write_files(df, num_rows, split_option, size_per_file, num_files):
    if split_option == "File Size":
        num_files = None
        size_per_file = size_per_file * 1024 * 1024  # Convert MB to bytes
        st.write(f"Splitting file into {math.ceil(num_rows / (size_per_file / 1024))} files with approximately {size_per_file} bytes each.")
        for i in range(math.ceil(num_rows / (size_per_file / 1024))):
            start_index = i * (size_per_file / 1024)
            end_index = min((i + 1) * (size_per_file / 1024), num_rows)
            split_df = df.iloc[int(start_index):int(end_index)]
            split_df.to_excel(f"split_file_{i+1}.xlsx", index=False)
        st.write("Files split successfully.")
    else:
        size_per_file = None
        st.write(f"Splitting file into {num_files} files.")
        for i in range(num_files):
            start_index = i * (num_rows // num_files)
            end_index = min((i + 1) * (num_rows // num_files), num_rows)
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
        st.write(f"Size of file: {file_size / 1024:.2f} KB")

    # Choose split method
    st.write("Choose how you want to split the file:")
    split_option = st.radio("Split by:", ("File Size", "Number of Files"))

    if split_option == "File Size":
        num_files = None
        if file_size is not None:
            max_mb = file_size / (1024 * 1024)
        else:
            max_mb = 200  # Default maximum value if file size is unknown
        size_per_file = st.slider("Choose size per file (MB):", min_value=1, max_value=max_mb, step=1, value=200)
    else:
        size_per_file = None
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
                split_and_write_files(df, num_rows, split_option, size_per_file, num_files)

if __name__ == "__main__":
    main()
ChatGPT
