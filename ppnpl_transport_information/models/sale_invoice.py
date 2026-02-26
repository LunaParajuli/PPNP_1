from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    transport_picking_id = fields.Many2one(
        'stock.picking',
        string="Select Delivery for Transport",
        
    )

    vehicle_name = fields.Char(
        string="Vehicle Name",
        compute='_compute_transport_details',
        store=True,
        readonly=True
    )
    driver_name = fields.Char(
        string="Driver Name",
        compute='_compute_transport_details',
        store=True,
        readonly=True
    )
    registration_number = fields.Char(
        string="Registration Number",
        compute='_compute_transport_details',
        store=True,
        readonly=True
    )
    dispatch_date = fields.Datetime(
        string="Dispatch Date",
        compute='_compute_transport_details',
        store=True,
        readonly=True
    )

    @api.depends(
        'transport_picking_id',
        'transport_picking_id.vehicle_name',
        'transport_picking_id.driver_name',
        'transport_picking_id.registration_number',
        'transport_picking_id.dispatch_date',
    )
    def _compute_transport_details(self):
        for order in self:
            picking = order.transport_picking_id
            if picking:
                order.vehicle_name        = picking.vehicle_name
                order.driver_name         = picking.driver_name
                order.registration_number = picking.registration_number
                order.dispatch_date       = picking.dispatch_date
            else:
                order.vehicle_name        = False
                order.driver_name         = False
                order.registration_number = False
                order.dispatch_date       = False