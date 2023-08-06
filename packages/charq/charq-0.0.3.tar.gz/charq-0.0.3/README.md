# Welcome to CharQ!
### v.0.0.3 mar 2021

CharQ is a simple python module that provides some character blocks, random words, number and pass.

In this moment exist's two classes, CharAscii and WordGenerate.

The class CharAscii have the following methods:
- ``ascii()``: return a table with all printable ascii characters;
- ``num()``: return a table with all numbers in str format;
- ``lower(optionally)``: return a table with a-z characters, all lowers - if any character or number is passed as a parameter, it returns the same list but with two more indices, where they are, respectively, a `` space`` and a `` \ n``;
- ``up(optionally)``: return a table with A-Z characters, all uppers - if any character or number is passed as a parameter, it returns the same list but with two more indices, where they are, respectively, a `` space`` and a `` \ n``;
- ``lower_up(optionally)``: return a table with a-z and A-Z characters, all lowers and uppers - if any character or number is passed as a parameter, it returns the same list but with two more indices, where they are, respectively, a `` space`` and a `` \ n``;
- ``lower_up_num(optionally)``: return a table with a-z, A-Z and 0-9 characters, all lowers, uppers and numbers - if any character or number is passed as a parameter, it returns the same list but with two more indices, where they are, respectively, a `` space`` and a `` \ n``;
- ``symbols()``: return a table of ascii symbols printables;
- ``as_str()``: Convert class atribute val to str.
- ``get_bin(list)``: It receives a list of characteres as a parameter and returns it in a 8-digit binary.

The class WordGenerate have the following methods:
- ``word()``: return a random word, you optionally can pass the arguments tam to chose how many characters you want in your random word, and in case you choose between 'lower', 'up' or 'camel', default ``tam=10, case='lower'``;
- ``num()``: return a random number, you also can optionally pass the arguments ``tam`` to choose how many numbers, and ``typen`` to chose between formats 'str' or 'int', default ``tam=2, typen='int'``;
- ``passw()``: return a random password, use the argument ``tam`` to choose how many characters you want in your pass, default ``tam=8``;
- ``as_list()``: Convert class atribute val to table

Both classes have an attribute "val" and this attribute has the same value returned by the last method invoked by the instantiated class.

## How to Install
Just use: 
> pip install charq

## How to use
Class CharAscii.
``` 
from charq.charq import CharAscii

a = CharAscii()
a.ascii()
>>> [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '\x7f', '\n'] 
# a.val has the same value
a.num()
>>> ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
a.lower()
>>> ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] 
a.up()
>>> ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'] 
a.lower_up()
>>> ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'] 
a.lower_up_num()
>>> ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
a.as_str()
>>> 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' 

```
Class WordGenerate.
```
from charq.charq import CharAscii

a = WordGenerate()
a.word()
>>> 'ktopzxhnyn'
# a.val has the same value
a.word(tam=12, case='camel')
>>> 'Detisgihjuhx' 
a.num()
>>> 67
a.num(tam=5, typen='str')
>>> '86514'
a.passw()
>>> '{Ivb>}-"' 
a.passw(tam=20)
>>> "p(/ozfDZd3&psT]'5/0K" 
a.as_list()
>>> ['p', '(', '/', 'o', 'z', 'f', 'D', 'Z', 'd', '3', '&', 'p', 's', 'T', ']', "'", '5', '/', '0', 'K']
```

https://pypi.org/project/charq/
