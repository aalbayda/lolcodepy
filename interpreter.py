_W='Typecasting'
_V='Expression'
_U="<class 'bool'>"
_T='TROOF'
_S='YARN'
_R='NUMBR'
_Q='NUMBAR'
_P='Not Equal'
_O='Equal'
_N='Min'
_M='Max'
_L='Modulo'
_K='Divide'
_J='Multiply'
_I='Subtract'
_H='Add'
_G=False
_F="<class 'float'>"
_E="<class 'int'>"
_D=True
_C='Break'
_B="<class 'str'>"
_A='IT'
symbol_table={_A:None}
stdin=[]
print_output=''
def op(token_type,subtree):
	D=subtree;C=token_type
	if C in[_H,_I,_J,_K,_L,_M,_N,_O,_P]:
		A=expression(D[0]);B=expression(D[1])
		if str(type(A))==_B and str(type(B))==_B:
			if'.'in A:A=float(A)
			else:A=int(A)
			if'.'in B:B=float(B)
			else:B=int(B)
		if str(type(A))==_E and str(type(B))==_F or str(type(A))==_F and str(type(B))==_E:A=float(A);B=float(B)
		elif str(type(A))==_B and str(type(B))==_E:A=int(A)
		elif str(type(A))==_E and str(type(B))==_B:B=int(B)
		elif str(type(A))==_B and str(type(B))==_F:A=float(A)
		elif str(type(A))==_F and str(type(B))==_B:B=float(B)
		if C==_H:return expression(A)+expression(B)
		elif C==_I:return expression(A)-expression(B)
		elif C==_J:return expression(A)*expression(B)
		elif C==_K:return expression(A)/expression(B)
		elif C==_L:return expression(A)%expression(B)
		elif C==_M:return max(expression(A),expression(B))
		elif C==_N:return min(expression(A),expression(B))
		elif C==_O:return expression(A)==expression(B)
		elif C==_P:return expression(A)!=expression(B)
	elif C=='And':return bool(expression(D[0]))and bool(expression(D[1]))
	elif C=='Or':return bool(expression(D[0]))or bool(expression(D[1]))
	elif C=='Xor':return bool(expression(D[0]))^bool(expression(D[1]))
	elif C=='Not':return not bool(expression(D[0]))
	elif C=='Any':
		E=[]
		for F in D:E.append(expression(F))
		if _D in E:return _D
		return _G
	elif C=='All':
		E=[]
		for F in D:E.append(expression(F))
		if _G in E:return _G
		return _D
def expression(node):
	A=node
	if str(type(A))in[_E,_F,_B,_U]:return A
	elif'Literal'in A.type:
		if A.type=='String Literal':return str(A.value.replace('"',''))
		elif A.type=='Integer Literal':return int(A.value)
		elif A.type=='Float Literal':return float(A.value)
		elif A.type=='Boolean Literal':
			if A.value=='WIN':return _D
			elif A.value=='FAIL':return _G
	elif A.type=='Identifier':return symbol_table[A.value]
	elif A.type==_V:return expression(A.children[0])
	elif A.type=='Concatenate':
		E=A.children;D=''
		for F in E:D+=str(expression(F))
		return D
	elif A.type==_W:
		B=expression(A.children[0]);C=A.children[1].children[0].value
		if C==_Q:return float(B)
		elif C==_R:return int(B)
		elif C==_S:return str(B)
		elif C==_T:return bool(B)
	elif A.type in[_H,_I,_J,_K,_L,_M,_N,_O,_P,'And','Or','Xor','Not','Any','All']:return op(A.type,A.children)
def declaration(node):
	A=node
	if len(A.children)==1:symbol_table[A.children[0].value]=None
	else:symbol_table[A.children[0].value]=expression(A.children[1])
def typecasting(node):
	A=node.children[0].children[0].value;B=node.children[1].children[0].value
	if B==_R:symbol_table[_A]=int(symbol_table[A])
	elif B==_Q:symbol_table[_A]=float(symbol_table[A])
	elif B==_S:symbol_table[_A]=str(symbol_table[A])
	elif B==_T:symbol_table[_A]=bool(symbol_table[A])
def retypecasting(node):
	A=node.children[0].value;B=node.children[1].children[0].value
	if B==_R:symbol_table[A]=int(symbol_table[A])
	elif B==_Q:symbol_table[A]=float(symbol_table[A])
	elif B==_S:symbol_table[A]=str(symbol_table[A])
	elif B==_T:symbol_table[A]=bool(symbol_table[A])
def assignment(node):symbol_table[node.children[0].value]=expression(node.children[1])
def loop(node):
	A=node;B=1
	if A.children[0].value=='NERFIN':B*=-1
	E=A.children[1].value;C=A.children[2].value;F=A.children[3]
	while _D:
		D=expression(F)
		if C=='WILE'and D==_G:break
		if C=='TIL'and D==_D:break
		G=codeblock(A.children[4])
		if G==_C:return
		symbol_table[E]+=B
def ifthen(node):
	A=node
	if symbol_table[_A]:codeblock(A.children[0])
	elif len(A.children)==2:codeblock(A.children[1])
def switch(node):
	for A in node.children:
		if expression(A.value.value)==str(symbol_table[_A]):
			B=codeblock(A.children[0])
			if B==_C:return
		if A.value.value=='Default':
			B=codeblock(A.children[0])
			if B==_C:return
def input_interpreter(node):global stdin;symbol_table[node.children[0].value]=stdin.pop(0)
def print_interpreter(node):
	global print_output;B=node.children
	for C in B:
		A=expression(C)
		if str(type(A))=="<class 'NoneType'>":A='NOOB'
		elif str(type(A))==_U:
			if str(A)=='True':A='WIN'
			else:A='FAIL'
		print_output+=str(A)
	print_output+='\n'
def statement(node):
	A=node.children[0]
	if A.type==_V:symbol_table[_A]=expression(A.children[0])
	elif A.type=='Declaration':declaration(A)
	elif A.type=='Variable Assignment':assignment(A)
	elif A.type==_W:typecasting(A)
	elif A.type=='Typecasting Reassignment':retypecasting(A)
	elif A.type=='If-Then':ifthen(A)
	elif A.type=='Switch':switch(A)
	elif A.type=='Loop':loop(A)
	elif A.type==_C:return _C
	elif A.type=='Print':print_interpreter(A)
	elif A.type=='Input':input_interpreter(A)
def codeblock(node):
	A=node.children
	for B in A:
		C=statement(B)
		if C==_C:return _C
def interpret(root,user_inputs):global symbol_table,stdin,print_output;print_output='';stdin=user_inputs;symbol_table={_A:None};codeblock(root);return{'symbol_table':symbol_table,'print_output':print_output}