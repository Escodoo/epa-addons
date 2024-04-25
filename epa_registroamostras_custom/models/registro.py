from odoo import api, fields, models


class RegistroAmostras(models.Model):
    _name = "regamostras.amostra"

    laboratorio = fields.Many2one(
        "res.partner", string="Laboratório", required=True
    )  # Base

    projeto = fields.Many2one(
        "project.project", string="Projeto", required=True
    )  # Base (seleciona o cliente a partir disso)

    cliente = fields.Many2one("res.users", string="Cliente", required=True)  # Base

    ponto = fields.Char(string="Ponto", required=True)

    matriz = fields.Selection(
        [
            ("agua_sub", "Água Subterrâneas"),
            ("agua_super", "Água Superficial"),
            ("efluente_ind", "Efluente industrial"),
            ("efleunte_liq", "Efluente líquido"),
            ("lodo", "Lolo"),
            ("solo", "Solo"),
        ],
        string="Matriz",
        required=True,
    )

    grupo = fields.Char(string="Grupo do Parâmetro")  # Mudar para Many2one (?) Base?

    profundidade = fields.Char(
        string="Profundidade (cm)", default="0"
    )  # Definir unidade de medida padrão

    laudo = fields.Char(string="Laudo")

    orcamento = fields.Float(string="Orçamento")  # !!! Mudar para Monetário

    faturamento = fields.Float(string="Faturamento")  # !!! Mudar para Monetário

    funcionario = fields.Many2one(
        "hr.employee", string="Funcionário", required=True
    )  # Base

    localizacao = fields.Char(string="Localização")

    parametros = fields.Many2many("amostra.parametros", string="Parâmetros")

    data_coleta = fields.Date(string="Data da coleta", required=True)

    data_recebimento = fields.Date(string="Data de recebimento")

    previsao_entrega = fields.Date(string="Previsão entrega")

    data_envio = fields.Date(string="Envio ao laboratório")

    data_criacao = fields.Datetime(
        string="Criação do registro", default=lambda self: fields.datetime.now()
    )

    pendencia_sim = fields.Boolean(string="Sim")

    pendencia_nao = fields.Boolean(string="Não")

    status = fields.Selection(
        [
            ("aberto", "Aberto"),
            ("recebido", "Recebido"),  # Confirmação de Recebimento do Laboratório
            ("publicado", "Laudo Publicado"),
            ("pendente", "Pendente"),
            ("concluido", "Concluído"),
        ],
        string="Status",
        required=True,
        default="aberto",
    )

    @api.onchange("pendencia_sim", "pendencia_nao", "localizacao", "laudo")
    def _onchange_status(self):
        if (
            self.pendencia_nao
            and self.pendencia_sim
            and self.laudo
            and self.localizacao == ""
        ):
            self.status = "aberto"
        elif self.pendencia_nao:
            self.status = "concluido"
        elif self.pendencia_sim:
            self.status = "pendente"
        elif self.laudo:
            self.status = "publicado"
        elif self.localizacao:
            self.status = "recebido"
        else:
            self.status = "aberto"

    @api.onchange("pendencia_nao")
    def _onchange_pendencia_nao(self):
        if self.pendencia_nao:
            self.pendencia_sim = ""

    @api.onchange("pendencia_sim")
    def _onchange_pendencia_sim(self):
        if self.pendencia_sim:
            self.pendencia_nao = ""

    @api.onchange("matriz")
    def onchange_matriz(self):
        if self.matriz != "solo":
            self.profundidade = "0"

    # Função para ID sequencial da amostra

    @api.depends("ponto")
    def _compute_id_no(self):
        for each in self:
            if each.ponto == "Ponto":
                temp = ""
            else:
                temp = str(each.ponto) + "/"

            # pode mudar pra sempre exibir x casas ou x algarismos ----- DEFINIR UNIDADE DO SISTEMA (EXIBIR NA MENOR UNIDADE POSSIVEL PARA RETIRAR VIRGULA)
            temp += str(each.profundidade) + "/"

            data_list = str(each.data_coleta).split("-")
            data_temp = data_list[0][2:4]

            each.id_no = temp + data_temp + "/EPA/" + str(each.id)
        print(len(self))

    id_no = fields.Char(compute="_compute_id_no")
