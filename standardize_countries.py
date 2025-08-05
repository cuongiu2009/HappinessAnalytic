import pandas as pd
import numpy as np

# UN M49 Standard Country Names Mapping
# This dictionary maps current names to UN M49 standard names
country_mapping = {
    # Current variations to UN M49 standard
    "Bahamas, The": "Bahamas",
    "Bolivia": "Bolivia (Plurinational State of)",
    "Congo, Dem. Rep.": "Democratic Republic of the Congo", 
    "Congo, Rep.": "Congo",
    "Cote d'Ivoire": "Côte d'Ivoire",
    "Iran, Islamic Rep.": "Iran (Islamic Republic of)",
    "Korea, Dem. People's Rep.": "Democratic People's Republic of Korea",
    "Korea, Rep.": "Republic of Korea",
    "Kyrgyz Republic": "Kyrgyzstan",
    "Lao PDR": "Lao People's Democratic Republic",
    "Macedonia, FYR": "North Macedonia",
    "Micronesia, Fed. Sts.": "Micronesia (Federated States of)",
    "Moldova": "Republic of Moldova",
    "Myanmar": "Myanmar",
    "Russian Federation": "Russian Federation",
    "Slovak Republic": "Slovakia", 
    "St. Kitts and Nevis": "Saint Kitts and Nevis",
    "St. Lucia": "Saint Lucia",
    "St. Vincent and the Grenadines": "Saint Vincent and the Grenadines",
    "Syrian Arab Republic": "Syrian Arab Republic",
    "Tanzania": "United Republic of Tanzania",
    "Turkey": "Türkiye",
    "United States": "United States of America",
    "Venezuela, RB": "Venezuela (Bolivarian Republic of)",
    "Vietnam": "Viet Nam",
    "Yemen, Rep.": "Yemen",
    
    # Regional/Aggregate names - keep as is or map to standard
    "Arab World": "Arab World",
    "Africa Eastern and Southern": "Africa Eastern and Southern",
    "Africa Western and Central": "Africa Western and Central", 
    "Central Europe and the Baltics": "Central Europe and the Baltics",
    "Channel Islands": "Channel Islands",
    
    # Names that are already correct according to UN M49
    "Afghanistan": "Afghanistan",
    "Albania": "Albania", 
    "Algeria": "Algeria",
    "American Samoa": "American Samoa",
    "Andorra": "Andorra",
    "Angola": "Angola",
    "Antigua and Barbuda": "Antigua and Barbuda",
    "Argentina": "Argentina",
    "Armenia": "Armenia",
    "Aruba": "Aruba",
    "Australia": "Australia",
    "Austria": "Austria",
    "Azerbaijan": "Azerbaijan",
    "Bahrain": "Bahrain",
    "Bangladesh": "Bangladesh",
    "Barbados": "Barbados",
    "Belarus": "Belarus",
    "Belgium": "Belgium",
    "Belize": "Belize",
    "Benin": "Benin",
    "Bermuda": "Bermuda",
    "Bhutan": "Bhutan",
    "Bosnia and Herzegovina": "Bosnia and Herzegovina",
    "Botswana": "Botswana",
    "Brazil": "Brazil",
    "Brunei Darussalam": "Brunei Darussalam",
    "Bulgaria": "Bulgaria",
    "Burkina Faso": "Burkina Faso",
    "Burundi": "Burundi",
    "Cameroon": "Cameroon",
    "Canada": "Canada",
    "Central African Republic": "Central African Republic",
    "Chad": "Chad",
    "Chile": "Chile",
    "China": "China",
    "Colombia": "Colombia",
    "Costa Rica": "Costa Rica",
    "Croatia": "Croatia",
    "Cyprus": "Cyprus",
    "Denmark": "Denmark",
    "Ecuador": "Ecuador",
    "Egypt": "Egypt",
    "Finland": "Finland",
    "France": "France",
    "Germany": "Germany",
    "Ghana": "Ghana",
    "Greece": "Greece",
    "Hungary": "Hungary",
    "Iceland": "Iceland",
    "India": "India",
    "Indonesia": "Indonesia",
    "Iraq": "Iraq",
    "Ireland": "Ireland",
    "Israel": "Israel",
    "Italy": "Italy",
    "Jamaica": "Jamaica",
    "Japan": "Japan",
    "Jordan": "Jordan",
    "Kazakhstan": "Kazakhstan",
    "Kenya": "Kenya",
    "Kuwait": "Kuwait",
    "Latvia": "Latvia",
    "Lebanon": "Lebanon",
    "Lithuania": "Lithuania",
    "Luxembourg": "Luxembourg",
    "Malaysia": "Malaysia",
    "Malta": "Malta",
    "Mexico": "Mexico",
    "Mongolia": "Mongolia",
    "Morocco": "Morocco",
    "Nepal": "Nepal",
    "Netherlands": "Netherlands (Kingdom of the)",
    "New Zealand": "New Zealand",
    "Norway": "Norway",
    "Pakistan": "Pakistan",
    "Panama": "Panama",
    "Peru": "Peru",
    "Philippines": "Philippines",
    "Poland": "Poland",
    "Portugal": "Portugal",
    "Romania": "Romania",
    "Saudi Arabia": "Saudi Arabia",
    "Singapore": "Singapore",
    "Slovenia": "Slovenia",
    "South Africa": "South Africa", 
    "Spain": "Spain",
    "Sri Lanka": "Sri Lanka",
    "Sweden": "Sweden",
    "Switzerland": "Switzerland",
    "Thailand": "Thailand",
    "Tunisia": "Tunisia",
    "Ukraine": "Ukraine",
    "United Arab Emirates": "United Arab Emirates",
    "United Kingdom": "United Kingdom of Great Britain and Northern Ireland",
    "Uruguay": "Uruguay",
}

