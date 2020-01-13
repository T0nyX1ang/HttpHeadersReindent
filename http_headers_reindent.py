import sublime
import sublime_plugin
import json

# Http Headers Reindent.
# A tool to reindent http header file from Fiddler to Python dictionary format.
# Tony Xiang (C) 2020
# Licensed under MIT.

config = {}

class HttpHeadersReindentCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sep = config.get('sep')
		ignore = config.get('ignore')
		for region in self.view.sel():
			content = self.view.substr(region)
			self.view.replace(edit, region, self.convert(content, sep, ignore))

	def convert(self, sentence, sep, ignore):
		result = {}
		lword = ''
		rword = ''
		quote_met = False
		for char in sentence:
			if char in ignore:
				continue
			elif char != ':' and quote_met is False:
				lword += char
			elif char == ':' and quote_met is False:
				quote_met = True
			elif quote_met is True:
				if char not in sep:
					rword += char
				else:
					# deal with whitespaces in lword and rword
					i = 0
					while rword[i] == ' ':
						i += 1
					rword = rword[i:]
					j = len(lword) - 1
					while lword[j] == ' ':
						j -= 1
					lword = lword[:j + 1]
					# generate the key-value pair
					result[lword] = rword
					quote_met = False
					lword, rword = '', ''
		if len(result) == 0:
			return ''
		else:
			return json.dumps(result, indent=4)

def plugin_loaded():
	global config
	config = sublime.load_settings("HttpHeadersReindent.sublime-settings")
