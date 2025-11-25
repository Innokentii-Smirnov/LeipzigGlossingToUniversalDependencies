morphdict = {
      "ABL" : "Case=Abl",
      "PERL" : "Case=Per",
      "LOC" : "Case=Loc",
      "DAT" : "Case=Dat",
      "INST" : "Case=Ins",
      "VOC" : "Case=Voc",
      "CAUSEE" : "Case=Cau",
      "COM" : "Case=Com",
      "COMP" : "Case=Cmp",
      "LIM" : "Case=Lim",
      "REP" : "Case=Rep",

      "CONV" : "VerbForm=Conv",
      "NMN" : "VerbForm=Vnoun",
      "ATR" : "VerbForm=Part",

      "SG" : "Number=Sing",
      "DU" : "Number=Dual",
      "PL" : "Number=Plur",

      "1" : "Person=1",
      "2" : "Person=2",
      "3" : "Person=3",

      "IND" : "Mood=Ind",
      "DES" : "Mood=Des",
      "IMP" : "Mood=Imp",
      "COND" : "Mood=Cnd",
      "HORT" : "Mood=Hort",
      "JUSS" : "Mood=Jus",
      "PROB" : "Mood=Prob",
      "PROH" : "Mood=Proh",
      "ISP" : "Mood=Indir",
      "SUBJ" : "Mood=Subj",

      "EVID" : "Evident=Nfh",

      "INCL" : "Clusivity=In",
      "EXCL" : "Clusivity=Ex",

      "CAUS" : "Voice=Caus",

      "INDEF" : "Definite=Ind",
      "ANY" : "Definite=Ind",

      "PROG" : "Aspect=Prog",
      "ANT" : "Aspect=Ant",
      "ITER" : "Aspect=Iter",
      "USIT" : "Aspect=Usit",
      "RES" : "Aspect=Res",
      "COMPL" : "Aspect=Compl",
      "SIM" : "Aspect=Sim",
      "AVERT" : "Aspect=Avert",
      "HAB" : "Aspect=Hab",
      "MULT" : "Aspect=Mult",

      "NEG" : "Polarity=Neg",

      "FUT" : "Tense=Fut",

      "DIM" : "Degree=Dim",

      "CL" : "Classifier=Yes",
      "PRED" : "Predicative=Yes",
      "FOC" : "Focus=Yes",
      "EMPH" : "Emphatic=Yes",
      "QU" : "Question=Yes",
      "COORD" : "Coordinating=Yes",
      "REFL" : "Reflex=Yes",
      "REC" : "Reciprocal=Yes",
      "CONC" : "Conces=Yes",
      "ADD" : "Add=Yes",

      "DISC" : "INTJ",

      "A" : "NounType=Agent",
      "L" : "NounType=Locat",
      "P" : "NounType=Proc",
      "I" : "NounType=Ing",
      "VRB" : "NounType=Deverb",
      "COLL" : "NumType=Collective",
      
      "AUX" : "VerbType=Aux",

      }

# Дополнительная конфигурация (опциональная).
# Если параметры ниже отсутствуют в файле конфигурации,
# они получают значения, подходящие для нивхского языка.

# True, если в языке есть прилагательные.
# Если значение этого признака False или он отсутствует в файле конфигурации,
# все прилагательные считаются глаголами.
adjectives = False

# True, если в языке есть префиксы.
# Если значение этого признака False или он отсутствует в файле конфигурации,
# все префиксы считаются проклитиками (точнее, инкорпорированными местоимениями).
prefixes = False

# Список дефолтных значений морфосинтаксических признаков
# для каждой из тех частей речи, для которых они необходимы.
defaults: dict[str, list[str | tuple[list[str], str]]] = {
    'NOUN': ['Case=Null'],
    'VERB': ['VerbForm=Fin', (['VerbForm=Fin', 'Mood!=Imp'], 'Tense=Pres_Aor'), (['VerbForm=Vnoun'], 'Tense=Pres_Aor')]
}

# Если дефолтное значение - tuple из двух элементов, значит,
# первый элемент - это список условий, при которых нужно
# использовать данное дефолтное значение.

# Условия имеют вид Feature=Value или Feature!=Value
# и означают, что значение по умолчанию должно быть приписано при
# наличии или отсутствии определенного значения
# некоторого другого признака, соответственно.

# Порядок приписывания дефолтных значений достаточно важен,
# поскольку автоматически приписанное значение может использоваться
# в условиях для приписывания дефолтных значений последующим признакам.
# Значения приписываются в том порядке, в котором они указаны
# в списке дефолтных значений для данной части речи.

# Например:

# defaults = {
#  'NOUN': ['Case=Nom'],
#  'VERB': ['VerbForm=Fin', (['VerbForm=Fin', 'Mood!=Imp'], 'Tense=Pres')]
# }

# В данном случае время по умолчанию подставляется только
# для финитных словоформ, у которых наклонение не является
# императивом (или совсем не указано).

# Заметим, что финитность приписывается автоматически
# и поэтому должна идти в списке перед временем.
