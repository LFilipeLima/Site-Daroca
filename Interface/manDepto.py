import sys
from PySide6.QtCore import QtMsgType
from PySide6.QtWidgets import QApplication, QMainWindow, QStatusBar, QDialog, QTableWidgetItem
from FrmDepto_ui import Ui_FrmDepto
from FrmConexao_ui import Ui_dlgConectar
import pyodbc as bd
from datetime import datetime

global conexao, meuCursor

class FormPrincipal(QMainWindow, Ui_FrmDepto):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # associa o evento Click de cada botão a um método
        # da classe FormPrincipal que implementa o algoritmo
        # que se espera que esse botão dispare para execução
        self.action_Sair.triggered.connect(self.sairDoPrograma)
        self.action_Novo.triggered.connect(self.novoRegistro)
        self.action_Editar.triggered.connect(self.editarRegistro)
        self.action_Salvar.triggered.connect(self.salvarRegistro)
        self.action_Excluir.triggered.connect(self.excluirRegistro)
        self.action_Cancelar.triggered.connect(self.cancelarAcao)       
        self.abas.currentChanged.connect(self.mudarTab)  

        self.osDados = []
        self.quantosDados = 0
        self.registroAtual = -1  # índice do registro visitado (na tela)
        self.buscarDados()

        self.action_Inicio.triggered.connect(self.irAoInicio)
        self.action_Anterior.triggered.connect(self.irAoAnterior)
        self.action_Proximo.triggered.connect(self.irAoProximo)
        self.action_Fim.triggered.connect(self.irAoFim)
        self.atualizarTela()    # exibirá o registro atual da tabela 

        self.show()
        self.situacao = "navegando"

    def buscarDados(self):
        try:
            sComando = "SELECt Prod.nome, Prod.valor, Prod.imagem, "+\
                " prod.descricao , Prod.categoria "+\
                " FROM daroca.produtos as Prod "+\
                " ORDER BY prod.id"
            resultado = meuCursor.execute(sComando)
            self.osDados = resultado.fetchall()    # vetor de registros
            self.quantosDados = len(self.osDados)  # quantos registros
            if self.quantosDados > 0:   # dados foram trazidos
                self.registroAtual = 0  # posiciona no primeiro índice
        except:
            print("Erro ao buscar os dados para navegação.")

    def irAoInicio(self):
        self.registroAtual = 0
        self.atualizarTela()
        
    def irAoAnterior(self):
        if self.registroAtual > 0:
            self.registroAtual -= 1			# recua índice
            self.atualizarTela()
            
    def irAoProximo(self):
        if self.registroAtual < self.quantosDados - 1:
            self.registroAtual += 1			# avança índice
            self.atualizarTela()
            
    def irAoFim(self):
        self.registroAtual = self.quantosDados - 1
        self.atualizarTela()
        
    def atualizarTela(self):
        if self.quantosDados > 0:        # há dados para exibir
            self.Name_Prod.setText(self.osDados[self.registroAtual][0])
            self.Valor_Prod.setValue(self.osDados[self.registroAtual][1])
            self.IMG_Prod.setText(self.osDados[self.registroAtual][2])
            self.Descr_Prod.setText(self.osDados[self.registroAtual][3])
            self.CAT_Prod.setValue(self.osDados[self.registroAtual][4])
            
        else:
            self.limparTela()    # tabela de dados está vazia
            
    def limparTela(self):
        self.Name_Prod.setText("")
        self.Valor_Prod.setText("")
        self.IMG_Prod.setText("")
        self.Descr_Prod.setText("")
        self.CAT_Prod.setValue(0)

    def novoRegistro(self):
        self.Name_Prod.setText("")
        self.Valor_Prod.setValue(0)
        self.IMG_Prod.setText("")
        self.Descr_Prod.setText("")
        self.CAT_Prod.setValue(0)
        self.situacao = "incluindo"
     
        self.statusBar.showMessage("Digite os dados acima")

    def editarRegistro(self):
        self.situacao = "editando"
        self.Name_Prod.setFocus()             # coloca cursor nesse campo    # impede digitação
        self.statusBar.showMessage("Altere os dados acima")

    def salvarRegistro(self):
       
        if self.situacao == "incluindo":
            sComando = "insert into daroca.produtos "+\
                " (nome,valor,imagem,descricao,categoria) "+\
                " values( ?, ? , ?,?,?)  "

            try:        # tente executar o comando abaixo:
               
                meuCursor.execute(sComando,self.Name_Prod.text(), 
                                           float(self.Valor_Prod.value()),
                                           self.IMG_Prod.text(),
                                           self.Descr_Prod.text(),
                                           int(self.CAT_Prod.value())
                )
                                           
                meuCursor.commit()  # enviar as mudanças para o BD
                self.statusBar.showMessage("Inserido") 
   
            except Exception as erro:     # em caso de erro
                if hasattr(erro, 'message'):
                    mensagem = erro.message
                else:
                    mensagem = erro.args[1]
                self.statusBar.showMessage(mensagem)

        elif self.situacao =="editando":
            sComando = "Update daroca.produtos set nome = ?, valor = ?, imagem=? ,descricao=? , categoria=? where id =?"

            try:        # tente executar o comando abaixo:
    
                meuCursor.execute(sComando, 
                                           self.Name_Prod.text(), 
                                           float(self.Valor_Prod.value()),
                                           self.IMG_Prod.text(),
                                           self.Descr_Prod.text(),
                                           int(self.CAT_Prod.value()),
                                           int(self.ID_Prod.value())
                )
                meuCursor.commit()  # enviar as mudanças para o BD
                self.statusBar.showMessage("Alterado")  
  
            except Exception as erro:     # em caso de erro
                if hasattr(erro, 'message'):
                    mensagem = erro.message
                else:
                    mensagem = erro.args[1]
                self.statusBar.showMessage(mensagem)
        self.situacao = "navegando"
        self.buscarDados()
        self.atualizarTela()

    def excluirRegistro(self):
        self.situacao = "excluindo"
        self.situacao = "excluindo"
        sComando = "delete from daroca.produtos where nome=?"
        try:        # tente executar o comando abaixo:
            meuCursor.execute(sComando, self.Name_Prod.text())
            meuCursor.commit()  # enviar as mudanças para o BD
            self.statusBar.showMessage("Excluído")        
        except Exception as erro:     # em caso de erro
                if hasattr(erro, 'message'):
                    mensagem = erro.message
                else:
                    mensagem = erro.args[1]
                self.statusBar.showMessage(mensagem)
        self.situacao = "navegando"
        self.buscarDados()
        self.atualizarTela()

    def cancelarAcao(self):
        self.situacao = "navegando"
    
    def mudarTab(self):
        if self.abas.currentIndex() == 1: # busca no BD os registros 
            try: 
                sComando =  "Select id,nome,valor,imagem,descricao,categoria from daroca.produtos order by id"
                
                result = meuCursor.execute(sComando)
                regs = result.fetchall()
                numeroDeLinhas = len(regs)
                self.gridDepto.setRowCount(numeroDeLinhas)
                for indice in range(0, numeroDeLinhas, 1):
                    item_IDProd    = QTableWidgetItem(str(regs[indice][0]))
                    item_NomeProd = QTableWidgetItem(regs[indice][1])
                    item_valor = QTableWidgetItem(str(regs[indice][2]))
                    item_Imagem = QTableWidgetItem(regs[indice][3])
                    item_descr = QTableWidgetItem(regs[indice][4])
                    item_cat  = QTableWidgetItem(str(regs[indice][5]))
                
                    
                    self.gridDepto.setItem(indice, 0, item_IDProd)
                    self.gridDepto.setItem(indice, 1, item_NomeProd)
                    self.gridDepto.setItem(indice, 2, item_valor)
                    self.gridDepto.setItem(indice, 3, item_Imagem)
                    self.gridDepto.setItem(indice, 4, item_descr)
                    self.gridDepto.setItem(indice, 5, item_cat)

                self.gridDepto.resizeColumnsToContents()
                self.gridDepto.resizeRowsToContents()
                self.statusBar.showMessage("Listagem")
            except Exception as erro:     # em caso de erro
                if hasattr(erro, 'message'):
                    mensagem = erro.message
                else:
                    mensagem = erro.args[1]
                self.statusBar.showMessage(mensagem)





    def sairDoPrograma(self):
        self.close()

class DialogoConexao(QDialog, Ui_dlgConectar):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setModal(True)

aplicacao = QApplication(sys.argv)
dlgCon = DialogoConexao()   # cria instância da janela de conexão ao BD
if dlgCon.exec() == QDialog.Accepted:
    try:
        conexao = bd.connect(driver="SQL Server",
                            server=f"{dlgCon.edServidor.text()}",
                            database=f"{dlgCon.edBancoDeDados.text()}",
                            uid=f"{dlgCon.edUsuario.text()}",
                            pwd=f"{dlgCon.edSenha.text()}") 
        print("Conexão bem sucedida!")
        meuCursor = conexao.cursor()  # cursor: objeto de acesso ao BD
        janela = FormPrincipal()
        aplicacao.exec()
    except:
        print("Não foi possível conectar ao banco de dados")




