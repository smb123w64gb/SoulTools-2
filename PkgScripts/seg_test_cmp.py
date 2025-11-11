import segs
import sys

infile = open(sys.argv[1],'rb')
seg_file = segs.SEGS()
newseg = seg_file.writefile(infile)

outfile = open(sys.argv[1] + ".cmp",'wb')
newseg.write(outfile)

