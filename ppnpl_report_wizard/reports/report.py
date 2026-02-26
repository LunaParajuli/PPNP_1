from odoo import models
import io
import base64
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.image import Image as XLImage
from PIL import Image as PILImage

class SalespersonReportExcel(models.AbstractModel):
    _name = 'report.ppnpl_report_wizard.report_salesperson_excel'
    _inherit = 'report.ppnpl_report_wizard.report_salesperson_template'
    _description = 'Salesperson Report Excel'

    def _generate_excel(self, values):
        wb = Workbook()
        ws = wb.active
        ws.title = "Salesperson Report"

        # --- Styles ---
        header_font = Font(name='Arial', bold=True, size=10, color='FFFFFF')
        header_fill = PatternFill('solid', start_color='2E75B6')
        title_font = Font(name='Arial', bold=True, size=14)
        bold_font = Font(name='Arial', bold=True, size=10)
        normal_font = Font(name='Arial', size=10)
        center = Alignment(horizontal='center', vertical='center')
        left = Alignment(horizontal='left', vertical='center')
        right = Alignment(horizontal='right', vertical='center')
        thin = Side(style='thin', color='000000')
        border = Border(left=thin, right=thin, top=thin, bottom=thin)
        total_fill = PatternFill('solid', start_color='D9E1F2')

        # --- Column Widths ---
        ws.column_dimensions['A'].width = 8
        ws.column_dimensions['B'].width = 12
        ws.column_dimensions['C'].width = 35
        ws.column_dimensions['D'].width = 12
        ws.column_dimensions['E'].width = 15
        ws.column_dimensions['F'].width = 15
        ws.column_dimensions['G'].width = 15

        # --- Header Section ---
        ws.merge_cells('A1:G1')
        ws['A1'] = 'Salesperson Performance Report'
        ws['A1'].font = title_font
        ws['A1'].alignment = center

        ws.merge_cells('A2:G2')
        ws['A2'] = f"Salesperson: {values['salesperson_name']}"
        ws['A2'].font = bold_font
        ws['A2'].alignment = left

        ws.merge_cells('A3:G3')
        ws['A3'] = f"Period: {values['date_from']} to {values['date_to']}"
        ws['A3'].font = bold_font
        ws['A3'].alignment = left

        ws.append([]) # Spacer

        # --- Table Headers ---
        headers = ['S.No', 'Product Image', 'Product', 'Qty', 'Unit Price(Rs)', 'Tax', 'Amount(Rs)']
        for col, h in enumerate(headers, start=1):
            cell = ws.cell(row=5, column=col, value=h)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = center
            cell.border = border

        # --- Data Rows ---
        for idx, line in enumerate(values['docs'], start=1):
            row = ws.max_row + 1
            row_data = [
                idx,
                '',
                
                line.product_id.name,
                line.product_uom_qty,
                line.price_unit,
                sum(line.tax_ids.mapped('amount')),
                line.price_total,
            ]
            
            # Write text/numeric data
            for col, val in enumerate(row_data, start=1):
                cell = ws.cell(row=row, column=col, value=val)
                cell.font = normal_font
                cell.border = border
                if col in (4, 5, 6, 7):
                    cell.alignment = right
                    if col in (5, 7):
                        cell.number_format = '#,##0.00'
                    elif col == 6:
                        cell.number_format = '0.00"%"'
                else:
                    cell.alignment = left
            
            
            # --- Image Embedding Logic ---
            if line.product_id.image_128:
                try:
                    # 1. Decode
                    raw_image = line.product_id.image_128
                    if isinstance(raw_image, str):
                        raw_image = base64.b64decode(raw_image)
                    
                    # 2. Open with PIL
                    img_io = io.BytesIO(raw_image)
                    pil_img = PILImage.open(img_io)
                    
                    # 3. Force RGB mode (removes transparency which can break Excel)
                    if pil_img.mode in ('RGBA', 'P'):
                        pil_img = pil_img.convert('RGB')
                        
                    # 4. Resize
                    pil_img.thumbnail((60, 60))
                    
                    # 5. Save to a NEW buffer
                    final_img_io = io.BytesIO()
                    pil_img.save(final_img_io, format='PNG')
                    
                    # 6. Create XLImage and Anchor
                    xl_img = XLImage(final_img_io)
                    # We don't necessarily need to set width/height again if thumbnailed,
                    # but anchoring is mandatory.
                    ws.add_image(xl_img, f'B{row}')
                    
                    # 7. Set Row Height (Mandatory for visibility)
                    ws.row_dimensions[row].height = 60
                    
                except Exception as e:
                    # Log the error so you can see it in the terminal!
                    import logging
                    _logger = logging.getLogger(__name__)
                    _logger.error("Excel Image Error: %s", e)

        # --- Footer Section ---
        total_row = ws.max_row + 1
        ws.merge_cells(f'A{total_row}:F{total_row}')
        total_label = ws.cell(row=total_row, column=1, value='Grand Total(Rs)')
        total_label.font = bold_font
        total_label.fill = total_fill
        total_label.alignment = right
        total_label.border = border

        total_val = ws.cell(row=total_row, column=7, value=values['grand_total'])
        total_val.font = bold_font
        total_val.fill = total_fill
        total_val.alignment = right
        total_val.number_format = '#,##0.00'
        total_val.border = border

        words_row = total_row + 1
        ws.merge_cells(f'A{words_row}:G{words_row}')
        words_cell = ws.cell(row=words_row, column=1, value=f"Amount in Words: {values['amount_in_words']}")
        words_cell.font = Font(name='Arial', bold=True, size=10, italic=True)
        words_cell.alignment = left

        output = io.BytesIO()
        wb.save(output)
        return output.getvalue()