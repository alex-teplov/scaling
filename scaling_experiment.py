
import os

class Experiment:
	# source_log = ''
	# launch_parameters = {}
	# launch_data = {}
	# data_extract = {}
	# comment = ''

	def __init__(self, log_path):
		self.source_log = log_path
		self.launch_parameters = self.extract_params(log_path)
		self.comment = ''
		if self.check_file(log_path):
			# print("Not a log file")
			self.comment = 'Error in datafile import. Required rerun on the params {0}'.format(self.launch_parameters)
		else:
			self.launch_data = self.readlog(log_path)
			self.data_extract = self.log_max_time(log_path)
			# print ("Experiment {0} inited".format(self.source_log))
	
	def print(self,mode=''):
		print('*  Log path:\n*      {0}'.format(self.source_log))
		print('*  Launch parameters of the experiment: ')
		for parameter in self.launch_parameters:
			print('*      {0} : {1}'.format(parameter,self.launch_parameters[parameter]))
		if self.comment:
			print('*  Comment: {0}'.format(self.comment))
		print('*  Max time between processes in log:')
		for key in self.data_extract:
			print('*     {0} : {1}'.format(key,self.data_extract[key]))
		if mode:
			print('* Full data of logfile:')
			for key in self.launch_data:
				print ('*      {0} : '.format(key))
				for proc in self.launch_data[key]:
					print('*        {0} : {1}'.format(proc,self.launch_data[key][proc]))



	def check_file(self, logfile):
		# TODO:
		# move to the regexp in the check and try to formalize the checking of the file correctness.
		# print('Check method')
		filedata = open(logfile,'r')
		if (filedata.read(32))=='--------------------------------':
			# print("Error file")
			filedata.close()
			return 1
		else:
			filedata.close()
			return 0

	def extract_params(self, logfile):
		#TODO:
		#implement abstract parameters set for this method
		# print('Extract method')
		linewords = logfile.split('/')
		params = linewords[-1].split('_')
		# print (params)
		params_data = {}
		params_data['Procs'] = int(params[1][1:])
		params_data['Problem_size'] = int(params[2][:-1])*1000
		params_data['Levels'] = int(params[3][1:])
		params_data['Tolerance'] = int(params[4][1:])
		return params_data

	def readlog(self, logfile):
		# print('Readlog method')
		filedata = open(logfile,"r")
		# print (filedata.readlines())
		log_data = {}
		for line in filedata.readlines():
			# print (line)
			if line == "" or line =='\n' or line.find(":") ==-1:
				# print ("Line Skiped")
				continue
			# print ('Line is : " {0} "'.format(line))
			rank_number = int(line.split(":")[0].split(' ')[1][:-1])
			# print('Rank is " {0} "'.format(rank_number))
			step_number = line.split(":")[0].split(' ')[-1]
			# print ('Step is: " {0} "'.format(step_number))
			step_time = float(line.split(":")[1])
			# print ('Step time is: " {0} "'.format(step_time))
			# print (log_data.get(step_number))
			if log_data.get(step_number) == None:
				log_data[step_number] = {}
			log_data[step_number][rank_number] = step_time
			# print (log_data.get(step_number))
	
		# print(log_data)
		filedata.close()
		return log_data
	def log_max_time(self, logfile):
		log_data = self.readlog(logfile)    # Possible to avoid double call of readlog for the same file
		log_max_time = {}
		# print(log_data)
		# print(log_data.keys())
		for key in log_data.keys():
				log_max_time[key] = max(log_data[key].values())
		# print(log_max_time)
		return log_max_time

class MergedExperiment(Experiment):
	# source_log = set()
	# comment = set()

	def __init__(self, experiment_obj):
		self.source_log = {experiment_obj.source_log,} 
		self.launch_parameters = experiment_obj.launch_parameters
		self.launch_data = {}
		self.data_extract = {}
		self.comment = set()
		for key in experiment_obj.launch_data.keys():
			self.launch_data[key] = [experiment_obj.launch_data[key]]
		for key in experiment_obj.data_extract.keys():
			self.data_extract[key] = [experiment_obj.data_extract[key]]
		# self.data_extract = experiment_obj.data_extract
		self.comment.add(experiment_obj.comment)

	def merge(self, experiment_obj):
		if self.launch_parameters == experiment_obj.launch_parameters:
			# print('Merge is possible')
			self.source_log.add(experiment_obj.source_log)
			for key in experiment_obj.launch_data.keys():
				self.launch_data[key].append(experiment_obj.launch_data[key])
			for key in experiment_obj.data_extract.keys():

				self.data_extract[key].append(experiment_obj.data_extract[key])
			return 0

		else:
			# print('Error: Merge is impossible')
			return 1
class Timing:
	def __init__(self, params, time):
		self.params = params
		self.time = time

	def __eq__(self, other):
		return self.params == other.params

	# def __lt__(self, other):
	# 	for param in self.params:
	# 		if self.params[param]<other.params[param]:
	# 			return self<other
				



class Application_part:

	def __init__(self, part_name, parameters, time):
		self.part_name = part_name
		self.param_timing = [Timing(parameters,time),]
		
	def add(self, parameters, time):
		self.param_timing.append(Timing(parameters, time))

	def print_in_file(self,filename=''):
		# TODO:
		# implement abstract parameter set output
		# Add support of correctness checking and visualisation parameters script
		# Need to add parameters bounds to the default filename
		if not filename:
			filename = '{0}_timing.txt'.format(self.part_name)
			output = []
		f = open(filename,'w')
		for timing in self.param_timing:
			output.append((timing.params['Procs'], timing.params['Levels'], timing.time))
		output = sorted(output)
		for line in output:
			f.write('{0} {1} {2}\n'.format(line[0],line[1],line[2]))
		f.close()

