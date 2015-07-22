
import sublime, sublime_plugin
import urllib
import threading
import sys
import os
import re

# create a tag with a comment, caps P then colon i.e

#P:

# comment will the become a query to stackoverflow, the top answer is returned directly into your code


# notes --
# http://pythonprogramming.net/urllib-tutorial-python-3/
# http://pythonprogramming.net/parse-website-using-regular-expressions-urllib/?completed=/regular-expressions-regex-tutorial-python-3/
# http://code.tutsplus.com/tutorials/how-to-create-a-sublime-text-2-plugin--net-22685
# https://www.sublimetext.com/docs/3/api_reference.html


# https://github.com/mgonto/sublime-config/tree/master/Packages/Default



class ExampleCommand(sublime_plugin.TextCommand):


	def normalize_line_endings(self, string):
	        string = string.replace('\r\n', '\n').replace('\r', '\n')
	        line_endings = self.view.settings().get('default_line_ending')
	        if line_endings == 'windows':
	            string = string.replace('\n', '\r\n')
	        elif line_endings == 'mac':
	            string = string.replace('\n', '\r')
	        return string


	def run(self, edit, **args ):

		# print("args")
		# print(args)


		# NOTE - bit worried this strips newlines out of code. so will have to look at better solution.
		output = '\n' + '\n'.join( args['result'].split('\\n') )


		# print('test')
		# print(args['result'])
		# print('test2')
		# print(args['result'].splitlines())


		#output = self.normalize_line_endings(output)


		self.view.insert(edit, args['line_length'], output )







class EventsCommand(sublime_plugin.EventListener):

	def on_post_save_async(self, view):
		view.run_command('pseudo')





class duplicateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            # if region.empty():
            line = self.view.line(region)
            line_contents = self.view.substr(line) + '\n'
            self.view.insert(edit, line.begin(), line_contents)
            # else:
            #     self.view.insert(edit, region.begin(), self.view.substr(region))


class PseudoCommand(sublime_plugin.TextCommand):
    
    def run(self, view):

    	for region in self.view.sel():
    		line = self.view.line(region)
    		selected = self.view.substr(line).strip()# + '\n'

    		print( 'pseudo selected:', selected )

    		if selected.startswith('#P:'):
    			
    			print('ok')

				# clean it up for a query
    			selected = selected.split('#P:')[1].strip()

    			threads=[]
    			thread=StackoverflowApiCall( self.view.sel(), selected, line, 5 )
    			threads.append(thread)
    			thread.start()
    			sublime.set_timeout(lambda:self.handle_threads(threads,self.view),100)


    def handle_threads(self,threads,view):
    	for thread in threads:
    		if thread.result is not None:

    			args={
    			'result':thread.result,
    			'linecount':thread.line.begin(),
    			'line_length':thread.line.end(),
    			'query':thread.query
    			}

    			self.view.run_command( 'example', args )
    			
    			return

    	# if fail try again in a sec
    	sublime.set_timeout(lambda:self.handle_threads(threads,view),100)



class StackoverflowApiCall(threading.Thread):

	def __init__(self, sel, string, line, timeout):
		self.sel = sel
		self.query = string
		self.timeout = timeout
		self.line = line
		self.result = None
		threading.Thread.__init__(self)


	def run(self):

		url = 'http://stackoverflow.com/search?tab=relevance&q=%s' % urllib.parse.quote(self.query)
		print('url::', url)

		resp = urllib.request.urlopen( url )
		#print( resp.read().decode('utf-8') )

		r = re.compile('(?<=href=").*?(?=")')
		data = r.findall( resp.read().decode('utf-8') )
		# print('data')
		# print(data)

		qs=[]
		for link in data:
		 	if '/questions/' in link:
		 		qs.append(link)
		# 		print(link)


		#print(qs[1])

		q = urllib.request.urlopen( "http://stackoverflow.com/%s" % qs[1] )
		
		reg = re.compile('<code>(.*?)</code>')

		p = reg.search( str(q.read()) )
		print('----')
		#print(p)
		print(p.groups()[0])
		



		self.result = p.groups()[0]
		return
		
		# TODO - if fail no result
		self.result = False











#P: abstract class java



#P: python run terminal command


#P: reverse array in java




#P: jquery last element





#P:reverse array in Java :css :gist :verbose


#P:compare arrays python








#P: singleton in python
# loop through the array

# slpit array on 4th item


# WITH TAGS
#re.compile('(<div class="deg">.*?</div>)')

# WITHOUT TAGS
#re.compile('<div class="deg">(.*?)</div>')

