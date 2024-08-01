# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class HrExpense(models.Model):
    _inherit = "hr.expense"

    fiscal_document_number = fields.Char(
        string="Fiscal Document",
        stored=True,
        copy=True,
    )
    fiscal_document_partner_id = fields.Many2one(
        "res.partner",
        string="Document Partner",
        domain=[("company_type", "=", "company")],
        stored=True,
        copy=True,
    )
    show_fiscal_document = fields.Boolean(compute="_compute_show_fiscal_document")

    def _get_account_move_line_values(self):
        move_line_values_by_expense = super()._get_account_move_line_values()
        for expense_id, move_lines in move_line_values_by_expense.items():
            expense = self.browse(expense_id)
            for move_line in move_lines:
                if "date_maturity" in move_line.keys():
                    move_line["date_maturity"] = expense.sheet_id.maturity_date
        return move_line_values_by_expense

    @api.depends("product_id.categ_id")
    def _compute_show_fiscal_document(self):
        for record in self:
            record.show_fiscal_document = record.product_id.categ_id.id == 31
