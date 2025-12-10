from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Cardapio
from .forms import CardapioForm

def login_view(request):
    # ESPIÃO 1: Avisa que alguém tentou entrar na página
    print("--- ALGUÉM ACESSOU A TELA DE LOGIN ---")

    if request.method == 'POST':
        # ESPIÃO 2: Avisa que o botão foi clicado
        print("--- O BOTÃO 'ENTRAR' FOI CLICADO! ---")
        
        tipo = request.POST.get('tipo')
        matricula = request.POST.get('matricula_aluno')
        
        # ESPIÃO 3: Mostra o que o Python recebeu do HTML
        print(f"--- DADOS RECEBIDOS: TIPO={tipo} | MATRICULA={matricula} ---")

        if tipo == 'aluno':
            print("--- TIPO É ALUNO! TENTANDO REDIRECIONAR... ---")
            response = redirect('index')
            
            if matricula:
                response.set_cookie('iflanche_matricula', matricula)
            
            return response
            
        elif tipo == 'servidor':
            print("--- TIPO É SERVIDOR! VERIFICANDO SENHA... ---")
            usuario = request.POST.get('username')
            senha = request.POST.get('password')
            user = authenticate(request, username=usuario, password=senha)
            
            if user is not None:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                print("--- SENHA ERRADA! ---")
                return render(request, 'core/login.html', {'erro': 'Usuário ou senha incorretos'})
    
    # Se chegou aqui, é porque algo deu errado ou é o primeiro acesso
    print("--- NADA ACONTECEU, RENDERIZANDO A TELA DE NOVO ---")
    return render(request, 'core/login.html')

# --- 2. LOGOUT ---
def logout_view(request):
    logout(request)
    return redirect('login')

# --- 3. PAINEL DO ALUNO (Público) ---
def index(request):
    # 1. Pega o cardápio do banco
    itens_cardapio = Cardapio.objects.all()
    
    # 2. Pega a matrícula do Cookie
    matricula_aluno = request.COOKIES.get('iflanche_matricula', 'Visitante')
    
    # 3. DETETIVE DE CURSOS (Lógica Nova)
    curso_nome = 'Curso não identificado' # Valor padrão
    
    if matricula_aluno == 'Visitante':
        curso_nome = 'Visitante Externo'
    elif '111' in matricula_aluno:
        curso_nome = 'Técnico em Informática para Internet'
    elif '114' in matricula_aluno:
        curso_nome = 'Técnico em Meio Ambiente'
    elif '101' in matricula_aluno:
        curso_nome = 'Técnico em Edificações'
    else:
        curso_nome = 'Outro Curso / Integrado'

    # 4. Entrega tudo para o HTML
    return render(request, 'core/index.html', {
        'cardapio': itens_cardapio,
        'matricula_contexto': matricula_aluno,
        'curso_contexto': curso_nome  # Nova variável que vamos usar no HTML
    })
# --- 4. PAINEL DO SERVIDOR (Protegido por Senha) ---
@login_required(login_url='login') # Só entra se estiver logado!
def admin_dashboard(request):
    itens_cardapio = Cardapio.objects.all()
    form = CardapioForm() # Formulário vazio para o modal
    return render(request, 'core/admin.html', {
        'cardapio': itens_cardapio, 
        'form': form
    })

# --- 5. SALVAR REFEIÇÃO (Usando Forms) ---
@login_required(login_url='login')
def salvar_refeicao(request):
    if request.method == "POST":
        id_refeicao = request.POST.get('id_refeicao')
        
        if id_refeicao:
            # Edição
            refeicao = get_object_or_404(Cardapio, id=id_refeicao)
            form = CardapioForm(request.POST, instance=refeicao)
        else:
            # Criação
            form = CardapioForm(request.POST)

        if form.is_valid():
            form.save()
            
    return redirect('admin_dashboard')

# --- 6. DELETAR ---
@login_required(login_url='login')
def deletar_refeicao(request, id):
    refeicao = get_object_or_404(Cardapio, id=id)
    refeicao.delete()
    return redirect('admin_dashboard')