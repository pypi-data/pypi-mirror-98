



import os
import typing
import lesscpy
import io

from pypine import *







class LessC(AbstractProcessor):

	__FILE_TYPE_INFO = FileTypeInfo.guessFromFileName("x.css")

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, minify:bool = False):
		super().__init__(
			actionIfUnprocessable=EnumAction.Ignore
		)

		assert isinstance(minify, bool)

		self.__minify = minify
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def isProcessable(self, f) -> bool:
		if f.dataType not in [ "file" ]:					# TODO: support URLs!
			return False
		return f.fileName.endswith(".less")
	#

	def processElement(self, ctx:Context, f):
		rawText = f.readText()
		rawText = lesscpy.compile(
			io.StringIO(rawText),
			minify=self.__minify,
			tabs=True,
		)
		assert isinstance(rawText, str)

		f2 = InMemoryFile(f.relFilePathWithoutExt + ".css", LessC.__FILE_TYPE_INFO, rawText)
		return f2
	#

#






