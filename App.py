import ply.lex as lex
import ply.yacc as yacc
import pandas as pd
import matplotlib.pyplot as plt

# Analisador Sintático para OWL
# Alunos: Vítor Duarte e Ricardo Júnior

# Lendo o arquivo no diretório do projeto, contendo o exemplo a ser analisado.
PATH = 'dados3.txt'

try:    
    with open(PATH, 'r') as arquivo:
        file = arquivo.read()
except FileNotFoundError:
    print(f"Arquivo não encontrado '{PATH}' !!!")
except Exception as e:
    print(f"ERRO: '{e}'")

environment = {
    'classes': {},
    'individuals': {},
    'relations': {}
}

# Abaixo estão as palavras reservadas da linguagem e logo em seguida todos os tokens
reserved = {
    'some': 'SOME',
    'all': 'ALL',
    'value': 'VALUE',
    'min': 'MIN',
    'max': 'MAX',
    'exactly': 'EXACTLY',
    'that': 'THAT',
    'not': 'NOT',
    'and': 'AND',
    'or': 'OR',
    'only': 'ONLY',
    'class': 'CLASS',
    'equivalentto': 'EQUIVALENTO',
    'individuals': 'INDIVIDUALS',
    'subclassof': 'SUBCLASSOF',
    'disjointclasses': 'DISJOINTCLASSES'
}

tokens = [
    'ID',
    'HAS',
    'IS',
    'OF',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'LBRACE',
    'RBRACE',
    'COMMA',
    'GT',
    'LT',
    'EQ',
    'COLON',
    'CARDINALITY',
    'DATA_TYPE',
    'PROPERTY',
    'RESERVED',
    'AT'
] + list(reserved.values())

t_SOME = r'some'
t_ALL = r'all'
t_VALUE = r'value'
t_MIN = r'min'
t_MAX = r'max'
t_EXACTLY = r'exactly'
t_THAT = r'that'
t_NOT = r'not'
t_AND = r'and'
t_OR = r'or'
t_CLASS = r'class'
t_EQUIVALENTO = r'equivalentto'
t_INDIVIDUALS = r'individuals'
t_SUBCLASSOF = r'subclassof'
t_DISJOINTCLASSES = r'disjointclasses'
t_HAS = r'has'
t_IS = r'is'
t_OF = r'of'
t_ONLY = r'only'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_COMMA = r','
t_GT = r'>'
t_LT = r'<'
t_COLON = r':'
t_EQ = r'='
t_AT = r','

# Abaixo estão as funções para reconhecer cada token ou palavra reservada da linguagem, contendo as expressões regulares para reconhecer as cadeias.
def t_RESERVED(t):
    r'(individuals|subclassof|disjointclasses|some|all|and|value|min|max|exactly|only|that|not)'
    t.type = reserved.get(t.value, 'RESERVED')  # Usando o dicionário de palavras reservadas
    return t

def t_DATA_TYPE(t):
    r'(owl:|rdfs:|xsd:)\w+'
    t.type = 'DATA_TYPE'
    return t

def t_INDIVIDUAL(t):
    r'[A-Z][a-zA-Z0-9]*\d+'
    t.type = 'INDIVIDUALS'
    return t

def t_PROPERTY(t):
    r'(\bis\w*Of\b)|(\bhas\w*\b)|([a-z]+\w*)'
    t.type = 'PROPERTY'
    return t

def t_CARDINALITY(t):
    r'\d+'
    t.type = 'CARDINALITY'
    return t

