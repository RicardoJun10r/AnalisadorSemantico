from owlready2 import * # type: ignore

def check_semantics(ontology_file):
    errors = []
    onto = get_ontology(ontology_file).load()

    # Verifica precedência dos operadores
    for axiom in onto.axioms():
        if isinstance(axiom, Or) and len(axiom.property_chain) > 1:
            errors.append("Precedência dos operadores não é clara: {}".format(axiom))

    # Verifica coerção
    for axiom in onto.axioms():
        if isinstance(axiom, PropertyRestriction) and axiom.cardinality is not None:
            if isinstance(axiom.cardinality, str):
                errors.append("Coerção implícita: {}".format(axiom))

    # Verifica sobrecarregamento
    for axiom in onto.axioms():
        if isinstance(axiom, PropertyRestriction) and isinstance(axiom.property(), ObjectPropertyClass):
            if len(axiom.property().restrictions) > 1:
                errors.append("Sobrecarregamento detectado: {}".format(axiom))

    return errors

# Exemplo de uso
ontology_file = "ontology.owl"  # Substitua pelo nome do arquivo da sua ontologia
semantic_errors = check_semantics(ontology_file)
if semantic_errors:
    print("Foram encontrados os seguintes erros semânticos:")
    for error in semantic_errors:
        print(error)
else:
    print("Nenhum erro semântico encontrado.")
