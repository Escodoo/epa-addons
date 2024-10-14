# Copyright 2024 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        # Check if opportunity_id exists in the values
        if vals.get("opportunity_id"):
            # Assign analytic account from context if available
            if "default_analytic_account_id" in self.env.context:
                analytic_account_id = self.env.context["default_analytic_account_id"]
                vals["analytic_account_id"] = analytic_account_id

                analytic_account = self.env["account.analytic.account"].browse(
                    analytic_account_id
                )
                if analytic_account:
                    vals["name"] = analytic_account.name
        else:
            if not self.env.user.has_group("sales_team.group_sale_manager"):
                raise UserError(
                    _(
                        "You are not allowed to create a sale order without an opportunity. "
                        "Contact your sales administrator."
                    )
                )

        # Proceed with the regular creation of the sale order
        return super().create(vals)
