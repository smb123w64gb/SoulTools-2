import sys
import smd_lib

obj = open(sys.argv[1], "r")

inModel = smd_lib.SMD()
inModel.read(obj)