#!/usr/local/bin/python3.9
#Created by : Shubham Passi
#Date : 07-07-22

import config
import controller
import multiprocessing

#It will let keep an eye on all the directories at same time
if __name__ == "__main__" :
	for path in config.config_dict["all_path"]:
		multiprocessing.Process(target = controller.monitor_folder, args = (path,)).start()
