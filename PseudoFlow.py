import sublime, sublime_plugin

import urllib
#import urllib2
import threading

import sys
import os

import re

#http://pythonprogramming.net/urllib-tutorial-python-3/
#http://pythonprogramming.net/parse-website-using-regular-expressions-urllib/?completed=/regular-expressions-regex-tutorial-python-3/


#http://docs.python-guide.org/en/latest/scenarios/scrape/

#print(os.path.join(os.path.dirname(__file__)))

#sys.path.append(os.path.join(os.path.dirname(__file__), "bs4"))
#sys.path.append(os.path.join(os.path.dirname(__file__), "bs4.builder"))

#import bs4

#from bs4 import BeautifulSoup

#import PseudoFlow.bs4.builder
#import PseudoFlow.bs4
#from PseudoFlow.bs4 import BeautifulSoup


# command will turn pseudo code comments in to queries on stackoverflow and let you insert code from there


#follow this tutorial
# http://code.tutsplus.com/tutorials/how-to-create-a-sublime-text-2-plugin--net-22685



class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args ):
		self.view.insert(edit, 0, args['test'] )



class eventsCommand(sublime_plugin.EventListener):

	def on_post_save_async(self, view):
		view.run_command('pseudo')
		print('on post save')


	# def on_modified_async(self,view):
	# 	print('test thing thing')


class PseudoCommand(sublime_plugin.TextCommand):
    
    def run(self, view):
        
        sel = self.view.sel()
        selected = None

        print('sel')
        print(sel)

        if len(sel) > 0:
            selected = self.view.substr(self.view.word(sel[0])).strip()
            print(selected )
            if selected.startswith('#P:'):
            	print('run pseudo flow')
            	selected = selected[1:]
            	threads=[]
            	thread=StackoverflowApiCall(sel, selected, 5)
            	threads.append(thread)
            	thread.start()
            	sublime.set_timeout(lambda:self.handle_threads(threads,self.view),100)


    def handle_threads(self,threads,view):
    	for thread in threads:
    		if thread.result is not None:
    			print('results')
    			print(thread.result)
    			#self.view.run_command('example')
    			#self.view.insert(view, 0, thread.result )
    			#self.view.insert(self.edit, 0, thread.result )
    			args={'test':thread.result}
    			
    			self.view.run_command('example',args )
    			
    			return

    	sublime.set_timeout(lambda:self.handle_threads(threads,view),100)



class StackoverflowApiCall(threading.Thread):

	def __init__(self, sel, string, timeout):
		self.sel = sel
		self.original = string
		self.timeout = timeout
		self.result = None

		print( "sel" )
		print( sel )
		print( "string" )
		print( string )

		threading.Thread.__init__(self)


	def run(self):

		resp = urllib.request.urlopen('http://stackoverflow.com/search?tab=relevance&q=compare%20arrays%20python')
		#print( resp.read().decode('utf-8') )

		#soup = BeautifulSoup( x.read(), 'lxml' )
		#soup = PseudoFlow.bs4.BeautifulSoup(x.read())

		#p = re.findall(r'<code>(.*?)<code>', str( resp.read().decode('utf-8') ))
		# print('cunt')
		# print(p)


		r = re.compile('(?<=href=").*?(?=")')
		data = r.findall( resp.read().decode('utf-8') )
		# print('data')
		# print(data)

		qs=[]
		for link in data:
		 	if '/questions/' in link:
		 		qs.append(link)
		# 		print(link)


		print(qs[1])

		#"http://stackoverflow.com/%s" % data[1]
		q = urllib.request.urlopen( "http://stackoverflow.com/%s" % qs[1] )
		

		#r = re.compile('(?<=code).*?(?=</code>)')

		p = re.findall(r'(?=<code>).*?(?=</code>)', str( q.read() ))
		print('----')
		print(p)

		self.result = p[0]
		return
		#self.view.insert(edit, 0, "Hello, World!")
		


		# if fail no result
		self.result = False



	# def run(self):
	# 	try:
	# 		x = urllib.request.urlopen('http://stackoverflow.com/search?tab=relevance&q=compare%20arrays%20python')
	# 		print( x.read() )
	# 		return
	# 	except:
	# 		print('fucked it')

	# 	self.result = False




#P:



	# def run(self, edit):
	# 	self.view.insert(edit, 0, "Hello, World!")


# class twoCommand(sublime_plugin.Plugin):

# 	def onPostSave(self, view):
# 		print "test"