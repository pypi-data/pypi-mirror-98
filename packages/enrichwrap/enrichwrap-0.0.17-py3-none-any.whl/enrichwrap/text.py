import glob
import os

from markdown import markdown

sampleloc = os.path.dirname(__file__) + '\samples'


def joke():
    return markdown(u'Wenn ist das Nunst\u00fcck git und Slotermeyer?'
                    u'Ja! ... **Beiherhund** das Oder die Flipperwaldt '
                    u'gersput.')

def checkfile():
    print('checking samples another way')
    print(glob.glob(sampleloc + '\*.*'))

