# Copyright 2023 - TODAY, Rodrigo Neves Trindade <rodrigo.trindade@escodoo.com.br>
# Copyright 2023 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockRequest(models.Model):
    _inherit = "stock.request"

    def _default_egd_currency_id(self):
        company_id = (
            self.env.context.get("force_company")
            or self.env.context.get("company_id")
            or self.env.user.company_id.id
        )
        return self.env["res.company"].browse(company_id).currency_id

    egd_price_subtotal = fields.Monetary(
        string="Subtotal",
        compute="_compute_egd_price_subtotal",
        readonly=True,
        store=True,
    )

    currency_id = fields.Many2one(
        "res.currency", "Currency", required=True, default=_default_egd_currency_id
    )

    @api.depends("product_id", "product_uom_qty")
    def _compute_egd_price_subtotal(self):
        for record in self:
            product_qty = record.product_uom_qty
            product_price = record.product_id.standard_price
            record.egd_price_subtotal = product_qty * product_price
