# Copyright 2024 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class LabParameterGroup(models.Model):

    _name = "lab.parameter.group"
    _description = "Lab Parameter Group"

    name = fields.Char(string="Name", required=True)
