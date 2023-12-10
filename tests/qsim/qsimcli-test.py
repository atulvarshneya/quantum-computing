import qsim.qcli as cli
import sys
import io

cliscript = """i 4
h 0
c 0 1
x 0
y 0
z 0
q

"""

sys.stdin= io.StringIO(cliscript)
cli.main()