from odoo import fields, models


class Laboratorios(models.Model):
    _name = "laboratorios.laboratorio"

    nome = fields.Char("Nome do Laboratório", required=True)

    def name_get(self, context=None):
        if context == None:
            context = {}
        result = []
        if context.get("custom_display_name", "labnomes"):
            for rec in self:
                result.append((rec.id, rec.nome))
            return result
        return result
