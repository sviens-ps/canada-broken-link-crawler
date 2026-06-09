from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

def write_excel(rows, output_path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Page Details"

    headers = list(rows[0].keys())
    ws.append(headers)

    for r in rows:
        ws.append(list(r.values()))

    # Create table
    table_ref = f"A1:{chr(65+len(headers)-1)}{len(rows)+1}"
    table = Table(displayName="tbl_PageDetails", ref=table_ref)

    style = TableStyleInfo(
        name="TableStyleMedium9",
        showRowStripes=True,
        showColumnStripes=False
    )
    table.tableStyleInfo = style
    ws.add_table(table)

    # Freeze header
    ws.freeze_panes = "A2"

    # Auto column width
    for col in ws.columns:
        max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_length + 2

    wb.save(output_path)
