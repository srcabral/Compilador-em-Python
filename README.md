# Compilador em Python 3.6
Este projeto é parte de uma atividade acadêmica que tinha como objetivo principal desenvolver um compilador em uma linguagem para gerar um código em C.

## Descrição do Projeto
Python é uma linguagem simples e fácil de trabalhar, por isso foi escolhida para o desenvolvimento deste compilador.

O projeto consiste da seguinte forma: dado como entrada um arquivo txt simbolizando uma linguagem nomeada como linguagem Mgol, o programa deve ser capaz de compilar o mesmo e gerar um arquivo escrito em linguagem C. 

Para isso, o projeto foi divido em 3 etapas bem definidas: 
* desenvolvimento do analisador léxico
* desenvolvimento do analisador sintático
* desenvolvimento do analisador semântico

O desenvolvimento do analisador semântico contém as partes desenvolvidas no analizador léxico e sintático, portanto é a parte final de todo este projeto.

## Informações extras sobre o Projeto
Como sabemos, o formalismo empregado pelo analisador léxico é o das Expressões Regulares. Tendo em vista isso, foi implementado no analisador léxico um DFA (Autômato Finito Determístico) representado por uma tabela de transição sobre os símbolos lidos de acordo com o estado atual do DFA. Por fim, a função do analisador léxico é retornar uma estrutura que contém 3 campos: token, lexema e tipo.

Sobre o analisador sintático o formalizo adotado é da GLC (Gramática Livre de Contexto), logo o funcionamento dessa parte do projeto consiste em receber a estrutura retornada pelo analisador léxico e por meio da estratégia de análise sintática Bottom-up, uma tabela sintática foi implementada para representar o autômato LR(0), e sobre essa tabela sintática, o analisador sintático utiliza-a para fazer as devidas análises sintáticas sobre o arquivo txt Mgol.

E por fim, o analisador semântico foi desenvolvido de maneira que ele é gerenciado pelo analisador sintático, isto é, análise semântica dirigida pelo sintático. Logos as regras semanticas são aplicadas sempre que uma operação de redução ocorre no analisador sintático.

A junção dessas 3 etapas consiste neste projeto final, que como já mencionado, recebe um arquivo escrito em linguagem hipotética (denominada de linguagem Mgol) e compila o mesmo para gerar um código simples escrito em linguagem C.
