import pandas as pd
import numpy as np

def calculate_pet(temp_df, lat_df):
    """
    Calculates monthly Potential Evapotranspiration (PET) using the Thornthwaite equation.
    """
    # Merge latitude data
    df = pd.merge(temp_df, lat_df, on='District')

    # Ensure temperature is above 0 for the formula
    df['Mean_Temperature_C'] = df['Mean_Temperature_C'].clip(lower=0)

    # Calculate monthly heat index 'i'
    df['monthly_i'] = (df['Mean_Temperature_C'] / 5) ** 1.514

    # Calculate annual heat index 'I' for each year and district
    annual_I = df.groupby(['Year', 'District'])['monthly_i'].sum().reset_index()
    annual_I.rename(columns={'monthly_i': 'annual_I'}, inplace=True)

    # Merge annual_I back to the monthly data
    df = pd.merge(df, annual_I, on=['Year', 'District'])

    # Calculate exponent 'a' based on the annual heat index
    I = df['annual_I']
    a = (6.75e-7 * I**3) - (7.71e-5 * I**2) + (1.792e-2 * I) + 0.49239
    df['exponent_a'] = a

    # Calculate unadjusted PET
    # Replace I=0 with NaN to avoid division by zero errors, then handle NaNs
    df['unadjusted_pet'] = 16 * (10 * df['Mean_Temperature_C'] / df['annual_I'].replace(0, np.nan)) ** df['exponent_a']

    # Daylight/Latitude Correction Factors for 20 deg N Latitude (representative for Odisha)
    correction_factors = {
        1: 0.87, 2: 0.89, 3: 1.03, 4: 1.12, 5: 1.20, 6: 1.18,
        7: 1.20, 8: 1.15, 9: 1.05, 10: 0.98, 11: 0.89, 12: 0.85
    }
    df['correction_factor'] = df['Month_Num'].map(correction_factors)

    # Calculate final monthly PET in mm (original formula is in cm)
    df['PET_mm'] = df['unadjusted_pet'] * df['correction_factor'] * 10 

    return df[['Year', 'Month_Num', 'District', 'PET_mm']]

# --- Main Script ---
try:
    print("Loading datasets...")
    temp_df = pd.read_csv("odisha_monthly_temperature_1993_2017_synthetic.csv")
    rainfall_df = pd.read_csv("Rainfall.csv")

    # Latitude Data for Odisha Districts (approximate center)
    latitudes = {
        'District': ['Angul', 'Balasore', 'Bargarh', 'Bhadrak', 'Bolangir', 'Boudh', 'Cuttack',
                     'Deogarh', 'Dhenkanal', 'Gajapati', 'Ganjam', 'Jagatsinghpur', 'Jajpur',
                     'Jharsuguda', 'Kalahandi', 'Kandhamal', 'Kendrapara', 'Keonjhar', 'Khordha',
                     'Koraput', 'Malkangiri', 'Mayurbhanj', 'Nabarangpur', 'Nayagarh', 'Nuapada',
                     'Puri', 'Rayagada', 'Sambalpur', 'Sonepur', 'Sundargarh'],
        'Latitude': [20.83, 21.49, 21.33, 21.06, 20.72, 20.84, 20.47, 21.53, 20.66, 19.10,
                     19.46, 20.27, 20.84, 21.90, 19.90, 20.55, 20.50, 21.65, 20.26, 18.81,
                     18.35, 21.92, 19.23, 20.26, 20.82, 19.81, 19.29, 21.47, 21.08, 22.09]
    }
    lat_df = pd.DataFrame(latitudes)

    print("Calculating monthly Potential Evapotranspiration (PET)...")
    pet_df = calculate_pet(temp_df, lat_df)

    print("Aggregating PET to seasonal values for the Kharif season...")
    # Sowing: June (Month 6)
    # Peak: July, August (Months 7, 8)
    # Flowering: September (Month 9)
    pet_sowing = pet_df[pet_df['Month_Num'] == 6].rename(columns={'PET_mm': 'PET_Sowing_Kharif'})
    pet_peak = pet_df[pet_df['Month_Num'].isin([7, 8])].groupby(['Year', 'District'])['PET_mm'].sum().reset_index().rename(columns={'PET_mm': 'PET_Peak_Kharif'})
    pet_flowering = pet_df[pet_df['Month_Num'] == 9].rename(columns={'PET_mm': 'PET_Flowering_Kharif'})
    
    # Merge seasonal PET data into a single dataframe
    seasonal_pet_df = pd.merge(pet_sowing[['Year', 'District', 'PET_Sowing_Kharif']], pet_peak, on=['Year', 'District'])
    seasonal_pet_df = pd.merge(seasonal_pet_df, pet_flowering[['Year', 'District', 'PET_Flowering_Kharif']], on=['Year', 'District'])

    print("Merging seasonal PET with rainfall data...")
    final_df = pd.merge(rainfall_df, seasonal_pet_df, on=['Year', 'District'], how='left')

    print("Calculating final Water Deficit columns...")
    final_df['Water_Deficit_Sowing_Kharif'] = final_df['PET_Sowing_Kharif'] - final_df['Rainfall_Sowing_Kharif']
    final_df['Water_Deficit_Peak_Kharif'] = final_df['PET_Peak_Kharif'] - final_df['Rainfall_Peak_Kharif']
    final_df['Water_Deficit_Flowering_Kharif'] = final_df['PET_Flowering_Kharif'] - final_df['Rainfall_Flowering_Kharif']
    
    # Fill any potential NaNs that might result from merges
    final_df.fillna(0, inplace=True)

    output_filename = 'rainfall_with_water_deficit.csv'
    final_df.to_csv(output_filename, index=False)
    
    print(f"\nSuccess! The final dataset has been saved as '{output_filename}'")
    print("Here is a preview:")
    print(final_df.head())

except FileNotFoundError as e:
    print(f"\nError: A required file was not found. Details: {e}")
    print("Please make sure the script, 'odisha_monthly_temperature_1993_2017_synthetic.csv', and 'Rainfall.csv' are in the same folder.")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")