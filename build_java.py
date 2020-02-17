import sublime
import sublime_plugin

import subprocess
import threading
import os


class BuildJavaCommand(sublime_plugin.WindowCommand):

	encoding = 'utf-8'
	killed = False
	proc = None
	panel = None
	panel_lock = threading.Lock()

	def is_enabled(self, kill=False):
		# The Cancel build option should only be available
		# when the process is still running
		if kill:
			return self.proc is not None and self.proc.poll() is None
		return True
	def getInput(self, userResponse):
		#Gets the user input and saves it as a self variable
		self.runClass = userResponse

	def run(self, kill=False):
		if kill:
			if self.proc:
				self.killed = True
				self.proc.terminate()
			return

		vars = self.window.extract_variables()
		
		working_dir = vars['folder'] + "\\src\\"

		#Get lines from the java configuration options if it exists
		javatxt = {}
		if os.path.exists(vars['folder'] + "\\java.txt"):
			with open(vars['folder'] + "\\java.txt") as file:
				for line in file:
					line = line.strip().split("=")
					javatxt.update({line[0]:line[1]})
					

		#Get the class to run unless it's defined in the java.txt file
		if 'runClass' not in javatxt:
			self.runClass = vars['file_base_name']
		else:
			self.runClass = javatxt['runClass']
		

		#Get any add-modules options from the java.txt file
		if 'add-modules' in javatxt:
			self.add_modules = " --add-modules={}".format(javatxt["add-modules"])
		else:
			self.add_modules = ""

		#Get any module-path options from java.txt file
		if 'module-path' in javatxt:
			self.module_path =" --module-path {}".format(javatxt['module-path'])

		else:
			self.module_path = ""

		#Get any additional build options from the java.txt file
		if 'additional-options' in javatxt:
			self.additional_options = " {}".format(javatxt['additional-options'])

		else:
			self.additional_options = ""

		#Get any additional run options from the java.txt file
		if 'run-options' in javatxt:
			self.run_options = " {}".format(javatxt['run-options'])
		else:
			self.run_options = ""

		#Create the classpath
		classpath = ""

		if os.path.exists(vars['folder'] + "\\classpath.txt"):
			with open(vars['folder'] + "\\classpath.txt") as file:
				for line in file:
					#Get each line in the classpath
					classpath += "\"" + line.strip() + "\";"
		#Add the default classpath options, the output directory and the current working dir
		classpath += "{}\\src;{};{}\\bin".format(vars['folder'], vars['folder'], vars['folder'])


		# A lock is used to ensure only one thread is
		# touching the output panel at a time
		with self.panel_lock:
			# Creating the panel implicitly clears any previous contents
			self.panel = self.window.create_output_panel('exec')

			# Enable result navigation. The result_file_regex does
			# the primary matching, but result_line_regex is used
			# when build output includes some entries that only
			# contain line/column info beneath a previous line
			# listing the file info. The result_base_dir sets the
			# path to resolve relative file names against.
			settings = self.panel.settings()
			settings.set(
				'result_file_regex',
				r'^File "([^"]+)" line (\d+) col (\d+)'
			)
			settings.set(
				'result_line_regex',
				r'^\s+line (\d+) col (\d+)'
			)
			settings.set('result_base_dir', working_dir)

			self.window.run_command('show_panel', {'panel': 'output.exec'})

		if self.proc is not None:
			self.proc.terminate()
			self.proc = None

		command = 'echo Building... & javac -d {} --class-path {}{} {} & echo Running... & java --class-path {}{}{}{} {}'
		command = command.format(working_dir + "..\\bin", classpath, self.additional_options, vars['file'], classpath,self.module_path, self.add_modules, self.run_options, self.runClass)

		self.proc = subprocess.Popen(
			command,
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT,
			cwd=working_dir,
			shell=True
		)

		self.killed = False

		threading.Thread(
			target=self.read_handle,
			args=(self.proc.stdout,)
		).start()

	def read_handle(self, handle):
		chunk_size = 2 ** 13
		out = b''
		while True:
			try:
				data = os.read(handle.fileno(), chunk_size)
				# If exactly the requested number of bytes was
				# read, there may be more data, and the current
				# data may contain part of a multibyte char
				out += data
				if len(data) == chunk_size:
					continue
				if data == b'' and out == b'':
					raise IOError('EOF')
				# We pass out to a function to ensure the
				# timeout gets the value of out right now,
				# rather than a future (mutated) version
				self.queue_write(out.decode(self.encoding))
				if data == b'':
					raise IOError('EOF')
				out = b''
			except (UnicodeDecodeError) as e:
				msg = 'Error decoding output using %s - %s'
				self.queue_write(msg  % (self.encoding, str(e)))
				break
			except (IOError):
				if self.killed:
					msg = 'Cancelled'
				else:
					msg = 'Finished'
				self.queue_write('\n[%s]' % msg)
				break

	def queue_write(self, text):
		sublime.set_timeout(lambda: self.do_write(text), 1)

	def do_write(self, text):
		with self.panel_lock:
			self.panel.run_command('append', {'characters': text})
