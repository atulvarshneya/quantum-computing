

class QSimError(BaseException):
	def __init__(self,arg):
		self.args = arg
		self.msg = arg
	def __str__(self):
		return self.msg
