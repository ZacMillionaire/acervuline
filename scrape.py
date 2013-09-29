#____________#
# Acervuline v0.a bunch of numbers to prevent the version from being 1
# - Everything is terrible edition
#
# A horrible/excellent way to send thousands of requests in a quest for data
#
# All this fantasticly horrible code was made by Scott Schultz of Brisbane. What it does is incredibly specific so unless you have a lot of time on your hands
# and want a bunch of numbers and words with no real point I'd recommend you run this script and go to the pub or something.
#
# Its what I did.

import urllib, urllib2, re

discipline_list = []
unit_list = []
def get_page_source(url):
	#'http://www.qut.edu.au/study/unit-search'

	#Send some headers so a sysadmin can have fun wondering where 10000 requests were coming from
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	values = {
		'name' : 'Scotch and Schultz',
		'location' : 'Brisbane',
		'language' : 'Python',
		'program' : 'Acervuline :: Palladian',
		'desc' : 'A data mining program. Collects Unit information including educational calendar dates, disciplines, unit codes and related information.',
		'contact' : 'Any queries please contact Schultz at dev@jotunga.com'
	}
	headers = {'User-Agent' : user_agent}

	data = urllib.urlencode(values)
	req = urllib2.Request(url, data, headers)

	downloaded_data  = urllib2.urlopen(req)

	downloaded_data = downloaded_data.readlines()

	return downloaded_data

def get_calendar_page_links(data_list):
	data_buffer = ''
	for line in data_list:
		data_buffer = data_buffer+line

	regex = re.compile("<select.*?name=\"cal\">(.*?)</select>",re.I|re.M|re.S)
	regex_results = regex.search(data_buffer)

	select_options = re.compile("<option value=\"(.*?)\">(.*?)</option>",re.I|re.M|re.S)
	select_options_result = select_options.findall(str(regex_results.groups(0)))

	calendar_list = []

	for option_item in select_options_result:
		if option_item[0] != 'WONoSelectionString': #WONoSelectionString is what the uni system uses for ---any--- in select boxes, its still valid, but its useless
			calendar_list.append([option_item[0],option_item[1],"http://www.qut.edu.au/study/unit-search/?cal="+option_item[0]])

	return calendar_list

def build_discipline_list(calendar_link):
	page_source = get_page_source(calendar_link[2])

	data_buffer = ''
	for line in page_source:
		data_buffer = data_buffer+line

	regex = re.compile("<select.*?name=\"discipline\">(.*?)</select>",re.I|re.M|re.S)
	regex_results = regex.search(data_buffer)

	select_options = re.compile("<option value=\"(.*?)\">(.*?)</option>",re.I|re.M|re.S)
	select_options_result = select_options.findall(str(regex_results.groups(0)))

	for option_item in select_options_result:
		if option_item[0] != 'WONoSelectionString': #WONoSelectionString is what the uni system uses for ---any--- in select boxes, its still valid, but its useless
			discipline_list.append([option_item[0],option_item[1],"http://www.qut.edu.au/study/unit-search/?discipline="+option_item[0]])

def build_unit_lists(data_list):
	page_source = get_page_source(data_list[2])

	data_buffer = ''
	for line in page_source:
		data_buffer = data_buffer+line
	# To keep in mind, this is just a global unit-search, this does not account for student.qut.edu.au/studying/units/.*?
	# I am currently unsure of any differences

	# escape dots and questionmarks because I use dot matches all, and the question mark is a regex thing
	regex = re.compile("<td valign = \"TOP\">.*?<a href=\"http://www\.qut\.edu\.au/study/unit-search/unit\?unitCode=(.*?)&amp;idunit=(.*?)\">(.*?)</a></td>",re.I|re.M|re.S)
	regex_results = regex.findall(data_buffer)

	for unit_item in regex_results:
		unit_list.append([unit_item[1],unit_item[0],"http://www.qut.edu.au/study/unit-search/unit?idunit="+unit_item[1]])

