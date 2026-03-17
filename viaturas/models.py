from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Viatura(models.Model):
    modelo = models.CharField(max_length=50, default="Desconhecido")
    prefixo = models.CharField(max_length=20)
    placa = models.CharField(max_length=10)
    km = models.IntegerField()
    foto = models.ImageField(upload_to="viaturas/", blank=True, null=True)

    def __str__(self):
        return f"{self.prefixo} - {self.placa}"


STATUS_CHOICES = [
    ("ok", "OK"),
    ("nao_possui", "Não possui"),
    ("alteracao", "Alteração"),
]


TROCA_OLEO_CHOICES = [
    ("sim", "Sim"),
    ("nao", "Não"),
]


class Checklist(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Policial"
    )

    viatura = models.ForeignKey(
        Viatura,
        on_delete=models.CASCADE
    )

    km_atual = models.IntegerField(
        verbose_name="KM Atual da Viatura",
        null=True,
        blank=True
    )

    km_troca_oleo = models.IntegerField(
        verbose_name="KM da Próxima Troca de Óleo",
        null=True,
        blank=True
    )

    troca_oleo = models.CharField(
        max_length=3,
        choices=TROCA_OLEO_CHOICES,
        default="nao",
        verbose_name="Troca de óleo"
    )

    triangulo = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    chave_roda = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    estepe = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    kit_ferramenta_estepe = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    macaco = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    extintor = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    baterias = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    cartao_abastecimento = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")

    sistema_iluminacao = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    sistema_sinalizacao = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    retrovisores = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    estribo = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    intermitente = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    radio_comunicacao = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    tapetes = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    equipamento_som = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    quebra_mato = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    cinto_seguranca = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    direcao = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    calotas = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    palheta_limpador = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    painel = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    ignicao = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    ar_condicionado = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    manuais = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")

    sistema_motor = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    sistema_injecao = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    sistema_refrigeracao = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    chave_ignicao = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    botoes_vidro = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    tablet = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")
    drive = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ok")

    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.viatura} - {self.usuario} - {self.data}"


class ChecklistFoto(models.Model):

    checklist = models.ForeignKey(
        Checklist,
        on_delete=models.CASCADE,
        related_name="fotos"
    )

    imagem = models.ImageField(upload_to="checklist/")

    def save(self, *args, **kwargs):

        if self.checklist.fotos.count() >= 10:
            raise ValidationError("Não é permitido mais de 10 fotos por checklist")

        super().save(*args, **kwargs)