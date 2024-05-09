import streamlit as st
import pandas as pd
import base64
import io

def merge_excel_files(files):
    # Read the first file to initialize the dataframe
    merged_df = pd.read_excel(files[0], engine='openpyxl')
    
    # Iterate over the remaining files and append them to the merged dataframe
    for file in files[1:]:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file, engine='openpyxl')
        else:
            st.warning(f"Ignored unsupported file format: {file.name}")
            continue
        merged_df = pd.concat([merged_df, df], ignore_index=True)
    
    # Drop duplicate headers
    merged_df = merged_df.drop_duplicates(keep='first')
    
    return merged_df

def main():
    st.title("Excel Files Merger")
    
    # File uploader
    uploaded_files = st.file_uploader("Upload Excel files", type=['csv', 'xlsx'], accept_multiple_files=True)
    
    if uploaded_files:
        st.write("Files to be merged:")
        for file in uploaded_files:
            st.write(file.name)
        
        # Merge files
        merged_df = merge_excel_files(uploaded_files)
        
        # Display merged dataframe
        st.write("Merged DataFrame:")
        st.write(merged_df)
        
        # Export to Excel
        st.markdown(get_download_link(merged_df), unsafe_allow_html=True)

def get_download_link(df):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()  # Close the ExcelWriter object
    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="merged_file.xlsx">Download XLSX File</a>'
    return href

if __name__ == "__main__":
    main()
