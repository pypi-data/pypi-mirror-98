"""juc2.art.symbols"""

from juc2.art.meta import _Meta


arrow_down = r'''
     .
       .
   . ;.
    .;
     ;;.
   ;.;;
   ;;;;.
   ;;;;;
   ;;;;;
   ;;;;;
   ;;;;;
   ;;;;;
 ..;;;;;..
  ':::::'
    ':`
'''

arrow_left = r'''
    .
  .;;............ ..
.;;;;::::::::::::..
 ':;;:::::::::::: . .
   ':
'''

arrow_right = r'''
                .
 .. ............;;.
  ..::::::::::::;;;;.
. . ::::::::::::;;:'
                :'
'''

arrow_up = r'''
     .
   .:;:.
 .:;;;;;:.
   ;;;;;
   ;;;;;
   ;;;;;
   ;;;;;
   ;:;;;
   : ;;;
     ;:;
   . :.;
     . :
   .   .

      .
'''


class Symbols:

    class ArrowDown(_Meta):
        author = 'unknown'
        figure = arrow_down

    class ArrowLeft(_Meta):
        author = 'unknown'
        figure = arrow_left

    class ArrowRight(_Meta):
        author = 'unknown'
        figure = arrow_right
    
    class ArrowUp(_Meta):
        author = 'unknown'
        figure = arrow_up
