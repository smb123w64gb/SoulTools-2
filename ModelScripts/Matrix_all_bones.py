import model_fmt_sc2,sys,copy

import math

def euler_to_degrees(roll, pitch, yaw):
  roll_deg = math.degrees(roll)
  pitch_deg = math.degrees(pitch)
  yaw_deg = math.degrees(yaw)
  return roll_deg, pitch_deg, yaw_deg

def degrees_to_radians(roll, pitch, yaw):
  roll_rad = roll * (math.pi / 180)
  pitch_rad = pitch * (math.pi / 180)
  yaw_rad = yaw * (math.pi / 180)
  return roll_rad, pitch_rad, yaw_rad

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