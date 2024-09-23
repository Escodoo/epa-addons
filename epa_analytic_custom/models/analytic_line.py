# Copyright 2024 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):

    _name = "account.analytic.line"
    _inherit = ["account.analytic.line", "mail.thread"]

    name = fields.Char(tracking=True)
    date = fields.Date(tracking=True)
    amount = fields.Monetary(tracking=True)
    account_id = fields.Many2one(tracking=True)
    partner_id = fields.Many2one(tracking=True)
    product_id = fields.Many2one(tracking=True)

    def _can_edit_line(self, vals=None):
        self.ensure_one()
        if (
            self.move_id
            and self.move_id.payment_line_ids
            and not self.user_has_groups(
                "epa_analytic_custom.group_allow_edit_analytic_line"
            )
        ):
            return False
        return True

    def write(self, vals):
        for record in self:
            if not record._can_edit_line(vals):
                raise ValidationError(
                    _(
                        "You are not allowed to edit analytic lines linked with journal items"
                    )
                )
        return super(AccountAnalyticLine, self).write(vals)

    def unlink(self):
        for record in self:
            if not record._can_edit_line():
                raise ValidationError(
                    _(
                        "You are not allowed to delete analytic lines linked with journal items"
                    )
                )
        return super(AccountAnalyticLine, self).unlink()
