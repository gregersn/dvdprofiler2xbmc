#!/usr/bin/python
'''
Parses exported database from DVD Profiler in XML format,
and creates fake files for XBMC.

http://wiki.xbmc.org/index.php?title=HOW-TO:Catalog_and_use_lookups_on_your_offline_DVD/CD_movie_library_%28via_fake_files%29
http://invelos.com/

By default uses the file Collection.xml in current directory.
Writes files into folder named output under current directory

Discs/titles/entries set with "count as" to 0 in DVD Profiler will be ignored.
Entries that has a count higher than 1 will be treated as multipled entris,
and script will try to split the title with / as token, making one fake
file per result in a / split.


'''

from lxml import etree

#TODO Get file name from command line
collection = etree.parse(open("Collection.xml", "r"))

# Does a string to binary conversion
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
	# Try using Original Title first, if set.
	entryTitle = entry.find("OriginalTitle").text
	if entryTitle is None:
		entryTitle = entry.find("Title").text

	media = handleMediaType(entry.find("MediaTypes"))
	boxset = handleBoxSet(entry.find("BoxSet"))
	countAs = entry.find("CountAs").text
	
	titles = []
	if int(countAs) < 1:
		print "*** Skipping not counted: " + entryTitle.encode('utf-8')
		return

	if int(countAs) > 1:
		print "*** More than one title: " + entryTitle.encode('utf-8')
		titles = entryTitle.split('/')
	else:
		titles.append(entryTitle)

	
	for entryTitle in titles:
		entryTitle = entryTitle.rstrip().lstrip()
		filename = entryTitle.encode('utf-8') + " ("+entry.find("ProductionYear").text+")."+media+".disc"
		# Remove some unwanted characters for use as filename
		filename = filename.replace('/', ' ')
		filename = filename.replace(':', ' ')
		filename = filename.replace('\\', ' ')
		filename = filename.replace('?', ' ')
		filename = filename.replace('!', ' ')
		print filename

		fp = open("output/"+filename, "w")
		fp.close()
	
def handleCollection(collection):
	entries = collection.findall("DVD")
	for entry in entries:
		handleEntry(entry)

handleCollection(collection)

