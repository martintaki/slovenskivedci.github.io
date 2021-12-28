import yaml
import os

import glob
countries={}
institutions={}
alllst=[]

stats={
    "countries" : {},
    'man':0,
    'woman':0,
    'hindex':[],
    'affiliation': {}
      }


#os.system("rm country_*")
#os.system("rm affiliation_*")
os.system("rm _data/*yaml")


import unicodedata

def repl(text):
	return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('UTF-8').replace(",","_").replace("(","_").replace(")","_")

for y in glob.glob("./people/*.yaml"):
	with open(y) as f:
		dic = yaml.safe_load(f)

		if int(dic['hindex']) < 30:
			continue

		if dic['country'] not in countries:
			countries[dic['country']] = []

		if dic['affiliation'] not in institutions:
			institutions[dic['affiliation']] = []

		dic["countryurl"]=repl(dic["country"].replace(" ","_"))
		dic["fieldurl"]=repl(dic["field"].replace(" ","_"))
		dic["positionurl"]=repl(dic["position"].replace(" ","_"))
		dic["affiliationurl"]=repl(dic["affiliation"].replace(" ","_"))
		dic["cityurl"]=repl(dic["city"].replace(" ","_"))
		dic["sexurl"]=repl(dic["sex"].replace(" ","_"))

		dic["last"]=repl(dic["last"])
		
		links=dic['links']
		links=[ [k, links[k]] for k in links]

		links = sorted(links, key=lambda kv: kv[0].lower())

		dic['links'] = links

		try:
			  if len(dic["sex"] )==3:
				  stats["man"]+=1
			  else:
				  stats["woman"]+=1
		except:
			print("Error in SEX in ",y,"SEX = ",dic["sex"],"LENGTH = ", len(dic["sex"]))


		institutions[dic['affiliation']].append(dic)

		if dic["country"] not in stats["countries"]:
			stats["countries"][dic["country"]] = 0
		if dic["affiliation"] not in stats["affiliation"]:
			stats["affiliation"][dic["affiliation"]] = 0
		stats["countries"][dic["country"]] += 1
		stats["affiliation"][dic["affiliation"]] += 1
		stats["hindex"].append(int(dic['hindex']))

		countries[dic['country']].append(dic)
		alllst.append(dic)





alllst = sorted(alllst,key= lambda e: (-int(e['hindex']), e['last'] ))
with open(r'_data/all.yaml', 'w') as file:
	documents = yaml.dump(alllst, file)









with open(r'_data/page.yaml', 'w') as file:
	documents = yaml.dump(stats, file)






'''
for k in countries:
	countries[k] = sorted(countries[k],key= lambda e: -int(e['hindex']))
	countrycode = repl(k.replace(" ","_"))
	with open(r'_data/country_%s.yaml'%countrycode, 'w') as file:
			documents = yaml.dump(countries[k], file)

	os.system("sed 's/DATAFILE/country_%s/g' template.style > country_%s.html"%(countrycode,countrycode))




for k in institutions:
	institutions[k] = sorted(institutions[k],key= lambda e: -int(e['hindex']))
	affcode = repl(k.replace(" ","_"))
	print(affcode)

	with open(r'_data/institution_%s.yaml'%affcode, 'w') as file:
			documents = yaml.dump(institutions[k], file)
	os.system("sed 's/DATAFILE/institution_%s/g' template.style > affiliation_%s.html"%(affcode,affcode))

os.system("sed 's/DATAFILE/all/g' template.style > index.html")
'''
