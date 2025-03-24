# Copyright 2025 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Job(models.Model):

    _inherit = "hr.job"

    epa_required_education_formation = fields.Many2many(
        comodel_name="epa_hr.required.education",
        string="Required Education / Formation",
    )
    epa_required_knowledge = fields.Many2many(
        comodel_name="epa_hr.required.knowledge",
        string="Required Knowledge",
    )
    epa_nr_compliance = fields.Many2many(
        comodel_name="epa_hr.nr.compliance",
        string="NR Compliance",
    )
    epa_administrative_procedure = fields.Many2many(
        comodel_name="epa_hr.administrative.procedure",
        string="Administrative Procedure",
    )
    epa_management_procedure = fields.Many2many(
        comodel_name="epa_hr.management.procedure",
        string="Management Procedure",
    )
    epa_operational_procedure = fields.Many2many(
        comodel_name="epa_hr.operational.procedure",
        string="Operational Procedure",
    )
    epa_safety_procedure = fields.Many2many(
        comodel_name="epa_hr.safety.procedure",
        string="Safety Procedure",
    )
    epa_technical_procedure = fields.Many2many(
        comodel_name="epa_hr.technical.procedure",
        string="Technical Procedure",
    )
    epa_technical_instruction = fields.Many2many(
        comodel_name="epa_hr.technical.instruction",
        string="Technical Instruction",
    )
    epa_skills_behavior = fields.Many2many(
        comodel_name="epa_hr.skills.behavior",
        string="Skills / Behavior",
    )
    epa_salary_currency = fields.Many2one(
        comodel_name="res.currency",
        string="Salary Currency",
        default=lambda self: self.env.company.currency_id,
    )
    epa_salary = fields.Monetary(
        currency_field="epa_salary_currency",
        string="Salary",
    )
    epa_responsibilities = fields.Text(string="Responsibilities")


class RequiredEducation(models.Model):

    _name = "epa_hr.required.education"
    _description = "Required Education / Formation"

    name = fields.Char(string="Required Education / Formation")


class RequiredKnowledge(models.Model):

    _name = "epa_hr.required.knowledge"
    _description = "Required Knowledge"

    name = fields.Char(string="Required Knowledge")


class NRCompliance(models.Model):

    _name = "epa_hr.nr.compliance"
    _description = "NR Compliance"

    name = fields.Char(string="NR Compliance")


class AdministrativeProcedure(models.Model):

    _name = "epa_hr.administrative.procedure"
    _description = "Administrative Procedure"

    name = fields.Char(string="Administrative Procedure")


class ManagementProcedure(models.Model):

    _name = "epa_hr.management.procedure"
    _description = "Management Procedure"

    name = fields.Char(string="Management Procedure")


class OperationalProcedure(models.Model):

    _name = "epa_hr.operational.procedure"
    _description = "Operational Procedure"

    name = fields.Char(string="Operational Procedure")


class SafetyProcedure(models.Model):

    _name = "epa_hr.safety.procedure"
    _description = "Safety Procedure"

    name = fields.Char(string="Safety Procedure")


class TechnicalProcedure(models.Model):

    _name = "epa_hr.technical.procedure"
    _description = "Technical Procedure"

    name = fields.Char(string="Technical Procedure")


class TechnicalInstruction(models.Model):

    _name = "epa_hr.technical.instruction"
    _description = "Technical Instruction"

    name = fields.Char(string="Technical Instruction")


class SkillsBehavior(models.Model):

    _name = "epa_hr.skills.behavior"
    _description = "Skills / Behavior"

    name = fields.Char(string="Skills / Behavior")
