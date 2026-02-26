from odoo import models, fields

class InventoryDetail(models.Model):
    _name = "inventory.detail"
    _description = 'Inventory Details'
    _rec_name = 'i_name'
    
    # Use lambda for the default date to ensure it's calculated at the moment of creation
    date = fields.Datetime(string="Date", default=fields.Datetime.now)
    i_name = fields.Char(string="Inventory Name", required=True)
    
    company_id = fields.Many2one(
        'res.company', 
        string='Company', 
        default=lambda self: self.env.company,
        required=True
    )