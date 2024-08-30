# Copyright 2024 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class LabSampleReplicateWizard(models.TransientModel):

    _name = "lab.sample.replicate.wizard"
    _description = "Lab Sample Replicate Wizard"

    quantity = fields.Integer(
        string="Number of Copies",
        required=True,
        default=2,
    )

    def action_replicate_lab_sample(self):
        sample_ids = []
        active_ids = self.env.context.get("active_ids")
        for active_id in active_ids:
            for _quantity in range(self.quantity):
                sample_id = self.env["lab.sample"].browse(active_id)
                sample_id_link = (
                    "<a href=# data-oe-model=lab.sample data-oe-id={}>{}</a>".format(
                        sample_id.id, sample_id.name
                    )
                )
                copy_sample_id = sample_id.copy()
                copy_sample_id.message_post(
                    body=_("This sample is a copy of " + sample_id_link)
                )
                sample_ids.append(copy_sample_id.id)

        result = self.env["ir.actions.act_window"]._for_xml_id(
            "epa_lab_sample_management.lab_sample_act_window"
        )
        result["domain"] = [("id", "in", sample_ids)]
        return result
