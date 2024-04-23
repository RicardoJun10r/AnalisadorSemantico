import ply.lex as lex
import ply.yacc as yacc
import pandas as pd
import matplotlib.pyplot as plt

# Analisador Sintático para OWL
# Alunos: Vítor Duarte e Ricardo Júnior

# Lendo o arquivo no diretório do projeto, contendo o exemplo a ser analisado.
PATH = 'dados4.txt'

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
    descricao_classes : CLASS COLON ID subclasso_classes propriedades descricao_classes
                      | CLASS COLON ID subclasso_classes descricao_classes
                      | CLASS COLON ID propriedades descricao_classes
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
                      | DISJOINTCLASSES COLON expressao_classes descricao_classes
                      | EQUIVALENTO COLON expressao_classes descricao_classes
                      | SUBCLASSOF COLON expressao_classes descricao_classes
                      | DISJOINTCLASSES COLON expressao_classes
                      | EQUIVALENTO COLON expressao_classes
                      | SUBCLASSOF COLON expressao_classes propriedades
                      | SUBCLASSOF COLON expressao_classes
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

def p_propriedades(p):
    '''
    propriedades : expressao_classes descricao_classes propriedades
                 | expressao_classes propriedades
                 | empty
    '''
    global property_count
    property_count += 1
    class_name = p[-2]
    property_name = p[1]
    if class_name in environment['classes']:
        environment['classes'][class_name]['properties'].append(property_name)
    else:
        print(f"Erro semântico: Classe '{class_name}' não encontrada para registrar a propriedade '{property_name}'.")

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

# Analisador Semantico
def semantic_analysis(environment):
    errors_found = False
    semantic_errors_count = 0
    
    # Lista de operadores e sua precedência
    operator_precedence = {
        '>': 1,
        '<': 1,
        '>=': 1,
        '<=': 1,
        '==': 1,
    }
    
    def check_operator_precedence(restriction, class_name, property_name):
        operators = ['>', '<', '>=', '<=', '==', 'and', 'or']
        if len(restriction) == 3 and restriction[1] in operator_precedence:
            operator = restriction[1]
            expected_precedence = operator_precedence[operator]
            if restriction[0] in operators and restriction[2] in operators:
                # Ambos os operandos são operadores, então verifique a precedência de cada um
                left_precedence = operator_precedence.get(restriction[0], 0)
                right_precedence = operator_precedence.get(restriction[2], 0)
                if left_precedence > expected_precedence or right_precedence > expected_precedence:
                    print(f"Erro semântico: O operador '{operator}' na restrição da propriedade '{property_name}' na classe '{class_name}' tem precedência mais alta do que o esperado.")
                    return True
            elif restriction[0] in operators and restriction[1] in operators:
                # Caso especial: o primeiro operando é um operador e o segundo é o valor
                # Verifique apenas a precedência do primeiro operador
                left_precedence = operator_precedence.get(restriction[0], 0)
                if left_precedence > expected_precedence:
                    print(f"Erro semântico: O operador '{operator}' na restrição da propriedade '{property_name}' na classe '{class_name}' tem precedência mais alta do que o esperado.")
                    return True
        return False

    # Função para verificar a consistência das restrições de valores mínimos, máximos e exatos
    def check_cardinality_restrictions(restriction, class_name, property_name):
        if restriction[0] == 'exactly':
            if restriction[2] != 1:
                print(f"Erro semântico: Restrição 'exactly' para a propriedade '{property_name}' na classe '{class_name}' deve ter o valor '1'.")
                return True
        return False
    
    # Verificar consistência das propriedades
    for class_name, class_data in environment['classes'].items():
        for property_name in class_data['properties']:
            if property_name not in environment['relations']:
                print(f"Erro semântico: Propriedade '{property_name}' não definida na classe '{class_name}'.")
                errors_found = True
                semantic_errors_count += 1
            elif 'INDIVIDUALS' in environment['relations'][property_name]:
                print(f"Erro semântico: A propriedade de dados '{property_name}' na classe '{class_name}' não pode ter uma classe como domínio.")
                errors_found = True
                semantic_errors_count += 1
            elif 'DATA_TYPE' not in environment['relations'][property_name]:
                print(f"Erro semântico: A propriedade de dados '{property_name}' na classe '{class_name}' deve ter um tipo de dado como imagem.")
                errors_found = True
                semantic_errors_count += 1
            else:
                # Verificar as restrições sobre propriedades
                for restriction in class_data['properties'][property_name]:
                    if isinstance(restriction, tuple) and isinstance(restriction[0], str) and restriction[0] in ['min', 'max', 'exactly']:
                        # Verificar se o numeral está presente após os operadores min, max ou exactly
                        if len(restriction) < 3 or not isinstance(restriction[2], int):
                            print(f"Erro semântico: Após o operador '{restriction[0]}' na restrição da propriedade '{property_name}' na classe '{class_name}', é esperado um numeral.")
                            errors_found = True
                            semantic_errors_count += 1
                        else:
                            # Verificar a precedência dos operadores
                            if check_operator_precedence(restriction, class_name, property_name):
                                errors_found = True
                                semantic_errors_count += 1
                            # Verificar consistência das restrições de cardinalidade
                            if check_cardinality_restrictions(restriction, class_name, property_name):
                                errors_found = True
                                semantic_errors_count += 1
    
    # Outras verificações podem ser adicionadas aqui
    if not errors_found:
        print("Análise semântica concluída: Sem erros encontrados.")
    else:
        print(f"Análise semântica concluída: Foram encontrados {semantic_errors_count} erros.")

# Construção do analisador Sintático
parser = yacc.yacc()

# Analisa os dados utilizando o parser
parser.parse(file)

# Analisador Semantico
semantic_analysis(environment)