#!/usr/bin/env python
import urllib2
import urllib
import re

# Exception Handler Class
class TransliterateError(Exception):
    pass

class Transliterate:
    _langCode = {
            'en':'ENGLISH',
            'ar':'ARABIC',
            'bn': 'BENGALI',
            'gu':'GUJARATI',
            'hi':'HINDI',
            'kn':'KANNADA',
            'ml':'MALAYALAM',
            'mr':'MARATHI',
            'ne':'NEPALI',
            'fa':'PERSIAN',
            'pa':'PUNJABI',
            'ta':'TAMIL',
            'te':'TELUGU',
            'ur':'URDU'
            }
   
    _getData = {
            'langpair' :  'en|kn',
            'num' : '5',
            'text' :   'Hello',
            'tl_app' :  '3',
            'tlqt' :  '1',
            'version' : '2',
            }

#init function. Defaulte language hindi
    def __init__(self,dest = 'kn'):
        if dest not in self._langCode:
            raise TransliterateError, "Destination language %s not supported"%dest
        self._dest = dest
        self._getData['langpair'] = 'en|kn' 
        #compose the GET Request
        try:
            params = urllib.urlencode(self._getData)		
	    url = 'http://www.google.com/transliterate/indic' 
	    page = urllib.urlopen(url,params).read()
        except Exception:
            pass


    def _getUnicode(self,s):
        """
        Return the unicode string corresponding to the encoding in s
        """
        answer = u''
        uniPattern = re.compile('\\u([0-9a-fA-F]+)')
        return answer.join([unichr(int(x, 16)) for x in uniPattern.findall(s)])


    def _getTrans(self,word):
        if word == '':
            return u''
        dest = self._dest
        #The text parameter contains the word to Transliterate
        self._getData['text'] = word
        params = urllib.urlencode(self._getData)		
	url = 'http://www.google.com/transliterate/indic' 
	page = urllib.urlopen(url,params).read()
        responsePattern = '"%s",\n\[\n"([^"]+)'%re.escape(self._getData['text'])
        response = re.compile(responsePattern)
        string = response.findall(page)
        if(len(string) == 0):
            raise TransliterateError, 'Unable to get transliteration of %s'%word
        convertedString = self._getUnicode(string[0])
        return convertedString


    def getTransliteration(self,line):
        """
        Returns transliteration of line
        By default it is hindi
        """
        #Transliteration seems to return nothing with with non-(alphanumeric) characters, so sending only alphabets
        stripped = ''
	answer = u''
        dest = self._dest
        for char in line:
            if not char.isalpha():
                answer += self._getTrans(stripped) + char
                stripped = ''
            else:
                stripped += char
        answer += self._getTrans(stripped)
        return answer

if __name__ == '__main__':
    x = Transliterate('kn')
    while True:
        try:
            inp = raw_input()
            print x.getTransliteration(inp).encode("UTF-8")
        except EOFError:
            break
