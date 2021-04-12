
class QCktException(Exception):
	def __init__(self,msg):
		self.args = msg
		self.msg = msg
	
	def __str__(self):
		return self.msg
