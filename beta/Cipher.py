# -*- coding: utf-8 -*-
"""
Here we have cipher class for deciphering 
youtube signature

"""
from typing import Union, Callable
from typing import List, Tuple 
from typing import Dict, NoReturn
from typing import Any, Optional
from re import match, findall
import logging
from .Error import RegexError
from .Config import (__issues__,__github__)


logg = logging.getLogger(__name__)

def Reverse(arr:List[str], _:int) -> List[str]:
	'''
	here we will reverse the string

	example:
	>>> Reverse(['n','1','3'])
	['3', '1', 'n']
	'''
	return arr[::-1]

def Splice(arr:List[str], b:int) -> List[str]:
	'''
	here we will reverse the string

	example:
	>>> Splice(['n','1','3'],1)
	['1','n']
	'''
	return arr[b:]

def Switch(arr:List[str], b:int) -> List[str]:
	'''
	here we will swap the some chars

	var c = a[0];a[0] = a[b % a.length];a[b] = c
	'''
	tmp=arr[0]
	arr[0]=arr[b%len(arr)]
	arr[b]=tmp
	return arr

class Cipher():
	'''
	Here we will decrypt the signature of youtube videos

	js is the raw string javascript of base.js

	:param str js:
		pass javascript of base.js

	:rtype: None
	:returns: nothing
	'''
	def __init__(self,js:str) -> None:
		'''
		js is the raw string javascript of base.js

		:param str js:
			pass javascript of base.js

		:rtype: None
		:returns: nothing
		'''
		self.funs_methods = self.Get_funs(js)
		variable_name = self.funs_methods[0].split(".")[0]
		self.js_func = self.Get_js_funcs(js,variable_name)
		self.convert_funcs = self.Get_funs_objects(self.js_func)

	def Get_signature(self,sig:List[str]) -> str:
		'''
		This function will return decipher signarure

		:param list[str] sig:
			cipher signature provied by youtube

		:rtype: str
		:returns: will return decipher signature
		'''
		sig=list(sig)
		for n in self.funs_methods:
			func_name, b = self.Parsec_js_methods(n)
			sig=self.convert_funcs[func_name](sig,b)
		return "".join(sig)


	@staticmethod
	def Parsec_js_methods(s:str) -> Tuple[str, int]:
		'''
		This the parse the methods

		Example:

		>>> Parsec_js_methods("wv.TY(a,37)")
		('TY',37)
		'''
		d=s.split(".")[1]
		return d.split("(")[0], int(d.split(",")[1][:-1])
	@staticmethod
	def Func_check(s:str) -> Callable[[List[str],int], List[str]]:
		'''
		This will check compair the js function
		and return the python object

		:param str s:
			pass the js fuction

		:rtype: object
		:returns: will return python object

		example:

		>>> Func_check('TY:function(a){a.reverse()')
		<function Reverse at 0x7fd281937710>
		'''

		check = [
			{"c":["reverse"], "func": Reverse},
			{"c":["splice"], "func" : Splice},
			{"c":[ ".length","%",], "func" : Switch},
		]
		
		for n in check:
			for m in n["c"]:
				if m in s:
					return n["func"]


	def Get_funs_objects(self,funs:List[str]) -> Dict[str, Callable[[List[str],int], List[str]]]:
		'''
		This function will return the dict with
		javascript function name and object

		:param List[str] funs:
			pass the list of function

		:rtype: Dict[str, Callable[[List[str],int], List[str]]]
		:returns: dict of function name and function object

		example:

		>>> Get_funs_objects(['TY:function(a){a.reverse()}', 'A3:function(a,b){a.splice(0,b)}',
			'vd:function(a,b){var c=a[0];a[0]=a[b%a.length];a[b%a.length]=c}}'])
		{'TY': <function Reverse at 0x7f0f9cfce7a0>, 'A3': <function Splice at 0x7f0f9cfd63b0>, 
			'vd': <function Switch at 0x7f0f9cfd6710>}
		'''
		f={}
		for n in funs:
			tm=n.split(":")
			f[tm[0]] = self.Func_check(tm[1])
		return f

	@staticmethod
	def Get_funs(js:str) -> List[str]:
		'''
		Will return the method of encryption

		:param str js:
			pass the raw js of base.js

		:rtype: List[str]
		:returns: the decipher method/algorithm in list of strings

		example:

		>>> Get_funs(js)
		... ['wv.TY(a,37)', 'wv.vd(a,10)', 'wv.TY(a,7)', 'wv.A3(a,1)', 'wv.vd(a,13)', 'wv.A3(a,2)', 'wv.vd(a,15)']
		'''
		match=r'function\(a\){a=a.split\(""\);(.*);return a.join\(""\)};'
		d=findall(match,js)[0].split(";")
		if d:
			logg.debug(f"Found algorithm for decipher in JS")
			return d
		else:
			logg.error("We do not ")
			raise RegexError(f"{match} Pattern do not found in base.js, please contact {__issues__}, help us make it more stable for everyone")
	@staticmethod
	def Get_js_funcs(js:str,var:str) -> List[str]:
		'''
		will return the js raw function as string

		:param str js:
			raw js html
		:param str var:
			js variable name

		:rtype: List[str]
		:returns: the variable content/program from base.js

		Example.

		>>> Get_js_funcs(js, var)
		... ['TY:function(a){a.reverse()', 'A3:function(a,b){a.splice(0,b)', 
			'vd:function(a,b){var c=a[0];a[0]=a[b%a.length];a[b%a.length]=c}']
		'''
		match=r"var "+var+"={(.*?)};"
		d=findall(match,js.replace("\n",""))[0].split("},")
		if d:
			logg.debug(f"Variable: <{var}> found in base.js for decipher the signature")
			return [n+"}" for n in d]
		else:
			logg.error(f"Variable <{var}> do not found in base.js, please contact {__issues__}")
			raise RegexError(f"Variable <{var}> do not found in base.js, please contact {__issues__}")