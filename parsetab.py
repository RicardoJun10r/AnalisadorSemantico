
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ALL AND AT CARDINALITY CLASS COLON COMMA DATA_TYPE DISJOINTCLASSES EQ EQUIVALENTO EXACTLY GT HAS ID INDIVIDUALS IS LBRACE LBRACKET LPAREN LT MAX MIN NOT OF ONLY OR PROPERTY RBRACE RBRACKET RESERVED RPAREN SOME SUBCLASSOF THAT VALUE\n    ontologia : descricao_classes descricao_individuals\n    \n    descricao_classes : CLASS COLON ID subclasso_classes propriedades descricao_classes\n                      | CLASS COLON ID subclasso_classes descricao_classes\n                      | CLASS COLON ID propriedades descricao_classes\n                      | CLASS COLON ID\n    \n    subclasso_classes : SUBCLASSOF COLON expressao_classes propriedades descricao_classes\n                      | DISJOINTCLASSES COLON expressao_classes descricao_classes\n                      | EQUIVALENTO COLON expressao_classes descricao_classes\n                      | SUBCLASSOF COLON expressao_classes descricao_classes\n                      | DISJOINTCLASSES COLON expressao_classes\n                      | EQUIVALENTO COLON expressao_classes\n                      | SUBCLASSOF COLON expressao_classes propriedades\n                      | SUBCLASSOF COLON expressao_classes\n    \n    propriedades : expressao_classes descricao_classes propriedades\n                 | expressao_classes propriedades\n                 | empty\n    \n    descricao_individuals : INDIVIDUALS COLON ID COMMA ID descricao_individuals\n                          | INDIVIDUALS COLON ID\n                          | empty\n    \n    expressao_classes : ID\n                      | ID AND LPAREN expressao_classes COMMA expressao_classes RPAREN\n                      | ID AND LPAREN expressao_classes COMMA ID SOME ID RPAREN\n                      | ID AND LPAREN ID SOME ID RPAREN\n                      | ID AND LPAREN ID COMMA ID SOME ID RPAREN\n    \n    empty :\n    '
    
