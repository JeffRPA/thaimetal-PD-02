
def grouping_column(file_path, group_by):

    import pandas as pd
    import time

    # Write Excel (retry)
    max_retries=3
    delay_sec=1

    df = pd.read_excel(file_path)

    # Make sure CW quantity is numeric

    df['CW quantity'] = pd.to_numeric(df['CW quantity'], errors='coerce').fillna(0)
    df['Quantity2'] = pd.to_numeric(df['Quantity2'], errors='coerce').fillna(0)

    # Group by Number and sum CW quantity
    grouped_df = (
        df.groupby(group_by, as_index=False)
          .agg({
              'CW quantity': 'sum',
              'Quantity2': 'sum'
          })
    )

    for attempt in range(1, max_retries + 1):
        try:
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                grouped_df.to_excel(writer, sheet_name='Sheet2', index=False)
            return {"status": "success", "message": "group successfully", "rows": len(grouped_df)}
        except Exception as e:
            if attempt == max_retries:
                return {"status": "error", "message": f"write file failure {max_retries} times: {e}"}
            time.sleep(delay_sec)

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
