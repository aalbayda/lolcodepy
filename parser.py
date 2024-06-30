_P='Condition End Delimiter'
_O='Literal'
_N='Default'
_M='Case'
_L=False
_K='Concatenate'
_J='String Literal'
_I='Typecasting Reassignment'
_H='Variable Assignment'
_G='Input'
_F=True
_E='Operation Delimiter'
_D='Identifier'
_C='Expression'
_B=None
_A='Newline'
tokens=[]
index=0
current=_B,_B,0
next=_B,_B,1
error=''
class Grammar:
	def __init__(A,type,value=_B,children=_B):A.type=type;A.value=value;A.children=children
def expect(expected_type):
	A=expected_type;global current,next,index,tokens,error
	if current[0]==A:
		index+=1
		if index+1<len(tokens):current=tokens[index]
	else:error='Syntax Error at line '+str(current[2])+': Expected a '+A+' but got a '+current[0]+'!';return
def literal():
	B='Type Literal';A='String Delimiter';global current
	if not _O in current[0]and current[0]!=A:return
	if current[0]==A:expect(A);C=current[1];expect(_J);expect(A);return Grammar(type=_J,value=C)
	elif current[0]==B:return Grammar(type=B,value=current[1])
	else:return Grammar(type=current[0],value=current[1])
def typecast():
	C='Typecasting Assignment';A=[]
	if current[0]!='Typecasting Declaration':return
	expect(current[0]);B=expr()
	if B.children[0].type!=_D:expect(_D)
	A.append(B)
	if current[0]==C:expect(C)
	type=expr();A.append(type);return Grammar(type='Typecasting',children=A)
def smoosh():
	global current
	if current[0]!=_K:return
	B=[];expect(current[0]);A=expr()
	if A.type==_C:B.append(A)
	else:expect(_C)
	expect(_E);A=expr()
	if A.type==_C:B.append(A)
	else:expect(_C)
	while current[0]==_E:
		expect(current[0]);A=expr()
		if A.type==_C:B.append(A)
		else:expect(_C);B.append(A)
	return Grammar(type=_K,children=B)
def op(anyall=_L):
	G='Any';F='All';E='Not';A=anyall;global current,expr,error;C=[]
	if current[0]not in[_K,'Add','Subtract','Multiply','Divide','Modulo','Max','Min','And','Or','Xor',E,'Equal','Not Equal',F,G]:return
	D=current[0];expect(D)
	if D in[G,F]:
		if A==_F:error=f"Syntax Error at line {current[2]}: Any/All should not nest into itself";return
		A=_F
	B=expr(A)
	if B:C.append(B)
	else:expect(_C)
	if D!=E and current[0]!=_A:
		expect(_E);B=expr(A)
		if B:C.append(B)
		else:expect(_C)
		while A and current[0]==_E:expect(current[0]);B=expr(A);C.append(B)
		if A==_F and current[0]!=_E and current[0]!=_C and current[0]!=_A:expect('Anyall Delimiter')
	return Grammar(type=D,children=C)
def identifier(value=_B):return Grammar(type=_D,value=value)
def expr(anyall=_L):
	global current;A=[];C=op(anyall);B=literal();D=typecast();E=smoosh()
	if C:A.append(C)
	elif B:
		A.append(B)
		if B.type!=_J:expect(B.type)
	elif D:A.append(D)
	elif E:A.append(E)
	elif current[0]==_D:A.append(identifier(current[1]));expect(_D)
	else:return
	return Grammar(_C,children=A)
def print_grammar():
	B='Print';global current
	if current[0]!=B:return
	expect(B);C=[];A=expr()
	if not A:expect(_C)
	while A:
		C.append(A)
		if current[0]==_E:expect(current[0])
		A=expr()
		if current[0]==_E:expect(_E)
	return Grammar(type=B,children=C)
def input_grammar():
	global current
	if current[0]!=_G:return
	A=[];expect(_G)
	if current[0]==_D:A.append(Grammar(type=current[0],value=current[1]));expect(current[0]);return Grammar(type=_G,children=A)
	expect(_D)
def declaration():
	global current
	if current[0]!='Variable Declaration':return
	A=[];expect(current[0]);A.append(identifier(current[1]));expect(_D)
	if current[0]=='Variable Initialization':
		expect(current[0]);B=expr()
		if B:A.append(B)
		else:expect(_C)
	return Grammar(type='Declaration',children=A)
