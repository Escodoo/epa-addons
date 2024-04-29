# Copyright 2024 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields, models


class HrEmployeePublic(models.Model):
    _inherit = "hr.employee.public"

    # TODO: Include this field to allow public users to access hr_attendances_overtime.
    # This needs to be reviewed later due to its implications.
    attendance_sheet_id = fields.Many2one(
        "hr.attendance.sheet", string="Attendance Sheet"
    )
