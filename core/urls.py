from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    
    # Rota específica que recebe o POST do formulário do aluno
    path('entrar-aluno/', views.processar_login_aluno, name='processar_login_aluno'),
    
    # Rota específica que recebe o POST do servidor
    path('entrar-servidor/', views.processar_login_servidor, name='processar_login_servidor'),
    
    # A página nova que você pediu
    path('cardapio-semanal/', views.cardapio_aluno, name='cardapio_aluno'),
    
    path('perfil/', views.perfil_aluno, name='perfil'),
    path('logout/', views.logout_view, name='logout'),
    
    # Admin
    path('admin-painel/', views.admin_dashboard, name='admin_dashboard'),
    path('salvar/', views.salvar_refeicao, name='salvar_refeicao'),
    path('deletar/<int:id>/', views.deletar_refeicao, name='deletar_refeicao'),
]
