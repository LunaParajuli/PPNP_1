from odoo import models, fields, api


class SaleOrderLineCustom(models.Model):
    _name='sale.order.line.custom'
    _description='Custom Sale Order Line'

    order_id = fields.Many2one('sale.order', string="Sale Order")
    sale_product_id = fields.Many2one('sale.product', string="Sale Product")
    currency_id2= fields.Many2one(
        related='order_id.currency_id', 
        depends=['order_id.currency_id'],
        store=True,
        string="Currency", 
        ) 

    # Mirror fields for the Sale Order tab
    product_price = fields.Monetary(string="Current Price", currency_field="currency_id2")
    prev_product_price = fields.Monetary(string="Previous Price", currency_field="currency_id2")
    
    product_quantity = fields.Float(string="Current Quantity")
    prev_product_quantity = fields.Float(string="Previous Quantity")

    product_discount = fields.Float(string="Current Discount (%)")
    prev_product_discount = fields.Float(string="Previous Discount (%)")
    
    product_amount = fields.Monetary(string="Current Amount", currency_field="currency_id2")
    prev_product_amount = fields.Monetary(string="Previous Amount", currency_field="currency_id2")


    @api.onchange('sale_product_id')
    def _onchange_sale_product_id(self):
        if self.sale_product_id:
            
             # Sync Previous
            self.prev_product_price = self.sale_product_id.prev_price
            self.prev_product_quantity = self.sale_product_id.prev_quantity
            self.prev_product_discount = self.sale_product_id.prev_discount
            self.prev_product_amount = self.sale_product_id.prev_amount
            
            
            # Sync Current
            self.product_price = self.sale_product_id.price
            self.product_quantity = self.sale_product_id.quantity
            self.product_discount = self.sale_product_id.discount
            self.product_amount = self.sale_product_id.amount
           
        else:
            self.product_price = self.prev_product_price = 0.0
            self.product_quantity = self.prev_product_quantity = 0.0
            self.product_discount = self.prev_product_discount = 0.0
            self.product_amount = self.prev_product_amount = 0.0
            
            
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    line_ids = fields.One2many('sale.order.line.custom', 'order_id', string="Custom Order Lines")
    
    
    
   