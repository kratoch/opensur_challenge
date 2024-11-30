from odoo import fields, models


class CurrencyPropertyAccounts(models.Model):
    _name = 'currency.property.accounts'
    _description = 'Currency Property Accounts'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=True,
        readonly=True
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        required=True
    )
    property_account_receivable_id = fields.Many2one(
        comodel_name='account.account',
        string='Account Receivable',
        required=True
    )
    property_account_payable_id = fields.Many2one(
        comodel_name='account.account',
        string='Account Payable',
        required=True
    )
