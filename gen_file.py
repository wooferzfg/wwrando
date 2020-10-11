import yaml
import os
from paths import LOGIC_PATH, TYPE_PATH, TRICK_PATH
from collections import OrderedDict

forbidden_keys = ["Paths","Original item"]
source_file = "logic_locations.txt"
file_details = ["LagoLunatic","Standard","The regular TWW Logic","standard.dv_im",]
format_title = '<inject Creator="{}" Type="{}" Description="{}" Change="{}" File="{}" Chechsum="{}">\n'


class YamlOrderedDictLoader(yaml.SafeLoader):
  pass

YamlOrderedDictLoader.add_constructor(
  yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
  lambda loader, node: OrderedDict(loader.construct_pairs(node))
)

with open(os.path.join(LOGIC_PATH, source_file)) as f:
  item_locations = yaml.load(f, YamlOrderedDictLoader)

final_locations = ''
change=0
for location in item_locations:
  location_data = [location]
  change+=1
  for key, value in item_locations[location].items():
    if(key in forbidden_keys):
      continue
    location_data.append(value)
  for i in range(0,2):
    splitStr = location_data[i].split('"')
    result = "'".join(splitStr)
    location_data[i] = result
    splitStr = location_data[i].split('&')
    result = "AND".join(splitStr)
    location_data[i] = result
    splitStr = location_data[i].split('|')
    result = "OR".join(splitStr)
    location_data[i] = result
  final_locations+='  <check Name="{}" Mode="o" Need="{}" Types="{}"/>\n'.format(location_data[0],location_data[1],location_data[2])
checksum = (((len(file_details[0]))**((change%2)*((len(file_details[2]))%6+1)))%(len(file_details[1])))
format_title = format_title.format(file_details[0],file_details[1],file_details[2],change,file_details[3],checksum)
doc_cont = format_title+final_locations+"</inject>"
print(doc_cont)
doc_cont.encode(encoding='UTF-8',errors='strict')

try:
  with open(os.path.join(TYPE_PATH, file_details[3]),'x') as g:
    g.write(doc_cont)
except:
  with open(os.path.join(TYPE_PATH, file_details[3]),'w') as g:
    g.write(doc_cont)
