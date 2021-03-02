from wwlib.rarc import *
from wwlib.gcm import *
from paths import *
import os
import unicodedata as ucc

gcm = GCM("/Users/zach_lucius/Desktop/iso/Legend of Zelda, The - The Wind Waker (USA).iso")
gcm.read_entire_disc()
data = gcm.read_file_data("files/res/Msg/itemicon.arc")
outp = "/Users/zach_lucius/Desktop/tww/res/Msg/hold/"
arc = RARC()
arc.read(data)
arc.extract_all_files_to_disk(outp)
#arc.extract_all_files_to_disk(outp)
# '''
# kerning data starts: 0x01208C
# kerning data ends:   0x01224B
# '''
'''
numList = []
for i in range(225):
  char = chr(i)
  catV = ucc.category(char)
  if char in ["\\",'"']:
    if char == "\\":
      numList.append('\\x{0:0{1}X}:\n\tname   : "{2}"\n\tvalue  : {0}\n\ttype   : {3}'.format(i,2,"\\\\",catV))
    elif char == '"':
      numList.append("\\x{0:0{1}X}:\n\tname   : '{2}'\n\tvalue  : {0}\n\ttype   : {3}".format(i,2,char,catV))
  elif catV != "Cc":
    numList.append('\\x{0:0{1}X}:\n\tname   : "{2}"\n\tvalue  : {0}\n\ttype   : {3}'.format(i,2,char,catV))
  else:
    numList.append('\\x{0:0{1}X}:\n\tname   : "{2}"\n\tvalue  : {0}\n\ttype   : {3}'.format(i,2,"\u2729Special Character",catV))

filePath = "/Users/zach_lucius/Desktop/tww/res/Msg/hold/rock_24_20_4i_usa.bfn"
contents = b""
with open(filePath, "rb") as f:
  contents = f.read()
start = int("0x01208C",16)
end   = int("0x01224B",16)+1
kewd  = contents[start:end]

actn  = False
final = ""
titl  = ""
u     = 0
k     = 0
totl  = 0

for byte in kewd:
  if not actn:
    actn = True
    k = byte
    titl = "{}\n\tkerning: {}".format(numList[u],k)
    u+= 1
  else:
    actn = False
    titl = "{}\n\twidth  : {}".format(titl,byte)
    totl += byte+k
    titl = "{}\n\ttotal  : {}\n".format(titl,byte+k)
    final+=titl
titl = "total:\n\ttotal  : {}\n\taverage: {}\n".format(totl,totl//224)
final+=titl
final = "  ".join(final.split("\t"))
final.encode(encoding='UTF-8',errors='replace')
print(final)
with open(os.path.join(DATA_PATH,"kerning.txt"),"w") as g:
  g.write(final)
'''
