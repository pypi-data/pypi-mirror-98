# <img src="https://uploads-ssl.webflow.com/5ea5d3315186cf5ec60c3ee4/5edf1c94ce4c859f2b188094_logo.svg" alt="Pip.Services Logo" width="200"> <br/> Tokenizers, parsers and expression calculators in Python

This module is a part of the [Pip.Services](http://pip.services.org) polyglot microservices toolkit.
It provides syntax and lexical analyzers and expression calculator optimized for repeated calculations.

The module contains the following packages:
- **Calculator** - Expression calculator
- **CSV** - CSV tokenizer
- **IO** - input/output utility classes to support lexical analysis
- **Mustache** - Mustache templating engine
- **Tokenizers** - lexical analyzers to break incoming character streams into tokens
- **Variants** - dynamic objects that can hold any values and operators for them

<a name="links"></a> Quick links:

* [API Reference](https://pip-services3-python.github.io/pip-services3-expressions-python/)
* [Change Log](CHANGELOG.md)
* [Get Help](https://www.pipservices.org/community/help)
* [Contribute](https://www.pipservices.org/community/contribute)

## Use

Install the Python package as
```bash
pip install pip_services3_expressions
```

The example below shows how to use expression calculator to dynamically
calculate user-defined expressions.

```python
from pip_services3_expressions.variants.Variant import Variant
from pip_services3_expressions.calculator.variables.Variable import Variable
from pip_services3_expressions.calculator.ExpressionCalculator import ExpressionCalculator
from pip_services3_expressions.calculator.variables.VariableCollection import VariableCollection

# ...

clalculator = ExpressionCalculator()

clalculator.expression = "A + b / (3 - Max(-123, 1)*2)"
vars = VariableCollection()
vars.add(Variable("A", Variant(1)))
vars.add(Variable("B", Variant("3")))

result = clalculator.evaluate_with_variables(vars)
print('The result of the expression is ' + result.as_string)
# ...
```

This is an example to process mustache templates.
```python
mustache = MustacheTemplate()
mustache.template = "Hello, {{{NAME}}}{{#ESCLAMATION}}!{{/ESCLAMATION}}{{#unless ESCLAMATION}}.{{/unless}}"
result = mustache.evaluate_with_variables({ 'NAME': 'Mike', 'ESCLAMATION': True }) 
print("The result of template evaluation is '" + result + "'")
```

## Develop

For development you shall install the following prerequisites:
* Python 3.7+
* Visual Studio Code or another IDE of your choice
* Docker

Install dependencies:
```bash
pip install -r requirements.txt
```

Run automated tests:
```bash
python test.py
```

Generate API documentation:
```bash
./docgen.ps1
```

Before committing changes run dockerized build and test as:
```bash
./build.ps1
./test.ps1
./clear.ps1
```

## Contacts

The module is created and maintained by **Sergey Seroukhov**
