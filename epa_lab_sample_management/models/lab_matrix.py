# Copyright 2024 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class LabMatrix(models.Model):

    _name = "lab.matrix"
    _description = "Lab Matrix"

    name = fields.Char(required=True)
