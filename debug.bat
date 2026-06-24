@goto start
:loop
cls
@rem pause
:start
@py .\calc.py --test
@goto loop