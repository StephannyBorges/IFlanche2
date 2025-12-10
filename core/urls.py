from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), # Nova rota
    path('aluno/', views.index, name='index'),
    path('gerenciar/', views.admin_dashboard, name='admin_dashboard'),
    path('salvar/', views.salvar_refeicao, name='salvar_refeicao'),
    path('deletar/<int:id>/', views.deletar_refeicao, name='deletar_refeicao'),
]