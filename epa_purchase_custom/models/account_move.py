# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        # lots of duplicate calls to action_post, so we remove those already posted
        to_post_invoices = self.filtered(
            lambda inv: inv.state != "posted"
            and inv.payment_state in ["not_paid", "in_payment", "paid"]
            and inv.move_type == "in_invoice"
        )

        for invoice in to_post_invoices:
            if (
                invoice.company_id.block_invoice_validation_exceeding_purchase
                and invoice.partner_id.partner_block_invoice_validation_exceeding_purchase
                and invoice.move_type == "in_invoice"
            ):
                purchase_orders = invoice.env["purchase.order"].search(
                    [("invoice_ids", "in", self.id)]
                )

                if purchase_orders and sum(invoice.mapped("amount_total")) > sum(
                    purchase_orders.mapped("amount_total")
                ):
                    raise UserError(
                        _(
                            "You cannot validate this invoice because the total amount "
                            "exceeds the total amount on the purchase order."
                        )
                    )

        return super().action_post()
