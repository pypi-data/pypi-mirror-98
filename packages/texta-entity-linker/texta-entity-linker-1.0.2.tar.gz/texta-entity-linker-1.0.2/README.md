### Installation

```
pip install https://pypi.texta.ee/texta-concatenator/texta-concatenator-latest.tar.gz
```



### Description

Texta EntityLinker servers as a method to link together multiple entities in the form of Texta Facts to create a more concrete
and united profile of the personal information which exists in the processed text.

This process will **ONLY** work on documents which have been previously processed by Texta MLP and contain the "BOUNDED" type Facts.

In addition, the EntityLinker needs an abbreviations.json file which contains key-value pairs of institutions shorthand name and full name. This package comes
with a base file which it uses by default but it is always possible to change it by giving the class a filepath of the file you wish to use.


*This package has no support for applying Texta MLP, you need to install the package by yourself or apply it on already processed documents.*

### Usage

#### Create an instance the class:
```python
from texta_entitylinker.entity_linker import EntityLinker

# Using the built-in abbreviations.json file.
c = EntityLinker()

# or inserting the file by path.
c = EntityLinker(abbr_file="/home/texta/abbreviations.json")
```

#### Prepare the input you wish to parse:

Letter 1:
```
Dear all, 

Let`s not forget that I intend to concure the whole of Persian Empire!

Best wishes,
Alexander Great
aleksandersuur356eKr@mail.ee
phone: 76883266

```

Letter 2:

```
От: Terry Pratchett < tpratchett@gmail.com >
Кому: Joe Abercrombie < jabercrombie@gmail.com >
Название: Разъяснение

Дорогой Joe,

Как вы? Надеюсь, у тебя все хорошо. Последний месяц я писал свой новый роман, 
который обещал представить в начале лета. Я тоже немного почитал и обожаю твою 
новую книгу!

Я просто хотел уточнить, что Alexander Great жил в Македонии.

Лучший,
Terry

```

Letter 3:

```
Dear Terry!

Terry Pratchett already created Discworld. This name is taken. Other than that I found 
the piece fascanating and see great potential in you! I strongly encourage you to take 
action in publishing your works. Btw, if you would like to show your works to Pratchett 
as well, he`s interested. I talked about you to him. His email is tpratchett@gmail.com. 
Feel free to write him!

Joe


From: Terry Berry < bigfan@gmail.com >
To: Joe Abercrombie < jabercrombie@gmail.com >
Title: Question

Hi Joe,

I finally finished my draft and I`m sending it to you. The hardest part 
was creating new places. What do you think of the names of the places I created?

Terry Berry
 
```

#### Process input through the Texta MLP package:

```python
from texta_mlp.mlp import MLP

# This folder should contain all the MLP associated models and data.
# If they don't exists, it will download them and store it at paths location,
# creating directories as needed.

# All the inputs must be processed one by one.
m = MLP(resource_dir="/home/texta/mlp_data")
mlp_analysis = m.process(letter_1)
```

This process does the basic Entity parsing and creates the BOUNDED facts needed for the entity linking process:

```
[
 {
  'doc_path': 'text.text',
  'fact': 'EMAIL',
  'lemma': None,
  'spans': '[[114, 142]]',
  'str_val': 'aleksandersuur356eKr@mail.ee'
 },

 {
  'doc_path': 'text.text',
  'fact': 'LOC',
  'lemma': None,
  'spans': '[[67, 81]]',
  'str_val': 'Persian Empire'
 },

 {
  'doc_path': 'text.text',
  'fact': 'BOUNDED',
  'lemma': "{'PER': ['Alexander Great'], 'EMAIL': "
           "['aleksandersuur356ekr@mail.ee'], 'PHONE': ['76883266']}",
  'spans': '[[98, 113], [114, 142], [151, 159]]',
  'str_val': "{'PER': ['Alexander Great'], 'EMAIL': "
             "['aleksandersuur356eKr@mail.ee'], 'PHONE': ['76883266']}"
 },

 {
  'doc_path': 'text.text',
  'fact': 'NAMEMAIL',
  'lemma': None,
  'spans': '[[98, 142]]',
  'str_val': 'Alexander Great aleksandersuur356eKr@mail.ee'
 },

 {
  'doc_path': 'text.text',
  'fact': 'PHONE',
  'lemma': None,
  'spans': '[[151, 159]]',
  'str_val': '76883266'
}
]
```

#### Load the batch into the EntityLinker:
```python
# Note that the full result of the MLP process is necessary, 
# not only the texta_facts dictionary.
c.from_json([mlp_letter_1, mlp_letter_2, mlp_letter_3])
```

#### Trigger the process for entity linking:
```python
# On larger datasets, this might take a long time.
c.link_entities()
```

#### Miscellaneous information:


You can check the length of the database lists and the content with functions:
 - cn._just_pers_infos() (type "close_persons", persons appearing close in letter(s)), 
 - cn._bounded() (the original unconcatenated bounded), 
 - cn._unsure_infos() (type "unsure_whose_entities", enities that have >=2 candidate persons, not sure to whom it belongs), 
 - cn._no_personas_infos() (type "no_per_close_entities", entities appearing close in letter(s) without persons nearby),
 - cn._persona_infos() (type "person_info", the real deal, entities with its person).
    
#### Output:

After the .link_entities() function has finished its job, you can view the full results
of the entity linking with:
```
c.to_json()

[
    {"type": "person_info", "PER": "Alexander Great", "LOC": ["Македония", "Persian Empire"], "EMAIL": ["aleksandersuur356eKr@mail.ee"], "PHONE": ["76883266"]}
    {"type": "person_info", "PER": "Joe Abercrombie", "EMAIL": ["jabercrombie@gmail.com"]}
    {"type": "person_info", "PER": "Terry Berry", "EMAIL": ["bigfan@gmail.com"]}
    {"type": "person_info", "PER": "Terry Pratchett", "EMAIL": ["tpratchett@gmail.com"]}
]