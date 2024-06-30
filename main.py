from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout,QHBoxLayout,QInputDialog,QTableWidget,QTableWidgetItem,QPushButton,QTextEdit,QFileDialog
from PyQt5.QtGui import QTextOption
from lexer import lex
from parser import parse
from interpreter import interpret
import sys
class Window(QWidget):
	def __init__(A):super().__init__();A.initUI();A.code='';A.stdio='';A.stdout=''
	def initUI(A):B=QVBoxLayout();C=QHBoxLayout();D=QVBoxLayout();A.loadFileButton=QPushButton('Load LOLCode File',A);A.loadFileButton.clicked.connect(A.loadFile);D.addWidget(A.loadFileButton);A.box1=QTextEdit(A);A.box1.setFixedSize(600,300);D.addWidget(A.box1);C.addLayout(D);A.tableWidget1=QTableWidget(A);A.tableWidget1.setRowCount(10);A.tableWidget1.setColumnCount(2);A.tableWidget1.setHorizontalHeaderLabels(['Lexeme','Classification']);C.addWidget(A.tableWidget1);A.tableWidget2=QTableWidget(A);A.tableWidget2.setRowCount(10);A.tableWidget2.setColumnCount(2);A.tableWidget2.setHorizontalHeaderLabels(['Identifier','Value']);C.addWidget(A.tableWidget2);B.addLayout(C);A.executeButton=QPushButton('Execute  ▶️',A);A.executeButton.clicked.connect(A.execute);B.addWidget(A.executeButton);A.outputBox=QTextEdit(A);A.outputBox.setFixedSize(1175,400);A.outputBox.setReadOnly(True);A.outputBox.setWordWrapMode(QTextOption.WordWrap);B.addWidget(A.outputBox);A.setLayout(B);A.setWindowTitle('Albayda - CMSC 124 - LOLCode Interpreter');A.setFixedSize(1200,800)
	def loadFile(A):
		F=QFileDialog.Options();C,H=QFileDialog.getOpenFileName(A,'Load LOLCode File','','LOLCode Files (*.lol)',options=F);D=None
		if C:
			with open(C,'r')as G:E=G.read();A.box1.setText(E);D=E.split('\n')
			A.tableWidget1.setRowCount(10);A.tableWidget2.setRowCount(10)
			for B in range(10):A.tableWidget1.setItem(B,0,QTableWidgetItem(''));A.tableWidget1.setItem(B,1,QTableWidgetItem(''));A.tableWidget2.setItem(B,0,QTableWidgetItem(''));A.tableWidget2.setItem(B,1,QTableWidgetItem(''))
			A.outputBox.setText('')
		if not D:A.outputBox.setText('File empty!');return
	def execute(A):
		N='error';A.code=A.box1.toPlainText().split('\n');G=lex(A.code);C=G['tokens'];H=G[N]
		if H:A.outputBox.setText(H);return
		if len(C)>10:A.tableWidget1.setRowCount(len(C))
		for B in range(len(C)):
			E=C[B][1]
			if E=='\n':E='\\n'
			O=C[B][0];A.tableWidget1.setItem(B,0,QTableWidgetItem(E));A.tableWidget1.setItem(B,1,QTableWidgetItem(O))
		if len(C)>0:F=parse(C)
		else:A.outputBox.setText('Empty token list!');return
		P=F['parse_tree'];I=F[N]
		if I:A.outputBox.setText(I);return
		J=[]
		for Q in F['input_variables']:
			K,R=QInputDialog.getText(A,'User Input',f"GIMMEH {Q}:")
			if R and K!='':J.append(K)
		try:L=interpret(P,J)
		except Exception as S:A.outputBox.setText('Interpretor Error:\n'+str(S));return
		D=L['symbol_table'];T=L['print_output']
		if len(D)>10:A.tableWidget2.setRowCount(len(D))
		B=0
		for M in D:A.tableWidget2.setItem(B,0,QTableWidgetItem(str(M)));A.tableWidget2.setItem(B,1,QTableWidgetItem(str(D[M])));B+=1
		A.outputBox.setText(T)
def main():A=QApplication(sys.argv);B=Window();B.show();sys.exit(A.exec_())
main()