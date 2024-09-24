# Copyright 2024 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CrmLeadAnalyticAccountWizard(models.TransientModel):
    _name = "crm.lead.analytic.account.wizard"
    _description = "Wizard to select or create analytic account"

    lead_id = fields.Many2one("crm.lead", string="Lead", required=True)

    create_new_analytic = fields.Boolean(
        string="Create a new Analytic Account", default=False
    )

    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Select an existing Analytic Account",
    )

    @api.onchange("create_new_analytic")
    def _onchange_create_new_analytic(self):
        if self.create_new_analytic:
            self.analytic_account_id = False

    def action_confirm(self):
        self.ensure_one()
        if self.create_new_analytic:
            analytic_account = self.env["account.analytic.account"].create(
                {
                    "name": self.lead_id.name,
                    "partner_id": self.lead_id.partner_id.id,
                }
            )
            self.lead_id.quotation_analytic_account_id = analytic_account.id
        else:
            if not self.analytic_account_id:
                raise ValidationError(
                    _("Please select an existing Analytic Account or create a new one.")
                )
            self.lead_id.quotation_analytic_account_id = self.analytic_account_id.id

        return self.lead_id.action_new_quotation()
