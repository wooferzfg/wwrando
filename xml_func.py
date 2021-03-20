import xml.dom.minidom as minidom
from paths import TYPE_PATH
import os
import glob
from collections import OrderedDict
from class_ms import * # Remember to correct this later, Zach
import re
import yaml
#from logic.logic import Logic

file_ext = [".dv_im",".yaml",".xml"]
file_split = ["/","\\"]
file_path = "./logic_types/"
file_paths = ["./logic_types/",".\\logic_types\\","./logic_types",".\\logic_types"]
extempt_files_var = ["example","standard"]
extempt_files = []
formats_var = ["{0}{2}{1}","{2}{1}","{0}\\{2}{1}","\\{2}{1}","{0}/{2}{1}","/{2}{1}"]
for file in extempt_files_var:
  for format in formats_var:
    for path in file_paths:
      for ext in file_ext:
        extemption = (format.format(path,ext,file))
        extempt_files.append(extemption)



def splitbyReturn(string,items,output):
  string = string[:]
  for item in items:
    list = string.split(item)
    string = list[output]
  return string

def reParse(string):
  list = string.split(' AND ')
  reString = ' & '.join(list)
  list = reString.split(' OR ')
  reString = ' | '.join(list)
  list = reString.split(" '")
  reString = ' "'.join(list)
  list = reString.split("' ")
  string = '" '.join(list)
  if(string[-1]=="'"):
    string = string[0:len(string)-1]+'"'
  return string


def parseXML(file):
  with open(os.path.join(TYPE_PATH, file)) as f:
    reads = minidom.parse(f)
  checks = reads.getElementsByTagName('check')
  locations = OrderedDict()
  for check in checks:
    data = OrderedDict()
    name = (check.attributes['Name'].value)[:]
    mode =  check.attributes['Mode'].value
    data['Mode'] = mode
    if(1):
      req_string = check.attributes['Need'].value
      #data['Need'] = Logic.parse_logic_expression(req_string)
      data['Need'] = reParse(req_string)
    data['Types'] = (check.attributes['Types'].value).split(',')
    try:
      data['Glitches'] = check.attributes['Glitches'].value
    except:
      pass
    if(mode=='f'):
      data['Item'] = check.attributes['Item'].value
    locations[name] = data
  return locations

def parseYAML(file):
  with open(logic_path) as f:
    reads = yaml.load(f, YamlOrderedDictLoader)
  try:
    del reads["Injection"]
    del reads["Change UI"]
  except:
    pass
  return reads

def parseFile(file):
  if(logic_path[-4:]==".dv_im"[-4:] or logic_path[-4:]==".xml"[-4:]):
    parseXML(file)
  elif(logic_path[-4:]==".yaml"[-4:]):
    parseYAML(file)
  else:
    print("\n\n\n\nHow?\n\n\n\n")


def getXML(logic_path):
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
      #filename = (filename.split("."))[0]
      assert(file==filename)
    except:
      #print("Interal file name,{}, does not match external,{}.").format((file+file_ext),filename)
      desc = desc+" FAILED FILESUM."
      file = filename
      pass
    if(1):
      try:
        totl = len(reads.getElementsByTagName('check'))
        assert(totl==chan)
      except:
        desc = desc+" FAILED CHANGESUM."
        chan = totl
        pass
    try:
      if(1):
        a = len(crea)
        b = chan%2
        c = len(file)%6+1
        d = len(desc)
        sum = (a**(b+c))%d
        try:
          assert(sum==int(chec))
        except:
          desc = desc+" FAILED CHECKSUM."
          chec = sum
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
  except:
    filename = splitbyReturn(logic_path,file_split,-1)
    data['Creator'] = 'Unknown'
    data['File'] = filename
    data['Description'] = 'File is missing <inject> tag. FAILED FILESUM. FAILED CHANGESUM. FAILED CHECKSUM.'
    data['Changes'] = 'Unknown'
    data['Checksum'] = 'Unknown'
    type = (filename.split("."))[0]
    pass
  try:
    hold = OrderedDict()
    changeUI = (inject.getElementsByTagName('changeUI'))[0]
    try:
      attrUIList = changeUI.attributes
      for i in range(attrUIList.attributes.length):
        attr = attrUIList.attributes.item(i)
        hold[attr.name] = attr.value
    except:
      hold = OrderedDict()
  except:
    pass
  return data, type, hold

def getYAML(logic_path):
  data = OrderedDict()
  with open(logic_path) as f:
    raw_inject = yaml.load(f, YamlOrderedDictLoader)
  try:
    inject = raw_inject["Injection"]
    try:
      crea = inject["Creator"]
      type = inject["Type"]
      desc = inject["Description"]
      chan = int(inject["Change Total"])
      file = inject["File Name"]
      chec = int(inject["Checksum"])
    except:
      pass
    try:
      filename = splitbyReturn(logic_path,file_split,-1)
      #filename = (filename.split("."))[0]
      assert(file==filename)
    except:
      #print("Interal file name,{}, does not match external,{}.").format((file+file_ext),filename)
      desc = desc+" FAILED FILESUM."
      print(filename)
      file = filename
      pass
    if(1):
      try:
        totl = len(raw_inject)-2
        assert(totl==chan)
      except:
        desc = desc+" FAILED CHANGESUM."
        print(totl)
        chan = totl
        pass
    try:
      if(1):
        a = len(crea)
        b = chan%2
        c = len(file)%6+1
        d = len(desc)
        sum = (a**(b+c))%d
        try:
          assert(sum==int(chec))
        except:
          desc = desc+" FAILED CHECKSUM."
          print(sum)
          chec = sum
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
  except:
    filename = splitbyReturn(logic_path,file_split,-1)
    data['Creator'] = 'Unknown'
    data['File'] = filename
    data['Description'] = 'File is missing <inject> tag. FAILED FILESUM. FAILED CHANGESUM. FAILED CHECKSUM.'
    data['Changes'] = 'Unknown'
    data['Checksum'] = 'Unknown'
    type = (filename.split("."))[0]
    pass
  try:
    hold = OrderedDict()
    changeUI = raw_inject["Change UI"]
    try:
      for key in changeUI:
        value = changeUI[key]
        name = key.lower()
        setting = "progression_" + re.sub(" ","_",name)
        hold[setting] = value
    except:
      hold = OrderedDict()
  except:
    pass
  return data, type, hold

def get_all_custom_logic(*args):
  custom_logic_names = OrderedDict()
  custom_logic_paths = []
  for ext in file_ext:
    for file in (glob.glob("{}*{}".format(file_path,ext))):
      custom_logic_paths.append(file)
  for logic_path in custom_logic_paths:
    typeDict = OrderedDict()
    #print(logic_path)
    if(logic_path in extempt_files):
      continue
    if(logic_path[-4:]==".dv_im"[-4:] or logic_path[-4:]==".xml"[-4:]):
      data, type, hold = getXML(logic_path)
      typeDict["Data"] = data
      typeDict["Change UI"] = hold
      custom_logic_names[type] = typeDict
    elif(logic_path[-4:]==".yaml"[-4:]):
      data, type, hold = getYAML(logic_path)
      typeDict["Data"] = data
      typeDict["Change UI"] = hold
      custom_logic_names[type] = typeDict
    else:
      print("\n\n\n\nHow?\n\n\n\n")
  return custom_logic_names
