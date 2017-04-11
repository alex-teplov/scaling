
import os
from scaling_experiment import *
import itertools
import numpy

log_directory = '/Users/teplov/Dropbox/НИВЦ/Upsala/Logs from Jonathan dence/'


def dir_extract(dir_path, filter_value):
	fileslist = os.listdir(dir_path)
	datafiles = filter(lambda x: x.endswith(filter_value), fileslist)
	dir_data = []
	for file in datafiles:
		full_file_name = dir_path+file
		# print (file)
		
		dir_data.append(Experiment(full_file_name))
	return dir_data
		


def collect_params(launch_set):
	params_names = set()
	params = {}
	for experiment in launch_set:
		params_names = params_names.union(set(experiment.launch_parameters.keys()))
		for param in experiment.launch_parameters.keys():
			if params.get(param) == None:
				params[param] = set()
			params[param].add(experiment.launch_parameters[param])
			params[param] = set(params[param])

			
	print(params_names)
	return params


data = dir_extract(log_directory, '.log')

print ("\n Total number of parsed logs: {0}".format(len(data)))

# print('\n Comments in the data:')
# for experiment in data:
# 	if experiment.comment =='':
# 		pass
# 	else:
# 		print(experiment.source_log, experiment.comment)


merged_data = []
experiment_set = data[0:]
i=0
print ("Number of logs : {0}".format(len(experiment_set)))
for experiment in experiment_set:
	# print (experiment.source_log)
	if experiment.comment:
		continue

	for merged_experiment in reversed(merged_data):
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
parts_array = {}
data_set =  merged_data[0:]
for data in data_set:
	# print('Parsing merge data:')
	# print ('Parameters: {0}'.format(data.launch_parameters))
	for app_part in data.data_extract:
		
		# print('     {0} : {1}'.format(app_part, numpy.percentile(data.data_extract[app_part],75)))
		if parts_array.get(app_part):
			
			parts_array[app_part].add(data.launch_parameters,numpy.percentile(data.data_extract[app_part],75))

		else: 
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

for part in parts_array:
	output = []
	print(part)

	f = open('{0}_timing.txt'.format(parts_array[part].part_name),'w')
	for timing in parts_array[part].param_timing:
		output.append((timing.params['Procs'], timing.params['Levels'], timing.time))
	output = sorted(output)
	for line in output:


	# print ('            {0} : {1}'.format(timing.params, timing.time))
	
	# print ('{0} {1} {2}'.format(timing.params['Procs'], timing.params['Levels'], timing.time))
		# f.write('{0} {1} {2}\n'.format(timing.params['Procs'], timing.params['Levels'], timing.time))
		f.write('{0} {1} {2}\n'.format(line[0],line[1],line[2]))
	
	f.close()








