from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import common


class TestAccountMove(common.TransactionCase):
    def setUp(self):
        super(TestAccountMove, self).setUp()

        # Get a demo company, partner and a product
        self.company = self.env.ref("base.main_company")
        self.partner = self.env.ref("base.res_partner_1")
        self.product = self.env.ref("product.product_product_4")

    def test_action_post(self):
        # Create a purchase order
        self.purchase_order = self.env["purchase.order"].create(
            {
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "date_order": fields.Date.today(),
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "name": self.product.name,
                            "product_qty": 1.0,
                            "price_unit": 1000.0,
                            "taxes_id": False,
                        },
                    )
                ],
            }
        )

        # Create an invoice with the amount_total bigger than the purchase order
        self.invoice = self.env["account.move"].create(
            {
                "move_type": "in_invoice",
                "payment_state": "not_paid",
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "date": fields.Date.today(),
                "invoice_date": fields.Date.today(),
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "name": self.product.name,
                            "quantity": 1.0,
                            "price_unit": 1000.0,
                            "price_total": 1000.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "name": self.product.name,
                            "quantity": 1.0,
                            "price_unit": 100.0,
                            "price_total": 100.0,
                        },
                    ),
                ],
            }
        )

        # Add the created invoice to the purchase order
        self.purchase_order.invoice_ids = self.invoice
        self.purchase_order.write({"invoice_ids": [(4, self.invoice.id)]})

        # Set conditions to trigger UserError in action_post
        self.company.block_invoice_validation_exceeding_purchase = True
        self.partner.partner_block_invoice_validation_exceeding_purchase = True

        with self.assertRaises(UserError):
            # This should raise UserError as the invoice total exceeds the purchase order total
            self.invoice.action_post()

        # Reset conditions to avoid UserError
        self.company.block_invoice_validation_exceeding_purchase = False
        self.partner.partner_block_invoice_validation_exceeding_purchase = False

        # Now, the action should be successful without raising UserError
        self.invoice.action_post()
