import glob
import os

from markdown import markdown

def joke():
    return markdown(u'Wenn ist das Nunst\u00fcck git und Slotermeyer?'
                    u'Ja! ... **Beiherhund** das Oder die Flipperwaldt '
                    u'gersput.')

def checkfile():
    print('value of __file__')
    print(__file__)
    print('parent directory:')
    print(os.path.join(os.path.dirname(__file__), '..'))
    print('where program resides:')
    print(os.path.join(os.path.realpath(__file__)))
    print('Absolute path:')
    print(os.path.abspath(os.path.dirname(__file__)))
    print('do I have samples?')
    print(glob.glob(os.path.join(os.path.dirname(__file__), '.') + '\samples\*.*'))
    print('dirname = ' , os.path.dirname(__file__))
    print('checking samples that way')
    print(glob.glob(os.path.dirname(__file__) + '\samples\*.*'))

