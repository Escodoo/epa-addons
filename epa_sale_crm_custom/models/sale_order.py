# Copyright 2024 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        if vals.get("opportunity_id"):
            if not vals.get("name"):
                vals["name"] = self.env["ir.sequence"].next_by_code("sale.order") or "/"
            if "default_analytic_account_id" in self.env.context:
                analytic_account_id = self.env.context["default_analytic_account_id"]
                vals["analytic_account_id"] = analytic_account_id
            if vals["analytic_account_id"]:
                analytic_account = self.env["account.analytic.account"].browse(
                    vals["analytic_account_id"]
                )
                vals["name"] = analytic_account.name[3:]
            return super().create(vals)
