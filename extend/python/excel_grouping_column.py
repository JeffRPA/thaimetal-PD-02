
def grouping_column(file_path, group_by, group_field):

    import pandas as pd

    # file_path = "Inventory transactions originator_639063906271164721.xlsx"
    # Read the Excel file (first sheet by default, or specify sheet_name="Sheet1")

    df = pd.read_excel(file_path)

    # Make sure CW quantity is numeric

    df[group_field] = pd.to_numeric(df[group_field], errors='coerce').fillna(0)

    # Group by Number and sum CW quantity
    grouped_df = (
        df.groupby(group_by, as_index=False)[group_field]
        .sum()
    )

    # Write to a new sheet in the SAME Excel file
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        grouped_df.to_excel(writer, sheet_name='Sheet2', index=False)

    return('successfully group column')

def extract_zero_cw_quantity(file_path, sheet_name="Sheet2"):
    import pandas as pd
    """
    Read grouped sheet and return a list of Code
    where summed CW quantity is 0
    """

    # Read grouped sheet
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Ensure numeric
    df['CW quantity'] = pd.to_numeric(df['CW quantity'], errors='coerce').fillna(0)
    
    # Filter rows where CW quantity == 0
    zero_df = df[df['CW quantity'] == 0]
    
    # Extract Code column as list
    zero_codes = zero_df['Number'].tolist()

    return zero_codes
