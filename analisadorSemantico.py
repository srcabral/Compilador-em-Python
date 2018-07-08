####	CONSTRUÇÃO DE UM COMPILADOR 	####
'''
	Autor: Sérgio Castro Cabral
	Data: 30/06/2018
	
	Descrição:
		Implementação de um Analisador Léxico, Sintático e Semântico para a
		construção de um compilador que lê um código 
		em Mgol e o compila para a linguagem C.

'''
################################################################################
#                                                                              #
#  Representação dos símbolos de acordo com as colunas da tabela de transição  #
#																			   # 	
################################################################################
# simbolo D (digitos) : coluna 0
# simbolo L (letras) : coluna 1
# simbolo " (aspas) : coluna 2
# simbolo { (abre Chaves) : coluna 3
# simbolo } (fecha Chaves) : coluna 4
# simbolo ' ' (espaço em branco) : coluna 5
# simbolo EOF (fim de arquivo) : coluna 6
# simbolo < (sinal menor) : coluna 7
# simbolo > (sinal maior) : coluna 8
# simbolo = (sinal igual) : coluna 9
# simbolo - (sinal menos) : coluna 10
# simbolo + (sinal mais) : coluna 11
# simbolo * (sinal multiplicação) : coluna 12
# simbolo / (sinal divisão) : coluna 13
# simbolo . (ponto) : coluna 14
# simbolo ( (abre parenteses) : coluna 15
# simbolo ) (fecha parenteses) : coluna 16
# simbolo ; (sinal delimitador) : coluna 17
# simbolo ERRO (sinal de erro ou qualquer caracter não previsto): coluna 18
# simbolo e (nº cientifico) : coluna 19
# simbolo E (nº cientifico) : coluna 20
# simbolo _ (underline) : coluna 21
# simbolo /n (quebra de linha) : coluna 5
# simbolo /t (tabulação) : coluna 5
################################################################################





import sys
import string


'''*********************** ETAPA 1: ANALISADOR LÉXICO ************************'''

### TABELA DE SIMBOLOS INICIALIZADA COM AS PALAVRAS RESERVADAS DA LINGUAGEM ### 
symbolTable = {}
symbolTable ['inicio'] = 'inicio', 'inicio', 'Delimitador'
symbolTable ['varinicio'] = 'varinicio', 'varinicio', 'Delimitador'
symbolTable ['varfim'] = 'varfim', 'varfim', 'Delimitador'
symbolTable ['escreva'] = 'escreva', 'escreva', 'Função'
symbolTable ['leia'] = 'leia', 'leia', 'Função'
symbolTable ['se'] = 'se', 'se', 'Condicional'
symbolTable ['entao'] = 'entao', 'entao', 'Condicional'
symbolTable ['senao'] = 'senao', 'senao', 'Condicional'
symbolTable ['fimse'] = 'fimse', 'fimse', 'Delimitador'
symbolTable ['fim'] = 'fim', 'fim', 'Delimitador'
symbolTable ['inteiro'] = 'int', 'inteiro', 'Numerico'
symbolTable ['literal'] = 'lit', 'literal', 'Literal'
symbolTable ['real'] = 'real', 'real', 'Numerico'


