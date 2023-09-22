# Copyright 2023 - TODAY, Rodrigo Neves Trindade <rodrigo.trindade@escodoo.com.br>
# Copyright 2023 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    def _default_egd_currency_id(self):
        company_id = (
            self.env.context.get("force_company")
            or self.env.context.get("company_id")
            or self.env.user.company_id.id
        )
        return self.env["res.company"].browse(company_id).currency_id

    egd_price_total = fields.Monetary(
        string="Total", compute="_compute_egd_price_total", readonly=True, store=True
    )

    currency_id = fields.Many2one(
        "res.currency", "Currency", required=True, default=_default_egd_currency_id
    )

    @api.depends("stock_request_order_ids", "stock_request_order_ids.egd_price_total")
    def _compute_egd_price_total(self):
        for record in self:
            total = 0.0
            for line in record.stock_request_order_ids:
                total += line.egd_price_total
            record.egd_price_total = total
