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

# Regras de produção sintáticas
def p_ontologia(p):
    '''
    ontologia : descricao_classes descricao_individuals
    '''
    print("Debug: Entrou na regra p_ontologia")

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
        environment['classes'][class_name] = {'subClassOf': [], 'properties': []}

def p_subclasso_classes(p):
    '''
    subclasso_classes : SUBCLASSOF COLON expressao_classes propriedades
                      | SUBCLASSOF COLON expressao_classes
                      | empty
    '''
    if len(p) > 2:
        subclass_expr = p[3]
        environment['classes'][p[-1]]['subClassOf'] = subclass_expr

def p_propriedades(p):
    '''
    propriedades : PROPERTY propriedades
                 | PROPERTY
                 | empty
    '''
    if len(p) > 1:
        property_name = p[1]
        # Check if the property is not already in the environment and add if necessary
        if property_name not in environment['relations']:
            environment['relations'][property_name] = {}
        # Add the property to the current class
        if len(p) > 2:
            class_name = p[-1]
            environment['classes'][class_name]['properties'].append(property_name)


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
        return
    else:
        print("Erro sintático: Fim inesperado do arquivo")


def p_empty(p):
    '''
    empty :
    '''
    pass

def semantic_analysis():
    global environment
    errors_found = False
    semantic_errors_count = 0

    # Função para imprimir erros semânticos
    def print_semantic_error(message, error_type):
        nonlocal errors_found, semantic_errors_count
        print(f"Erro semântico ({error_type}): {message}")
        errors_found = True
        semantic_errors_count += 1

    # Verifica a ordem dos operadores 
    def check_header_order():
        expected_operators = ['Individuals', 'SubclassOf', 'EquivalentTo', 'DisjointClasses']
        found_operators = [op.strip() for op in file.split('\n') if op.strip().endswith(':')]

        for expected_op, found_op in zip(expected_operators, found_operators):
            if expected_op != found_op:
                print_semantic_error(f"As declarações estão fora de ordem. Esperado: {expected_op}, mas encontrado: {found_op}", "precedência_operadores")

    # Verifica coerção incorreta e classificação incorreta de propriedades
    def check_properties():
        data_properties = set()
        object_properties = set()
        overloaded_properties = set()

        for class_name, class_data in environment['classes'].items():
            properties = class_data.get('properties', [])
            for property_name in properties:
                property_data = environment['relations'].get(property_name, {})
                if 'range' in property_data:
                    if property_data['range'].startswith('xsd:'):
                        data_properties.add(property_name)
                    else:
                        object_properties.add(property_name)
                    if properties.count(property_name) > 1:
                        overloaded_properties.add(property_name)

        for property_name in data_properties:
            property_data = environment['relations'].get(property_name, {})
            if 'range' in property_data:
                if not property_data['range'].startswith('xsd:'):
                    print_semantic_error(f"A propriedade '{property_name}' é classificada como data property, mas é usada como object property", "sobrecarregamento_propriedades")
                elif property_data['range'] != 'xsd:string':
                    print_semantic_error(f"O intervalo da propriedade '{property_name}' está definido como '{property_data['range']}', mas é usado como tipo 'xsd:string'", "coerção_incorreta")

        for property_name in overloaded_properties:
            print_semantic_error(f"A propriedade '{property_name}' está sobrecarregada", "sobrecarregamento_propriedades")

    check_header_order()
    check_properties()

    if not errors_found:
        print("Análise semântica concluída: Sem erros encontrados.")
    else:
        print(f"Análise semântica concluída: Foram encontrados {semantic_errors_count} erro(s).")

def obter_tipos_propriedade(class_name, property_name):
    property_types = set()  # Conjunto para armazenar os tipos de valores encontrados

    if 'String' in class_name:
        property_types.add('string')
    elif 'Integer' in class_name:
        property_types.add('integer')
    elif 'Float' in class_name:
        property_types.add('float')

    return property_types

# Função principal
current_class = None  # Variável para rastrear a classe atual
current_relation = None  # Variável para rastrear a relação atual
current_individual = None  # Variável para rastrear o indivíduo atual

while True:
    tok = lexer.token()
    if not tok:
        break
    found_tokens.append((tok.lineno, tok.type, tok.value))
    
    if tok.type == 'PROPERTY':
        property_count += 1
        property_name = tok.value
        # Verifica se a propriedade já está no ambiente e adiciona se necessário
        if property_name not in environment['relations']:
            environment['relations'][property_name] = {}
        # Adiciona a propriedade à classe atual, se houver
        if current_class:
            environment['classes'][current_class]['properties'].append(property_name)
        # Define a relação atual
        current_relation = property_name
    elif tok.type == 'CLASS':
        classes_count += 1
        class_name = tok.value
        if class_name.islower():
            primitive_classes_count += 1
        # Verifica se a classe já está no ambiente e adiciona se necessário
        if class_name not in environment['classes']:
            environment['classes'][class_name] = {'subClassOf': [], 'properties': []}
        # Define a classe atual para associar propriedades
        current_class = class_name
    elif tok.type == 'RELATION':
        # Define a relação atual
        current_relation = tok.value
    elif tok.type == 'INDIVIDUAL':
        # Define o indivíduo atual
        current_individual = tok.value
        # Adiciona o indivíduo ao ambiente
        if current_individual not in environment['individuals']:
            environment['individuals'][current_individual] = {'subClassOf': [], 'properties': []}
    elif tok.type == 'TYPES':
        # Adiciona os tipos ao indivíduo atual
        environment['individuals'][current_individual]['subClassOf'].append(tok.value)
    elif tok.type == 'FACTS':
        # Adiciona os fatos ao indivíduo atual
        environment['individuals'][current_individual]['properties'].append(tok.value)
    elif tok.type == 'DOMAIN':
        # Define o domínio para a relação atual
        environment['relations'][current_relation]['domain'] = tok.value
    elif tok.type == 'RANGE':
        # Define a faixa para a relação atual
        environment['relations'][current_relation]['range'] = tok.value
    elif tok.type == 'INVERSEOF':
        # Define a inversa para a relação atual
        environment['relations'][current_relation]['inverseOf'] = tok.value

# Construção do analisador Sintático
parser = yacc.yacc()

# Analisa os dados utilizando o parser
parser.parse(file)

print("Análise Semântica: ")

# Analisador Semantico
semantic_analysis()
