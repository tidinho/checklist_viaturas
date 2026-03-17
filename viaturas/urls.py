from django.urls import path
from .views import cadastro_policial, LoginView, LogoutView, ViaturaView, ChecklistView,EditarViaturaView , ExcluirViaturaView, gerar_pdf
from . import views

urlpatterns = [
    path("cadastro/", cadastro_policial, name="cadastro_policial"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("viaturas/", ViaturaView.as_view(), name="viaturas"),
    path("checklist/", ChecklistView.as_view(), name="checklist"),
    path("checklist/editar/<int:pk>/", EditarViaturaView.as_view(), name="editar_viatura"),
    path("checklist/excluir/<int:pk>/", ExcluirViaturaView.as_view(), name="excluir_viatura"),
    path("checklist/pdf/<int:checklist_id>/", gerar_pdf, name="gerar_pdf"),
    path('foto/<int:pk>/metadados/', views.metadados_foto, name='metadados_foto'),

]