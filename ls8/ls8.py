"""MAIN"""

import sys
from cpu import CPU  

cpu = CPU()

if len(sys.argv) != 2:
    sys.exit(1)

else: 
    cpu.load(sys.argv[1])

cpu.run()