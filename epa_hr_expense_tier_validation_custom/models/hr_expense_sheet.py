# Copyright 2024 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class HrExpenseSheet(models.Model):

    _inherit = "hr.expense.sheet"
    # Adapting state according to v12.0 usability
    _state_from = ["draft"]
    _state_to = ["submit", "approve", "post", "done"]
