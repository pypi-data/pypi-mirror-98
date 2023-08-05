
# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
try:
	from nettoolkit import IO, STR, DB
except:
	raise Exception("Mandatory Module Import Failed: pandas")
from os import path, remove
from shutil import copyfile
from random import randint


# ------------------------------------------------------------------------------
# VARS
# ------------------------------------------------------------------------------
VAR_DB_FIND_COLUMN = 'FIND'
VAR_DB_REPL_COLUMN = 'REPLACE'
SECTION_STARTER = ("GOAHEAD FOR", "REPEAT EACH")
SECTION_STOPPER = ("GOAHEAD END", "REPEAT STOP")

COMPARATORS = ("%2==", "%2!=", " ==", " !=", ">=", "<=", "> ", "< ")
RECURSIVE_SELECTED = False

# ------------------------------------------------------------------------------
# Definitions
# ------------------------------------------------------------------------------

def section_type(line):
	'''
	section type detector and trim logic line
	--> tuple containing (updated line, index)
		updated line: trimmed line by removing section detectors
		index: -1=Normal line, 0=Apply once section, 1=Repeat Section

	:param line: condition line from template
	:type str:
	'''
	if line[:11] == SECTION_STARTER[0]:
		repeat = 0
		line = line[11:].lstrip()
	elif line[:11] == SECTION_STARTER[1]:
		repeat = 1
		line = line[11:].lstrip()
	else:
		return (line, -1)
	return (line, repeat)


def fnr(temporary_template, var_db_df):
	'''
	find and replace
	Find and Replace will get apply on template backup text file.
	---> None

	:param var_db_df : database containing two columns - FIND and REPLACE
	:type DataFrame:
	'''
	for x in var_db_df.iterrows():
		_find = x[1][VAR_DB_FIND_COLUMN]
		_replace = x[1][VAR_DB_REPL_COLUMN]
		if _find.strip() != '':
			IO.update(temporary_template, _find, _replace)


class ConfGen():

	def __init__(self, 
		hostname=None,
		ip=None,
		template_file=None,
		output_file=None,
		xls_db=None,
		xls_db_sheet=None, 
		xls_db_df = None,
		var_db=None, 
		var_db_sheet=None,
		var_db_df=None,
		confGen_minimal=False,
		):
		self.hostname = hostname
		self.ip = ip
		self.template_file = template_file
		self.output_file = output_file
		self.xls_db = xls_db
		self.xls_db_sheet = xls_db_sheet
		self.xls_db_df = xls_db_df
		self.var_db = var_db
		self.var_db_sheet = var_db_sheet
		self.var_db_df = var_db_df
		self.confGen_minimal = confGen_minimal

	def generate(self):
		self.select_table_db()
		self.select_var_db()
		text_config = self.random_text_file()
		fnr(text_config, self.var_db_df)
		if self.xls_db_df is None: return None
		self.create_blank_file()
		self.generate_config(text_config)
		self.delete_temp_template(text_config)

	def select_table_db(self):
		if self.xls_db_df: return None
		try:
			if not self.xls_db_sheet:
				raise Exception(f"InputMissingOrInvalid-Error-tables")
			self.xls_db_df = DB.read_excel(file=self.xls_db, sheet=self.xls_db_sheet)
		except:
			raise Exception("InputMissingOrInvalid-Error-tables")

	def select_var_db(self):
		if self.var_db_df: return None
		try:
			if not self.var_db_sheet:
				raise Exception("InputMissingOrInvalid-Error-var")            
			self.var_db_df = DB.read_excel(file=self.var_db, sheet=self.var_db_sheet)
		except:
			raise Exception("InputMissingOrInvalid-va")

	def random_text_file(self, ):
		while True:
			random_number = randint(1, 1000000)
			random_file_name = 'temp_tmplate_' + str(random_number) + '.txt'
			temporary_template = random_file_name
			try:
				with open(temporary_template) as f: pass
			except:
				break
		try:
			copyfile(self.template_file, temporary_template)
		except FileNotFoundError as e:
			return None
		return temporary_template

	def create_blank_file(self): IO.to_file(self.output_file, '')

	def generate_config(self, text_config):
		# ~~~~~~~~~` Start Reading Template ~~~~~~~~~~
		with open(text_config, 'r') as f:
			while True:
				line = f.readline()
				# eof & blank
				if not line: break
				if line.strip() == '': continue

				# --------------- FULL TEMPLATE REPLACE IF REQUESTED ---------------- #
				if not self.confGen_minimal:
					# sub-section than extract slice of that section
					if section_type(line)[1] != -1:
						line = Section(f, line, self.xls_db_df, self.template_file).slice

				# write updated line(s)
				IO.add_to_file(self.output_file, line)

	def delete_temp_template(self, text_config):
		# ~~~~~~~ Delete Temporary Template File ~~~~~~~~
		remove(text_config)




