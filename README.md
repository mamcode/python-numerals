python-numerals
===============

Módulos numerals para convertir un número en una cadena literal del número. Puede usarse para cantidades de dinero.

Esto es una adaptación del valioso [Numerals.py](http://ls-l.org/pystore/Numerals.py) desarrollado por Chema Cortés

Es un fork sencillo para utilizarlo con cantidades de dinero.

También se utiliza [Python-Inflector](https://github.com/bermi/Python-Inflector) para hacer los plurales y singulares de los terminos de la moneda.

Ejemplo:
========

>>> numerals(1202.34, andword='con', money=True, currency_word='bolívar', cents_word='céntimo')
'mil doscientos dos bolívares con treinta y cuatro céntimos'