def scrape_unit_info(unit_list):
	page_source = get_page_source(unit_list[2])

	data_buffer = ''
	for line in page_source:
		data_buffer = data_buffer+line

	unit_info_list = []

	unit_info_list.append(unit_list)

	course_offer_regex = re.compile("<th>Courses unit offered in:</th>.*?<td>(.*?)</td>",re.I|re.M|re.S)
	unit_info_list.append(course_offer_regex.findall(data_buffer))

	prereq_regex = re.compile("<th>Prerequisite\(s\):</th>.*?<td>(.*?)</td>",re.I|re.M|re.S)
	unit_info_list.append(prereq_regex.findall(data_buffer))
	
	antireq_regex = re.compile("<th>Antirequisite\(s\):</th>.*?<td>(.*?)</td>",re.I|re.M|re.S)
	unit_info_list.append(antireq_regex.findall(data_buffer))
	
	equiv_regex = re.compile("<th>Equivalent\(s\):</th>.*?<td>(.*?)</td>",re.I|re.M|re.S)
	unit_info_list.append(equiv_regex.findall(data_buffer))

	other_req_regex = re.compile("<th>Other requisite\(s\):.*?</th>.*?<td>(.*?)</td>",re.I|re.M|re.S)
	unit_info_list.append(other_req_regex.findall(data_buffer))
	
	credit_regex = re.compile("<th>Credit points:</th>.*?<td>(.*?)</td>",re.I|re.M|re.S)
	unit_info_list.append(credit_regex.findall(data_buffer))
	
	campus_regex = re.compile("<th>Campus:</th>.*?<td>(.*?)</td>",re.I|re.M|re.S)
	unit_info_list.append(campus_regex.findall(data_buffer))
	
	study_period_regex = re.compile("<th>Teaching period:</th>.*?<td>(.*?)</td>",re.I|re.M|re.S)
	unit_info_list.append(study_period_regex.findall(data_buffer))

	csp_regex = re.compile("<th>CSP student contribution.*?</th>.*?<td>(.*?)</td>",re.I|re.M|re.S)
	unit_info_list.append(csp_regex.findall(data_buffer))

	domestic_fee_regex = re.compile("<th>Domestic tuition unit fee.*?</th>.*?<td>(.*?)</td>",re.I|re.M|re.S)
	unit_info_list.append(domestic_fee_regex.findall(data_buffer))

	international_fee_regex = re.compile("<th>International unit fee.*?</th>.*?<td>(.*?)</td>",re.I|re.M|re.S)
	unit_info_list.append(international_fee_regex.findall(data_buffer))
	
	synopsis_regex = re.compile("<H3>Synopsis:</H3>.*?<p>(.*?)</p>",re.I|re.M|re.S)
	unit_info_list.append(synopsis_regex.findall(data_buffer))

	# This will probably work better idk why I didn't think of this the first time around.
	# All of that up there is still a mess though.
	for key,info_entry in enumerate(unit_info_list):
		try:
			info_entry[0]
		except IndexError:
			unit_info_list[key] = 0
		else:
			pattern = re.compile(r'&nbsp;|&amp;+')
			sentence = re.sub(pattern, '', info_entry[0])
			unit_info_list[key] = sentence.strip()
	return unit_info_list

def dump_to_file(lists,names):

	data_buffer = ''
	i = 0
	for list_object in lists:
		data_buffer += "-----%s-----\n"%(names[i])
		for list_item in list_object:
			data_buffer = data_buffer+"\t%s\n"%(str(list_item))
		i += 1
	#print data_buffer
	output_file = open('dumped_data.ohgodwhy','w')
	output_file.write(data_buffer)
	output_file.close()

# HEY GUESS WHAT WOULD'VE PROBABLY SAVED A 6 HOUR EXECUTION? UNIT TESTING!
# I'm still not going to put them in proper though. Of course.

# Test 1
# expects:
#['46436', 0, 0, 0, 0, 'An application, interview and subsequent approval by the Unit Coordinator is required to enrol in this unit. In addition to completion of the following units: AYN417  AYN418.', '12', 'Gardens Point', '2013 SEM-1 and 2013 SEM-2', '$1,224', '$2,544', '$3,072', 'This unit fosters learning through work related experience. Students will be given the opportunity to experience the work that is performed by accountants which will enable them to more effectively learn and practice accounting discipline knowledge and graduate capabilities. Admission to this unit is by application and subsequent approval by the unit coordinator. <br><br>For additional important information about this unit please refer to the current unit outline.']
# unit_info = scrape_unit_info(['46436', 'AYN460', 'http://www.qut.edu.au/study/unit-search/unit?idunit=46436'])
# print unit_info
# exit()


