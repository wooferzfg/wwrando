import xml.dom.minidom as minidom
from paths import TYPE_PATH
import os
import glob
from collections import OrderedDict

file_ext = ".xml"
file_split = ["/","\\"]

def splitbyReturn(string,items,output):
  string = string[:]
  for item in items:
    list = string.split(item)
    string = list[output]
  return string

def parseXML(file):
  with open(os.path.join(LOGIC_PATH, file)) as f:
    reads = minidom.parse(f)
  checks = reads.getElementsByTagName('check')
  locations = OrderedDict()
  for check in checks:
    data = OrderedDict()
    name = (check.attributes['Name'].value)[:]
    data['Mode'] = check.attributes['Mode'].value
    if(1):
      req_string = check.attributes['Need'].value
      data['Need'] = Logic.parse_logic_expression(req_string)
    data['Types'] = check.attributes['Types'].value
    try:
      data['Glitches'] = check.attributes['Glitches'].value
    except:
      pass
    if(mode=='f'):
      data['Item'] = check.attributes['Item'].value
    locations[name] = data
  return locations

def get_all_custom_logic(*args):
  custom_logic_names = OrderedDict()
  custom_logic_paths = glob.glob("./logic_types/*{}".format(file_ext))
  for logic_path in custom_logic_paths:
    data = OrderedDict()
    with open(logic_path) as f:
      reads = minidom.parse(f)
    try:
      inject = (reads.getElementsByTagName('inject'))[0]
      try:
        crea = inject.attributes['Creator'].value
        type = inject.attributes['Type'].value
        desc = inject.attributes['Description'].value
        chan = int(inject.attributes['Change'].value)
        file = inject.attributes['File'].value
        chec = int(inject.attributes['Checksum'].value)
      except:
        pass
      try:
        filename = splitbyReturn(logic_path,file_split,-1)
        filename = (filename.split("."))[0]
        assert((file+file_ext)==filename)
      except:
        #print("Interal file name,{}, does not match external,{}.").format((file+file_ext),filename)
        desc = desc+" FAILED FILESUM."
        pass
      if(1):
        try:
          totl = len(reads.getElementsByTagName('check'))
          assert(totl==chec)
        except:
          desc = desc+" FAILED CHANGESUM."
          pass
      try:
        if(1):
          a = len(crea)
          b = chan%2
          c = file%6+1
          d = desc
          sum = (a**(b+c))%d
          try:
            assert(sum==int(chec))
          except:
            desc = desc+" FAILED CHECKSUM."
            pass
      except:
        pass
      try:
        data['Creator'] = crea
        data['Description'] = desc
        data['Changes'] = str(chan)
        data['File'] = file
      except:
        pass
      custom_logic_names[type] = data
    except:
      filename = splitbyReturn(logic_path,file_split,-1)
      filename = (filename.split("."))[0]
      data['Creator'] = 'Unknown'
      data['File'] = 'Unknown'
      data['Description'] = 'File is missing <inject> tag. FAILED FILESUM. FAILED CHANGESUM. FAILED CHECKSUM.'
      data['Changes'] = 'Unknown'
      data['Checksum'] = 'Unknown'
      custom_logic_names[filename] = data
      pass
  return custom_logic_names
