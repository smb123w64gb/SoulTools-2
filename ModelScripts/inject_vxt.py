import model_fmt_sc2,sys
mdl_file = open(sys.argv[1], "rb")

mdl = model_fmt_sc2.VM()

mdl.read(mdl_file)
mdl_file.close()

texture_file = open(sys.argv[2], "rb")
mdl.texture = texture_file.read()
texture_file.close()
mdl_file = open(sys.argv[1], "wb")

mdl.write(mdl_file)