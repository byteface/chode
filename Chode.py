import sublime, sublime_plugin
import urllib
import threading
import sys
import os
import re

# create comment, then a p, then a colon i.e

#p:

#TODO add more. currently only python . do //p:  asap

#TODO - parse multilines.. means stripping ends off. <!--p: or /*p:

# comment will be sent as a query to stackoverflow, the top answer of the top result is returned directly into your code
# for different answers try rewording your query.

# To work your cursor must be ON THE LINE YOU WANT TO RUN and then press save.


#p: css round corners

#p: jquery last item in a list :v

#p:abstract class java

#p: reverse array in java

#p: delete the mongo database


#p:compare arrays python



#p: singleton in python



# notes --
# http://pythonprogramming.net/urllib-tutorial-python-3/
# http://pythonprogramming.net/parse-website-using-regular-expressions-urllib/?completed=/regular-expressions-regex-tutorial-python-3/
# http://code.tutsplus.com/tutorials/how-to-create-a-sublime-text-2-plugin--net-22685
# https://www.sublimetext.com/docs/3/api_reference.html


# https://github.com/mgonto/sublime-config/tree/master/Packages/Default



class ExampleCommand(sublime_plugin.TextCommand):


	# def normalize_line_endings(self, string):
	#         string = string.replace('\r\n', '\n').replace('\r', '\n')
	#         line_endings = self.view.settings().get('default_line_ending')
	#         if line_endings == 'windows':
	#             string = string.replace('\n', '\r\n')
	#         elif line_endings == 'mac':
	#             string = string.replace('\n', '\r')
	#         return string


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

		#output = urllib.parse.quote( output, encoding='utf-8', errors='replace')


		# TODO - check if i only have to do this for HTML code. we may need to take the interpretter class of the HTML class to decide parsing

		import html.parser
		h = html.parser.HTMLParser()
		output = h.unescape( output )

		self.view.insert(edit, args['line_length'], output )







class EventsCommand(sublime_plugin.EventListener):

	def on_post_save_async(self, view):
		view.run_command('chode')





class duplicateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            # if region.empty():
            line = self.view.line(region)
            line_contents = self.view.substr(line) + '\n'
            self.view.insert(edit, line.begin(), line_contents)
            # else:
            #     self.view.insert(edit, region.begin(), self.view.substr(region))


class ChodeCommand(sublime_plugin.TextCommand):
    
    def run(self, view):

    	for region in self.view.sel():
    		line = self.view.line(region)
    		selected = self.view.substr(line).strip()# + '\n'

    		print( 'pseudo selected:', selected )

    		# TODO - startswith func that returns char it starts with... or empty string
    		if selected.startswith('#p:'):
    			
    			print('ok')

				# clean it up for a query
    			# selected = selected.split('#p:')[1].strip()
    			selected, params = self.get_parameters(selected)

    			threads=[]
    			thread=StackoverflowApiCall( self.view.sel(), selected, params, line, 5 )
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



    def get_parameters(self,string):
    	
    	# strip off the call
    	string = string.split('#p:')[1].strip()

    	p={}

    	params = string.split(':')

    	query=params[0].strip()

    	# for param in params:
    	# 	if 'css' in param // TODO - langs

    	p['verbose']=False

    	for param in params:
    		if 'v' in param.strip():
    			p['verbose']=True


    	return query, p
    			





class StackoverflowApiCall(threading.Thread):

	def __init__(self, sel, string, params, line, timeout):
		self.sel = sel
		self.query = string
		self.params = params
		self.line = line
		self.timeout = timeout
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
		

		# VERBOSE MODE

		if self.params['verbose'] == True:

			print('verbose')
			
			reg = re.compile('<td class="answercell">(.*?)</td>')
			#reg = re.compile('<div class="post-text" itemprop="text">(.*?)</div>')

			p = reg.search( str(q.read()) )
			#print('----')
			#print(p)
		
			self.result = p.groups()[0]
			return
		
		else:

			print('non verbose')

			reg = re.compile('<td class="answercell">(.*?)</td>')
			p = reg.search( str(q.read()) )

			answer = p.groups()[0]
			# print('---- ANSER')
			# print(answer)

			# # CODE ONLY
			reg2 = re.compile('<code>(.*?)</code>')
			ans = reg2.search( answer )

			print('------------------')
			print(ans.groups()[0])

			self.result = ans.groups()[0]
			return


			# NON VERBOSE MODE
			#reg = re.compile('<code>(.*?)</code>')




#		p = reg.search( str(q.read()) )
		#print('----')
		#print(p)
	
#		self.result = p.groups()[0]
#		return

		# answer = p.groups()[0]

		# print('---- ANSER')
		# print(answer)


		# # CODE ONLY
		# reg2 = re.compile('<code>(.*?)</code>')
		# ans = reg2.search( answer )

		# print('------------------')
		# print(ans.groups()[0])

		# self.result = ans.groups()[0]
		# return


		# TODO - if fail no result
		self.result = False







# WITH TAGS
#re.compile('(<div class="deg">.*?</div>)')

# WITHOUT TAGS
#re.compile('<div class="deg">(.*?)</div>')