# Test 2
# expects:
#['43713', 'BS92, IF49', 0, 0, 'GSN234', 0, '12', 'Gardens Point', '2013 SEM-1', '$1,224', '$2,544', '$3,072', 'The unit introduces the students to the field of entrepreneurship research and the problems, theories and methods that are prevalent in (empirical) research on entrepreneurship. Students learn to "know the field" including its historical development; its "infrastructure" of journals, conferences and research centres, and its contemporary research questions and approaches. The students will develop an ability to assess the strengths and weaknesses of the field and gain insights into where and how they can contribute to its research frontier.']
# unit_info = scrape_unit_info(['43713', 'MGN534', 'http://www.qut.edu.au/study/unit-search/unit?idunit=43713'])
# print unit_info
# exit()


# Test 3
# expects:
#['45637', 0, 'BSB111 or CTB111', 'LWB364', 'AYB325, AYX219', 0, '12', 'Gardens Point', '2013 SEM-1 and 2013 SEM-2', '$1,224', '$2,136', '$2,868', "This unit introduces students to the statutory framework of the Australian taxation system. Elements in the determination of taxable income and the levy of income tax are examined including general and specific categories of assessable income and allowable deductions, capital gains tax and administration aspects of the tax system. The taxation of fringe benefits is also examined. The unit also provides  a brief overview of the taxation of partnerships, trusts and companies and an overview of the goods and services tax. Emphasis is placed on developing students' skills in problem solving through research and analysis of taxation issues."]
# unit_info = scrape_unit_info(['45637', 'AYB219', 'http://www.qut.edu.au/study/unit-search/unit?unitCode=AYB219&idunit=45637'])
# print unit_info
# exit()


# And all this shit below is a horrible mess I just wanted it to work for now

data_list = get_page_source('http://www.qut.edu.au/study/unit-search')
calendars = get_calendar_page_links(data_list)

print "Got %d calendars"%(len(calendars))
print "Buidling discipline lists based on calendars...\n"
for calendar_link in calendars:
	print "\tGetting discipline list for %s..."%(calendar_link[1])
	old_discipline_list_length = len(discipline_list)
	build_discipline_list(calendar_link)
	print "\t...Collection complete. Got %d disciplines\n"%(len(discipline_list)-old_discipline_list_length)

print "Found and collected a total of %d disciplines across %d calendars."%(len(discipline_list),len(calendars))
print "Performing deduplication..."
old_discipline_list_length = len(discipline_list)
discipline_list = sorted(set(map(tuple, discipline_list)))
discipline_list = map(list,discipline_list)
print "...Finished. Removed %d duplicates.\n"%(old_discipline_list_length-len(discipline_list))

print "Now for the fun part. Building Unit lists...\n"
for discipline in discipline_list:
	print "\tCollection for %s..."%(discipline[1])
	old_unit_list_length = len(unit_list)
	build_unit_lists(discipline)
	print "\t...Collection complete. Found %d units.\n"%(len(unit_list)-old_unit_list_length)

print "Unit list complete. Collected a total of %d units."%(len(unit_list))
print "Performing deduplication..."
unit_list_size = len(unit_list)
unit_list = sorted(set(map(tuple, unit_list)))
unit_list = map(list, unit_list)
print "\t...Finished. %d duplicates removed.\n"%(unit_list_size-len(unit_list))

print "Dumping data..."
dump_to_file([calendars,discipline_list,unit_list],['Calendars','Disciplines','Units'])
print "...Finished.\n"

print "I hope you have a lot of time on your hands cause this'll take a few years."
for i,unit in enumerate(unit_list):
	print "\tScraping data for unit code %s (item %d of %d (%f%%))"%(unit[1],(i+1),len(unit_list),(float(i+1)/len(unit_list))*100) # Guess what should've ACTUALLY been a float?
	scraped_data = scrape_unit_info(unit)
	print "\tData Collected. Adding %s..."%(unit[1])
	with open('scraped_data.ohgodwhy','a') as dump_file:
		dump_file.write("\t%sEOL\n"%(str(scraped_data)))
	print "\tData dumped.\n"

print "At long last my suffering is at an end."
exit()