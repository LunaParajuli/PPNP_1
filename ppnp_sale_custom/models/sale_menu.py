from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleProduct(models.Model):
    _name = 'sale.product'
    _description = 'Sale Product'
    _rec_name = 'name'

    name = fields.Char(string="Product Name", required=True)
    currency_id= fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id)          

    # Current Fields
    date = fields.Date(string="Date",tracking=True)
    price = fields.Monetary(string=" Price", default=0.0 , currency_field="currency_id",tracking=True)
    quantity = fields.Float(string=" Quantity", default=0.0)
    discount = fields.Float(string=" Discount (%)", default=0.0)
    amount = fields.Monetary(string=" Amount", compute="_compute_amount", store=True, currency_field="currency_id",tracking=True)

    # Previous Fields
    prev_price = fields.Monetary(string="Prev Price" , currency_field="currency_id", default=0.0)
    prev_quantity = fields.Float(string="Prev Quantity", default=0.0)
    prev_discount = fields.Float(string="Prev Discount (%)", default=0.0)
    prev_amount = fields.Monetary(string="Previous Amount" , currency_field="currency_id" ,default=0.0 )
    
        
    # Add the company id field
    company_id = fields.Many2one(
        'res.company', 
        string='Company', 
        default=lambda self: self.env.company,
        required=True
    )


    @api.depends('price', 'quantity', 'discount')
    def _compute_amount(self):
        for record in self:
            subtotal = record.price * record.quantity
            record.amount = subtotal - (subtotal * record.discount / 100.0)


    @api.onchange('date')
    def validation_error_func(self):
        today = fields.Date.today() 
        if self.date and self.date >= today: 
            raise ValidationError("You cannot set a date later than today.")

    @api.onchange('discount')
    def _onchange_discount(self):
        """Warns the user immediately when discount is invalid"""
        if self.discount < 0 or self.discount > 100:
            return {
                'warning': {
                    'title': "Invalid Discount",
                    'message': "Discount must be between 0 and 100%! Please enter a valid discount.",
                }
            }
                    
    @api.constrains('price', 'quantity', 'discount')
    def _check_values(self):
        """
        Runs before saving to database.
        Raises error and BLOCKS saving if values are invalid.
        """
        for record in self:
            if record.price < 0:
                raise ValidationError(
                    "❌ Price cannot be negative!\n"
                    f"You entered: {record.price}\n"
                    "Please enter a valid price (0 or greater)."
                )
            if record.quantity <= 0:
                raise ValidationError(
                    "❌ Quantity must be greater than 0!\n"
                    f"You entered: {record.quantity}\n"
                    "Please enter a valid quantity."
                )
            if record.discount < 0 or record.discount > 100:
                raise ValidationError(
                    "❌ Discount must be between 0 and 100%!\n"
                    f"You entered: {record.discount}%\n"
                    "Please enter a valid discount."
                )         
