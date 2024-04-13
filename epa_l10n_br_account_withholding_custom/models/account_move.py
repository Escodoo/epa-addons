# Copyright 2024 Marcel Savegnago - Escodoo (https://www.escodoo.com.br)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMove(models.Model):

    _inherit = "account.move"

    wh_move_id = fields.Many2one(
        "account.move",
        string="WH Vendor Bill",
        compute="_compute_wh_move_id",
        store=True,
    )
    wh_move_partner_id = fields.Many2one(
        "res.partner", string="WH Partner", compute="_compute_wh_move_id", store=True
    )
    wh_fiscal_document_id = fields.Many2one(
        "l10n_br_fiscal.document",
        string="WH Fiscal Document",
        compute="_compute_wh_move_id",
        store=True,
    )

    @api.depends("line_ids")
    def _compute_wh_move_id(self):
        for move in self:
            line = move.line_ids.mapped("wh_move_line_id")
            if line:
                move.wh_move_id = line.move_id
                move.wh_move_partner_id = line.move_id.partner_id
                move.wh_fiscal_document_id = line.move_id.fiscal_document_id
