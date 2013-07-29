# -*- coding: utf-8 -*-

from api import ReversiAPI
from pprint import pprint
   
def main():
    confirm = 0
    key = u'c459b21f8cdd0ddfc49b3dda90eb1b64b676d9dc'
    r = ReversiAPI()

    for i in xrange(10):
        if r.mail_check('appp_red@mail.ru'):
            res = r.new_game(key)
        
            while res['state'] == "playing":
                #r.display(res)
            
                if confirm:
                    raw_input('Press enter to continue...')
                res = r.play(key, res)
                #pprint(res)
            
            pprint(r.score(key))


        
if __name__ == '__main__':
    main()
