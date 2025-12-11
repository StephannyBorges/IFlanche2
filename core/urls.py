from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('suap-auth/', views.suap_login_view, name='suap_login'),
    path('suap-callback/', views.suap_callback, name='suap_callback'), # <--- NOVA ROTA OBRIGATÓRIA
    path('logout/', views.logout_view, name='logout'),
    path('aluno/', views.index, name='index'),
    path('gerenciar/', views.admin_dashboard, name='admin_dashboard'),
    path('salvar/', views.salvar_refeicao, name='salvar_refeicao'),
    path('deletar/<int:id>/', views.deletar_refeicao, name='deletar_refeicao'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('redirecionar/', views.redirecionar_pos_login, name='redirecionar_login'),
    path('painel_servidor/', views.painel_servidor, name='painel_servidor'),
]