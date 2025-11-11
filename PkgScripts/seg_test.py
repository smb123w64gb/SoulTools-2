import segs
import sys

infile = open(sys.argv[1],'rb')
seg_file = segs.SEGS()
seg_file.read(infile)

outfile = open(sys.argv[1] + ".dec",'wb')
for x in seg_file.ents:
    outfile.write(x.data)
