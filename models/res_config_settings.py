from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    rounding_difference_amount = fields.Float(
        string="Rounding Difference Amount",
        default=0.04,
        help="Maximum amount allowed to be considered as Rounding Difference in the Base Currency balance control of "
             "journal entries. (Usually 0.04) It should only apply to entries where Debit/Credit were calculated from "
             "Foreign Currency amounts (there is at least one line in the entry with a currency different from the base "
             "currency)."
    )
    rounding_difference_amount_usd = fields.Float(
        string="Rounding Difference Amount (USD)",
        default=0.01,
        help="Maximum amount allowed to be considered as Rounding Difference in the USD balance control of accounting "
             "entries. (Usually 0.01)"
    )


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update({
            'rounding_difference_amount': float(
                self.env['ir.config_parameter'].sudo().get_param('rounding_difference_amount', default=0.04)),
            'rounding_difference_amount_usd': float(
                self.env['ir.config_parameter'].sudo().get_param('rounding_difference_amount_usd', default=0.01)),
        })
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('rounding_difference_amount', self.rounding_difference_amount)
        self.env['ir.config_parameter'].sudo().set_param('rounding_difference_amount_usd',
                                                         self.rounding_difference_amount_usd)