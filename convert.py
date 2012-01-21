#!/usr/bin/python

from lxml import etree

collection = etree.parse(open("Collection.xml", "r"))

def binary(text):
	if text == 'true':
		return True
	if text == 'false':
		return False

	return None

def handleMediaType(mediaTypes):
	if binary(mediaTypes.find("BluRay").text) is True:
		return "bluray"
	if binary(mediaTypes.find("HDDVD").text) is True:
		return "hddvd"
	if binary(mediaTypes.find("DVD").text) is True:
		return "dvd"
		
def handleBoxSet(boxSet):
	parent = False
	boxset = True
	if boxSet.find("Parent").text is None:
		parent = False

	if len(boxSet.find("Contents")) == 0:
		boxset = False
	
	return boxset	


def handleEntry(entry):
#	for title in entry.iter("Title"):
#		print title.text.encode('ascii', 'ignore')
	
	entryTitle = entry.find("OriginalTitle").text
	if entryTitle is None:
		entryTitle = entry.find("Title").text

	entryTitle.lstrip().rstrip()
	media = handleMediaType(entry.find("MediaTypes"))
	boxset = handleBoxSet(entry.find("BoxSet"))
#	if boxset is True:
#		print "*** Skipping boxset *** "
#		return 
	countAs = entry.find("CountAs").text
	
	titles = []
	if int(countAs) < 1:
		print "*** Skipping not counted: " + entryTitle.encode('utf-8')
		return

	if int(countAs) > 1:
		print "************"
		print "*** More than one title: " + entryTitle.encode('utf-8')
		titles = entryTitle.split('/')
	else:
		titles.append(entryTitle)

	
	for entryTitle in titles:
		entryTitle = entryTitle.rstrip().lstrip()
		filename = entryTitle.encode('utf-8') + " ("+entry.find("ProductionYear").text+")."+media+".disc"
		print filename
		filename = filename.replace('/', ' ')
		filename = filename.replace(':', ' ')
		filename = filename.replace('\\', ' ')
		filename = filename.replace('?', ' ')
		filename = filename.replace('!', ' ')

		fp = open("output/"+filename, "w")
		fp.close()
	
def handleCollection(collection):
#	for entry in collection.iter("DVD"):
#		handleEntry(entry)
	entries = collection.findall("DVD")
	for entry in entries:
		handleEntry(entry)

handleCollection(collection)