### TABELA DE TRANSIÇÃO DO AUTOMATO FINITO DETERMINISTICO ###
tableTrasition = [
	[ 1,  8,  6, 21, -1,  0,  9, 11, 14, 10, 20, 20, 20, 20,  0, 19, 18, 16, 17,  8,  8, -1],
	[ 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  2, -1, -1, -1, -1,  4,  4, -1],
	[ 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[ 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  4,  4, -1],
	[22, -1, -1, -1, -1, -1, -1, -1, -1, -1,  5,  5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[22, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[ 6,  6,  7,  6,  6,  6, -1,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6],
	[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[ 8,  8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  8,  8,  8],
	[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[-1, -1, -1, -1, -1, -1, -1, -1, 12, 15, 13, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[-1, -1, -1, -1, -1, -1, -1, -1, -1, 15, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[21, 21, 21, 21,  0, 21, -1, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21],
	[22, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
]




## Retorna o número correspondente ao símbolo ##
def symbol(currentChar, prevState):
	if currentChar.isdigit():
		return 0 # É um digito
	elif currentChar == 'e' and prevState == 1 or currentChar == 'e' and prevState == 3: # Número Científico
		return 19
	elif currentChar == 'E' and prevState == 1 or currentChar == 'E' and prevState == 3: # Número Científico
		return 20
	elif currentChar.isalpha() :
		return 1 # É uma letra
	elif currentChar == '"':
		return 2
	elif currentChar == '{':
		return 3
	elif currentChar == '}':
		return 4
	elif currentChar == ' ' or currentChar == '\n' or currentChar == '\t':
		return 5
	elif currentChar == 'EOF':
		return 6
	elif currentChar == '<':
		return 7
	elif currentChar == '>':
		return 8
	elif currentChar == '=':
		return 9
	elif currentChar == '-':
		return 10
	elif currentChar == '+':
		return 11
	elif currentChar == '*':
		return 12
	elif currentChar == '/':
		return 13
	elif currentChar == '.':
		return 14
	elif currentChar == '(':
		return 15
	elif currentChar == ')':
		return 16
	elif currentChar == ';':
		return 17
	elif currentChar == '_':
		return 21
	else:
		return 18  # Qualquer caracter diferente 
	
		
# Retorna o token correspondente ao símbolo 
def token(finalState):
		if finalState == 1 or finalState == 3 or finalState == 22:
			return 'num' # Constante Numerica

		elif finalState == 7:
			return 'literal' # Constante Literal ou comentário 

		elif finalState == 8:
			return 'id' # Identificador

		elif finalState == 9:
			return 'EOF' # Fim de arquivo

		elif finalState == 10 or finalState == 11 or finalState == 12 or finalState == 14 or finalState == 15:
			return 'OPR' # Operador relacional

		elif finalState == 13:
			return 'RCB' # Atribuição

		elif finalState == 20:
			return 'OPM' # Operador aritmético

		elif finalState == 19:
			return 'AB_P' # Abre parênteses

		elif finalState == 18:
			return 'FC_P' # Fecha parênteses
		
		elif finalState == 16:
			return 'PT_V' # Ponto vírgula

		elif finalState == 17:
			return 'ERRO' 

# Verifica se o estado atual é um estado final
def isFinalStates(state):
	# String contendo os estados finais da tabela de transição
	finalState = [1, 3, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22]
	size = len(finalState)
	i = 0
	while i < size:
		if state == finalState[i]:
			return True
		i += 1
	return False


# Faz a analise lexica e retorna o token correspondente
def lexico():
	global cursor
	global line
	global arquivo
	global numChar
	global position

	typeToken = {} # Dicionario usado para auxiliar quando for enviar tokens de outros tipos que nao seja um tipo "id"

	if cursor == numChar:
		bufferInput = ''
		typeToken[bufferInput] = ['EOF', bufferInput, 'Fim de arquivo']
		return typeToken[bufferInput]

	currentState = 0
	prevState = 0
	bufferInput = ''
	char = arquivo[cursor]
	flag = 0

	nextState = tableTrasition[currentState][symbol(char, prevState)]

	while nextState != -1:
		currentState = nextState # Atualiza o estado atual

		if char == '\n':
			line += 1 # Inidica a linha do arquivo atual
			position = 1 

		if char != '\n' and char != '\t' and char != ' ': # Ignora quebra de linha, tabulação e espaço em branco
			bufferInput += char # Adiciona o caracter lido no buffer de entrada 
			if '{' in bufferInput:
				if '}' in bufferInput:
					bufferInput = ''
				
		cursor += 1 # Indica a posição do cursor no arquivo
		position += 1 

		if cursor < numChar: # Verfica se o cursor chegou no final do arquivo
			char = arquivo[cursor] # Pega o proximo caracter
			prevState = currentState # Atualiza o estado anterior

		else:
			flag = 1 # Sinaliza que chegou no final do arquivo 

		if flag != 1:
			nextState = tableTrasition[currentState][symbol(char, prevState)] # Retorna proximo estado
		else:
			# Caso seja o último caracter lido do arquivo o cursor não estará apontando para 
			# a proxima posição, logo próximo estado recebe -1 para o loop parar, para análise
			# do que está no buffer de entrada seja feita
			nextState = -1 


	if isFinalStates(currentState):
		if bufferInput not in symbolTable and token(currentState) == 'id':
			symbolTable[bufferInput] = 'id', bufferInput, ' '

			#print('\n\t\tTABELA DE SÍMBOLOS')
			#print('\n\t|  TOKEN   |   LEXEMA   |   TIPO   |')
			#print('\t------------------------------------')

			#aux = symbolTable[bufferInput]
			#typeToken = str(aux[0])
			return symbolTable[bufferInput] #typeToken
			#print('\t------------------------------------')


			#print('\n\nTABELA DE SÍMBOLOS ATUALIZADA\n')
			#for x in symbolTable.items():
			#	print(x)
		
		elif bufferInput in symbolTable:
			#aux = symbolTable[bufferInput]
			#typeToken = str(aux[0])
			return symbolTable[bufferInput] #typeToken
			#print('\t------------------------------------')

		
		else:
			if token(currentState) == 'ERRO': # Caracter inválido lido 
				print('\n\nERRO ECONTRADO!!')
				print('Linha: {} | Posição: {}'.format(line, position-2))
				print('Caracter "{}" não é permitido pela linguagem'.format(bufferInput[len(bufferInput)-1]))
				sys.exit()
			else:
				if token(currentState) == 'num':
					typeToken[bufferInput] = ['num', bufferInput, bufferInput]
					return typeToken[bufferInput]
				elif token(currentState) == 'literal':
					typeToken[bufferInput] = ['literal', bufferInput, 'Constante Literal']
					return typeToken[bufferInput]
				elif token(currentState) == 'OPR':
					typeToken[bufferInput] = ['opr', bufferInput, bufferInput]
					return typeToken[bufferInput]
				elif token(currentState) == 'RCB':
					typeToken[bufferInput] = ['rcb', bufferInput, '=']
					return typeToken[bufferInput]
				elif token(currentState) == 'OPM':
					typeToken[bufferInput] = ['opm', bufferInput, bufferInput]
					return typeToken[bufferInput]
				elif token(currentState) == 'AB_P':
					typeToken[bufferInput] = ['AB_P', bufferInput, 'Abre Parênteses']
					return typeToken[bufferInput]
				elif token(currentState) == 'FC_P':
					typeToken[bufferInput] = ['FC_P', bufferInput, 'Fecha Parênteses']
					return typeToken[bufferInput]
				elif token(currentState) == 'PT_V':
					typeToken[bufferInput] = ['PT_V', bufferInput, 'Ponto Vírgula']
					return typeToken[bufferInput]

	# Verifica a condição que gerou o erro
	else:
		print('\n\nERRO LEXICO ECONTRADO!!')
		print('Linha: {} | Posição: {}'.format(line, position-2))
		
		if currentState == 0 and char == '}':
			print('Tipo de erro: Fechamento de chave sem ter uma chave aberta')
			sys.exit()
		elif currentState == 2:
			print('Tipo de erro: Esperava número após o ponto!')
			sys.exit()
		elif currentState == 4:
			print('Tipo de erro: Notação de número cíentifico inválido')
			sys.exit()
		elif currentState == 5:
			print('Tipo de erro: Esperava número após notação científica!')
			sys.exit()
		elif currentState == 6:
			print('Tipo de erro: Esperava fechamento da aspas!')
			sys.exit()
		elif currentState == 21:
			print('Tipo de erro: Esperava fechamento da chave!')
			sys.exit()
		else:
			print('Erro inesperado!')
			sys.exit()

'''*********************** ETAPA 2: ANALISADOR SINTÁTICO ************************'''

tableSyntax = [
	#inicio 	varinicio 	varfim	id 		int 	real 	lit 	leia 	escreva literal	num 	rcb 	se 		(		)		entao 	opr 	fimse 	fim 	$ 		opm 	; 		P 		V 		LV 		D 		TIPO 	A 		ES 		ARG 	CMD 	LD 		OPRD 	COND 	CABEÇALHO	EXP_R	CORPO		
	['S1',		'E0',		'E0',	'E0',	'E0',	'E0',	'E0',	'E0', 	'E0', 	'E0',	'E0', 	'E0', 	'E0', 	'E0', 	'E0', 	'E0', 	'E0', 	'E0', 	'E0', 	'E0', 	'E0', 	'E0',	57,		-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E1', 		'S2', 		'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1',	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	-1, 	15, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E2', 		'E2', 		'S7', 	'S9', 	'E2', 	'E2', 	'E2', 	'E2', 	'E2', 	'E2',	'E2', 	'E2', 	'E2', 	'E2', 	'E2', 	'E2', 	'E2', 	'E2', 	'E2', 	'E2', 	'E2', 	'E2', 	-1, 	-1, 	 3, 	 4, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E3', 		'E3', 		'E3', 	'R3', 	'E3', 	'E3', 	'E3', 	'R3', 	'R3',	'E3',	'E3', 	'E3', 	'R3', 	'E3', 	'E3', 	'E3', 	'E3', 	'E3', 	'R3', 	'E3', 	'E3', 	'E3', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E4', 		'E4', 		'S7', 	'S9',	'E4', 	'E4', 	'E4', 	'E4', 	'E4', 	'E4',	'E4',	'E4', 	'E4', 	'E4', 	'E4', 	'E4', 	'E4', 	'E4', 	'E4', 	'E4', 	'E4', 	'E4', 	-1, 	-1, 	 5,		 4,		-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E5', 		'E5', 		'E5', 	'R4', 	'E5', 	'E5', 	'E5', 	'R4', 	'R4', 	'E5',	'E5', 	'E5', 	'R4', 	'E5', 	'E5', 	'E5', 	'E5', 	'E5', 	'R4', 	'E5', 	'E5',	'E5', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E6', 		'E6', 		'E6', 	'E6', 	'E6', 	'E6', 	'E6', 	'E6', 	'E6', 	'E6',	'E6', 	'E6', 	'E6', 	'E6', 	'E6', 	'E6', 	'E6', 	'E6', 	'E6', 	'R22', 	'E6', 	'E6', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E7', 		'E7', 		'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'E7',	'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'S8', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E8', 		'E8', 		'E8', 	'R5', 	'E8', 	'E8', 	'E8', 	'R5', 	'R5', 	'E8',	'E8', 	'E8', 	'R5', 	'E8', 	'E8', 	'E8', 	'E8', 	'E8', 	'R5', 	'E8', 	'E8', 	'E8', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E9', 		'E9', 		'E9', 	'E9', 	'S12', 	'S13', 	'S14', 	'E9', 	'E9', 	'E9',	'E9', 	'E9', 	'E9', 	'E9', 	'E9', 	'E9', 	'E9', 	'E9', 	'E9', 	'E9', 	'E9', 	'E9', 	-1, 	-1, 	-1, 	-1, 	10,		-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E10', 	'E10', 		'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'E10',	'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'S11', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,  	-1, 	-1, 	-1, 	 	-1,	 	-1 ],
	['E11', 	'E11', 		'R6', 	'R6', 	'E11', 	'E11', 	'E11', 	'E11', 	'E11', 	'E11',	'E11', 	'E11', 	'E11', 	'E11', 	'E11', 	'E11', 	'E11', 	'E11', 	'E11', 	'E11', 	'E11', 	'E11', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E12', 	'E12', 		'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'E12',	'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'R7', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1,	 	-1 ],
	['E13', 	'E13', 		'E13', 	'E13', 	'E13', 	'E13', 	'E13', 	'E13', 	'E13',  'E13',	'E13', 	'E13', 	'E13', 	'E13', 	'E13', 	'E13', 	'E13', 	'E13', 	'E13', 	'E13', 	'E13', 	'R8', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E14', 	'E14', 		'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'E14',	'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'R9', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1,		-1 ],
	['E15', 	'E15', 		'E15', 	'S31', 	'E15', 	'E15', 	'E15', 	'S22', 	'S25', 	'E15',	'E15', 	'E15', 	'S40', 	'E15', 	'E15', 	'E15', 	'E15', 	'E15', 	'S21', 	'E15', 	'E15', 	'E15', 	-1, 	-1, 	-1, 	-1, 	-1, 	58, 	16, 	-1, 	18, 	-1, 	-1, 	20, 	48, 		-1, 	-1 ],
	['E16', 	'E16', 		'E16', 	'S31', 	'E16', 	'E16', 	'E16', 	'S22', 	'S25', 	'E16',	'E16', 	'E16', 	'S40', 	'E16', 	'E16', 	'E16', 	'E16', 	'E16', 	'S21', 	'E16', 	'E16', 	'E16', 	-1, 	-1, 	-1, 	-1, 	-1, 	17, 	16, 	-1, 	18, 	-1, 	-1, 	20, 	48, 		-1, 	-1 ],
	['E17', 	'E17', 		'E17', 	'E17', 	'E17', 	'E17', 	'E17', 	'E17', 	'E17', 	'E17',	'E17', 	'E17', 	'E17', 	'E17', 	'E17', 	'17', 	'E17', 	'E17', 	'E17', 	'R10', 	'E17', 	'E17', 	-1, 	-1,	 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E18', 	'E18', 		'E18', 	'S31', 	'E18', 	'E18', 	'E18', 	'S22', 	'S25', 	'E18',	'E18', 	'E18', 	'S40', 	'E18', 	'E18', 	'E18', 	'E18', 	'E18', 	'S21', 	'E18', 	'E18', 	'E18', 	-1, 	-1, 	-1, 	-1, 	-1,	 	19, 	16, 	-1, 	18, 	-1, 	-1, 	20, 	48, 		-1, 	-1 ],
	['E19', 	'E19', 		'E19', 	'E19', 	'E19', 	'E19', 	'E19', 	'E19', 	'E19', 	'E19',	'E19', 	'E19', 	'E19', 	'E19', 	'E19', 	'E19', 	'E19', 	'E19', 	'E19', 	'R16', 	'E19', 	'E19',  -1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,			-1, 	-1 ],
	['E20', 	'E20', 		'E20', 	'S31', 	'E20', 	'E20', 	'E20', 	'S22', 	'S25', 	'E20',	'E20', 	'E20', 	'S40', 	'E20', 	'E20', 	'E20', 	'E20', 	'E20', 	'S21', 	'E20', 	'E20', 	'E20', 	-1, 	-1, 	-1, 	-1, 	-1,	 	 6,		16, 	-1, 	18, 	-1, 	-1, 	20, 	48, 		-1, 	-1 ],
	['E21', 	'E21', 		'E21', 	'E21', 	'E21', 	'E21', 	'E21', 	'E21', 	'E21', 	'E21',	'E21', 	'E21',	'E21', 	'E21', 	'E21', 	'E21', 	'E21', 	'E21', 	'E21', 	'R30', 	'E21', 	'E21', 	-1,		-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1,	 	-1 ],
	['E22', 	'E22', 		'E22', 	'S23', 	'E22', 	'E22', 	'E22', 	'E22', 	'E22', 	'E22',	'E22', 	'E22', 	'E22', 	'E22', 	'E22', 	'E22', 	'E22', 	'E22', 	'E22', 	'E22', 	'E22', 	'E22', 	-1, 	-1, 	-1,	 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E23', 	'E23', 		'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'E23',	'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'S24', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1,	 	-1 ],
	['E24', 	'E24', 		'E24', 	'R11', 	'E24', 	'E24', 	'E24', 	'R11', 	'R11', 	'E24',	'E24', 	'E24', 	'R11', 	'E24', 	'E24', 	'E24', 	'E24', 	'R11', 	'R11', 	'E24', 	'E24', 	'E24', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1,		-1 ],
	['E25', 	'E25', 		'E25', 	'S30', 	'E25', 	'E25', 	'E25', 	'E25', 	'E25', 	'S28',	'S29', 	'E25', 	'E25', 	'E25', 	'E25', 	'E25', 	'E25', 	'E25', 	'E25', 	'E25', 	'E25', 	'E25', 	-1, 	-1,	 	-1,		-1, 	-1, 	-1, 	-1, 	26, 	-1, 	-1,	 	-1,		-1,	 	-1,	 	 	-1,		-1 ],
	['E26', 	'E26', 		'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'E26',	'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'S27', 	-1, 	-1, 	-1, 	-1, 	-1,	 	-1,		-1,		-1, 	-1, 	-1, 	-1, 	-1,		-1, 		-1, 	-1 ],
	['E27', 	'E27', 		'E27', 	'R12', 	'E27', 	'E27', 	'E27', 	'R12', 	'R12', 	'E27',	'E27', 	'E27', 	'R12', 	'E27', 	'E27', 	'E27', 	'E27', 	'R12', 	'R12', 	'E27', 	'E27', 	'E27', 	-1, 	-1,	 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E28', 	'E28', 		'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'E28',	'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'R13', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E29', 	'E29', 		'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'E29',	'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'R14', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E30', 	'E30', 		'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'E30',	'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'R15', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E31', 	'E31', 		'E31', 	'E31', 	'E31', 	'E31', 	'E31', 	'E31', 	'E31', 	'E31',	'E31', 	'S32', 	'E31', 	'E31', 	'E31', 	'E31', 	'E31', 	'E31',  'E31', 	'E31', 	'E31', 	'E31', 	-1, 	-1,	 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E32', 	'E32', 		'E32', 	'S35', 	'E32', 	'E32', 	'E32', 	'E32', 	'E32', 	'E32',	'S36', 	'E32', 	'E32', 	'E32', 	'E32', 	'E32', 	'E32', 	'E32', 	'E32', 	'E32', 	'E32', 	'E32', 	-1, 	-1, 	-1, 	-1,	 	-1, 	-1, 	-1,	 	-1,		-1,	 	33, 	37, 	-1, 	-1, 		-1, 	-1 ],
	['E33', 	'E33', 		'E33', 	'E33', 	'E33', 	'E33', 	'E33', 	'E33', 	'E33', 	'E33',	'E33', 	'E33', 	'E33', 	'E33', 	'E33', 	'E33', 	'E33', 	'E33', 	'E33',  'E33', 	'E33', 	'S34', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E34', 	'E34', 		'E34', 	'R17', 	'E34', 	'E34', 	'E34', 	'R17', 	'R17', 	'E34',	'E34', 	'E34', 	'R17', 	'E34', 	'E34', 	'E34', 	'E34', 	'R17', 	'R17', 	'E34', 	'E34', 	'E34', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E35', 	'E35', 		'E35', 	'E35', 	'E35', 	'E35', 	'E35', 	'E35', 	'E35', 	'E35',	'E35', 	'E35', 	'E35', 	'E35', 	'R20', 	'E35', 	'R20', 	'E35', 	'E35', 	'E35', 	'R20', 	'R20',  -1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E36', 	'E36', 		'E36', 	'E36', 	'E36', 	'E36', 	'E36', 	'E36', 	'E36', 	'E36',	'E36', 	'E36', 	'E36', 	'E36', 	'R21', 	'E36', 	'R21', 	'E36', 	'E36', 	'E36', 	'R21', 	'R21',  -1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E37', 	'E37', 		'E37', 	'E37', 	'E37', 	'E37', 	'E37', 	'E37', 	'E37', 	'E37',	'E37', 	'E37', 	'E37', 	'E37', 	'E37', 	'E37', 	'E37', 	'E37', 	'E37', 	'E37', 	'S38', 	'R19',  -1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E38', 	'E38', 		'E38', 	'S35', 	'E38', 	'E38', 	'E38', 	'E38', 	'E38', 	'E38',	'S36', 	'E38', 	'E38', 	'E38', 	'E38', 	'E38', 	'E38', 	'E38', 	'E38', 	'E38', 	'E38', 	'E38', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1,	 	39, 	-1, 	-1, 		-1,		-1 ],
	['E39', 	'E39', 		'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'E39',	'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'R18',  -1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E40', 	'E40', 		'E40', 	'E40', 	'E40', 	'E40', 	'E40', 	'E40', 	'E40', 	'E40',	'E40', 	'E40', 	'E40', 	'S41', 	'E40', 	'40', 	'E40', 	'E40', 	'E40', 	'E40', 	'E40', 	'E40', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E41', 	'E41', 		'E41', 	'S35', 	'E41', 	'E41', 	'E41', 	'E41', 	'E41', 	'E41',	'S36', 	'E41', 	'E41', 	'E41', 	'E41', 	'E41',	'E41', 	'E41', 	'E41', 	'E41', 	'E41', 	'E41', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	42, 	-1, 	-1, 		45, 	-1 ],
	['E42', 	'E42', 		'E42', 	'E42', 	'E42', 	'E42', 	'E42', 	'E42', 	'E42', 	'E42',	'E42', 	'E42', 	'E42', 	'E42', 	'E42', 	'E42',	'S43', 	'E42', 	'E42', 	'E42', 	'E42', 	'E42', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E43', 	'E43', 		'E43', 	'S35', 	'E43', 	'E43', 	'E43', 	'E43', 	'E43', 	'E43',	'S36', 	'E43', 	'E43', 	'E43', 	'E43', 	'E43',	'E43', 	'E43', 	'E43', 	'E43', 	'E43', 	'E43', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	44, 	-1, 	-1, 		-1, 	-1 ],
	['E44', 	'E44', 		'E44', 	'E44', 	'E44', 	'E44', 	'E44', 	'E44', 	'E44', 	'E44',	'E44', 	'E44', 	'E44', 	'E44', 	'R25', 	'E44',	'E44', 	'E44', 	'E44', 	'E44', 	'E44', 	'E44', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E45', 	'E45', 		'E45', 	'E45', 	'E45', 	'E45', 	'E45', 	'E45', 	'E45', 	'E45',	'E45', 	'E45', 	'E45', 	'E45', 	'S46', 	'E45',	'E45', 	'E45', 	'E45', 	'E45', 	'E45', 	'E45', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E46', 	'E46', 		'E46', 	'E46', 	'E46', 	'E46', 	'E46', 	'E46', 	'E46', 	'E46',	'E46', 	'E46', 	'E46', 	'E46', 	'E46', 	'S47',	'E46', 	'E46', 	'E46', 	'E46', 	'E46', 	'E46', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E47', 	'E47', 		'E47', 	'R24', 	'E47', 	'E47', 	'E47', 	'R24', 	'R24', 	'E47',	'E47', 	'E47', 	'R24', 	'E47', 	'E47', 	'E47', 	'E47', 	'E47', 	'R24', 	'E47',  'E47', 	'E47', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E48', 	'E48', 		'E48', 	'S31', 	'E48', 	'E48', 	'E48', 	'S22', 	'S25', 	'E48',	'E48', 	'E48', 	'S40', 	'E48', 	'E48', 	'E48', 	'E48', 	'S55', 	'E48', 	'E48', 	'E48', 	'E48', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	50, 	-1, 	52,		-1, 	-1, 	53, 	48, 		-1, 	49 ],
	['E49', 	'E49', 		'E49', 	'R23', 	'E49', 	'E49', 	'E49', 	'R23', 	'R23', 	'E49',	'E49', 	'E49', 	'R23', 	'E49', 	'E49', 	'E49', 	'E49', 	'R23', 	'R23', 	'E49', 	'E49', 	'E49', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E50', 	'E50', 		'E50', 	'S31', 	'E50', 	'E50', 	'E50', 	'S22', 	'S25', 	'E50',	'E50', 	'E50', 	'S40', 	'E50', 	'E50', 	'E50', 	'E50',	'S55', 	'E50', 	'E50', 	'E50', 	'E50', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	50, 	-1, 	52,		-1, 	-1, 	53, 	48, 		-1, 	51 ],
	['E51', 	'E51', 		'E51', 	'R26', 	'E51', 	'E51', 	'E51', 	'R26', 	'R26', 	'E51',	'E51', 	'E51', 	'R26', 	'E51', 	'E51', 	'E51', 	'E51', 	'R26', 	'R26', 	'E51', 	'E51', 	'E51', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E52', 	'E52', 		'E52', 	'S31', 	'E52', 	'E52', 	'E52', 	'S22', 	'S25', 	'E52',	'E52', 	'E52', 	'S40', 	'E52', 	'E52', 	'E52', 	'E52',	'S55', 	'E52', 	'E52', 	'E52', 	'E52', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	50, 	-1, 	52,		-1, 	-1, 	53, 	48, 		-1, 	56 ],
	['E53', 	'E53', 		'E53', 	'S31', 	'E53', 	'E53', 	'E53', 	'S22', 	'S25', 	'E53',	'E53', 	'E53', 	'S40', 	'E53', 	'E53', 	'E53', 	'E53',	'S55', 	'E53', 	'E53', 	'E53', 	'E53', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	50, 	-1, 	52,		-1, 	-1, 	53, 	48, 		-1, 	54 ],
	['E54', 	'E54', 		'E54', 	'R28', 	'E54', 	'E54', 	'E54', 	'R28', 	'R28', 	'E54',	'E54', 	'E54', 	'R28', 	'E54', 	'E54', 	'E54', 	'E54', 	'R28', 	'R28', 	'E54', 	'E54', 	'E54', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E55', 	'E55', 		'E55', 	'R29', 	'E55', 	'E55', 	'E55', 	'R29', 	'R29', 	'E55',	'E55', 	'E55', 	'R29', 	'E55', 	'E55', 	'E55', 	'E55', 	'R29', 	'R29', 	'E55', 	'E55', 	'E55', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E56', 	'E56', 		'E56', 	'R27', 	'E56', 	'E56', 	'E56', 	'R27', 	'R27', 	'E56',	'E56', 	'E56', 	'R27', 	'E56', 	'E56', 	'E56', 	'E56', 	'R27', 	'R27', 	'E56', 	'E56', 	'E56', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E57', 	'E57', 		'E57', 	'E57', 	'E57', 	'E57', 	'E57', 	'E57', 	'E57', 	'E57',	'E57', 	'E57', 	'E57', 	'E57', 	'E57', 	'E57', 	'E57', 	'E57', 	'E57', 	'ACC', 	'E57', 	'E57', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E58', 	'E58', 		'E58', 	'E58', 	'E58', 	'E58', 	'E58', 	'E58', 	'E58', 	'E58',	'E58', 	'E58', 	'E58', 	'E58', 	'E58', 	'E58', 	'E58', 	'E58', 	'E58', 	'R2', 	'E58', 	'E58', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ]
]

# Representa na Tabela Sintatica a coluna referente ao simbolo terminal
def terminais(a):
	if a == 'inicio':
		return 0
	elif a == 'varinicio':
		return 1
	elif a == 'varfim':
		return 2
	elif a == 'id':
		return 3
	elif a == 'int':
		return 4
	elif a == 'real':
		return 5
	elif a == 'lit':
		return 6
	elif a == 'leia':
		return 7
	elif a == 'escreva':
		return 8
	elif a == 'literal':
		return 9
	elif a == 'num':
		return 10
	elif a == 'rcb':
		return 11
	elif a == 'se':
		return 12
	elif a == 'AB_P': # representa o '('
		return 13
	elif a == 'FC_P': # representa o ')'
		return 14
	elif a == 'entao':
		return 15
	elif a == 'opr': # operadores relacionais: <, >, ==, <>, <=, >=
		return 16
	elif a == 'fimse':
		return 17
	elif a == 'fim':
		return 18
	elif a == 'EOF': # $
		return 19
	elif a == 'opm': # operadores matematicos : +, -, *, /
		return 20
	elif a == 'PT_V': # representa o ';'
		return 21
		
# Representa na tabela sintatica o número da coluna referente ao não terminal
def notTerminal(A):
	if A == 'P':
		return 22
	elif A == 'V':
		return 23
	elif A == 'LV':
		return 24
	elif A == 'D':
		return 25
	elif A == 'TIPO':
		return 26
	elif A == 'A':
		return 27
	elif A == 'ES':
		return 28
	elif A == 'ARG':
		return 29
	elif A == 'CMD':
		return 30
	elif A == 'LD':
		return 31
	elif A == 'OPRD':
		return 32
	elif A == 'COND':
		return 33
	elif A == 'CABECALHO':
		return 34
	elif A == 'EXP_R':
		return 35
	elif A == 'CORPO':
		return 36

def errorSyntactic(stateError):
	if stateError == 0:
		print('Esperava palavra reservada: "inicio"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 1:
		print('Esperava palavra reservada: "varinicio"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 2:
		print('Esperava id ou Fechamento varfim'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 3:
		print('Esperava fechamento fim' +'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 4:
		print('Esperava "id" + "tipo": int / lit / real ou Fechamento varfim'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 5:
		print('Esperava inicialização: id / leia / escreva / se ou Fechamento fim' +'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 6:
		print('Condicional incorreta'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 7:
		print('Esperava ";" após varfim'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 8:
		print('Esperava inicialização: id / leia / escreva / se ou Fechamento fim' +'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 9:
		print('Esperava definição de tipo "int" / "lit" / "real"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 10:
		print('Esperava ";" após "TIPO"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 11:
		print('Declaração incorreta esperava fechamento "varfim" antes ";" ou "id" antes "TIPO"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 12 or stateError == 13 or stateError == 14:
		print('Esperava ";" após declaração de tipo'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 15 or stateError == 16 or stateError == 18 or stateError == 20:
		print('Esperava inicialização: id / leia / escreva / se ou Fechamento fim'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 17 or stateError == 19 or stateError == 21:
		print('Esperava fechamento'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 22:
		print('Esperava "id" após "leia"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 23:
		print('Esperava ";" após "id"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 25:
		print('Esperava argumento : "literal" / "num" / "id"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 26:
		print('Esperava ";" após argumento'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 28:
		print('Esperava ";"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 29:
		print('Esperava argumento "num"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 30:
		print('Esperava argumento "id"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 31:
		print('Esperava "(" após "se"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 32:
		print('Esperava ";" após atribuição'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 33:
		print('Esperava ";" após atribuição'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 34:
		print('Esperava inicialização de: "id" / "leia" / "escreva" / "se" ou Fechamento "fimse" / "fim"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 35 or stateError == 36:
		print('Esperava ";" ou ")"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 37:
		print('Esperava operador matemático : "+" / "-" / "*" / "/" após "num" ou operador : "+" após "id"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 38:
		print('Esperava "id" ou "num" após operador matematico'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 39:
		print('Esperava ";" após operação matemática ou concatenação'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 40:
		print('Esperava abertura de parênteses'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 41:
		print('Esperava "id" ou "num"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 42:
		print('Esperava operador relacional : ">" / "<" / "<>" / "=" / "<=" / ">="'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 43:
		print('Esperava "id" ou "num"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 44 or stateError == 45:
		print('Esperava fechamento de parênteses'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 46:
		print('Esperava palavra reservada "entao"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 47:
		print('Esperava declaração da condicional'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 48 or stateError == 53 or stateError == 52:
		print('Esperava inicialização: "se" / "leia" / "escreva" ... ou Fechamento "fim" ou "fimse"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 49:
		print('Esperava fechamento: "se" / "leia" / "escreva" ... ou Fechamento "fim" ou "fimse"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 50:
		print('Esperava inicialização: "se" / "leia" / "escreva" ... ou Fechamento "fim" ou "fimse"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 51:
		print('Esperava CORPO para expressao'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 54:
		print('Condicional sem CORPO'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 55: 
		print('Esperava palavra reserva "fimse" após CORPO'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 56:
		print('CMD sem CORPO'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 57:
		print('Sintaxe incorreta'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 58:
		print('Esperava fechamento "fim" de "inicio"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))

# Produçoes da gramatica
grammar = [
'P0 -> P',
'P -> inicio V A',
'V -> varinicio LV',
'LV -> D LV',
'LV -> varfim;',
'D -> id TIPO;',
'TIPO -> int',
'TIPO -> real',
'TIPO -> lit',
'A -> ES A',
'ES -> leia id;',
'ES -> escreva ARG;',
'ARG -> literal',
'ARG -> num',
'ARG -> id',
'A -> CMD A',
'CMD -> id rcb LD;',
'LD -> OPRD opm OPRD',
'LD -> OPRD',
'OPRD -> id',
'OPRD -> num',
'A -> COND A',
'COND -> CABECALHO CORPO',
'CABECALHO -> se (EXP_R) entao',
'EXP_R -> OPRD opr OPRD',
'CORPO -> ES CORPO',
'CORPO -> CMD CORPO',
'CORPO -> COND CORPO',
'CORPO -> fimse',
'A -> fim'
]
	
# Indica para qual não terminal a produção deve ser reduzida
production = [
	'P0',
	'P',  
	'V', 
	'LV', 
	'LV', 
	'D',
	'TIPO',
	'TIPO',
	'TIPO',
	'A',
	'ES',
	'ES',
	'ARG',
	'ARG',
	'ARG',
	'A',
	'CMD',
	'LD',
	'LD',
	'OPRD',
	'OPRD',
	'A',
	'COND',
	'CABECALHO',
	'EXP_R',
	'CORPO',
	'CORPO',
	'CORPO',
	'CORPO',
	'A'
]
	
# Indica a quantidade de elementos gerados por uma producao	
syzeProduction = [1,  3,  2,  2,  2,  3,  1,  1,  1,  2,  3,  3,  1,  1,  1,  2,  4,  3,  1,  1,  1,  2,  2,  5,  3,  2,  2,  2,  1,  1]

		
def syntactic():

	global flag7
	global flag2
	global flag3

	typeToken1 = None

	typeToken = lexico() 	# Vetor do tipo: Token / Lexema / Tipo retornado pelo Lexico
	a = str(typeToken[0]) 	# Acessa a posição 0 do vetor para pegar o Token 

	while(True):
		s = pilha.items[len(pilha.items)-1] # Pega o estado do topo da pilha
		#print(pilha.items) # Imprime os elementos armazenados na pilha
		#print('\n')
		
		aux = tableSyntax[s][terminais(a)] # Acessa uma posição da tabela sintatica de acordo com o estado e o terminal lido
		
		action = aux[:1] # Pega apenas a letra que configura um tipo de ação (S = Shift, R = Reduce, E = Error)
		# Verifica se action != Acept
		if action == 'S' or action == 'R' or action == 'E':
			stateLine = int(aux[1:]) # Pega o numero referente ao estado/regra gramatical/erro de estado
		
		if action == 'S':			
			pilha.push(a)
			pilha.push(stateLine)
		
			if typeToken[0] == 'id' or typeToken[0] == 'literal' or typeToken[0] == 'num':
				if typeToken[0] == 'id':
					flag2 = typeToken1
				if typeToken[0] == 'num':
					flag7 = typeToken1 # guarda o id 

				typeToken1 = typeToken
			
			typeToken = lexico()
			if typeToken[0] == 'opr':
				flag3 = typeToken

			a = str(typeToken[0])
		
		elif action == 'R':
			aux2 = production[stateLine-1] # Retorna a producao gerada
			lineProduction = stateLine-1
			

			# Desempilha de acordo com a quantidade de producoes
			for i in range(syzeProduction[stateLine-1]):
				pilha.pop()
				pilha.pop()
				
			
			stateLine = pilha.items[len(pilha.items)-1] # Retorna o estado para posterior desvio
			
			
			pilha.push(aux2) # Empilha o nao terminal referente a producao 
			pilha.push(tableSyntax[stateLine][notTerminal(aux2)]) # Empilha a linha do estado referente ao desvio
			
			semantic(grammar[lineProduction], typeToken1)
			#print (atributos.items)

			#print(pilha.items)			
			# Imprime a producao gerada pela gramatica
			#print('\nPRODUÇÃO GERADA: ' + grammar[lineProduction]+'\n')
			#print(typeToken1)
			 
		elif action == 'A':
			#print('\nPRODUÇÃO FINAL: ' + grammar[stateLine]+'\n')

			#for i in range(syzeProduction[stateLine-1]):
			#	pilha.pop()
			#	pilha.pop()

			#print(pilha.items)
			print('\n/*-----LINGUAGEM COMPILADA COM SUCESSO !!-----*/\n')

			return 
		elif action == 'E':
			#print('AlGUM ERRO OCORREU !')
			#print('Terminal: ' + a)
			print('ERRO SINATICO ENCONTRADO !!\n')
			errorSyntactic(stateLine)
			return 

'''*********************** ETAPA 3: ANALISADOR SEMÂNTICO ************************'''	


def semantic(production, typeToken):
	#aux = production.split('->') # Divide a producao em regra e sua derivacao removendo o símbolo '->'
	#regra = aux[0].replace(' ', '') # Retira o espaçamento que tem string da regra
	#derivacao = aux[1].split() # Cria um vetor da derivação ex.: ['id', 'TIPO']

	global T
	global flag3
	global flag7

	hashAux = {} # tabela hash auxiliar

	if 'LV -> varfim;' == production:
		print('Imprimido 3 linhas brancas no arquivo\n')
		objCode.write('\n\n\n')
		
	elif 'D -> id TIPO;' == production:
		print('Definido o tipo do id\n')
		tipo = atributos.pop()
		aux4 = symbolTable[typeToken[1]] 
		symbolTable[typeToken[1]] = aux4[0], aux4[1], tipo[2]
		objCode.write('\t' + tipo[2] + ' ' + symbolTable[typeToken[1]][1] + ' ' + ';\n')

	elif 'TIPO -> int' == production:
		hashAux['TIPO'] = ' ', ' ', 'int'
		atributos.push(hashAux['TIPO'])
	
	elif 'TIPO -> real' == production:
		hashAux['TIPO'] = ' ', ' ', 'double'
		atributos.push(hashAux['TIPO'])

	elif 'TIPO -> lit' == production:
		hashAux['TIPO'] = ' ', ' ', 'literal'
		atributos.push(hashAux['TIPO'])

	elif 'ES -> leia id;' == production:
		print('Código gerado para o comando leia\n')
		if symbolTable[typeToken[1]][2] == ' ':
			print('ERRO: Variável não declarada!')
			sys.exit(1)
		else:
			if symbolTable[typeToken[1]][2] == 'literal':
				objCode.write('\tscanf("%s", ' + symbolTable[typeToken[1]][1] + ');\n')
			elif symbolTable[typeToken[1]][2] == 'int':
				objCode.write('\tscanf("%d", ' + '&' + symbolTable[typeToken[1]][1] + ');\n')
			elif symbolTable[typeToken[1]][2] == 'double':
				objCode.write('\tscanf("%lf", ' + '&' + symbolTable[typeToken[1]][1] + ');\n')
	
	elif 'ES -> escreva ARG;' == production:
		print('Código gerado para o comando escreva\n')
		lexema = atributos.pop()
		if lexema[0] == 'id':
			if lexema[2] == 'int':
				objCode.write('\tprintf("%d", ' + lexema[1] + ');\n')
			elif lexema[2] == 'double':
				objCode.write('\tprintf("%lf", ' + lexema[1] + ');\n')
			else:
				objCode.write('\tprintf("%s", ' + lexema[1] + ');\n')	
		else:
			objCode.write('\tprintf(' + lexema[1] + ');\n')

	elif 'ARG -> literal' == production:
		print('Definindo ARG\n')
		hashAux['ARG'] = typeToken[0], typeToken[1], typeToken[2]
		atributos.push(hashAux['ARG'])

	elif 'ARG -> num' == production:
		print('Definindo ARG\n')
		hashAux['ARG'] = typeToken[0], typeToken[1], typeToken[2]
		atributos.push(hashAux['ARG'])

	elif 'ARG -> id' == production:
		if typeToken[1] not in symbolTable:
			print('ERRO: Variável não declarada')
			sys.exit(2)
		else:
			print('Definindo ARG\n')
			hashAux['ARG'] = typeToken[0], typeToken[1], typeToken[2]
			atributos.push(hashAux['ARG'])
	
	elif 'CMD -> id rcb LD;' == production:
		print('Verificando atribuição\n')
		print('TOKEN ANALISADO NO MOMENTO:')
		print(typeToken)
		
		if typeToken[0] == 'num':
			typeToken = flag7 

		elif flag2 != None:
			typeToken = flag2

		print(typeToken)
		if typeToken[1] not in symbolTable:
			print('ERRO: Variável não declarada!\n')
			sys.exit(3)
		else:
			LD = atributos.pop()
			print(LD)
			try:
				LD[2] == 'int' or type(int(LD[2])) == type(1)
				aux1 = type(1)
			except Exception:
				LD[2] == 'double' or type(float(LD[2])) == type(1.0)
				aux1 = type(1.0)
				
			if typeToken[2] == 'int':
				aux2 = type(1)
			elif typeToken[2] == 'double':
				aux2 = type(1.0)
			try:
				if type(aux2) == type(aux1):
					objCode.write('\t' + typeToken[1] + ' = ' + LD[1] + ';\n')
				else:
					print('ERRO: Tipos diferentes para atribuição\n')
					sys.exit(4)
			except Exception:
				print('ERRO: Vairável não declarada!\n')
				sys.exit()

	elif 'LD -> OPRD opm OPRD' == production:
		print('Verificando tipo de operadores\n')
		oprd1 = atributos.pop()
		oprd2 = atributos.pop()
		
		if oprd2[2] == 'int':
			aux1 = type(1)
		elif oprd[2] == 'double':
			aux1 = type(1.0)

		try:
			aux2 = int(oprd1[2])
		except Exception:
			aux2 = float(oprd1[2])

		if type(aux2) == aux1 and oprd1 != 'lit' and oprd2 != 'Constante Literal':
			T = T + 1
			aux = 'T' + str(T)
			hashAux['LD'] = oprd2[0], aux, oprd2[2]
			atributos.push(hashAux['LD'])
			objCode.write('\t' + aux + ' = ' + oprd2[1] + ' + ' + oprd1[1] + ';\n')
		else:
			print('ERRO: Operandos com tipos incompatíveis!\n')
			sys.exit(5)

	elif 'LD -> OPRD' == production:
		print('Passando OPRD para LD\n')
		oprd = atributos.pop()
		hashAux['LD'] = oprd[0], oprd[1], oprd[2]
		atributos.push(hashAux['LD'])

	elif 'OPRD -> id' == production:
		print('Passando atributos de id para OPRD\n')
		if typeToken[1] not in symbolTable:
			print('ERRO: Variável não declarada')
			sys.exit(6)
		else:
			hashAux['OPRD'] = typeToken[0], typeToken[1], typeToken[2]
			atributos.push(hashAux['OPRD'])

	elif 'OPRD -> num' == production:
		print('Passando atributos de num para OPRD\n')
		hashAux['OPRD'] = typeToken[0], typeToken[1], typeToken[2]
		atributos.push(hashAux['OPRD'])	

	elif 'COND -> CABECALHO CORPO' == production:
 		print('Imprimido } no arquivo\n')
 		objCode.write('\t}\n')

	elif 'CABECALHO -> se (EXP_R) entao' == production:
 		print('Imprimido condicional no arquivo\n')
 		exp_r = atributos.pop()
 		objCode.write('\tif(' + exp_r[1] + '){\n\t')

	elif 'EXP_R -> OPRD opr OPRD' == production:
		oprd1 = atributos.pop()
		oprd2 = atributos.pop()

		if oprd2[2] == 'int':
			aux1 = type(1)
		elif oprd[2] == 'double':
			aux1 = type(1.0)

		try:
			aux2 = int(oprd1[2])
		except Exception:
			aux2 = float(oprd1[2])

		if aux1 == type(aux2):
			T = T + 1
			aux = 'T' + str(T)

			hashAux['EXP_R'] = ' ', aux, ' '
			atributos.push(hashAux['EXP_R'])
			objCode.write('\t' + aux + ' = ' + oprd2[1] + flag3[2] + oprd1[1] + ';\n')
		else:
			print('ERRO: Operandos com tipos incompatíveis\n')
			sys.exit()
	
class Stack:
	def __init__(self):
		self.items = []

	def push(self, item):
		self.items.append(item)

	def pop(self):
		return self.items.pop()

	def isEmpty(self):
		return (self.items == [])

pilha = Stack() # pilha para auxiliar na analise Sintática
pilha.push(0)

atributos = Stack()	# pilha para auxiliar na analise Semântica
#atributos.push('}')


T = -1 #variavel temporária
flag7 = None
flag3 = None
flag2 = None

cursor = 0 # Indica a posição em que foi lido o último caracter
line = 1 # Indica a posição atual da linha do arquivo
position = 1 # Indica a posição do erro encontrado no arquivo


f = open("CodigoMgol.txt", 'r')
arquivo = f.read()
numChar = len(arquivo) 
f.close()

objCode = open("Programa.c", 'w')

objCode.write('#include <stdio.h>\n')
objCode.write('typedef char literal[256];\n')
objCode.write('\nvoid main(void){\n')

objCode.write('\t/*----Variaveis Temporarias----*/\n')
objCode.write('\tint T0;\n\tint T1;\n\tint T2;\n\tint T3;\n\tint T4;\n\t/*-----------------------------*/\n')

syntactic()

objCode.write('}')
objCode.close()

