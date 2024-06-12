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
        string="Picking Status",
        compute="_compute_picking_status",
        store=True,
        readonly=True,
        default="no",
    )

    @api.depends("state", "picking_ids.state")
    def _compute_picking_status(self):
        """
        Compute the picking status for the SO. Possible statuses:
        - no: if the SO is not in status 'sale' nor 'done', we consider that
          there is nothing to deliver. This is also the default value if the
          conditions of no other status is met.
        - cancel: all pickings are cancelled
        - delivered: if all  pickings are done or cancel.
        - partially_delivered: If at least one picking is done.
        - to_deliver: if all pickings are in confirmed, assigned, waiting or
          cancel state.
        """
        for order in self:
            picking_status = "no"
            if order.state in ("sale", "done") and order.picking_ids:
                pstates = [picking.state for picking in order.picking_ids]
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
            order.picking_status = picking_status
