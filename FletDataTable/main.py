from flet import *
import sqlite3

# Conectar no banco
conn = sqlite3.connect("dados.db", check_same_thread=False)
cursor = conn.cursor()

# Criar tabela do banco
cursor.execute(
    ''' CREATE TABLE IF NOT EXISTS clientes
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT)''')

# Classe para criar aplicativos, pode dar qualquer nome, desde que o parametro seja esse, e as duas funções obrigatórias
class App(UserControl):
    def __init__(self):
        super().__init__()
        
        # Atributos da classe App da função init
        self.todos_dados = Column(auto_scroll=True)
        self.adicionar_dados = TextField(label="Nome do dado:", autofocus=True)
        self.editar_dado = TextField(label="Editar")
    
    # Função para deletar dado
    def deletar(self, id, dialogo):
        # Deletar o Item através do id passado por parametro
        cursor.execute("DELETE FROM clientes WHERE id = ?", [id])
        # Fechar o modal através do parametro
        dialogo.open = False
        
        # Chamar a função de renderizar os dados
        self.todos_dados.controls.clear()
        self.renderizar_todos()
        self.page.update()

    # Função para atualizar dado
    def atualizar(self, id, dado, dialogo):
        # Atualizar Item através dos parametros
        cursor.execute("UPDATE clientes set nome = ? WHERE id = ?", (dado, id))
        conn.commit()
        
        # Fechar o modal através do parametro
        dialogo.open = False
        
        # Chamar a função de renderizar os dados
        self.todos_dados.controls.clear()
        self.renderizar_todos()
        self.page.update()
        
    # Abrir as ações de modal
    def abrir_acoes(self, e):
        # Nesta sessão nós precisamos do Id de onde for clicado
        id_user = e.control.subtitle.value # Nesta linha estamos recebendo o valor do subtitulo através do evento clicado
        self.editar_dado.value = e.control.title.value # Nesta linha, quando clicado no btn editar, teremos nosso dado atualizado
        self.update()
        
        # Iremos criar um alerta de dialogo
        dialog_alert = AlertDialog(
            title=Text(f"Editar ID {id_user}"),
            # Conteúdo para receber
            content=self.editar_dado,
            # Ações de botões
            actions=[
                # Neste botão estamos passando um lambda que vai receber um evento de click para receber os parametros de id e do dialogo para a função deletar
                ElevatedButton('Deletar', color="white", bgcolor=colors.RED_800, on_click=lambda e:self.deletar(id_user, dialog_alert)),
                # Neste botão estamos passando um lambda que vai receber um evento de click para receber os parametros de id, editar_dado para atualizar e do dialogo para a função atualizar
                ElevatedButton('Atualizar', color="white", on_click=lambda e:self.atualizar(id_user, self.editar_dado.value, dialog_alert))
            ],
            actions_alignment='spaceBetween'
        )
        
        # Estamos definindo que nosso dialogo de alerta vai ser passado para a página de dialogo
        self.page.dialog = dialog_alert
        # Quando essa função for passado definimos true para poder aparecer o dialogo
        dialog_alert.open = True
        # Atualizar a página
        self.page.update()
        
    # READ - mostrar os dados 
    def renderizar_todos(self):
        cursor.execute("SELECT * FROM clientes")
        conn.commit()
        
        dados = cursor.fetchall() # Percorrer todos os dados
        
        for dado in dados:
            # Vamos adicionar todos os dados existentes a coluna 
            self.todos_dados.controls.append(
                # ListTile nos permite pegar os ids do dado
                ListTile(
                    subtitle=Text(dado[0]), # Essa linha trás o Id
                    title=Text(dado[1]), # Essa linha pega o Nome
                    on_click=self.abrir_acoes
                ) 
            )
        self.update()
        
    
    # CREATE - criar dados
    def adicionar_novo_dado(self, e):
        cursor.execute("INSERT INTO clientes (nome) VALUES (?)", [self.adicionar_dados.value]) # Inserindo dados no banco
        conn.commit()
        
        self.todos_dados.controls.clear() # Limpando os dados da coluna
        self.renderizar_todos() # Chamar a função de renderizar os dados
        self.update() # Atualizando a página para ser dinâmica
        
        
    def build(self):
        # Estamos retornando uma coluna que está sendo adicionado na página através da instancia da classe
        return  Column([
            # Todos os atributos da função init pode ser passados para o build para adicionar na página
            Text("CRUD COM SQLITE", size=20, weight='bold'),
            self.adicionar_dados,
            FloatingActionButton(icon=icons.ADD, on_click=self.adicionar_novo_dado),
            # Aqui estamos adicionando a coluna que criamos para mostrar os dados
            self.todos_dados
        ])
        
def main(page: Page):
    page.update()
    page.window_width = 400
    # Instanciando a classe App para my_app
    my_app = App()

    page.add(
        my_app,
    )
    page.update()

app(target=main)