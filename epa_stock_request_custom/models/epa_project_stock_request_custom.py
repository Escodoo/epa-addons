# Copyright 2023 Escodoo - Rodrigo Neves Trindade
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EpaProjectTaskStockRequestCustom(models.Model):
    _inherit = "project.task"

    price_subtotal = fields.Float(
        string="SubTotal",
        compute="_compute_price_subtotal",
        readonly=True,
    )

    @api.depends("stock_request_order_ids")
    def _compute_price_subtotal(self):
        for record in self:
            record.price_subtotal = record.stock_request_order_ids.price_subtotal


class EpaProjectStockRequestCustom(models.Model):
    _inherit = "project.project"

    price_subtotal = fields.Float(
        string="Valor",
        compute="_compute_price_subtotal",
        readonly=True,
    )

    @api.depends("stock_request_order_ids")
    def _compute_price_subtotal(self):
        for record in self:
            record.price_subtotal = record.stock_request_order_ids.price_subtotal
