# -*- coding: utf-8 -*-

from odoo import models
from datetime import datetime


class ProductDetailsXlsx(models.AbstractModel):
    _name = 'report.ppnp_sale_custom.report_product_detail_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, docs):
        if not docs:
            return

        sheet = workbook.add_worksheet('Product Details')

        # Get company name and date
        company_name = self.env.company.name or "Company"
        current_date = datetime.today().strftime('%Y-%m-%d')

        # Formats
        bold = workbook.add_format({'bold': True})
        bold_center = workbook.add_format({'bold': True, 'align': 'center'})
        money = workbook.add_format({'num_format': '$#,##0.00'})

        # Row 0: Company Name and Date on same line (merged A1:E1)
        sheet.merge_range('A1:E1', f'{company_name}     Date: {current_date}')

        # Row 1: Report Title - centered and bold (merged A2:E2)
        sheet.merge_range('A2:E2', 'PRODUCT DETAIL REPORT', bold_center)
        
        
        
        # SET COLUMN WIDTHS
        sheet.set_column('A:A', 30)   # Column A (Product Name) - width 30
        sheet.set_column('B:B', 15)   # Column B (Price) - width 15
        sheet.set_column('C:C', 12)   # Column C (Quantity) - width 12
        sheet.set_column('D:D', 12)   # Column D (Discount) - width 12
        sheet.set_column('E:E', 15)   # Column E (Amount) - width 15
        

        # Row 3: Headers
        sheet.write(3, 0, 'Product Name', bold)
        sheet.write(3, 1, 'Price', bold)
        sheet.write(3, 2, 'Quantity', bold)
        sheet.write(3, 3, 'Discount', bold)
        sheet.write(3, 4, 'Amount', bold)

        # Data rows
        row = 4
        for obj in docs:
            sheet.write(row, 0, obj.name or '')
            sheet.write(row, 1, obj.price or 0.0, money)
            sheet.write(row, 2, obj.quantity or 0.0)
            sheet.write(row, 3, obj.discount or 0.0)
            sheet.write(row, 4, obj.amount or 0.0, money)
            row += 1
