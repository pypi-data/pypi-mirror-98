'''
Made By Kar1m The Creator Of Fepzary.
Decode And Encode Text And Text Files.
'''

lst = {
	'q':'!',
	'w':'@',
	'e':'#',
	'r':'$',
	't':'%',
	'y':'^',
	'u':'&',
	'i':'🍗',
	'o':'(',
	'p':')',
	'a':'-',
	's':'_',
	'd':'=',
	'f':'+',
	'g':'1',
	'h':'2',
	'j':'3',
	'k':'4',
	'l':'5',
	':':'6',
	',':'7',
	"'":'8',
	'"':'9',
	'?':'0',
	'/':'[',
	'.':']',
	'\\':'{',
	'>':'}',
	'<':'/',
	'm':'?',
	'n':'"',
	'b':"'",
	'v':',',
	'c':'.',
	'x':'<',
	'z':'>',
	'1':'a',
	'2':'s',
	'3':'d',
	'4':'f',
	'5':'g',
	'6':'h',
	'7':'j',
	'8':'k',
	'9':'l',
	'0':'m',
	'-':'n',
	'_':'b',
	'=':'v',
	'+':'c',
	'[':'x',
	']':'z',
	'{':'q',
	'}':'w',
	'\ ':'\ ',
	'|':'r',
	'!':'y',
	'@':'t',
	'#':'u',
	'$':'i',
	'%':'o',
	'^':'p',
	'&':';',
	'*':':',
	'(':'~',
	')':'`',
	'`':'e',
	'~':'|',
	';':'💤',
	' ': ' '
}


def encode(text):
    '''
    Encodes Text With Fepzary.
    '''
    encode = ""
    for letter in text.lower():
        if letter not in lst and letter != '💤' and letter != '🍗':
            encode += letter
        else:
            encode += lst.get(letter)
    return encode

def decode(text):
    '''
    Decodes Text With Fepzary.
    '''
    encode = ""
    keys = list(lst.keys())
    vals = list(lst.values())
    for letter in text.lower():
            if letter not in lst and letter != '💤' and letter != '🍗':
                encode += letter
            else:
                encode += keys[vals.index(letter)]
    return encode

def encode_file(file):
    '''
    Encodes A File With Fepzary.
    '''
    with open(file, "r") as f:
        text = f.read()
    encode = ""
    for letter in text.lower():
        if letter not in lst and letter != '🍗': # letter != '💤' and 
            encode += letter
        else:
            encode += lst.get(letter)
    return encode

def decode_file(file):
    '''
    Decodes A File With Fepzary.
    '''
    with open(file, "r") as f:
        text = f.read()
    encode = ""
    keys = list(lst.keys())
    vals = list(lst.values())
    for letter in text.lower():
            if letter not in lst and letter != '💤' and letter != '🍗':
                encode += letter
            else:
                encode += keys[vals.index(letter)]
    return encode