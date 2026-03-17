from django.views.generic import TemplateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils.timezone import localtime
from django.conf import settings

from .mixins import AdminRequiredMixin
from .models import ChecklistFoto, Viatura, Checklist
from .forms import ViaturaForm, ChecklistForm
from .utils import extrair_metadados

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from django.contrib.auth.models import User
from django.contrib import messages

import os


from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect


def cadastro_policial(request):

    if request.method == "POST":

        username = request.POST.get("username")
        nome_guerra = request.POST.get("nome_guerra")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "As senhas não conferem")
            return redirect("cadastro_policial")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Usuário já existe")
            return redirect("cadastro_policial")

        user = User.objects.create_user(
            username=username,
            password=password
        )

        # salva o nome de guerra no first_name
        user.first_name = nome_guerra
        user.save()

        messages.success(request, "Usuário cadastrado com sucesso!")
        return redirect("login")

    return render(request, "viaturas/cadastro_policial.html")

# ===============================
# LOGIN / LOGOUT
# ===============================

class LoginView(View):
    template_name = "viaturas/login.html"

    def get(self, request):
        return render(request, self.template_name, {"errors": False})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("viaturas" if user.is_staff else "checklist")

        return render(request, self.template_name, {"errors": True})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")


# ===============================
# VIATURAS
# ===============================

class ViaturaView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = "viaturas/viaturas.html"
    login_url = "login"

    def get(self, request):
        form = ViaturaForm()
        lista_viaturas = Viatura.objects.all().order_by("prefixo")
        paginator = Paginator(lista_viaturas, 5)
        page_number = request.GET.get("page")
        viaturas = paginator.get_page(page_number)
        return render(request, self.template_name, {"form": form, "viaturas": viaturas})

    def post(self, request):
        form = ViaturaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "🚓 Viatura cadastrada com sucesso!")
        return redirect("viaturas")


class EditarViaturaView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Viatura
    form_class = ViaturaForm
    template_name = "viaturas/editar_viatura.html"
    success_url = reverse_lazy("viaturas")

    def form_valid(self, form):
        messages.success(self.request, "✏️ Viatura editada com sucesso!")
        return super().form_valid(form)


class ExcluirViaturaView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Viatura
    template_name = "viaturas/confirmar_exclusao.html"
    success_url = reverse_lazy("viaturas")

    def form_valid(self, form):
        messages.success(self.request, "🗑️ Viatura excluída com sucesso!")
        return super().form_valid(form)


# ===============================
# CHECKLIST
# ===============================

class ChecklistView(LoginRequiredMixin, TemplateView):
    template_name = "viaturas/checklist.html"
    login_url = "login"

    def get(self, request, *args, **kwargs):
        form = ChecklistForm()
        if request.user.is_staff:
            lista_checklists = Checklist.objects.all().order_by("-data")
        else:
            lista_checklists = Checklist.objects.filter(usuario=request.user).order_by("-data")

        paginator = Paginator(lista_checklists, 5)
        page_number = request.GET.get("page")
        checklists = paginator.get_page(page_number)

        return render(request, self.template_name, {"form": form, "checklists": checklists})

    def post(self, request, *args, **kwargs):
        form = ChecklistForm(request.POST, request.FILES)
        if form.is_valid():
            checklist = form.save(commit=False)
            checklist.usuario = request.user
            checklist.save()

            fotos = request.FILES.getlist("fotos")
            for foto in fotos:
                try:
                    ChecklistFoto.objects.create(checklist=checklist, imagem=foto)
                except ValidationError as e:
                    messages.error(request, str(e))
                    break

            messages.success(request, "✅ Checklist realizado com sucesso!")
        else:
            messages.error(request, form.errors)

        return redirect("checklist")


# ===============================
# RODAPÉ PDF
# ===============================

def rodape(canvas, doc):
    canvas.saveState()
    data = localtime(doc.checklist.data).strftime("%d/%m/%Y %H:%M") if doc.checklist.data else ""
    texto = f"Sistema de Gestão de Viaturas - PMCE | Checklist realizado em: {data}"
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(10.5 * cm, 1 * cm, texto)
    canvas.restoreState()


# ===============================
# GERAR PDF
# ===============================

