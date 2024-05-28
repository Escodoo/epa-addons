# Copyright 2024 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CrmLead(models.Model):

    _inherit = "crm.lead"

    job_description = fields.Char("Job Description")
    interesting_client = fields.Boolean("Interesting Client")
    appropriate_equipment = fields.Boolean("Appropriate Equipment")
    adequate_documentation = fields.Boolean("Adequate Documentation")
    validated_methodologies = fields.Boolean("Validated Methodologies")
    available_labor = fields.Boolean("Available Labor")
    qualified_labor = fields.Boolean("Qualified Labor")
    completion_period = fields.Boolean("Feasible Completion Period")
    payment_term = fields.Boolean("Adequate Payment Term")
    operational_viability = fields.Boolean("Operational Viability")
    financial_viability = fields.Boolean("Financial Viability")
    client_financial_health = fields.Boolean("Client Adequate Financial Health")
    client_cash_flow = fields.Boolean("We Serve Client Cash Flow")
    technological_risks = fields.Boolean("Acceptable Technological Risks")
    legal_risks = fields.Boolean("Acceptable Legal Risks")
    political_risks = fields.Boolean("Acceptable Political Risks")
    all_above = fields.Boolean("All Of The Above")
    subcontracting_possibility = fields.Boolean("Subcontracting Possibility")
    subcontracting_laboratory = fields.Boolean("Laboratory")
    subcontracting_probe = fields.Boolean("Probe")
    subcontracting_sampling = fields.Boolean("Sampling")
    alias_name = fields.Char("Codename")
    subcontracting_others = fields.Char(string="Others")
    proposal_date = fields.Date("Proposal Date")

    group_companies = fields.Many2one('res.company', string="Group Companies")
    company_contacts = fields.Many2one('res.partner', string="Company Contacts")
    service_types = fields.Many2one('project.task', string="Types of Service")
    project_manager = fields.Many2one('hr.employee', string="Project Manager")

    @api.onchange(
        "interesting_client",
        "appropriate_equipment",
        "adequate_documentation",
        "validated_methodologies",
        "available_labor",
        "qualified_labor",
        "completion_period",
        "payment_term",
        "operational_viability",
        "financial_viability",
        "client_financial_health",
        "client_cash_flow",
        "technological_risks",
        "legal_risks",
        "political_risks",
    )
    def _onchange_fields_epa(self):
        if all(
            [
                self.interesting_client,
                self.appropriate_equipment,
                self.adequate_documentation,
                self.validated_methodologies,
                self.available_labor,
                self.qualified_labor,
                self.completion_period,
                self.payment_term,
                self.operational_viability,
                self.financial_viability,
                self.client_financial_health,
                self.client_cash_flow,
                self.technological_risks,
                self.legal_risks,
                self.political_risks,
            ]
        ):
            self.all_above = True
        else:
            self.all_above = False

    @api.onchange("subcontracting_possibility")
    def _onchange_epa_subcontracting_possibility(self):
        if not self.subcontracting_possibility:
            self.subcontracting_laboratory = False
            self.subcontracting_probe = False
            self.subcontracting_sampling = False
            self.subcontracting_others = ""

    @api.onchange("all_above")
    def _onchange_stage_all_above(self):
        if not self.all_above:
            self.stage_id = 1
        elif self.all_above:
            self.stage_id = 2
