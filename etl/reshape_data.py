import pandas as pd
import numpy as np

def reshape_crop_data_final_fix():
    """
    This script loads the ICRISAT dataset and uses the robust 'melt' and 'pivot_table'
    method to correctly reshape the data into the final "long" format.
    """
    print("--- Loading New Dataset ---")
    try:
        df = pd.read_csv("ICRISAT-District Level Data-Big.csv", encoding='latin1')
        print("Successfully loaded ICRISAT-District Level Data-Big.csv")
    except FileNotFoundError:
        print("Error: Make sure 'ICRISAT-District Level Data-Big.csv' is in the same folder.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # Filter for Odisha (named 'Orissa')
    df_odisha = df[df['State Name'] == 'Orissa'].copy()
    
    # --- Standardize Column Names (same as before) ---
    print("\n--- Standardizing Column Names ---")
    df_odisha.rename(columns={'Dist Name': 'District'}, inplace=True)
    
    new_cols = {}
    for col in df_odisha.columns:
        if ' AREA (' in col:
            crop_name = col.split(' AREA (')[0].strip()
            new_cols[col] = f"{crop_name}_AREA"
        elif ' YIELD (' in col:
            crop_name = col.split(' YIELD (')[0].strip()
            new_cols[col] = f"{crop_name}_YIELD"
        elif ' PRODUCTION (' in col:
            crop_name = col.split(' PRODUCTION (')[0].strip()
            new_cols[col] = f"{crop_name}_PROD"
            
    df_odisha.rename(columns=new_cols, inplace=True)
    print("Column names standardized successfully.")

    # --- Reshape Data using Melt and Pivot (THE CORE FIX) ---
    print("--- Reshaping Data using Melt and Pivot ---")
    
    # 1. Melt the DataFrame
    id_vars = ['District', 'Year']
    value_vars = [col for col in df_odisha.columns if '_' in col] # All the crop columns we created
    
    df_melted = df_odisha.melt(
        id_vars=id_vars,
        value_vars=value_vars,
        var_name='Crop_Metric',
        value_name='Value'
    )
    
    # 2. Split the 'Crop_Metric' column into 'Crop Type' and 'Metric'
    # 'RICE_AREA' becomes 'RICE' and 'AREA'
    df_melted[['Crop Type', 'Metric']] = df_melted['Crop_Metric'].str.rsplit('_', n=1, expand=True)

    # 3. Pivot the table to create separate AREA, YIELD, PROD columns
    df_pivoted = df_melted.pivot_table(
        index=['District', 'Year', 'Crop Type'],
        columns='Metric',
        values='Value',
        aggfunc='first' # Use 'first' as there's only one value per group
    ).reset_index()

    print("Reshaping complete.")

    # --- Final Cleaning ---
    print("\n--- Cleaning Final Dataset ---")
    # Convert data columns to numeric types
    df_pivoted['AREA'] = pd.to_numeric(df_pivoted['AREA'], errors='coerce')
    df_pivoted['YIELD'] = pd.to_numeric(df_pivoted['YIELD'], errors='coerce')
    print("Converted AREA and YIELD columns to numeric types.")

    # Drop rows with zero or NaN in area or yield
    df_pivoted.replace(0, np.nan, inplace=True)
    df_pivoted.dropna(subset=['AREA', 'YIELD'], inplace=True)
    print("Dropped rows with invalid AREA or YIELD.")

    # Reorder and select final columns
    final_df = df_pivoted[['Crop Type', 'District', 'Year', 'AREA', 'YIELD']]
    final_df = final_df.sort_values(by=['District', 'Year', 'Crop Type']).reset_index(drop=True)
    
    # Save the final, clean dataset
    output_filename = "reshaped_crop_data.csv"
    final_df.to_csv(output_filename, index=False)
    
    print(f"\nSuccessfully created the reshaped dataset!")
    print(f"==> Check for the output file: '{output_filename}' <==")
    
    if final_df.empty:
        print("\nWARNING: The final DataFrame is still empty. Please double check the source file's column naming conventions.")
    else:
        print("\n--- Final Reshaped DataFrame (First 5 Rows) ---")
        print(final_df.head())


if __name__ == '__main__':
    reshape_crop_data_final_fix()