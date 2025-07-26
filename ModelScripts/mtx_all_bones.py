from library import model_fmt_sc2
import sys,copy

mdl_file = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)
mdl_file.close()

cloned_matrix = copy.deepcopy(mdl.matrix_table[0])

new_matrixes = []

firstrun = True
for x in mdl.boneInfo:
    if(x.BoneNameOffset):
        clean = copy.copy(cloned_matrix)
        clean.Type = 2
        clean.ParentBoneIdx = x.BoneIdx
        new_matrixes.append(clean)

mdl.matrix_table = new_matrixes


mdl_file = open(sys.argv[1], "wb")

mdl.write(mdl_file)