# oarepo-taxonomies
Wrapper that connect Flask-Taxonomies with Invenio.

[![image][]][1]
[![image][2]][3]
[![image][4]][5]
[![image][6]][7]
[![image][8]][9]

  [image]: https://img.shields.io/travis/oarepo/oarepo-taxonomies.svg
  [1]: https://travis-ci.org/oarepo/oarepo-taxonomies
  [2]: https://img.shields.io/coveralls/oarepo/oarepo-taxonomies.svg
  [3]: https://coveralls.io/r/oarepo/oarepo-taxonomies
  [4]: https://img.shields.io/github/tag/oarepo/oarepo-taxonomies.svg
  [5]: https://github.com/oarepo/oarepo-taxonomies/releases
  [6]: https://img.shields.io/pypi/dm/oarepo-taxonomies.svg
  [7]: https://pypi.python.org/pypi/oarepo-taxonomies
  [8]: https://img.shields.io/github/license/oarepo/oarepo-taxonomies.svg
  [9]: https://github.com/oarepo/oarepo-taxonomies/blob/master/LICENSE
  


## Installation

The package is installed classically via the PyPi repository:

`pip install oarepo-taxonomies`

The database is initialized using the management task:

`invenio taxonomies init`

## Quick start

All functionality is provided by flask-taxonomies. For more details see: 
[flask-taxonomies](https://pypi.org/project/flask-taxonomies/7.0.0a13/).

In addition, this package adds the ability to import and export taxonomies using Excel files (* .xlsx)
and can dereference a reference to a taxonomy in an invenio record.

### Import from Excel

Importing from Excel is handled by the management task:

`invenio taxonomies import [OPTIONS] TAXONOMY_FILE`

Options:  
  --int TEXT  
  --str TEXT  
  --bool TEXT  
  --drop / --no-drop  
  --help
  
where:
* `TAXONOMY FILE` is path to the xlsx file (older xls file is not supported)
* `--int, --str, --bool` options are repeatable options and determine data type
* `--drop/--no-drop` Specifies whether the old taxonomy should be removed from the database when we import a
 taxonomy with the same **taxonomy code**.
 
#### Structure of Excel file

**Blocks**

Excel must contain two blocks. The first block contains taxonomy information and must contain one mandatory code column
(taxonomy identifier). Indeed, it can contain other user data (eg. title or description). 

The second block must be
separated from the first by a blank line and must contain two mandatory columns, **level** and **slug**, in exactly
 that order. The other columns are optional.
 
**Nested JSON**  
Taxonomies are internally represented as JSON, which can be nested. Excel spreadsheet is inherently linear and can not
store nested data. However, oarepo-taxonomies support nested JSON. Each value in a nested JSON has its own unique
address. Each JSON level is separated by an underscore, so each branched JSON can be transformed to linear as follows.

Nested:
```json
{
    "a": 1,
    "b": 2,
    "c": [{"d": [2, 3, 4], "e": [{"f": 1, "g": 2}]}]
}
```

Linear:
```json
{"a": 1,
 "b": 2,
 "c_0_d_0": 2,
 "c_0_d_1": 3,
 "c_0_d_2": 4,
 "c_0_e_0_f": 1,
 "c_0_e_0_g": 2
}
```

According to the same pattern, headings can be created in Excel and the data is transformed into a nested form.
 
**Level order**

Taxonomies are tree structures that are also not linear and cannot be transferred to an Excel spreadsheet environment.
Therefore, the sort order goes from root to the lowest child. Root (Taxonomy) -> level 1 first child - ... last
level all children, level 1 second offspring ... etc.

**Excel example**

| code   | title_cs | title_en       |                |
|--------|----------|----------------|----------------|
| cities | Města    | Cities         |                |
|        |          |                |                |
|        |          |                |                |
| level  | slug     |       title_cs |       title_en |
| 1      | eu       |         Evropa |         Europe |
| 2      | cz       | Česko          | Czechia        |
| 3      | prg      | Praha          | Prague         |
| 3      | brn      | Brno           | Brno           |
| 2      | de       | Německo        | Germany        |
| 3      | ber      | Berlín         | Berlin         |
| 3      | mun      | Mnichov        | Munich         |
| 2      | gb       | Velká Británie | United Kingdom |
| 3      | lon      | Londýn         | London         |
| 3      | man      | Manchester     | Manchester     |

The resulting json for the taxonomy will take the following form:

```json
{
  "code": "cities",
  "title": {
    "cs": "Města",
    "en": "Citites"
  }
}
```

and for individual Taxonomy Term:

```json
{
  "code": "Praha",
  "title": {
    "cs": "Praha",
    "en": "Prague"
  }
}
```

and tree structure:
<pre>
cities  
└-eu  
  |--cz  
  |  |--prg  
  |  └--brn  
  |--de  
  |  |--ber   
  |  └--mun  
  └--gb  
     |--lon   
     └--man      
</pre>  

### Export to Excel

Excel export is created using a management task `invenio taxonomies export TAXONOMY_CODE`.

An xlsx and csv file is created in the current folder where the task was run.

### Marshmallow
The Marshmallow module serialize Taxonomy and dereference reference from links/self.
The module provides the Marshmallow field `TaxonomyField` and schema ``TaxonomySchema``, 
which can be freely used in the user schema.
TaxonomyField/Schema receives any user data and checks if the user data is JSON/dict, string or list.

The output format of serialized taxonomies is the Taxonomic List, which contains ancestors in addition to the taxonomy
itself. The order of taxonomy is from the parent term to the finite element of the taxonomy. For taxonomy reason, the
serialization is opinionated. Example of taxonomy serialization is following:

```json5
[{
        'is_ancestor': true,
        'links': {'self': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a'},
        'test': 'extra_data'
    },
        {
            'created_at': '2014-08-11T05:26:03.869245',
            'email': 'ken@yahoo.com',
            'is_ancestor': false,
            'links': {
                'parent': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a',
                'self': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a/b'
            },
            'name': 'Ken',
            'test': 'extra_data'
        }]
```

Taxonomy representation can be changed in config file (e.g.: invenio.cfg). For more details 
please see [Flask-Taxonomies](https://github.com/oarepo/flask-taxonomies#includes-and-excludes).

This library use predefinded config that is located in `config.py`:

```python
FLASK_TAXONOMIES_REPRESENTATION = {
    "taxonomy": {
        'include': [INCLUDE_DATA, INCLUDE_ANCESTORS, INCLUDE_URL, INCLUDE_SELF,
                    INCLUDE_ANCESTOR_LIST, INCLUDE_ANCESTOR_TAG, INCLUDE_PARENT],
        'exclude': [],
        'select': None,
        'options': {}
    }
}
```

There are two ways to use TaxonomyField.

1. The input format is a dictionary or text string containing a link to the taxonomy.
    * dictionary:
        The dictionary must contain the nested dictionary with name `links`, which contains `self`.
    * string: Any text that contains a url to the taxonomy.
2. The input format is list of ancestors, where last is the referenced taxonomy.
 
* dictionary       
```python
from marshmallow import Schema

from oarepo_taxonomies.marshmallow import TaxonomyField

# custom schema
class TestSchema(Schema):
    field = TaxonomyField()

# taxonomy dict
random_user_taxonomy = {
    "created_at": "2014-08-11T05:26:03.869245",
    "email": "ken@yahoo.com",
    "name": "Ken",
    "links": {
        "self": "http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a/b"
    }
}

# record dict
data = {
    "field": random_user_taxonomy
}

schema = TestSchema()
result = schema.load(data)
assert result == {
    'field': [{
        'is_ancestor': True,
        'links': {'self': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a'},
        'test': 'extra_data'
    },
        {
            'created_at': '2014-08-11T05:26:03.869245',
            'email': 'ken@yahoo.com',
            'is_ancestor': False,
            'links': {
                'parent': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a',
                'self': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a/b'
            },
            'name': 'Ken',
            'test': 'extra_data'
        }]
}
```
    
* string       
```python
from marshmallow import Schema

from oarepo_taxonomies.marshmallow import TaxonomyField

# custom schema
class TestSchema(Schema):
    field = TaxonomyField()

# taxonomy reference as any string with url
random_user_taxonomy = "bla bla http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a/b"

# record dict
data = {
    "field": random_user_taxonomy
}

schema = TestSchema()
result = schema.load(data)
assert result == {
    'field': [{
                  'is_ancestor': True,
                  'links': {'self': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a'},
                  'test': 'extra_data'
              },
              {
                  'is_ancestor': False,
                  'links': {
                      'parent': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a',
                      'self': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a/b'
                  },
                  'test': 'extra_data'
              }]
}
```

* list
```python
from marshmallow import Schema

from oarepo_taxonomies.marshmallow import TaxonomyField

# custom schema
class TestSchema(Schema):
    field = TaxonomyField()

# taxonomy list with ancestor (root ancestor at the first place)
random_user_taxonomy = [
    {
        'links': {'self': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a'},
    },
    {
        'links': {
            'self': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a/b'
        },
        'test': 'extra_data',
        'next': 'bla',
        'another': 'something'
    }
]

# record dict
data = {
    "field": random_user_taxonomy
}

schema = TestSchema()
result = schema.load(data)
assert result == {
    'field': [{
        'is_ancestor': True,
        'links': {'self': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a'},
        'test': 'extra_data'
    },
        {
            'another': 'something',
            'is_ancestor': False,
            'links': {
                'parent': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a',
                'self': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a/b'
            },
            'next': 'bla',
            'test': 'extra_data'
        }]
}
```
#### TaxonomyField vs. TaxonomySchema

``TaxonomySchema`` is a marshmallow schema, that can be subclassed and used, for example,
inside ``Nested``.

``TaxonomyField`` is a marshmallow ``Field`` that is used as is. The field also allows extending
taxonomy metadata model with extra properties.

Signature of the factory is following `TaxonomyField(*args, extra=None, name=None, many=False,
 mixins: list = None, **kwargs)`
 
 * **args**: arbitrary arguments passed to marshmallow.schema
 * **extra**: a dictionary of extra marshmallow fields (key: field name, value: instance of Field)
 * **name**: optional name of the field (it is used as a name of the dynamically created class 
             on the background)
 * **mixins**: list of added mixins (class defining extra marshmallow Fields)
 * **kwargs**: arbitrary named arguments passed to the generated marshmallow schemas

```python
class InstitutionMixin:
    name = SanitizedUnicode()
    address = SanitizedUnicode()

class TestSchema(Schema):
    field = TaxonomyField(many=True, mixins=[InstitutionMixin])

random_user_taxonomy = [
        {
            'links': {'self': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a'},
        },
        {
            'links': {
                'self': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a/b'
            },
            'test': 'extra_data',
            'next': 'bla',
            'another': 'something',
            'name': 'Hogwarts',
            'address': 'Platform nine and three-quarters'
        }
    ]

data = {
    "field": random_user_taxonomy
}

schema = TestSchema()
result = schema.load(data)
assert result == {
    'field': [{
                  'is_ancestor': True,
                  'links': {'self': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a'},
                  'test': 'extra_data'
              },
              {
                  'address': 'Platform nine and three-quarters',
                  'another': 'something',
                  'is_ancestor': False,
                  'links': {
                      'parent': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a',
                      'self': 'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/a/b'
                  },
                  'name': 'Hogwarts',
                  'next': 'bla',
                  'test': 'extra_data'
              }]
}
```

### JSONSchemas

The library offers a predefined JSON schema for taxonomies.
The predefined schema is called with `"$ref": "../taxonomy-v2.0.0.json#/definitions/TaxonomyTerm"`
and is available in Invenio in `current_jsonschemas.list_schemas()`. 

Custom schema example:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "id": "https://example.com/schemas/example_json-v1.0.0.json",
  "additionalProperties": false,
  "title": "My site v1.0.0",
  "type": "object",
  "properties": {
    "$schema": {
      "type": "string"
    },
    "custom_taxonomy": {
      "$ref": "../taxonomy-v2.0.0.json#/definitions/TaxonomyTerm"
    }
  }
}

```

### Elasticsearch mapping

Predefined mappings can be used for indexing into Elasticsearch. If you want to use this mapping you must use the
library [OAREPO mapping includes](https://github.com/oarepo/oarepo-mapping-includes). A reference to
taxonomy mapping is then inserted to custom mapping as either 
`"type": "taxonomy-v2.0.0.json#/TaxonomyTerm"` or `"type": "taxonomy-term"`.

Custom mapping example:

```json
{
  "mappings": {
    "date_detection": false,
    "numeric_detection": false,
    "dynamic": false,
    "properties": {
      "$schema": {
        "type": "keyword",
        "index": true
      },
      "custom_taxonomy": {
        "type": "taxonomy-v2.0.0.json#/TaxonomyTerm"
      }
    }
  }
}
```

### Signals
This module will register the following signal handlers on the Flask Taxonomies signals that handle managing of
 reference Taxonomies whenever a Taxonomy or TaxonomyTerm changes:
 
 | Flask-Taxonomies signals     | Registred signal [handler](https://github.com/oarepo/oarepo-taxonomies/blob/master/oarepo_taxonomies/signals.py) | Description                                                                                      |
|------------------------------|--------------------------|--------------------------------------------------------------------------------------------------|
| before_taxonomy_deleted      | taxonomy_delete          | Checks if the changed taxonomy is a reference to any record. If so, they throw an exception.     |
| before_taxonomy_term_deleted | taxonomy_term_delete     | Checks if the changed TaxonomyTerm is a reference to any record. If so, they throw an exception. |
| after_taxonomy_term_updated  | taxonomy_term_update     | Replaces the link in the records to the moved TaxonomyTerm.                                      |
| after_taxonomy_term_moved    | taxonomy_term_moved      | Replaces the contents of the changed taxonomy in the referenced records.                         |