@login_required
def gerar_pdf(request, checklist_id):
    checklist = get_object_or_404(Checklist, id=checklist_id)

    if not request.user.is_staff and checklist.usuario != request.user:
        return HttpResponse("Sem permissão", status=403)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="checklist_{checklist.id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    doc.checklist = checklist
    styles = getSampleStyleSheet()
    elementos = []

    # Logo e cabeçalho
    logo_path = os.path.join(settings.BASE_DIR, "viaturas", "static", "imagens", "logo_pmce.png")
    if os.path.exists(logo_path):
        logo = Image(logo_path)
        logo.drawHeight = 3 * cm
        logo.drawWidth = 3 * cm
        texto = Paragraph(
            "<b>POLÍCIA MILITAR DO CEARÁ</b><br/>3º BATALHÃO DE POLÍCIA MILITAR<br/>SOBRAL - CE",
            styles["Normal"]
        )
        tabela_cabecalho = Table([[logo, texto]], colWidths=[4*cm, 12*cm])
        tabela_cabecalho.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
        elementos.append(tabela_cabecalho)

    elementos.append(Spacer(1,20))
    elementos.append(Paragraph("RELATÓRIO DE CHECKLIST DE VIATURA", styles["Title"]))
    elementos.append(Spacer(1,15))
    elementos.append(Paragraph(f"<b>VIATURA PREFIXO: {checklist.viatura.prefixo}</b>", styles["Heading1"]))
    elementos.append(Spacer(1,10))

    numero_relatorio = str(checklist.id).zfill(5)
    elementos.append(Paragraph(f"<b>Relatório nº:</b> {numero_relatorio}", styles["Normal"]))
    elementos.append(Spacer(1,15))

    data_formatada = localtime(checklist.data).strftime("%d/%m/%Y %H:%M") if checklist.data else ""
    elementos.append(Paragraph(f"<b>Policial:</b> {checklist.usuario}", styles["Normal"]))
    elementos.append(Paragraph(f"<b>Viatura:</b> {checklist.viatura}", styles["Normal"]))
    elementos.append(Paragraph(f"<b>KM Atual:</b> {checklist.km_atual}", styles["Normal"]))
    elementos.append(Paragraph(f"<b>KM Próxima Troca de Óleo:</b> {checklist.km_troca_oleo}", styles["Normal"]))
    elementos.append(Paragraph(f"<b>Data do Checklist:</b> {data_formatada}", styles["Normal"]))
    elementos.append(Spacer(1,20))

    # Tabela de itens
    dados = [
        ["Item", "Status"],
        ["Triângulo", checklist.triangulo],
        ["Chave de Roda", checklist.chave_roda],
        ["Estepe", checklist.estepe],
        ["Kit Ferramenta", checklist.kit_ferramenta_estepe],
        ["Macaco", checklist.macaco],
        ["Extintor", checklist.extintor],
        ["Baterias", checklist.baterias],
        ["Cartão Abastecimento", checklist.cartao_abastecimento],
        ["Sistema Iluminação", checklist.sistema_iluminacao],
        ["Sistema Sinalização", checklist.sistema_sinalizacao],
        ["Retrovisores", checklist.retrovisores],
        ["Estribo", checklist.estribo],
        ["Intermitente", checklist.intermitente],
        ["Rádio Comunicação", checklist.radio_comunicacao],
        ["Tapetes", checklist.tapetes],
        ["Equipamento Som", checklist.equipamento_som],
        ["Quebra Mato", checklist.quebra_mato],
        ["Cinto Segurança", checklist.cinto_seguranca],
        ["Direção", checklist.direcao],
        ["Calotas", checklist.calotas],
        ["Palheta Limpador", checklist.palheta_limpador],
        ["Painel", checklist.painel],
        ["Ignição", checklist.ignicao],
        ["Ar Condicionado", checklist.ar_condicionado],
        ["Manuais", checklist.manuais],
        ["Sistema Motor", checklist.sistema_motor],
        ["Sistema Injeção", checklist.sistema_injecao],
        ["Sistema Refrigeração", checklist.sistema_refrigeracao],
        ["Chave Ignição", checklist.chave_ignicao],
        ["Botões Vidro", checklist.botoes_vidro],
        ["Tablet", checklist.tablet],
        ["Drive", checklist.drive],
    ]
    tabela = Table(dados, colWidths=[9*cm, 6*cm])
    tabela.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.grey),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),1,colors.black),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
    ]))
    elementos.append(tabela)
    elementos.append(Spacer(1,40))

    # Assinatura
    assinatura = Table([[""], ["Assinatura do Policial"]], colWidths=[8*cm])
    assinatura.setStyle(TableStyle([
        ("LINEABOVE",(0,0),(-1,0),1,colors.black),
        ("ALIGN",(0,1),(-1,1),"CENTER")
    ]))
    elementos.append(assinatura)

    # Fotos
    fotos = checklist.fotos.all()
    if fotos:
        elementos.append(PageBreak())
        elementos.append(Paragraph("FOTOS DO CHECKLIST", styles["Heading2"]))
        elementos.append(Spacer(1,20))
        linhas, linha = [], []
        for foto in fotos:
            caminho = foto.imagem.path
            if os.path.exists(caminho):
                img = Image(caminho)
                img.drawHeight = 6*cm
                img.drawWidth = 6*cm
                linha.append(img)
                if len(linha) == 2:
                    linhas.append(linha)
                    linha = []
        if linha:
            linhas.append(linha)
        tabela_fotos = Table(linhas, colWidths=[8*cm, 8*cm])
        elementos.append(tabela_fotos)

    doc.build(elementos, onFirstPage=rodape, onLaterPages=rodape)
    return response


# ===============================
# METADADOS DA FOTO
# ===============================

def metadados_foto(request, pk):
    foto = get_object_or_404(ChecklistFoto, pk=pk)
    dados = extrair_metadados(foto.imagem.path)
    return render(request, "viaturas/metadados_foto.html", {"foto": foto, "dados": dados})