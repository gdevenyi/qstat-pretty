
from collections import OrderedDict, defaultdict
from datetime import datetime
import xml.etree.ElementTree as ET

def parse_xml(f):
	xml = ET.parse(f)
	root = xml.getroot()

	parse_time = lambda t: datetime.strptime(t,  '%Y-%m-%dT%H:%M:%S')

	def process_job(j):
		fields = {
			 'number': ('JB_job_number', int)
			,'priority': ('JAT_prio', float)
			,'name': ('JB_name', str)
			,'owner': ('JB_owner', str)
			,'state': ('state', str)
			,'t_submit': ('JB_submission_time', parse_time)
			,'t_start': ('JAT_start_time', parse_time)
			,'queue': ('queue_name', str)
			,'slots': ('slots', int)
			,'tasks': ('JB_ja_tasks', int)
		}

		def tagtext(t, f):
			if t != None: 
				return f(t.text)
			else: 
				return None

		return { key: tagtext(j.find(tag[0]), tag[1]) for key,tag in fields.items() }

	jobs = [ process_job(job_list) for job_list in  root.find('queue_info') ]

	return jobs