def standardize_country_names(file_path, output_path=None):
    """
    Standardize country names in CSV files according to UN M49 standard
    """
    # Read the CSV file, skipping the metadata at the top
    # Look for the actual header row
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the header row (contains "Country Name")
    header_row = None
    for i, line in enumerate(lines):
        if 'Country Name' in line:
            header_row = i
            break
    
    if header_row is None:
        print(f"Could not find header row in {file_path}")
        return
    
    print(f"Found header at row {header_row + 1}")
    
    # Read the CSV starting from the header row
    df = pd.read_csv(file_path, skiprows=header_row)
    
    # Find the country name column (usually "Country Name")
    country_col = None
    for col in df.columns:
        if 'Country Name' in col:
            country_col = col
            break
    
    if country_col is None:
        print(f"Could not find country name column in {file_path}")
        return
    
    print(f"Found country column: {country_col}")
    print(f"Original unique countries: {len(df[country_col].unique())}")
    
    # Store original values to track changes
    original_countries = df[country_col].copy()
    
    # Apply mapping
    df[country_col] = df[country_col].map(country_mapping).fillna(df[country_col])
    
    print(f"Updated unique countries: {len(df[country_col].unique())}")
    
    # Show changes made
    print("\nCountries that were updated:")
    changes_made = False
    for i, (old_name, new_name) in enumerate(zip(original_countries, df[country_col])):
        if old_name != new_name:
            print(f"  '{old_name}' → '{new_name}'")
            changes_made = True
    
    if not changes_made:
        print("  No changes were needed - all country names already conform to UN M49 standard")
    
    # Save the updated file, preserving the original metadata
    if output_path is None:
        output_path = file_path.replace('.csv', '_standardized.csv')
    
    # Write the file with original metadata preserved
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        # Write original metadata
        for i in range(header_row):
            f.write(lines[i])
        
        # Write updated data
        df.to_csv(f, index=False)
    
    print(f"\nStandardized file saved as: {output_path}")
    return df

def standardize_excel_file(file_path, output_path=None):
    """
    Standardize country names in Excel files according to UN M49 standard
    """
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        # Find the country name column
        country_col = None
        for col in df.columns:
            if 'country' in col.lower():
                country_col = col
                break
        
        if country_col is None:
            print(f"Could not find country name column in {file_path}")
            return
        
        print(f"Found country column: {country_col}")
        print(f"Original unique countries: {len(df[country_col].unique())}")
        
        # Apply mapping
        df[country_col] = df[country_col].map(country_mapping).fillna(df[country_col])
        
        print(f"Updated unique countries: {len(df[country_col].unique())}")
        
        # Save the updated file
        if output_path is None:
            output_path = file_path.replace('.xlsx', '_standardized.xlsx')
        
        df.to_excel(output_path, index=False)
        print(f"\nStandardized Excel file saved as: {output_path}")
        return df
        
    except Exception as e:
        print(f"Error processing Excel file: {e}")

if __name__ == "__main__":
    # Paths to your files
    base_path = r"c:\Users\Lenovo\Desktop\Code\SQL\World Happiness"
    
    # Standardize CSV files
    print("=" * 60)
    print("STANDARDIZING GDP.csv")
    print("=" * 60)
    standardize_country_names(f"{base_path}\\GPD.csv")
    
    print("\n" + "=" * 60)
    print("STANDARDIZING Population.csv")
    print("=" * 60)
    standardize_country_names(f"{base_path}\\Population.csv")
    
    print("\n" + "=" * 60)
    print("STANDARDIZING HDI.xlsx")
    print("=" * 60)
    standardize_excel_file(f"{base_path}\\HDI.xlsx")
    
    print("\n" + "=" * 60)
    print("STANDARDIZATION COMPLETE!")
    print("=" * 60)
    print("New files created:")
    print("- GPD_standardized.csv")
    print("- Population_standardized.csv") 
    print("- HDI_standardized.xlsx")
    print("\nAll country names now conform to UN M49 standard.")
