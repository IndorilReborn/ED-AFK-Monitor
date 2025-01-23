import os
import time
import json
from pathlib import Path
import argparse

# Arguments
parser = argparse.ArgumentParser(
    prog='AFK Monitor',
    description='Live event monitoring for Elite Dangerous AFK sessions')
parser.add_argument('-j', '--journal_folder', help='override default journal location')
args = parser.parse_args()

# Set journal folder
if not args.journal_folder:
	home_dir = str(Path.home())
	journal_dir = home_dir+'\\Saved Games\\Frontier Developments\\Elite Dangerous'
else:
	journal_dir = args.journal_folder

# Get latest journal file
files = []
fileslist = os.scandir(journal_dir)
for entry in fileslist:
	if entry.is_file():
		if entry.name[:7] == 'Journal':
			files.append(entry.name)
fileslist.close()
journal_file = files[len(files)-1]

print('ED AFK Monitor v250123 by CMDR PSIPAB')
print('Journal folder:',journal_dir)
print('Latest journal:', journal_file)
print('Monitoring... (Press Ctrl+C to stop)')

# Process incoming journal entries
def processline(line):
	ship = ''
	this_json = json.loads(line)
	if this_json['event'] == 'ShipTargeted':
		if 'Ship' in this_json:
			if 'Ship_Localised' in this_json:
				ship = this_json['Ship_Localised']
			else:
				ship = this_json['Ship'].title()
			print(this_json['timestamp'].replace('T',' ').replace('Z', ' | ')+ship)

# Open journal from end and watch for new lines
with open(journal_dir+'\\'+journal_file, 'r') as file:
	file.seek(0, 2)

	while True:
		line = file.readline()
		if not line:
			time.sleep(1)
			continue
		
		processline(line)
