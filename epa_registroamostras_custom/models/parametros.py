from odoo import fields, models


class Testes(models.Model):
    _name = "amostra.parametros"

    nome = fields.Char("Parametro", required=True)

    filtros = fields.Many2many("filtros.table", string="Filtros")

    # @api.model
    # def create(self, vals):
    #     obj = super(Testes, self).create(vals)
    #     print(self.filtros)
    #     if self.filtros == None:
    #         obj.write({'filtros': ""})
    #     return obj

    def name_get(self, context=None):
        if context == None:
            context = {}
        result = []
        if context.get("custom_display_name", "testesnomes"):
            for rec in self:
                result.append((rec.id, rec.nome))
            return result
        return result


class Filtros(models.Model):
    _name = "filtros.table"

    filtro = fields.Char(string="Grupo Customizado")