def assignment():
	global current,index,tokens
	if current[0]!=_D:return
	B=[];B.append(Grammar(type=current[0],value=current[1]));expect(current[0])
	if current[0]!=_H and current[0]!=_I:index-=1;current=tokens[index];return
	A=''
	if current[0]==_H:A=_H;expect(A)
	elif current[0]==_I:A=_I;expect(A)
	else:return
	C=expr()
	if C:B.append(C)
	else:expect(_C)
	return Grammar(type=A,children=B)
def loop():
	G='Loop Until';D='Loop';global current,error;A=[]
	if current[0]!='Loop Start Delimiter':return
	expect(current[0]);H=current[1];expect(_D);B=D
	if current[0]=='Loop Increment':B+=' Increment'
	else:B+=' Decrement'
	A.append(Grammar(type=B,value=current[1]));expect(B);expect('Loop-Variable Delimiter');E=expr()
	if not E.children[0].type==_D:error=f"Syntax Error in Line {current[2]}: Expected variable";return
	A.append(Grammar(type=_D,value=E.children[0].value))
	if current[0]==G or current[0]=='Loop While':
		C=D
		if current[0]==G:C+=' Until'
		else:C+=' While'
		A.append(Grammar(type=C,value=current[1]));expect(C);F=expr()
		if not F:expect(_C)
		A.append(F)
	expect(_A);I=codeblock();A.append(I);expect('Loop End Delimiter')
	if current[1]!=H:error=f"Syntax Error in Line {current[2]}: Unmatched loop name";return
	expect(current[0]);return Grammar(type=D,children=A)
def ifthen():
	B='Else';A=[]
	if current[0]!='If-Then Start Delimiter':return
	expect(current[0]);expect(_A);expect('If');expect(_A);A.append(codeblock())
	if current[0]==B:expect(B);expect(_A);A.append(codeblock())
	expect(_P);return Grammar(type='If-Then',children=A)
def case(default=_L):
	global error;B=[];A=_B
	if not default:
		expect(_M);A=literal()
		if _O in A.type:expect(f"{A.type.split()[0]} Literal")
		else:error=f"Syntax Error in Line {current[2]}: Expected a literal but got a {current[0]}";return
	else:A=Grammar(type='Case Value',value=_N);expect(_N)
	expect(_A);C=codeblock()
	if C:B.append(C)
	return Grammar(type=_M,children=B,value=A)
def switch():
	global current
	if current[0]!='Switch Start Delimiter':return
	A=[];expect(current[0]);expect(_A);B=case();A.append(B)
	while current[0]==_M:B=case();A.append(B)
	if current[0]==_N:C=case(_F);A.append(C)
	expect(_P);return Grammar(type='Switch',children=A)
def break_grammar():
	A='Break';global current;B=[]
	if current[0]!=A:return
	expect(current[0]);return Grammar(type=A,children=B)
def statement():
	global print_grammar,input_grammar,declaration,assignment,loop,ifthen,switch,expr;A=[];B=assignment();E=print_grammar();F=input_grammar();G=declaration();C=_B;D=_B
	if B:
		if B.type==_H:C=B
		elif B.type==_I:D=B
	H=loop();I=ifthen();J=switch();K=break_grammar();L=expr()
	if E:A.append(E)
	elif F:A.append(F)
	elif G:A.append(G)
	elif C:A.append(C)
	elif D:A.append(D)
	elif H:A.append(H)
	elif I:A.append(I)
	elif J:A.append(J)
	elif K:A.append(K)
	elif L:A.append(L)
	elif current[0]==_A:expect(_A);A.append(Grammar(type=_A));return Grammar(type=_A)
	else:return
	expect(_A);return Grammar('statement',children=A)
def codeblock():
	B=[];A=statement()
	while A:
		if A.type!=_A:B.append(A)
		A=statement()
	return Grammar(type='Codeblock',children=B)
def program():
	global statement;B=[]
	while current[0]==_A:expect(current[0])
	expect('Program Start Delimiter');expect(_A);A=codeblock()
	if A:B.append(A)
	expect('Program End Delimiter');return A
def parse(in_tokens):
	global current,next,tokens,index,error;tokens=in_tokens;index=0;current=_B,_B,0;next=_B,_B,1;error='';current=tokens[0]
	if len(tokens)>1:next=tokens[1]
	A=program();B=[]
	def C(tree,idx):
		for A in tree:
			if A:
				if A.type==_G:B.append(A.children[0].value)
				if A.children:C(A.children,idx+1)
	C(A.children,0);return{'parse_tree':A,'error':error,'input_variables':B}