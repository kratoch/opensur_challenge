from odoo import models, api
from odoo import fields
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    base_currency_only = fields.Boolean(string="Base Currency Only")
    usd_balance_warning = fields.Boolean(string="USD Amounts Not Balanced", compute='_compute_usd_balance_error')

    @api.depends('line_ids.debit_usd', 'line_ids.credit_usd')
    def _compute_usd_balance_error(self):
        for rec in self:
            total_debit_usd = round(sum(line.debit_usd for line in rec.line_ids), 2)
            total_credit_usd = round(sum(line.credit_usd for line in rec.line_ids), 2)
            rec.usd_balance_warning = total_debit_usd != total_credit_usd

    def action_post(self):
        for rec in self:
            if rec.usd_balance_warning:
                raise ValidationError("USD Amounts Not Balanced")
        return super(AccountMove, self).action_post()
