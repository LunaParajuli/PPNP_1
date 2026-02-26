from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    transport_picking_id = fields.Many2one(
        'stock.picking',
        string="Select Delivery for Transport"
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
        for move in self:
            picking = move.transport_picking_id
            if picking:
                move.vehicle_name        = picking.vehicle_name
                move.driver_name         = picking.driver_name
                move.registration_number = picking.registration_number
                move.dispatch_date       = picking.dispatch_date
            else:
                move.vehicle_name        = False
                move.driver_name         = False
                move.registration_number = False
                move.dispatch_date       = False