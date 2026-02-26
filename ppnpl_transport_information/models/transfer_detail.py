from odoo import models, fields

class InventoryDetail(models.Model):
    
    _inherit = 'stock.picking'

    vehicle_name = fields.Char(string="Vehicle Name")
    driver_name = fields.Char(string="Driver Name")
    registration_number = fields.Char(string="Registration Number")
    dispatch_date = fields.Datetime(
        string="Dispatch Date",
        default=fields.Datetime.now
    )