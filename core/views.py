from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Cardapio
from .forms import CardapioForm

# --- CONFIGURAÇÃO DE ALUNOS (FAKE SUAP) ---
ALUNOS_SUAP = {
    '2022111500': {'nome': 'Stephanny Borges', 'curso': 'Informática para Internet', 'foto': 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png'},
    '20221110040': {'nome': 'João Pedro', 'curso': 'Edificações', 'foto': 'https://cdn-icons-png.flaticon.com/512/3135/3135768.png'}
}

# 1. TELA DE LOGIN (Mostra o formulário)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    # Se já tiver o cookie do aluno, joga direto pro cardápio
    if 'iflanche_matricula' in request.COOKIES:
        return redirect('cardapio_aluno')
        
    return render(request, 'core/login.html')

# 2. PROCESSAR LOGIN DO ALUNO (ROTA ESPECÍFICA)
def processar_login_aluno(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        
        # Pega dados ou usa genérico
        dados = ALUNOS_SUAP.get(matricula, {
            'nome': 'Aluno(a)', 'curso': 'Integrado', 'foto': 'https://cdn-icons-png.flaticon.com/512/847/847969.png'
        })
        
        # FORÇA O REDIRECIONAMENTO PARA A PÁGINA NOVA
        response = redirect('cardapio_aluno')
        
        # Salva o cookie
        response.set_cookie('iflanche_matricula', matricula)
        response.set_cookie('iflanche_nome', dados['nome'])
        response.set_cookie('iflanche_curso', dados['curso'])
        response.set_cookie('iflanche_foto', dados['foto'])
        return response
        
    return redirect('login') # Se tentar entrar sem POST, volta pro login

# 3. PROCESSAR LOGIN DO SERVIDOR (CORRIGIDO)
def processar_login_servidor(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        senha = request.POST.get('password')
        
        # Tenta verificar se o usuário e senha existem no banco
        user = authenticate(request, username=usuario, password=senha)
        
        if user is not None:
            # SUCESSO: Faz o login do admin
            login(request, user)
            
            # Cria a resposta de redirecionamento para o painel
            response = redirect('admin_dashboard')
            
            # LIMPEZA IMPORTANTE:
            # Se entrou como admin, apagamos o cookie de aluno para evitar conflitos
            response.delete_cookie('iflanche_matricula')
            response.delete_cookie('iflanche_nome')
            response.delete_cookie('iflanche_curso')
            response.delete_cookie('iflanche_foto')
            
            return response
        else:
            # ERRO: Senha ou usuário errados
            # Renderiza a página de login novamente, mas enviando um aviso de erro
            # E força a aba 'servidor' a ficar aberta (se você ajustar o HTML depois, mas o erro já ajuda)
            return render(request, 'core/login.html', {
                'erro': 'Usuário ou senha incorretos. Tente novamente.',
                'aba_ativa': 'servidor' # Vamos usar isso no HTML opcionalmente
            })
            
    return redirect('login')

# 4. PÁGINA DO CARDÁPIO (EXCLUSIVA DO ALUNO)
def cardapio_aluno(request):
    # Se não tiver cookie, manda logar
    if 'iflanche_matricula' not in request.COOKIES:
        return redirect('login')
        
    itens = Cardapio.objects.all()
    dados_aluno = {
        'nome': request.COOKIES.get('iflanche_nome'),
        'foto': request.COOKIES.get('iflanche_foto'),
        'matricula': request.COOKIES.get('iflanche_matricula'),
        'curso': request.COOKIES.get('iflanche_curso'),
    }
    return render(request, 'core/cardapio_aluno.html', {'cardapio': itens, 'aluno': dados_aluno})

# 5. PERFIL DO ALUNO
def perfil_aluno(request):
    dados_aluno = {
        'nome': request.COOKIES.get('iflanche_nome'),
        'foto': request.COOKIES.get('iflanche_foto'),
        'matricula': request.COOKIES.get('iflanche_matricula'),
        'curso': request.COOKIES.get('iflanche_curso'),
    }
    return render(request, 'core/perfil.html', dados_aluno)

# 6. LOGOUT
def logout_view(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('iflanche_matricula')
    response.delete_cookie('iflanche_nome')
    response.delete_cookie('iflanche_curso')
    response.delete_cookie('iflanche_foto')
    return response

# 7. ADMINISTRAÇÃO (MANTIDO)
@login_required(login_url='login')
def admin_dashboard(request):
    itens = Cardapio.objects.all()
    form = CardapioForm()
    return render(request, 'core/admin.html', {'cardapio': itens, 'form': form})

@login_required
def salvar_refeicao(request):
    form = CardapioForm(request.POST)
    if form.is_valid(): form.save()
    return redirect('admin_dashboard')

@login_required
def deletar_refeicao(request, id):
    get_object_or_404(Cardapio, id=id).delete()
    return redirect('admin_dashboard')
