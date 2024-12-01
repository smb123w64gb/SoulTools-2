import model_fmt_sc2
import sys

mdl_file = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)
weght = 0.0
idxs = []
'''for x in mdl.wgtTbl.WeightBuffer4:
    idxs.append(str("%i : %.2f"%(x.bIdx,x.bWgt)))
    weght += x.bWgt
    if(weght>.999999):
        print("%s Count %i"%(str(idxs), len(idxs)))
        print(weght)
        idxs = []
        weght = 0.0'''
        