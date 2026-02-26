from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def write(self, vals):
        # 1. Use the ACTUAL technical name of your module here
        is_manager = self.env.user.has_group('ppnpl_accounting_move.group_contact_manager_special')
        
        # 2. Check if the user is a manager
        if not is_manager:
            for record in self:
                # record.ids check ensures the record exists in the DB
                if record.id:
                    raise UserError(_("Warning: You do not have permission to edit existing contacts. "
                                      "Please contact an administrator for master data changes."))
        
        return super(ResPartner, self).write(vals)