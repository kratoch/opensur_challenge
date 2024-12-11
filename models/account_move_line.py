from odoo import api, models, fields


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    debit_usd = fields.Monetary(currency_field='currency_id', string="Debit USD", compute='_compute_usd_amounts',
                                precompute=True, store=True)
    credit_usd = fields.Monetary(currency_field='currency_id', string="Credit USD", compute='_compute_usd_amounts',
                                 precompute=True, store=True)
    balance_usd = fields.Monetary(currency_field='currency_id', string="Balance USD", compute='_compute_usd_balance',
                                  precompute=True, store=True)

    usd_readonly_condition = fields.Boolean(string="USD Readonly Condition", default=True,
                                            compute='_compute_usd_readonly_condition')

    @api.depends('move_id', 'debit_usd', 'credit_usd')
    def _compute_usd_readonly_condition(self):
        user = self.env.user
        has_group = user.has_group('opensur_challenge.group_manager_usd_entries')
        if has_group:
            self.usd_readonly_condition = False
        else:
            self.usd_readonly_condition = True

    @api.depends('move_id.base_currency_only', 'currency_id', 'amount_currency', 'date', 'debit', 'credit')
    def _compute_usd_amounts(self):
        """Computes USD amounts for debit and credit of the move line."""
        usd_currency = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
        for line in self:
            if line.move_id.base_currency_only:
                line.debit_usd = 0.0
                line.credit_usd = 0.0
            elif line.currency_id == usd_currency:
                line.debit_usd = line.amount_currency if line.amount_currency > 0 else 0.0
                line.credit_usd = -line.amount_currency if line.amount_currency < 0 else 0.0
            else:
                # Convert the amount to USD based on the exchange rate at the date of the journal entry
                date = line.date or fields.Date.today()
                amount_in_usd = line.currency_id._convert(
                    abs(line.debit - line.credit),
                    usd_currency,
                    line.company_id,
                    date
                )
                if line.debit > line.credit:
                    line.debit_usd = amount_in_usd
                    line.credit_usd = 0.0
                else:
                    line.debit_usd = 0.0
                    line.credit_usd = amount_in_usd

    @api.depends('debit_usd', 'credit_usd')
    def _compute_usd_balance(self):
        """Computes the balance in USD for the move line."""
        for line in self:
            line.balance_usd = line.debit_usd - line.credit_usd
