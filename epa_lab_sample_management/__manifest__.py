# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "EPA Lab Sample Management",
    "summary": """
        Management of Laboratories Samples""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/epa-addons",
    "depends": ["project", "hr", "purchase"],
    "data": [
        "views/lab_matrix.xml",
        "views/lab_parameter_group.xml",
        "views/lab_parameter.xml",
        "views/lab_sample.xml",
        "views/menuitem.xml",
        "views/res_partner.xml",
        "wizard/lab_sample_replicate_wizard.xml",
        "security/lab_sample_security.xml",
        "security/ir.model.access.csv",
        "data/sequence.xml",
    ],
    "demo": [],
}
