# -*- encoding: utf-8 -*-
################################################################################
#
#    Módulos numerals para convertir un número en una cadena literal del número.
#    Chema Cortés - Agosto 1995
#    Convertido de clipper a python en Septiembre 2001
#    Adaptaciones hechas por Manuel Márquez para usarlo para cantidades de dinero
#    Copyright (C) 2014 Manuel Márquez <punketo28@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

from python_inflector.inflector import Inflector
from python_inflector.rules.spanish import Spanish

_n1 = ( "un","dos","tres","cuatro","cinco","seis","siete","ocho",
        "nueve","diez","once","doce","trece","catorce","quince",
        "dieciséis","diecisiete","dieciocho","diecinueve","veinte")

_n11 =( "un","dós","trés","cuatro","cinco","séis","siete","ocho","nueve")

_n2 = ( "dieci","veinti","treinta","cuarenta","cincuenta","sesenta",
        "setenta","ochenta","noventa")

_n3 = ( "ciento","dosc","tresc","cuatroc","quin","seisc",
        "setec","ochoc","novec")

def numerals(nNumero, lFemenino=0, andword='con', money=False, currency_word='bolívar', cents_word='céntimo'):
    """
    numerals(nNumero, lFemenino) --> cLiteral

    Convierte el número a una cadena literal de caracteres
    P.e.:       201     -->   "doscientos uno"
    1111     -->   "mil ciento once"

    <nNumero>       Número a convertir
    <lFemenino>     = 'true' si el Literal es femenino
    P.e.:   201     -->    "doscientas una"
    """
    # Nos aseguramos del tipo de <nNumero>
    # se podría adaptar para usar otros tipos (pe: float)

    #nNumero = long(nNumero)

    if nNumero<0:       cRes = "menos "+_numerals(-nNumero,lFemenino)
    elif nNumero==0:    cRes = "cero"
    if type(nNumero) == float:
        float_number = str(nNumero).split('.')
        nNumero = int(float_number[0])
        if nNumero == 0: cRes = "cero"
        else: cRes = _numerals(nNumero,lFemenino)
        dec = int(float_number[1])            
        if money:
            currency_word = currency_word.strip()
            cents_word = cents_word.strip()
            inflector_obj = Inflector(Inflector=Spanish)
            if nNumero != 1:
                currency_word = inflector_obj.pluralize(currency_word)
            cRes += ' '+currency_word
        if dec != 0: 
            cRes += ' '+andword.strip()+' '+_numerals(dec,lFemenino)
        if money:
            if dec != 1:
                cents_word = inflector_obj.pluralize(cents_word)
            cRes += ' '+cents_word
    else:               
        if type(nNumero) == str: nNumero = long(nNumero)
        if nNumero==0: cRes = "cero"
        else: cRes = _numerals(nNumero,lFemenino)
        if money:
            currency_word = currency_word.strip()
            inflector_obj = Inflector(Inflector=Spanish)
            if nNumero != 1:
                currency_word = inflector_obj.pluralize(currency_word)
            cRes += ' '+currency_word

    # Excepciones a considerar
    if not lFemenino and nNumero%10 == 1 and nNumero%100!=11 and not money:
        cRes += "o"

    return cRes


# Función auxiliar recursiva
def _numerals(n, lFemenino=0):

    # Localizar los billones    
    prim,resto = divmod(n,10L**12)
    if prim!=0:
        if prim==1:     cRes = "un billón"
        else:           cRes = _numerals(prim,0)+" billones" # Billones es masculino

        if resto!=0:    cRes += " "+_numerals(resto,lFemenino)

    else:
        # Localizar millones
        prim,resto = divmod(n,10**6)
        if prim!=0:
            if prim==1: cRes = "un millón"
            else:       cRes = _numerals(prim,0)+" millones" # Millones es masculino

            if resto!=0: cRes += " " + _numerals(resto,lFemenino)

        else:
            # Localizar los miles
            prim,resto = divmod(n,10**3)
            if prim!=0:
                if prim==1: cRes="mil"
                else:       cRes=_numerals(prim,lFemenino)+" mil"

                if resto!=0: cRes += " " + _numerals(resto,lFemenino)

            else:
                # Localizar los cientos
                prim,resto=divmod(n,100)
                if prim!=0:
                    if prim==1:
                        if resto==0:        cRes="cien"
                        else:               cRes="ciento"
                    else:
                        cRes=_n3[prim-1]
                        if lFemenino:       cRes+="ientas"
                        else:               cRes+="ientos"

                    if resto!=0:  cRes+=" "+_numerals(resto,lFemenino)

                else:
                    # Localizar las decenas
                    if lFemenino and n==1:              cRes="una"
                    elif n<=20:                         cRes=_n1[n-1]
                    else:
                        prim,resto=divmod(n,10)
                        cRes=_n2[prim-1]
                        if resto!=0:
                            if prim==2:                 cRes+=_n11[resto-1]
                            else:                       cRes+=" y "+_n1[resto-1]

                            if lFemenino and resto==1:  cRes+="a"
    return cRes

# Crear una demo interactiva
if __name__=="__main__":
    lFemenino=(raw_input("¿En masculino o femenino? ([M]/F) ") in "Ff")
    num=raw_input("Dame un número: ")
    print numerals(num,lFemenino)
