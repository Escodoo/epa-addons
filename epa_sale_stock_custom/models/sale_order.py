# Copyright 2024 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    picking_status = fields.Selection(
        [
            ("delivered", "Fully Delivered"),
            ("partially_delivered", "Partially Delivered"),
            ("to_deliver", "To Deliver"),
            ("cancel", "Delivery Cancelled"),
            ("no", "Nothing to Deliver"),
        ],
        compute="_compute_picking_status",
        search="_search_picking_status",
        readonly=True,
    )

    @api.depends("state", "picking_ids.state")
    def _compute_picking_status(self):
        for order in self:
            order.picking_status = order._get_picking_status()

    def _get_picking_status(self):
        self.ensure_one()
        picking_status = "no"
        if self.state in ("sale", "done") and self.picking_ids:
            pstates = self.picking_ids.mapped("state")
            if all([state == "cancel" for state in pstates]):
                picking_status = "cancel"
            elif all([state in ("done", "cancel") for state in pstates]):
                picking_status = "delivered"
            elif any([state == "done" for state in pstates]):
                picking_status = "partially_delivered"
            elif all(
                [
                    state in ("confirmed", "assigned", "waiting", "cancel")
                    for state in pstates
                ]
            ):
                picking_status = "to_deliver"
        return picking_status

    @api.model
    def _search_picking_status(self, operator, value):
        orders = self.search(
            [
                ("state", "in", ("sale", "done")),
                ("picking_ids", "!=", False),
            ]
        )

        if operator == "=":
            orders = orders.filtered(lambda o: o._get_picking_status() == value)
        elif operator == "!=":
            orders = orders.filtered(lambda o: o._get_picking_status() != value)
        elif operator == "in":
            orders = orders.filtered(lambda o: o._get_picking_status() in value)
        elif operator == "not in":
            orders = orders.filtered(lambda o: o._get_picking_status() not in value)
        else:
            raise ValueError("Unsupported operator %s" % operator)

        return [("id", "in", orders.ids)]
