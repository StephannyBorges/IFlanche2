import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Cardapio
from .forms import CardapioForm
from .forms import AlunoPerfilForm
from .models import Aluno


# --- CONFIGURAÇÕES DO SUAP (Preencha com seus dados reais!) ---
SUAP_CLIENT_ID = 'SEU_CLIENT_ID_AQUI'  # <--- Pegue isso no admin do SUAP
SUAP_CLIENT_SECRET = 'SEU_CLIENT_SECRET_AQUI' # <--- Pegue isso no admin do SUAP
SUAP_REDIRECT_URI = 'http://127.0.0.1:8000/suap-callback/' # <--- Tem que ser EXATO
SUAP_AUTH_URL = 'https://suap.ifrn.edu.br/o/authorize/'
SUAP_TOKEN_URL = 'https://suap.ifrn.edu.br/o/token/'
SUAP_USER_INFO_URL = 'https://suap.ifrn.edu.br/api/eu/'

# --- 1. LOGIN PRINCIPAL ---
def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        usuario = request.POST.get('username')
        senha = request.POST.get('password')
        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'core/login.html', {'erro': 'Usuário ou senha incorretos'})
    
    return render(request, 'core/login.html')

# --- SUBTITUA AQUELA PARTE DO SUAP NO SEU VIEWS.PY POR ISSO ---

# --- SIMULADOR DE SUAP (Coloque isso no views.py) ---

def suap_login_view(request):
    if request.method == 'POST':
        # Quando o usuário clica em "Acessar" na tela falsa do SUAP
        matricula = request.POST.get('usuario')
        
        # Simula o login com sucesso
        response = redirect('index')
        response.set_cookie('iflanche_matricula', matricula)
        response.set_cookie('iflanche_nome', 'Aluno Simulado')
        return response
    
    # Se for GET, mostra a tela falsa
    return render(request, 'core/suap.html')

def suap_callback(request):
    # Essa rota não será usada no modo Fake, 
    # pois o form do suap_fake.html vai postar para si mesmo.
    pass 

# --- Adicione essa lógica nova para tratar o POST do Fake SUAP ---
def fake_suap_post(request):
    if request.method == 'POST':
        # Aqui a gente finge que validou a senha
        matricula_digitada = request.POST.get('usuario')
        
        # Redireciona para o App logado
        response = redirect('index')
        
        # Salva o cookie para o sistema saber quem é
        response.set_cookie('iflanche_matricula', matricula_digitada)
        response.set_cookie('iflanche_nome', 'Aluno Teste (Simulação)')
        
        return response

# --- 4. LOGOUT ---
def logout_view(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('iflanche_matricula')
    response.delete_cookie('iflanche_nome')
    return response

# --- 5. PAINEL DO ALUNO ---
def index(request):
    itens_cardapio = Cardapio.objects.all()
    
    # --- LÓGICA HÍBRIDA (BANCO + COOKIE) ---
    
    contexto = {
        'cardapio': itens_cardapio,
        'matricula_contexto': 'Visitante',
        'nome_contexto': '',
        'curso_contexto': 'Faça Login',
        'foto_perfil_url': None # Novo campo para a foto
    }

    # CENÁRIO 1: Usuário logado de verdade (Django Auth)
    if request.user.is_authenticated:
        contexto['matricula_contexto'] = request.user.username
        contexto['nome_contexto'] = request.user.first_name or request.user.username
        
        # Tenta pegar dados extras do Aluno (Foto e Curso)
        try:
            # O 'hasattr' evita erro se o aluno não tiver perfil
            if hasattr(request.user, 'aluno'): 
                contexto['foto_perfil_url'] = request.user.aluno.foto_perfil.url if request.user.aluno.foto_perfil else None
                # Se você salvou curso no banco, pegue aqui: aluno.curso
        except:
            pass

        # Lógica do Curso pela matrícula (User real)
        if '111' in request.user.username: contexto['curso_contexto'] = 'Info. Internet'
        elif '114' in request.user.username: contexto['curso_contexto'] = 'Meio Ambiente'
        elif '101' in request.user.username: contexto['curso_contexto'] = 'Edificações'
        else: contexto['curso_contexto'] = 'Integrado'

    # CENÁRIO 2: Usuário do "SUAP Fake" (Apenas Cookie, sem banco)
    elif 'iflanche_matricula' in request.COOKIES:
        matricula = request.COOKIES.get('iflanche_matricula')
        contexto['matricula_contexto'] = matricula
        contexto['nome_contexto'] = request.COOKIES.get('iflanche_nome')
        
        if '111' in matricula: contexto['curso_contexto'] = 'Info. Internet'
        elif '114' in matricula: contexto['curso_contexto'] = 'Meio Ambiente'
        elif '101' in matricula: contexto['curso_contexto'] = 'Edificações'
        else: contexto['curso_contexto'] = 'Integrado'

    return render(request, 'core/index.html', context=contexto)

    # Lógica simples de curso baseada na matrícula
    if matricula_aluno == 'Visitante':
        curso_nome = 'Faça Login'
    elif '111' in matricula_aluno:
        curso_nome = 'Info. Internet'
    elif '114' in matricula_aluno:
        curso_nome = 'Meio Ambiente'
    else:
        curso_nome = 'Integrado'

    return render(request, 'core/index.html', {
        'cardapio': itens_cardapio,
        'matricula_contexto': matricula_aluno,
        'nome_contexto': nome_aluno,
        'curso_contexto': curso_nome
    })

# --- ROTAS ADMIN (Mantidas iguais) ---
@login_required(login_url='login')
def admin_dashboard(request):
    itens_cardapio = Cardapio.objects.all()
    form = CardapioForm()
    return render(request, 'core/admin.html', {'cardapio': itens_cardapio, 'form': form, 'user': request.user})

@login_required(login_url='login')
def salvar_refeicao(request):
    if request.method == "POST":
        id_refeicao = request.POST.get('id_refeicao')
        if id_refeicao:
            refeicao = get_object_or_404(Cardapio, id=id_refeicao)
            form = CardapioForm(request.POST, instance=refeicao)
        else:
            form = CardapioForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('admin_dashboard')

@login_required(login_url='login')
def deletar_refeicao(request, id):
    refeicao = get_object_or_404(Cardapio, id=id)
    refeicao.delete()
    return redirect('admin_dashboard')

@login_required
def editar_perfil(request):
    # Tenta pegar o perfil do aluno, se não existir, cria um vazio agora mesmo
    aluno, created = Aluno.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        form = AlunoPerfilForm(request.POST, request.FILES, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect('index') # Volta para a página inicial
    else:
        form = AlunoPerfilForm(instance=aluno)

    return render(request, 'editar_perfil.html', {'form': form, 'aluno': aluno})

@login_required
def redirecionar_pos_login(request):
    user = request.user
    if user.is_staff or user.is_superuser:
        return redirect('/painel_servidor/') 
    
    elif user.groups.filter(name='Nutricionistas').exists():
        return redirect('/admin/') 

    else:
        return redirect('index') 
    
@login_required
def painel_servidor(request):
    return render(request, 'core/admin.html')