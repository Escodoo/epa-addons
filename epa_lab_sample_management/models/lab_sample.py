# Copyright 2024 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# Copyright 2024 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class LabSample(models.Model):

    _name = "lab.sample"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Lab Sample"
    _order = "id desc"

    name = fields.Char(
        string="Name",
        default="/",
        compute="_compute_name",
        copy=False,
        readonly=True,
        store=True,
    )
    number = fields.Integer(
        string="Sample Number",
        readonly=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        tracking=True,
        default=lambda self: self.env.company,
    )
    laboratory_id = fields.Many2one(
        comodel_name="res.partner",
        string="Laboratory",
        required=True,
        tracking=True,
        domain="[('is_laboratory', '=', True)]",
    )
    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Analytic Account",
        required=True,
        tracking=True,
        domain="[('partner_id', '!=', False)]",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        related="analytic_account_id.partner_id",
        readonly=True,
        store=True,
    )
    matrix_id = fields.Many2one(
        comodel_name="lab.matrix",
        string="Matrix",
        required=True,
        tracking=True,
    )
    employee_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Employee",
        required=True,
        tracking=True,
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        readonly=True,
        related="company_id.currency_id",
        store=True,
    )
    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("open", "Open"),
            ("received", "Received"),
            ("published", "Published"),
            ("pending", "Pending"),
            ("done", "Done"),
            ("cancel", "Cancel"),
        ],
        string="Status",
        default="draft",
        required=True,
        copy=False,
        readonly=True,
        tracking=True,
    )
    is_pending = fields.Selection(
        [("yes", "Yes"), ("no", "No")],
        string="Is Pending?",
        readonly=True,
    )
    point = fields.Char(string="Point", required=True, tracking=True)
    location = fields.Char(string="Location")
    report = fields.Char(string="Report")
    collection_date = fields.Datetime(
        string="Collection Date", required=True, tracking=True
    )
    reception_date = fields.Date(string="Reception Date")
    delivery_forecast = fields.Date(
        string="Delivery Forecast", required=True, tracking=True
    )
    lab_submission_date = fields.Date(string="Lab Submission Date")
    depth = fields.Char(string="Depth")
    budget = fields.Monetary(currency_field="currency_id", string="Budget", default=0.0)
    billing = fields.Monetary(
        currency_field="currency_id",
        string="Billing",
        related="purchase_order_id.amount_total",
        store=True,
        default=0.0,
    )
    purchase_order_id = fields.Many2one(
        comodel_name="purchase.order", string="Purchase Order"
    )
    parameter_group_ids = fields.Many2many(
        comodel_name="lab.parameter.group", string="Parameters Groups"
    )
    parameter_ids = fields.Many2many(comodel_name="lab.parameter", string="Parameters")

    @api.model
    def create(self, vals):
        record = super(LabSample, self).create(vals)
        record.number = self.env["ir.sequence"].next_by_code("lab.sample")

        tracked_fields = self._get_tracked_fields()
        initial_values = {record.id: {}}
        for field_name in tracked_fields:
            if field_name in vals:
                initial_values[record.id][field_name] = False

        record.message_track(tracked_fields, initial_values)

        return record

    @api.depends("number", "company_id", "point", "depth", "collection_date")
    def _compute_name(self):
        for sample in self:
            if (
                sample.number
                and sample.company_id
                and sample.point
                and sample.id
                and sample.collection_date
            ):
                point = sample.point
                depth = sample.depth
                year = sample.collection_date.strftime("%y")
                company_name = sample.company_id.name.split(" ")[0].upper()
                number = sample.number
                if depth:
                    sample.name = f"{point}/{depth}/{year}/{company_name}/{number}"
                else:
                    sample.name = f"{point}/{year}/{company_name}/{number}"

    def action_confirm(self):
        for sample in self:
            sample.status = "open"

    def action_draft(self):
        for sample in self:
            sample.status = "draft"

    def action_cancel(self):
        for sample in self:
            sample.status = "cancel"

    def action_received(self):
        for sample in self:
            if sample.location:
                sample.status = "received"
            else:
                raise ValidationError(_("The location field must be filled in."))

    def action_publish(self):
        for sample in self:
            if sample.location and sample.report:
                sample.status = "published"
            else:
                raise ValidationError(
                    _("The location and report fields must be filled in.")
                )

    def action_pending(self):
        for sample in self:
            sample.status = "pending"
            sample.is_pending = "yes"

    def action_done(self):
        for sample in self:
            sample.status = "done"
            sample.is_pending = "no"

    @api.onchange("parameter_group_ids")
    def _onchange_parameter_group_ids(self):
        if self.parameter_group_ids:
            self.parameter_ids = self.env["lab.parameter"].search(
                [
                    ("group_id", "in", self.parameter_group_ids.ids),
                ]
            )
        else:
            self.parameter_ids = None
