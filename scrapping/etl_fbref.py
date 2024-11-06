import os
import requests
import yaml
import pandas as pd
from bs4 import BeautifulSoup
from utils.utils import Utils  # Importing Utils class

# Load YAML Configuration
def load_config():
    with open("scrapping/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config

def scrape_table(url, subdivide_columns, header_start, header_end, exclude_columns):
    """
    Generalized scraping function for a table with specific parameters.

    Parameters:
    url (str): URL of the page to scrape.
    subdivide_columns (int): Number of columns for data subdivision.
    header_start (int): Start index for slicing headers.
    header_end (int): End index for slicing headers.
    exclude_columns (list): Columns to exclude from the final table.

    Returns:
    DataFrame: A DataFrame containing the processed table data.
    """
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the data
    data = soup.find_all('td')
    column_data = Utils.extract_raw_data(data, 'td')
    divided_data = Utils.subdivide_list(column_data, subdivide_columns)
    
    # Extract the headers
    column_name_raw = soup.find_all('th')[header_start:header_end]
    column_name = Utils.extract_raw_data(column_name_raw, 'th')
    
    # Create DataFrame and drop any unnecessary columns
    df = pd.DataFrame(divided_data, columns=column_name)
    df.drop(['Matches'], inplace=True)
    
    return df

def main():
    # Load configuration
    config = load_config()
    
    # Create the data folder if it doesn't exist
    os.makedirs(config["data_folder"], exist_ok=True)

    # Iterate over each table configuration in YAML
    for i, table_config in enumerate(config["tables"]):
        try:
            # Scrape table based on YAML parameters
            df = scrape_table(
                url=table_config["url"],
                subdivide_columns=table_config["subdivide_columns"],
                header_start=table_config["header_start"],
                header_end=table_config["header_end"],
                exclude_columns=config["exclude_columns"]
            )
            
            # Save the DataFrame as CSV
            csv_path = os.path.join(config["data_folder"], f"table_{i + 1}.csv")
            df.to_csv(csv_path, index=False)
            print(f"Saved table from {table_config['url']} to {csv_path}")
        except Exception as e:
            print(f"Error processing {table_config['url']}: {e}")

if __name__ == "__main__":
    main()

