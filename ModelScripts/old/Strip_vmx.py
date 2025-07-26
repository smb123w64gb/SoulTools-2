from library import model_fmt_sc2
import sys

mdl_file = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)
mdl_file.close()

#print(mdl.Object_0[0].Possition)

mdl_file = open(sys.argv[2], "wb")

mdl.Object_0 = [mdl.Object_0[-1]]
mdl.Object_0[0].MatrixIndex = 0
mdl.Object_0[0].MaterailIndex = 0
mdl.materials = [mdl.materials[0]]
mdl.materials[0].TextureIdx0 = 0
mdl.Object_1 = []
mdl.Object_2 = []
mdl.header.WeightTableCount = 0

mdl.write(mdl_file)
mdl_file.close()
curtop = 1