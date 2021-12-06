
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftOPleftIDleftVAUTADDITIONNE AFFICHER DE ID NUMBER PUIS SOUSTRAIT VAUTprogram : sentenceprogram : sentence programsentence : subordinate "."sentence : subordinate PUIS sentence\n        | subordinate "," sentenceprint : AFFICHER expressionsubordinate : assign\n        | printassign : ID VAUT expressionexpression : NUMBERexpression : IDoperator : ADDITIONNE DE %prec OP\n        | SOUSTRAIT DE %prec OPexpression : expression operator expression %prec OP'
    
_lr_action_items = {'ID':([0,2,7,9,10,11,12,16,17,19,23,24,],[6,6,15,-3,6,6,15,-4,-5,15,-12,-13,]),'AFFICHER':([0,2,9,10,11,16,17,],[7,7,-3,7,7,-4,-5,]),'$end':([1,2,8,9,16,17,],[0,-1,-2,-3,-4,-5,]),'.':([3,4,5,13,14,15,18,22,],[9,-7,-8,-6,-10,-11,-9,-14,]),'PUIS':([3,4,5,13,14,15,18,22,],[10,-7,-8,-6,-10,-11,-9,-14,]),',':([3,4,5,13,14,15,18,22,],[11,-7,-8,-6,-10,-11,-9,-14,]),'VAUT':([6,],[12,]),'NUMBER':([7,12,19,23,24,],[14,14,14,-12,-13,]),'ADDITIONNE':([13,14,15,18,22,],[20,-10,-11,20,-14,]),'SOUSTRAIT':([13,14,15,18,22,],[21,-10,-11,21,-14,]),'DE':([20,21,],[23,24,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,2,],[1,8,]),'sentence':([0,2,10,11,],[2,2,16,17,]),'subordinate':([0,2,10,11,],[3,3,3,3,]),'assign':([0,2,10,11,],[4,4,4,4,]),'print':([0,2,10,11,],[5,5,5,5,]),'expression':([7,12,19,],[13,18,22,]),'operator':([13,18,22,],[19,19,19,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> sentence','program',1,'p_program_sentence','parser5.py',19),
  ('program -> sentence program','program',2,'p_program_recursive','parser5.py',23),
  ('sentence -> subordinate .','sentence',2,'p_sentence_subordinate','parser5.py',27),
  ('sentence -> subordinate PUIS sentence','sentence',3,'p_sentence_recursive','parser5.py',31),
  ('sentence -> subordinate , sentence','sentence',3,'p_sentence_recursive','parser5.py',32),
  ('print -> AFFICHER expression','print',2,'p_print','parser5.py',37),
  ('subordinate -> assign','subordinate',1,'p_subordinate_assign','parser5.py',41),
  ('subordinate -> print','subordinate',1,'p_subordinate_assign','parser5.py',42),
  ('assign -> ID VAUT expression','assign',3,'p_assign','parser5.py',46),
  ('expression -> NUMBER','expression',1,'p_expression_num','parser5.py',50),
  ('expression -> ID','expression',1,'p_expression_id','parser5.py',54),
  ('operator -> ADDITIONNE DE','operator',2,'p_operator','parser5.py',58),
  ('operator -> SOUSTRAIT DE','operator',2,'p_operator','parser5.py',59),
  ('expression -> expression operator expression','expression',3,'p_expression_op','parser5.py',63),
]
