import glob

import enrichwrap

def main():
    print(enrichwrap.joke())
    print(glob.glob('../enrichwrap/samples/*'))
    enrichwrap.checkfile()
