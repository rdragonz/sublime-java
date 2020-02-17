import sublime
import sublime_plugin


class psvmCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, self.view.sel()[0].begin(), "public static void main(String[] args){}")
		point = self.view.sel()[0].begin() - 1
		self.view.sel().clear()
		self.view.sel().add(point)


class classCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		allcontent = sublime.Region(0, self.view.size())
		self.view.replace(edit, allcontent, "public class ClassName {\n\t/**\n\t\t[Class Name]\n\t\tWritten By [Name] in [Year]\n\t\t[Project Name]\n\t\t[Project Description]\n\t*/\n\tpublic static void main(String[] args){\n\t\t\n\t}\n}")
		self.view.sel().clear()

class printlnCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, self.view.sel()[0].begin(), "System.out.println();")
		point = self.view.sel()[0].begin() - 2
		self.view.sel().clear()
		self.view.sel().add(point)