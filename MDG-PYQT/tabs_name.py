test_dict={'number': ['cost'], 'date': ['None'], 'date_level': ['None'], 'character': ['store'], 'aggregate': ['Sum']}

tab_value=''
i=0
for key,value in test_dict.items():
	# print(key,value)
	for tab_name in value:
		if(i==0):
			tab_value=tab_name
			i=1
		else:
			tab_value=tab_value+"-"+tab_name

print("dataset name "+tab_value)