def t_Class(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = 'CLASS'
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Erro léxico: Caractere ilegal '{t.value[0]}' na linha {t.lineno}, posição {t.lexpos}")
    t.lexer.skip(1)

# Inicialização do analisador léxico
lexer = lex.lex()

lexer.input(file)

# Declaração de variáveis para contar as ocorrências dos tokens e demais coisas
found_tokens = []
property_count = 0
classes_count = 0
primitive_classes_count = 0

# Função principal
while True:
    tok = lexer.token()
    if not tok:
        break
    found_tokens.append((tok.lineno, tok.type, tok.value))
    if tok.type == 'PROPERTY':
        property_count += 1
    elif tok.type == 'CLASS':
        classes_count += 1
        if tok.value.islower():
            primitive_classes_count += 1

# Em seguida está o resumo da análise
print(f"######################################## Resumo #########################################")
print(f"#                           Quantidade de Propriedades: {property_count}\t\t\t\t#")
print(f"#                           Quantidade de Classes: {classes_count}\t\t\t\t\t#")
print(f"#########################################################################################")

# Regras de produção sintáticas
def p_ontologia(p):
    '''
    ontologia : descricao_classes descricao_individuals
    '''

def p_descricao_classes(p):
    '''
    descricao_classes : CLASS COLON ID subclasso_classes descricao_classes
                      | CLASS COLON ID
    '''
    class_name = p[3]
    if class_name in environment['classes']:
        print(f"Erro semântico: Classe '{class_name}' já definida.")
    else:
        environment['classes'][class_name] = {'equivalentTo': [], 'subClassOf': [], 'disjointWith': [], 'properties': []}

def p_subclasso_classes(p):
    '''
    subclasso_classes : SUBCLASSOF COLON expressao_classes propriedades descricao_classes
                      | SUBCLASSOF COLON expressao_classes propriedades
                      | SUBCLASSOF COLON expressao_classes descricao_classes
                      | SUBCLASSOF COLON expressao_classes
                      | DISJOINTCLASSES COLON expressao_classes descricao_classes
                      | DISJOINTCLASSES COLON expressao_classes
                      | EQUIVALENTO COLON expressao_classes descricao_classes
                      | EQUIVALENTO COLON expressao_classes
                      | empty
    '''
    if len(p) > 2:
        if 'SUBCLASSOF' in p[1]:
            superclass = p[3]
            if superclass not in environment['classes']:
                print(f"Erro semântico: Superclasse '{superclass}' não definida.")
            else:
                environment['classes'][p[-1]]['subClassOf'].append(superclass)
        elif 'DISJOINTCLASSES' in p[1]:
            disjoint_class = p[3]
            if disjoint_class not in environment['classes']:
                print(f"Erro semântico: Classe disjunta '{disjoint_class}' não definida.")
            else:
                environment['classes'][p[-1]]['disjointWith'].append(disjoint_class)
        elif 'EQUIVALENTO' in p[1]:
            equivalent_class = p[3]
            if equivalent_class not in environment['classes']:
                print(f"Erro semântico: Classe equivalente '{equivalent_class}' não definida.")
            else:
                environment['classes'][p[-1]]['equivalentTo'].append(equivalent_class)

def p_properties(p):
    '''
    propriedades : expressao_classes descricao_classes propriedades
                 | expressao_classes propriedades
                 | empty
    '''
    global property_count
    property_count += 1

def p_descricao_individuals(p):
    '''
    descricao_individuals : INDIVIDUALS COLON ID COMMA ID descricao_individuals
                          | INDIVIDUALS COLON ID
                          | empty
    '''
    pass

def p_expressao_classes(p):
    '''
    expressao_classes : ID
                      | ID AND LPAREN expressao_classes COMMA expressao_classes RPAREN
                      | ID AND LPAREN expressao_classes COMMA ID SOME ID RPAREN
                      | ID AND LPAREN ID SOME ID RPAREN
                      | ID AND LPAREN ID COMMA ID SOME ID RPAREN
    '''

def p_error(p):
    if p:
        print(f"Erro sintático: Erro de sintaxe em '{p.value}' na linha {p.lineno}, posição {p.lexpos}")
        # Verifica se o número da linha está dentro dos limites do código
        if p.lineno - 1 < len(file.splitlines()):
            print(f"Trecho do código: {file.splitlines()[p.lineno - 1]}")
        else:
            print("Trecho do código indisponível")
    else:
        print("Erro sintático: Fim inesperado do arquivo")


def p_empty(p):
    '''
    empty :
    '''
    pass

# Construção do analisador Sintático
parser = yacc.yacc()

# Analisa os dados utilizando o parser
parser.parse(file)

# Analisador Semantico
def semantic_analysis(environment):
    errors_found = False
    
    # Verificar consistência das classes
    for class_name, class_data in environment['classes'].items():
        order = ['CLASS', 'EQUIVALENTO', 'SUBCLASSOF', 'DISJOINTCLASSES', 'INDIVIDUALS']
        current_order_index = 0
        
        for key in class_data.keys():
            if key == order[current_order_index]:
                current_order_index += 1
            else:
                print(f"Erro semântico: A palavra-chave '{key}' na descrição da classe '{class_name}' não segue a ordem correta.")
                errors_found = True
                break
                
        if current_order_index < len(order):
            print(f"Erro semântico: A descrição da classe '{class_name}' está incompleta. A palavra-chave '{order[current_order_index]}' é esperada.")
            errors_found = True
    
        for subclass in class_data['subClassOf']:
            if subclass not in environment['classes']:
                print(f"Erro semântico: Superclasse '{subclass}' não definida na classe '{class_name}'.")
                errors_found = True
        for disjoint_class in class_data['disjointWith']:
            if disjoint_class not in environment['classes']:
                print(f"Erro semântico: Classe disjunta '{disjoint_class}' não definida na classe '{class_name}'.")
                errors_found = True
        for equivalent_class in class_data['equivalentTo']:
            if equivalent_class not in environment['classes']:
                print(f"Erro semântico: Classe equivalente '{equivalent_class}' não definida na classe '{class_name}'.")
                errors_found = True
    
    # Verificar consistência das propriedades
    for class_name, class_data in environment['classes'].items():
        for property_name in class_data['properties']:
            if property_name not in environment['relations']:
                print(f"Erro semântico: Propriedade '{property_name}' não definida na classe '{class_name}'.")
                errors_found = True
    
    # Outras verificações podem ser adicionadas aqui
    
    if not errors_found:
        print("Análise semântica concluída: Sem erros encontrados.")
    else:
        print("Análise semântica concluída: Foram encontrados erros.")
        
print("ANALISE SEMANTICAAAAAAAAAAAAAAAAAAAAAAA")
# Chamada da análise semântica
semantic_analysis(environment)
