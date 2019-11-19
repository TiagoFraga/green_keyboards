import com.dtmilano.android.viewclient.EditText

class EditedEditText(EditText):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(EditText, self).__init__()
		self.arg = arg
	
	def type_without_sleep(self, text, alreadyTouched=False):
        if not text:
            return
        if not alreadyTouched:
            self.touch()
        self.device.type(text)
