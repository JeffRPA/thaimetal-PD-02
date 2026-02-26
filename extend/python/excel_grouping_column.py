
def grouping_column(file_path):

    import pandas as pd
    import time

    # Write Excel (retry)
    max_retries=3
    delay_sec=1

    df = pd.read_excel(file_path)

    # Make sure CW quantity is numeric

    df['CW quantity'] = pd.to_numeric(df['CW quantity'], errors='coerce').fillna(0)
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)

    df['Prefix'] = df['Number'].astype(str).str[:4]

    # Group by Number and sum CW quantity
    grouped_df = (
        df.groupby(['Number', 'Prefix'], as_index=False)
          .agg({
              'CW quantity': 'sum',
              'Quantity': 'sum'
          })
    )

    grouped_df['CW quantity'] = grouped_df['CW quantity'].round(6)
    grouped_df['Quantity'] = grouped_df['Quantity'].round(6)

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
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    df['CW quantity'] = pd.to_numeric(df['CW quantity'], errors='coerce').fillna(0)
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)
    
    rules = {
        'PDCD': lambda r: r['CW quantity'] == 0 and r['Quantity'] == 0,
        'PDFA': lambda r: r['Quantity'] == 0,
        'PDPK': lambda r: r['CW quantity'] == 0,
        'PDWG': lambda r: r['CW quantity'] == 0 and r['Quantity'] == 0,
    }
    
    result = []
    for _, row in df.iterrows():
        prefix = row['Prefix']
        if prefix in rules and rules[prefix](row):
            result.append(row['Number'])

    return result

def update_grouped_with_response(file_path, responses=None):

    import pandas as pd
    if responses is None:
        return "No response data provided"

    df_grouped = pd.read_excel(file_path, sheet_name="Sheet2")

    df_response = pd.DataFrame(responses)

    df_merged = df_grouped.merge(
        df_response,
        on="Number",
        how="left"  # keep all grouped rows
    )

    df_merged["process"] = df_merged["process"].fillna("")
    df_merged["reason"] = df_merged["reason"].fillna("")

    # 5?? Write to new sheet
    with pd.ExcelWriter(file_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df_merged.to_excel(writer, sheet_name="Status", index=False)

    return "New sheet created successfully"