from odoo import models, fields
from odoo.exceptions import ValidationError
from datetime import timedelta
from num2words import num2words


class SalespersonReportWizard(models.TransientModel):
    _name = 'salesperson.report.wizard'
    _description = 'Salesperson Report Wizard'

    user_id = fields.Many2one('res.users', string="Salesperson", required=True, default=lambda self: self.env.user)
    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)

    def _get_report_lines(self):
        self.ensure_one()
        date_to_inclusive = self.date_to + timedelta(days=1)
        return self.env['sale.order.line'].search([
            ('order_id.user_id', '=', self.user_id.id),
            ('order_id.date_order', '>=', self.date_from),
            ('order_id.date_order', '<', date_to_inclusive),
            ('order_id.state', 'in', ['sale', 'done']),
            ('display_type', '=', False),
        ])

    def action_generate_report(self):
        self.ensure_one()
        lines = self._get_report_lines()
        if not lines:
            raise ValidationError("No sales found for this salesperson in the selected period.")
        return self.env.ref('ppnpl_report_wizard.action_report_salesperson_pdf').report_action(
            lines, data={'wizard_id': self.id}
        )


class SalespersonReportPDF(models.AbstractModel):
    _name = 'report.ppnpl_report_wizard.report_salesperson_template'
    _description = 'Salesperson Report PDF'

    def _amount_to_words(self, amount):
        whole = int(amount)
        fraction = round((amount - whole) * 100)
        words = num2words(whole, lang='en_IN').title()
        if fraction:
            words += ' And ' + num2words(fraction, lang='en_IN').title() + ' Paisa'
        return words + ' Only'

    def _get_report_values(self, docids, data=None):
        wizard = self.env['salesperson.report.wizard'].browse(data['wizard_id'])
        lines = wizard._get_report_lines()
        grand_total = sum(lines.mapped('price_total'))

        return {
            'docs': lines,
            'salesperson_name': wizard.user_id.name,
            'date_from': wizard.date_from,
            'date_to': wizard.date_to,
            'grand_total': grand_total,
            'amount_in_words': self._amount_to_words(grand_total),
        }