# -----------------------------------------------------------------------------
# class: Section Selector  [ DATA SECTION LOGIC ]
# -----------------------------------------------------------------------------
class Section:
	'''Reads section of config and returns slice of that section

	INPUT
	-----
	:param f : template file
	:type text file:

	:param logic_line : condition line from template
	:type str:
	
	:param df : database on which condition to be apply
	:type DataFrame:
	
	OUTPUT
	------
	slice : updated config for the section

	'''

	def __init__(self, f, logic_line, df, template_name):
		'''
		Reads section of config and returns slice of that section
		:param f: template file
		:type file:

		:param logic_line: condition line from template
		:type str:

		:param df: database on which condition to be apply 
		:type DataFrame:
		'''
		self.template_name = template_name
		self.output_slice = ''
		self.section_lines = []
		if not df.empty:                            # Parent dataFrame
			self.logic_line = logic_line.lstrip()
			self.__set_section_type
			self.__set_filter_string(df)
			self.read_line = True
			self.__read_lines(f, df)
			if not self.filtered_dataframe.empty:    # Self DataFrame
				self.output_slice = Replicate(
					configSectionList=self.section_lines, 
					dataframe=self.filtered_dataframe,
					repeat=self.repeat
					).output

	@property
	def slice(self):
		'''
		---> updated output slice from template section
		'''
		return self.output_slice

	# ------------------------- LOCAL -------------------------- #

	# section type detector and strip logic line
	@property
	def __set_section_type(self):
		_ = section_type(self.logic_line)
		self.repeat = _[1]
		self.logic_line = _[0]

	# creates pandas filter string from Template condition line
	# and filtered dataframe from parent dataframe for condition provided
	# df : datafrmae to filter on        
	def __set_filter_string(self, df):
		while self.logic_line.find("( ") > -1:
			self.logic_line = self.logic_line.replace("( ", "(")
		while self.logic_line.find(" )") > -1:
			self.logic_line = self.logic_line.replace(" )", ")")
		if self.logic_line.find("((") > -1:
			self.logic_line = self.logic_line.replace("((", "((df['")
			i = -1
			for x in range(10):
				doubleBR_idx = self.logic_line.find("((")
				i = self.logic_line.find("(", i+1)
				if i == -1: break
				if i == doubleBR_idx: continue
				if i == doubleBR_idx+1: continue
				self.logic_line = self.logic_line[:i] + "(df['" + self.logic_line[i+1:]
		else:
			self.logic_line = self.logic_line.replace("(", "(df['")
		for _c in COMPARATORS:
			while self.logic_line.find(" " + _c) > -1:
				self.logic_line = self.logic_line.replace(" " + _c, _c)
			if self.logic_line.find(_c) > -1:
				self.logic_line = self.logic_line.replace(_c, "'] " + _c)
		self.logic_line = "df[ " + self.logic_line.strip() + " ]"
		self.logic_line = self.logic_line.replace(' != ""', '.notnull()')
		self.logic_line = self.logic_line.replace(' == ""', '.isnull()')
		self.logic_line = self.logic_line.replace('%2!= ""', '%2.notnull()')
		self.logic_line = self.logic_line.replace('%2== ""', '%2.isnull()')
		try:
			self.filtered_dataframe = eval(self.logic_line)
		except:
			print(f"Error in {self.template_name}")
			print(self.logic_line)
			raise Exception()

	# Continue reading lines from template file from where it stopped
	# Adds section lines to section_lines list
	# f : template file
	# df : Parent dataFrame
	def __read_lines(self, f, df):
		while self.read_line:
			line = f.readline()
			if line.strip() == '': continue
			if line.strip()[:11] in SECTION_STOPPER:
				self.read_line = False
			elif line.strip()[:11] in SECTION_STARTER:
				if RECURSIVE_SELECTED:
					_s = Section(f, line, self.filtered_dataframe, self.template_name)
				else:
					_s = Section(f, line, df, self.template_name)
				self.section_lines.extend(_s.slice)
			elif not self.filtered_dataframe.empty:
				self.section_lines.append(line)






# ------------------------------------------------------------------------------
# class: Replicate config [ CONFIGURATION REPLICATOR ]
# ------------------------------------------------------------------------------

class Replicate:
	''' Class to generate Repeatiative config from template list based on 
	Pandas DataFrame.

	INPUT
	-----
	:param configSectionList: lines/section from template
	:type list:
	
	:param dataframe: database for which section to be repeated/applied
	:type dataframe:

	:param repeat: True=repeat for all records, False=apply for first record
	:type boolean:

	OUTPUT
	------
	output: updated configuration output
	'''
	
	# class initializer
	def __init__(self, configSectionList, dataframe, repeat):
		self._output = []
		self.repeat = repeat
		self._tmplTpl = configSectionList
		self._shtData = dataframe
		self.__readAllData

	# updated config output
	@property
	def output(self): return self._output

	# ------------------------- LOCAL -------------------------- #

	# Go thru each line of data (data frame)
	@property
	def __readAllData(self):
		rows = max(self._shtData.count())
		for row in range(rows):
			self.__readingLine(row)
			if not self.repeat:
				break

	# Working on a single line
	def __readingLine(self, row):    
		tmpList = list(self._tmplTpl)         # Template commands in a list
		RowData = self._shtData.iloc[row]

		for i, line in enumerate(tmpList):          # Go thru lines
			for header in RowData.keys():           # Go thru columns
				if STR.found(line, header):
					try:
						if RowData[header] == 'nan': RowData[header] = ''
						if RowData[header] == False: RowData[header] = ''
						if int(RowData[header]) == RowData[header]:
							line = line.replace(header, str(int(RowData[header])))
						else:
							line = line.replace(header, str(RowData[header]))
					except:
						line = line.replace(header, str(RowData[header]))
			tmpList[i] = line

		# append updated line|tmpList to _output
		self._output.extend(tmpList)
		tmpList.clear()                    # clear list for next iteration



# ------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ------------------------------------------------------------------------------
