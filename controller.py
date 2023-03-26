#Import required library
import time
import config
import requests
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#Function that run all linux commands
def runCommand(cmd):
	sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
	rc = sp.wait()
	out,err = sp.communicate()

	if rc == 0 or rc == 1 :
		return '{}'.format(out)
	else:
		return 'error is: {}'.format(err)

#Event handler that will trigger when file will be created
class Handler(FileSystemEventHandler):
	def on_created(self, event):
		#logging currently scanning file path
		cmd = "echo '---------------- scanning {} --------------------' >> {}".format(event.src_path, config.config_dict["log_path"])
		runCommand(cmd)

		#scan recent file using clamav
		cmd = "/usr/bin/clamdscan -i -l {} {}".format(config.config_dict["log_path"], event.src_path)
		output = runCommand(cmd)

		for each_line in output.splitlines():
			if "Infected" in each_line:
				res = int(each_line.split(":")[1])
			elif "error is:" in each_line:
				res = each_line

		#logging the file that contains virus
		if res == 0:
			cmd = "echo 'file is safe' >> {}".format(config.config_dict["log_path"])
			runCommand(cmd)
		elif res == 1:
			temp = config.config_dict["telegram"]["json_data"]
			temp["text"] = "<b>Virus found at location </b> <pre>{}</pre>".format(event.src_path)

			response = requests.post("https://api.telegram.org/bot{}/sendMessage".format(config.config_dict["telegram"]["token"]),
				headers = config.config_dict["telegram"]["req_headers"],
				json = temp
			)
			print(response.status_code)

			#moving suspicious file into quarantine folder
			cmd = "mv {} {}".format(event.src_path, config.config_dict["quarantine_folder_path"])
			output = runCommand(cmd)

			if "mv: cannot" in output:
				cmd = "echo 'Error while sending quarantined file ( {} ) to designated quarantine folder: {}' >> {}".format(event.src_path, output, config.config_dict["log_path"])
				runCommand(cmd)
		else:
			#logging error into log file
			cmd = "echo 'Error: {} ' >> {} ".format(output, config.config_dict["log_path"])
			runCommand(cmd)

#These variable keep eye on target path
event_handler = Handler()
observer = Observer()

#Function to monitor path for infinite period
def monitor_folder(path):
	observer.schedule(event_handler, path, recursive=True)
	observer.start()

	try:
		while True:
			time.sleep(10)
	finally:
                observer.stop()
                observer.join()

