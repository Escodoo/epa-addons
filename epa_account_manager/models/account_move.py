# Copyright 2024 - TODAY, Matheus Marques <matheus.marques@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMove(models.Model):

    _inherit = "account.move"

    manager_id = fields.Many2one(
        "res.users", string="Manager", compute="_compute_manager_id", store=True
    )

    @api.depends("invoice_line_ids.analytic_account_id.manager_id")
    def _compute_manager_id(self):
        for record in self:

            analytic_accounts = record.invoice_line_ids.mapped("analytic_account_id")

            if analytic_accounts:
                record.manager_id = analytic_accounts[0].manager_id.id or False
            else:
                record.manager_id = False
