# Copyright 2024 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class Attendancesheet(models.Model):
    _name = "hr.attendance.sheet"
    _inherit = ["hr.attendance.sheet", "tier.validation"]
    _state_from = ["confirm"]
    _state_to = ["approved"]

    _tier_validation_manual_config = False