_lr_action_items = {'CLASS':([0,9,11,12,13,15,18,21,22,23,25,26,31,32,33,34,35,39,40,41,42,46,51,54,57,58,],[3,-5,-20,3,3,3,-16,3,-3,-4,-25,-15,-2,3,-14,3,3,3,-9,-7,-8,-6,-23,-21,-24,-22,]),'$end':([1,2,4,6,9,10,22,23,29,31,36,],[0,-25,-1,-19,-5,-18,-3,-4,-25,-2,-17,]),'INDIVIDUALS':([2,9,22,23,29,31,],[5,-5,-3,-4,5,-2,]),'COLON':([3,5,14,16,17,],[7,8,24,27,28,]),'ID':([7,8,9,11,12,15,18,19,22,23,24,25,26,27,28,30,31,32,33,34,35,39,40,41,42,43,44,45,46,51,52,53,54,57,58,],[9,10,11,-20,11,11,-16,29,-3,-4,11,11,-15,11,11,37,-2,11,-14,-10,-11,-12,-9,-7,-8,47,48,49,-6,-23,55,56,-21,-24,-22,]),'SUBCLASSOF':([9,],[14,]),'DISJOINTCLASSES':([9,],[16,]),'EQUIVALENTO':([9,],[17,]),'COMMA':([10,37,38,51,54,57,58,],[19,44,45,-23,-21,-24,-22,]),'AND':([11,37,49,],[20,20,20,]),'LPAREN':([20,],[30,]),'SOME':([37,48,49,],[43,52,53,]),'RPAREN':([47,49,50,51,54,55,56,57,58,],[51,-20,54,-23,-21,57,58,-24,-22,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'ontologia':([0,],[1,]),'descricao_classes':([0,12,13,15,21,32,34,35,39,],[2,22,23,25,31,40,41,42,46,]),'descricao_individuals':([2,29,],[4,36,]),'empty':([2,9,12,15,25,29,32,],[6,18,18,18,18,6,18,]),'subclasso_classes':([9,],[12,]),'propriedades':([9,12,15,25,32,],[13,21,26,33,39,]),'expressao_classes':([9,12,15,24,25,27,28,30,32,45,],[15,15,15,32,15,34,35,38,15,50,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> ontologia","S'",1,None,None,None),
  ('ontologia -> descricao_classes descricao_individuals','ontologia',2,'p_ontologia','app.py',175),
  ('descricao_classes -> CLASS COLON ID subclasso_classes propriedades descricao_classes','descricao_classes',6,'p_descricao_classes','app.py',180),
  ('descricao_classes -> CLASS COLON ID subclasso_classes descricao_classes','descricao_classes',5,'p_descricao_classes','app.py',181),
  ('descricao_classes -> CLASS COLON ID propriedades descricao_classes','descricao_classes',5,'p_descricao_classes','app.py',182),
  ('descricao_classes -> CLASS COLON ID','descricao_classes',3,'p_descricao_classes','app.py',183),
  ('subclasso_classes -> SUBCLASSOF COLON expressao_classes propriedades descricao_classes','subclasso_classes',5,'p_subclasso_classes','app.py',193),
  ('subclasso_classes -> DISJOINTCLASSES COLON expressao_classes descricao_classes','subclasso_classes',4,'p_subclasso_classes','app.py',194),
  ('subclasso_classes -> EQUIVALENTO COLON expressao_classes descricao_classes','subclasso_classes',4,'p_subclasso_classes','app.py',195),
  ('subclasso_classes -> SUBCLASSOF COLON expressao_classes descricao_classes','subclasso_classes',4,'p_subclasso_classes','app.py',196),
  ('subclasso_classes -> DISJOINTCLASSES COLON expressao_classes','subclasso_classes',3,'p_subclasso_classes','app.py',197),
  ('subclasso_classes -> EQUIVALENTO COLON expressao_classes','subclasso_classes',3,'p_subclasso_classes','app.py',198),
  ('subclasso_classes -> SUBCLASSOF COLON expressao_classes propriedades','subclasso_classes',4,'p_subclasso_classes','app.py',199),
  ('subclasso_classes -> SUBCLASSOF COLON expressao_classes','subclasso_classes',3,'p_subclasso_classes','app.py',200),
  ('propriedades -> expressao_classes descricao_classes propriedades','propriedades',3,'p_propriedades','app.py',224),
  ('propriedades -> expressao_classes propriedades','propriedades',2,'p_propriedades','app.py',225),
  ('propriedades -> empty','propriedades',1,'p_propriedades','app.py',226),
  ('descricao_individuals -> INDIVIDUALS COLON ID COMMA ID descricao_individuals','descricao_individuals',6,'p_descricao_individuals','app.py',239),
  ('descricao_individuals -> INDIVIDUALS COLON ID','descricao_individuals',3,'p_descricao_individuals','app.py',240),
  ('descricao_individuals -> empty','descricao_individuals',1,'p_descricao_individuals','app.py',241),
  ('expressao_classes -> ID','expressao_classes',1,'p_expressao_classes','app.py',247),
  ('expressao_classes -> ID AND LPAREN expressao_classes COMMA expressao_classes RPAREN','expressao_classes',7,'p_expressao_classes','app.py',248),
  ('expressao_classes -> ID AND LPAREN expressao_classes COMMA ID SOME ID RPAREN','expressao_classes',9,'p_expressao_classes','app.py',249),
  ('expressao_classes -> ID AND LPAREN ID SOME ID RPAREN','expressao_classes',7,'p_expressao_classes','app.py',250),
  ('expressao_classes -> ID AND LPAREN ID COMMA ID SOME ID RPAREN','expressao_classes',9,'p_expressao_classes','app.py',251),
  ('empty -> <empty>','empty',0,'p_empty','app.py',268),
]
