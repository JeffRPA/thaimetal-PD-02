

###########################################################################
#  errorlogedit.py
###########################################################################

def get_date_string_without_slash():
    from datetime import datetime
    """
    Returns the current date as a string in the format 'DDMMYYYY' without slashes.
    """
    current_date = datetime.now()
    return current_date.strftime("%d_%m_%Y")


def currenttime():
    import time
    
    return time.strftime("%H:%M:%S", time.localtime())


#type2.2
#target: create the log file   paste_values_to_excel  in the same row
#main header is row1   we insert emptyrow and log at row2
def insert_empty_row_at_and_write_cells_insamerow(xlsx_filepath, sheet_name, row, variables):
    
    import win32com.client as win32
    # Open Excel
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    excel.Visible = False  # Set to True if you want to see the Excel window
    excel.DisplayAlerts = False

    try:
        # Open the workbook
        workbook = excel.Workbooks.Open(xlsx_filepath)
        
        # Access the specific sheet
        sheet = workbook.Sheets(sheet_name)
        
        # Insert a blank row at the specified row
        sheet.Rows(row).Insert()

        # Paste each variable into the specified column of the row
        for variable, column_letter in variables:
            try:
                cell_position = f"{column_letter}{row}"
                sheet.Range(cell_position).Value = variable
            except Exception as e:
                print(f"Error pasting value '{variable}' into cell '{cell_position}': {e}")


        # Save the workbook
        workbook.Save()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close Excel
        workbook.Close(SaveChanges=True)
        excel.Quit()





