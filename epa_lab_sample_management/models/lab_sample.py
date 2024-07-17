# Copyright 2024 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# Copyright 2024 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class LabSample(models.Model):

    _name = "lab.sample"

    lab_id = fields.Many2one(
        comodel_name="lab.laboratory",
        string="Laboratory",
        required=True,
    )
    project_id = fields.Many2one(
        comodel_name="project.project",
        string="Project",
        required=True,
    )
    matrix_id = fields.Many2one(
        comodel_name="lab.matrix",
        string="Matrix",
        required=True,
    )
    employee_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Employee",
        required=True,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        required=True,
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        readonly=True,
    )
    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("open", "Open"),
            ("pending", "Pending"),
            ("received", "Received"),
            ("published", "Published"),
            ("done", "Done"),
        ],
        string="Status",
        default="draft",
        required=True,
    )
    issue_pending = fields.Selection(
        [("yes", "Yes"), ("no", "No")], string="Issue Pending"
    )
    report = fields.Text(string="Report")
    location = fields.Char(string="Location")
    collection_date = fields.Date(string="Collection Date")
    reception_date = fields.Date(string="Reception Date")
    delivery_forecast = fields.Date(string="Delivery Forecast")
    lab_submission_date = fields.Date(string="Lab Submission Date")
    creation_date = fields.Datetime(
        string="Creation Date", default=lambda self: fields.Datetime.now()
    )
    depth = fields.Float(string="Depth (cm)", default=0.0, help="Depth in centimeters")
    budget = fields.Monetary(string="Budget")
    billing = fields.Monetary(string="Billing")

    @api.onchange("issue_pending", "location", "report")
    def _onchange_status(self):
        if self.issue_pending and self.report and self.location == "":
            self.status = "open"
        elif self.issue_pending == "no":
            self.status = "done"
        elif self.issue_pending == "yes":
            self.status = "pending"
        elif self.report:
            self.status = "published"
        elif self.location:
            self.status = "received"
        else:
            self.status = "open"
