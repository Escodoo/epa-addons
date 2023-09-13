# Copyright 2023 Escodoo - Rodrigo Neves Trindade
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EpaStockRequestOrderCustom(models.Model):
    _inherit = "stock.request.order"

    price_subtotal = fields.Float(
        string="SubTotal",
        compute="_compute_price_subtotal",
        readonly=True,
    )

    price_total = fields.Float(
        string="Total",
        compute="_compute_amount",
        readonly=True,
    )

    def _compute_amount(self):
        total = 0.0
        for line in self.stock_request_ids:
            total += line.price_subtotal
        self.price_total = total

    @api.depends("stock_request_ids")
    def _compute_price_subtotal(self):
        for record in self:
            product_qty = record.stock_request_ids.product_uom_qty
            product_price = record.stock_request_ids.product_id.lst_price
            record.price_subtotal = product_qty * product_price


class EpaStockRequestCustom(models.Model):
    _inherit = "stock.request"

    price_subtotal = fields.Float(
        string="SubTotal",
        compute="_compute_price_subtotal",
        readonly=True,
    )

    @api.depends("product_id", "product_uom_qty")
    def _compute_price_subtotal(self):
        for record in self:
            product_qty = record.product_uom_qty
            product_price = record.product_id.lst_price
            record.price_subtotal = product_qty * product_price
