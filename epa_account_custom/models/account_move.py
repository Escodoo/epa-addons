# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# Copyright 2024 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    flexible_installments = fields.Boolean(default=False)

    @api.onchange(
        "line_ids",
        "invoice_payment_term_id",
        "invoice_date_due",
        "invoice_cash_rounding_id",
        "invoice_vendor_bill_id",
    )
    def _onchange_recompute_dynamic_lines(self):
        if not self.flexible_installments:
            self._recompute_dynamic_lines()

    @api.depends("restrict_mode_hash_table", "state")
    def _compute_show_reset_to_draft_button(self):
        for move in self:
            if move.line_ids.filtered(
                lambda line: line.payment_line_ids
            ) and not self.user_has_groups(
                "epa_account_custom.group_allow_back_move_to_draft"
            ):
                move.show_reset_to_draft_button = False
            else:
                move.show_reset_to_draft_button = (
                    not move.restrict_mode_hash_table
                    and move.state in ("posted", "cancel")
                )

    def button_draft(self):
        """Handles the action of resetting entries to draft status.

        Performs the operation of resetting entries to draft status. It iterates
        through each entry, verifies if any associated payment order, and raises a
        UserError if so, preventing the reset operation.

        Raises:
            UserError: If an entry is associated with a Payment Order
        """
        super().button_draft()
        for move in self:
            if move.line_ids.filtered(
                lambda line: line.payment_line_ids
            ) and not self.user_has_groups(
                "epa_account_custom.group_allow_back_move_to_draft"
            ):
                raise UserError(
                    _(
                        "You dont't have permission to change a Journal Entry to draft "
                        "when it's associated with a Payment Order."
                    )
                )
