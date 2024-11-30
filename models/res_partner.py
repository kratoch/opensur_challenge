from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    currency_property_accounts_ids = fields.One2many(
        comodel_name='currency.property.accounts',
        inverse_name='partner_id',
        string='Currency Property Accounts'
    )
