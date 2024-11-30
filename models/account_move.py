from contextlib import contextmanager

from odoo import models, api, _
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
                raise ValidationError(_("USD Amounts Not Balanced"))
        return super(AccountMove, self).action_post()

    # def _get_usd_unbalanced_moves(self, container):
    #     moves = container['records'].filtered(lambda move: move.line_ids)
    #     if not moves:
    #         return
    #
    #     # /!\ As this method is called in create / write, we can't make the assumption the computed stored fields
    #     # are already done. Then, this query MUST NOT depend on computed stored fields.
    #     # It happens as the ORM calls create() with the 'no_recompute' statement.
    #     self.env['account.move.line'].flush_model(['debit', 'credit', 'balance', 'currency_id', 'move_id'])
    #     self._cr.execute('''
    #         SELECT line.move_id,
    #                ROUND(SUM(line.debit_usd), currency.decimal_places) debit,
    #                ROUND(SUM(line.credit_usd), currency.decimal_places) credit
    #           FROM account_move_line line
    #           JOIN account_move move ON move.id = line.move_id
    #           JOIN res_company company ON company.id = move.company_id
    #           JOIN res_currency currency ON currency.id = company.currency_id
    #          WHERE line.move_id IN %s
    #       GROUP BY line.move_id, currency.decimal_places
    #         HAVING ROUND(SUM(line.balance_usd), currency.decimal_places) != 0
    #     ''', [tuple(moves.ids)])
    #
    #     return self._cr.fetchall()
    #
    # @contextmanager
    # def _check_balanced(self, container):
    #     """Validate rounding differences in journal entries."""
    #     for rec in self:
    #         with rec._disable_recursion(container, 'check_move_validity', default=True, target=False) as disabled:
    #             yield
    #             if disabled:
    #                 return
    #         unbalanced_moves = rec._get_unbalanced_moves(container)
    #         unbalanced_moves_usd = rec._get_usd_unbalanced_moves(container)
    #         if unbalanced_moves or unbalanced_moves_usd:
    #             rounding_difference_amount = float(rec.env['ir.config_parameter'].sudo().get_param(
    #                 'rounding_difference_amount'))
    #
    #             rounding_difference_amount_usd = float(rec.env['ir.config_parameter'].sudo().get_param(
    #                 'rounding_difference_amount_usd'))
    #
    #             if rounding_difference_amount or rounding_difference_amount_usd:
    #                 diff = unbalanced_moves[0][2] - unbalanced_moves[0][1]
    #                 diff_usd = unbalanced_moves_usd[0][2] - unbalanced_moves_usd[0][1]
    #
    #                 company = rec.company_id
    #                 income_account = company.income_currency_exchange_account_id
    #                 expense_account = company.expense_currency_exchange_account_id
    #
    #                 if abs(diff) <= float(rounding_difference_amount or 0):
    #                     if not income_account or not expense_account:
    #                         raise ValidationError(
    #                             _("Rounding difference adjustment requires exchange difference entries accounts configured in the company."))
    #                     if diff > 0:
    #                         rec.line_ids.create({'move_id': rec.id, 'debit': 0.0, 'credit': diff, 'account_id': expense_account.id})
    #                     elif diff < 0:
    #                         rec.line_ids.create({'move_id': rec.id, 'debit': abs(diff), 'credit': 0.0, 'account_id': income_account.id})
    #
    #                 if abs(diff_usd) <= float(rounding_difference_amount_usd or 0):
    #                     if not income_account or not expense_account:
    #                         raise ValidationError(
    #                             _("Rounding difference adjustment in USD requires exchange difference entries accounts configured in the company."))
    #                     if diff_usd > 0:
    #                         rec.line_ids.create(
    #                             {'move_id': rec.id, 'debit_usd': 0.0, 'credit_usd': diff_usd, 'account_id': expense_account.id})
    #                     elif diff_usd < 0:
    #                         rec.line_ids.create(
    #                             {'move_id': rec.id, 'debit_usd': abs(diff_usd), 'credit_usd': 0.0, 'account_id': income_account.id})


