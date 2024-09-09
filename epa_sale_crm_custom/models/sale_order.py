# Copyright 2024 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    attachment_ids = fields.Many2many(
        "ir.attachment",
        string="Attachments",
        help="Employee can submit any documents which supports their explanation",
        domain=[
            "&",
            "|",
            ("mimetype", "=", "application/pdf"),
            ("type", "=", "url"),
            ("res_model", "in", ["crm.lead", "sale.order"]),
        ],
    )

    @api.model
    def create(self, vals):
        if not vals.get("name"):
            vals["name"] = self.env["ir.sequence"].next_by_code("sale.order") or "/"
        if "default_analytic_account_id" in self.env.context:
            analytic_account_id = self.env.context["default_analytic_account_id"]
            vals["analytic_account_id"] = analytic_account_id
        return super().create(vals)
