# Copyright 2024 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class LabParameter(models.Model):

    _name = "lab.parameter"
    _description = "Lab Parameter"

    name = fields.Char("Name", required=True)
    group_id = fields.Many2one(
        comodel_name="lab.parameter.group",
        string="Parameter Group",
    )
