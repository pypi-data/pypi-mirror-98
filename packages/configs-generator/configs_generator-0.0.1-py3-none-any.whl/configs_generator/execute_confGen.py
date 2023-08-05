
# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
try:
	from nettoolkit import XL_READ
except:
	raise Exception("Mandatory Module Import Failed: nettoolkit")

from .confGen import ConfGen

# ------------------------------------------------------------------------------

class Execute_ConfGen():

	def __init__(self, 
		hostname=None,
		ip=None,
		filename=None, 
		pdf_dic=None, 
		template=None, 
		logger=None,
		report_id=None,
		):
		self.hostname = hostname
		self.ip = ip
		self.filename = filename
		self.dev_hostname = filename if filename else hostname
		self.attribs = {}
		self.logger = logger
		self.report_id = report_id
		self.set_input_attrs(pdf_dic, template)
		self.execute()

	def execute(self): 
		op = ConfGen(**self.attribs)
		op.generate()
		return op.output_file

	# ----------- Input Attributes for Confgen --------- #

	def set_input_attrs(self, pdf_dic, template):
		self.set_ip_hostname()
		self.set_src_attr(pdf_dic)
		self.set_template_attr(pdf_dic, template)
		self.set_op_attr()
		self.set_logger()

	def set_ip_hostname(self): 
		self.attribs['hostname'] = self.hostname
		self.attribs['ip'] = self.ip

	# def set_op_as_list_attr(self): self.attribs['op_list'] = False
	def set_op_attr(self): 
		self.attribs['output_file'] = self.logger.u['output_folder'] + self.dev_hostname + " - ALI.txt"
		self.attribs['confGen_minimal'] = self.logger.u['confGen_minimal']

	def set_src_attr(self, pdf_dic):
		if pdf_dic: self.set_src_attr_from_pdf_dic(pdf_dic)
		else: self.set_src_attr_from_db()

	def set_src_attr_from_db(self):
		self.db = self.filename if self.filename else self.logger.u['output_folder'] + self.hostname + ".xlsx"
		self.attribs['xls_db'] = self.db
		self.attribs['xls_db_sheet'] = 'tables'
		self.attribs['var_db'] = self.db
		self.attribs['var_db_sheet'] = 'var'

	def set_src_attr_from_pdf_dic(self, pdf_dic):
		self.pdf_dic = pdf_dic
		self.attribs['xls_db_df'] = self.pdf_dic['tables']
		self.attribs['var_db_df'] = self.pdf_dic['var']

	def set_template_attr(self, pdf_dic, template):
		if template: self.set_template_attr_from_template(template)
		elif pdf_dic: self.set_template_attr_from_df(pdf_dic)
		else: 
			self.set_template_attr_from_db()
			self.update_dev_hostname_fromdb()

	def set_template_attr_from_template(self, template):
		self.attribs['template_file'] = self.logger.u['jinja_folder'] + template

	def set_template_attr_from_df(self, pdf_dic):
		d = pdf_dic['var']["REPLACE"].get(pdf_dic['var']["FIND"]=='[template]')
		template = d[d.index[0]]
		if template[-4:] == ".txt": template = template[:-4]
		self.attribs['template_file'] = self.logger.u['jinja_folder'] + template + ".txt"

	def set_template_attr_from_db(self):
		self.temp_df = XL_READ(self.db, 'var')
		tf = self.temp_df.column_values('REPLACE', FIND='[template]').to_string(index=False).strip()
		if tf[-4:] == ".txt": tf = tf[:-4]
		self.attribs['template_file'] = self.logger.u['jinja_folder'] + tf + ".txt"

	def update_dev_hostname_fromdb(self):
		hn = self.temp_df.column_values('REPLACE', FIND='[dev_hostname]').to_string(index=False).strip()
		self.dev_hostname = hn

	def set_logger(self): 
		self.attribs['logger'] = self.logger
		self.attribs['report_id'] = self.report_id
