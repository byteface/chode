### Chode
TODO - insert image here

## About

Chode is a Sublime Plugin to help you CHeat at cODE. I wrote it in few hours and is a working proof of concept.


So I often write pseudo code / comments when developing or stubbing out an app or piece of functionality as a series of steps. i.e.


# create some class

# create some function

# loop through array compare this and that

# split out last item if is bigger than

# add it to the array and dispatch and event

# write it to the mongo database

etc


I then go about writing the real code, comment at a time. This is also useful when delegating work or showing others how you're thinking. You can stub whole applications quickly rather than making it up as you go and helps you to architect and discuss different posibilities or options.


Most people use Stackoverflow a lot. Even if you think you know the answer, It's useful to check incase there's a newer or better way to do things.


I figured it would be cool if code comments could quickly generate code exmaples to build off. pseudo code + stackoverflow = Chode. It took just a few hours to get a 'my first sublime plugin' working prototype and here it is.



## Installation
Download this whole folder and put in Sublime Packages folder, on my mac it looks like this...


/Users/mike/Library/Application\ Support/Sublime\ Text\ 3/Packages/Chode


restart and you're good to go.




## Usage

Chode runs when you save BUT it only analyses the line your cursor is currently on.

if the line starts with a comment, followed by a 'p', then a colon. ie. in python...


#p:


then everything after those characters will get sent to stackoverflow as a query. the top link is selected, then the best answer from that link inserted into your code.


i.e

#p: a singleton in python


click on that line, press save, would become...


#p: a singleton in python
<TOP ANSWER FROM STACK OVERFLOW GETS INSERTED HERE>



## FUTURE

I'm a busy guy and for now, whilst clunky, this is serving it's intended purpose. However I would love to do this...

• detect current language by getting filename. auto search on that language
• have some parameters i.e.

#p: some question :css :v

the :css parameter search in css even tho im in a .html file. or .js file.
the :v parameter returns verbose. i.e. whole post.

something like a :nv 'non verbose' parameter to only return the 1st code node only?

paramters to return second / third answer?

paramters to return answers from 2nd 3rd results. or newest or other filters?

settings with various default. i.e. verbose / non verbose. 

:gist - instead of checking stackoverflow check gist - (DO LOADS OF THESE?)


if popular write same plugin for other tools??? who knows.


