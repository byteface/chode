import sublime, sublime_plugin
import urllib
import threading
import sys
import os
import re

# create comment, then a p, then a colon i.e

# comment will be sent as a query to stackoverflow, the top answer of the top result is returned directly into your code
# for different answers try rewording your query.

#p:

# To work your cursor must be ON THE LINE YOU WANT TO RUN and then press save.


#p: css round corners :v

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


#TODO add more. currently only python . do //p:  asap
#TODO - parse multilines.. means stripping ends off. <!--p: or /*p:


class InjectCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args ):
		'''
		this command cleans up the code strings returned and injects them into sublime
		'''

		# NOTE - bit worried this strips newlines out of code. so will have to look at better solution.
		output = '\n' + '\n'.join( args['result'].split('\\n') )
		output = ''.join( output.split('\\r') )


		# TODO - check if i only have to do this for HTML code. we may need to take the interpretter class of the HTML class to decide parsing

		import html.parser
		h = html.parser.HTMLParser()
		output = h.unescape( output )

		output = output.replace("\\","")

		self.view.insert(edit, args['line_length'], output )



class EventsCommand(sublime_plugin.EventListener):

	def on_post_save_async(self, view):
		view.run_command('chode')



class ChodeCommand(sublime_plugin.TextCommand):

    # TODO - non single line comments.
	comments=[ '#','//','<!--','/*',"'",';','--','*','||','"','\\','*>','⍝','NB.','REM','::',':','C' ]

	def hasChode(self,string):
		'''
		detects a chode and returns the comment used
		'''
		for comment in self.comments:
			if string.startswith( '%sp:' % comment ):
				print('hasChode')
				return comment

		return ''


	def run(self, view):

		for region in self.view.sel():
			line = self.view.line(region)
			selected = self.view.substr(line).strip()

			print( 'pseudo selected:', selected )

			if len(self.hasChode(selected)) > 0:

				print('chode detected')
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

				self.view.run_command( 'inject', args )
				return

		# if fail try again in a sec
		sublime.set_timeout(lambda:self.handle_threads(threads,view),100)


	def get_parameters(self,string):

		# strip off the call
		string = string.split( '%sp:' % self.hasChode(string) )[1].strip()

		p={}

		params = string.split(':')

		query=params[0].strip()

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
		# print('url::', url)


		request = urllib.request.Request(url)
		request.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')
		resp = urllib.request.urlopen(request)

		#resp = urllib.request.urlopen( url )
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


		# print('HEY HEY HEY ----------------')
		# print(qs[1])


		url2 = "http://stackoverflow.com/%s" % qs[1]

		request2 = urllib.request.Request(url2)
		request2.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')
		q = urllib.request.urlopen(request2)

		#q = urllib.request.urlopen(  )
		

		#p:compare arrays python

		#p: test some other query

		#p: c++ recursion error happening :v

		# VERBOSE MODE

		if self.params['verbose'] == True:

			#print('verbose')
			
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

			# print('------------------')
			# print(ans.groups()[0])

			self.result = ans.groups()[0]
			return


		# TODO - if fail no result
		self.result = False





# WITH TAGS
#re.compile('(<div class="deg">.*?</div>)')

# WITHOUT TAGS
#re.compile('<div class="deg">(.*?)</div>')
