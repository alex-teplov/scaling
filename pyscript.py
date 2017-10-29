
import os
from scaling_experiment import *
import itertools
import numpy


# loading the path to the folder with logs of experiments
log_directory = '/Users/teplov/Dropbox/НИВЦ/Upsala/Logs from Jonathan dence/'


def dir_extract(dir_path, filter_value):

	# Extracting all the experiments data from folder with "dir_path" and ending with "filter value"
	# Result is list of the objects of Experiment class
	
	fileslist = os.listdir(dir_path)
	datafiles = filter(lambda x: x.endswith(filter_value), fileslist)
	dir_data = []
	for file in datafiles:
		full_file_name = dir_path+file
		# print (file)
		
		dir_data.append(Experiment(full_file_name))
	return dir_data
		


# extracting the data from the directory, filtering extentions only to *.log
dir_data = dir_extract(log_directory, '.log')

print ("\n Total number of parsed logs: {0}".format(len(dir_data)))

# print('\n Comments in the data:')
# for experiment in data:
# 	if experiment.comment =='':
# 		pass
# 	else:
# 		print(experiment.source_log, experiment.comment)

# initialize the dataset
merged_data = []
experiment_set = dir_data[0:]
# simply counter of iterations
i=0
print ("Number of logs : {0}".format(len(experiment_set)))
for experiment in experiment_set:
	# looping threw the experiments source files logs
	# print (experiment.source_log)
	if experiment.comment:
		#passing the experiments with special situations and errors they have not empty comment field
		continue

	for merged_experiment in reversed(merged_data):
		# trying to add the new experiment to the already passed experiments the merged data in the reversed number of iterations
		# because experiments have similar configurations
		if merged_experiment.merge(experiment):
			i+=1
			continue
		# print('0 Length of merged_data : {0}'.format(len(merged_data)))
		# print('0 Length of current source_log: {0}'.format(len(merged_experiment.source_log)))
		# print('0 Current data_extract : {0}'.format(merged_experiment.data_extract))
		i+=1
		break

	else:
		# print('Else')
		# If experiment with such parameters was not found we create a new branch and adding it to the merged data
		merged = MergedExperiment(experiment)
		i+=1
		# print('1 Creating new entiry')
		# print('1 Length of merged_data : {0}'.format(len(merged_data)))
		# print('1 Length of current source_log: {0}'.format(len(merged.source_log)))
		# print('1 Current data_extract : {0}'.format(merged.data_extract))

		# print(merged.source_log)
		merged_data.append(merged)





print('Number of iterations :{0}'.format(i))

# print('=======Total data========')

# print('merged_data length : {0}'.format(len(merged_data)))
# for data in merged_data:

# 	print('4 Length of current source_log: {0}'.format(len(data.source_log)))
# 	print('4 Params are : {0}'.format(data.launch_parameters))
# 	for log in data.source_log:
# 		print('      {0}'.format(log)) #print('4 Length of current source_log: {0}'.format(data.source_log))
# 	print('4 Current data_extract : {0}'.format(data.data_extract))


# print('\n========Extraction of data==========')
# for data in merged_data:
# 	print ('Parameters: {0}'.format(data.launch_parameters))
# 	for app_part in data.data_extract:
# 		print('     {0} : {1}'.format(app_part, numpy.percentile(data.data_extract[app_part],75)))


# print('=========Parts of the application===========')
# Separating the dataset to the application parts
parts_array = {}
data_set =  merged_data[0:]
for data in data_set:
	# Looping threw the dataset
	# print('Parsing merge data:')
	# print ('Parameters: {0}'.format(data.launch_parameters))
	for app_part in data.data_extract:
		# observing each application part separately
		
		# print('     {0} : {1}'.format(app_part, numpy.percentile(data.data_extract[app_part],75)))
		if parts_array.get(app_part):
			# trying to add to the existing application part
			parts_array[app_part].add(data.launch_parameters,numpy.percentile(data.data_extract[app_part],75))

		else: 
			# creating new application part if not found
			# print(' Creating App part with {0}, {1}, {2}'.format(app_part, data.launch_parameters,numpy.percentile(data.data_extract[app_part],75)))
			# part_entity = Application_part()
			application_part_entity = Application_part(app_part, data.launch_parameters, numpy.percentile(data.data_extract[app_part],75))
			# print(' Entity name : {0}'.format(application_part_entity.part_name))
			parts_array[application_part_entity.part_name] = application_part_entity


print ('Found parts: {0}'.format(len(parts_array)))
# for part in parts_array:
# 	print ('   {0}'.format(part))
# 	print ('       {0}'.format(parts_array[part].part_name))
# 	for timing in parts_array[part].param_timing:
# 		print ('            {0} : {1}'.format(timing.params, timing.time))



print(parts_array['Alloc'].part_name)


# Outputing the data into the files each for application part
for part in parts_array:
	output = []
	print(part)
	parts_array[part].print_in_file('log2',part)
	parts_array[part].generate_gnuplot_script(part)












