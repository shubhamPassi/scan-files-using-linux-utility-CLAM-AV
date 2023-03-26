config_dict = {
	#Array with all paths we want to monitor
	"all_path" : ['/home/ShubhamPassi/virus1', '/home/ShubhamPassi/virus2', '/home/ShubhamPassi/virus3'],

	#Telegram api parameters
	"telegram" : {
		"token" : "11104852249:AAEMMGxjZuD-TJWDAnGspM9C6Ku4HeEomsw",
		"req_headers" : {
			"Accept" : "application/json",
			"Content-Type" : "application/json"
		},
		"json_data" : {
			"text": "",
			"parse_mode": "HTML",
			"chat_id": -1001383454697
		}
	},

	#logging path
	"log_path" : "/home/ShubhamPassi//log",

	#quarantine folder path
	"quarantine_folder_path": "~/quarantine_folder/"
}
