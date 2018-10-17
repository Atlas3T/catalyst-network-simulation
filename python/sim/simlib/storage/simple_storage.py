import scipy.io
import os

class store:
	def __init__(self, home_directory: str):
		self.home_directory = home_directory

	def save_variable(self, directory: str, variable_name: str, obj):
		full_directory = os.path.normpath(self.home_directory + '/' + directory + '/')
		if not os.path.exists(full_directory):
			os.makedirs(full_directory)
		filename = os.path.normpath(full_directory + '/' + variable_name)
		scipy.io.savemat(filename, {variable_name : obj}, appendmat=True)

	def load_variable(self, directory: str, variable_name: str):
		full_directory = os.path.normpath(self.home_directory + "/" + directory + "/")
		filename = os.path.normpath(full_directory + "/" + variable_name)
		contents = scipy.io.loadmat(filename, appendmat=True)
		temp = contents[variable_name]
		return temp
