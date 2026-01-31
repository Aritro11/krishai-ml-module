import pandas as pd

# --- Configuration ---
# The name of the file you downloaded from ICRISAT
input_filename = 'ICRISAT-District Level Data Rainfall Data.csv'
# The name of the new file that will be created
output_filename = 'odisha_yearly_annual_rainfall.csv'


# --- Main Script ---
try:
    # Step 1: Read the original dataset
    print(f"Reading data from '{input_filename}'...")
    df = pd.read_csv(input_filename)

    # Step 2: Select the columns we need for the final output
    # We use .copy() to ensure we are working with a new dataframe
    result_df = df[['Year', 'Dist Name', 'ANNUAL RAINFALL (Millimeters)']].copy()

    # Step 3: Rename the columns for clarity and consistency
    result_df.rename(columns={
        'Dist Name': 'District',
        'ANNUAL RAINFALL (Millimeters)': 'Annual_Rainfall_mm'
    }, inplace=True)

    # Step 4: Save the newly formatted data to a CSV file
    result_df.to_csv(output_filename, index=False)

    print(f"\nSuccess! Processed data has been saved to '{output_filename}'")
    print("\nHere is a preview of the first 5 rows of your new file:")
    print(result_df.head())

except FileNotFoundError:
    print(f"\nError: The file '{input_filename}' was not found in this directory.")
    print("Please make sure the script and the CSV file are in the same folder.")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")