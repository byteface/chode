### Chode
TODO - insert image here


## About

Chode is a Sublime Plugin to help you CHeat at cODE. I wrote it in few hours and is a working proof of concept.


So I often write pseudo code / comments when developing or stubbing out an app or piece of functionality as a series of steps. i.e.

```
# create some class

# create some function

# loop through array compare this and that

# split out last item if is bigger than

# add it to the array and dispatch and event

# delete the mongo database
```

etc


I then go about writing the real code, comment at a time. This is also useful when delegating work or showing others how you're thinking of solving a problem. You can stub whole applications quickly.


Most people use Stackoverflow a lot. Even if you think you know the answer, It's useful to check incase there's a newer or better way to do things.


I figured it would be cool if code comments could quickly become code examples. pseudo code + stackoverflow = Chode. It took just a few hours to get a diiiiirty 'my first sublime plugin' working prototype and here it is.



## Usage

Chode runs when you save. IMPORTANT - It only analyses the line your cursor is currently on.

If the line starts with a comment, followed by a 'p', then a colon. ie. (at mo only hashtag works. will add more comments soon)

```
#p:
```

then everything after those characters will get sent to stackoverflow as a query. the top link is selected, then the best answer from that link inserted into your code.


i.e
```
#p: a singleton in python
```

click on that line, press save, would become...

```
#p: a singleton in python
<TOP ANSWER FROM STACK OVERFLOW GETS INSERTED HERE>
```

REMEMBER - To work your cursor must be ON THE LINE YOU WANT TO RUN and then press save.

why not try some of these examples. install plugin, paste these into a document, put cursor on line, press save.

```
#p: css round corners

#p: abstract class java

#p: reverse array in java

#p:reverse array in Java

# NOTICE THIS ONE HAS A PARAMETER - see about them below
#p:compare arrays python :v
```


The code block from teh top post is injected into your code.


## PARAMETERS

```
:v
```
makes it verbose. which means it add the whole post not just the first code block. Without the :v flag we only paste the first code block

try it yourself
```
#p:compare arrays python :v
```
or
```
#p:compare arrays python
```
will get very different results



## EXAMPLE

![alt tag](https://raw.github.com/byteface/chode/master/screenshots/shot1.png)

![alt tag](https://raw.github.com/byteface/chode/master/screenshots/shot2.png)


## Installation
Download this whole folder and put in Sublime Packages folder, on my mac it looks like this...

```
/Users/mike/Library/Application\ Support/Sublime\ Text\ 3/Packages/Chode
```

restart and you're good to go. I will hopefully make it all more proper soon and get into PackageControl




## FUTURE
```
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

a paramter that can return 2nd or 3rd answer?... or way to loop through answers.
```


if popular write same plugin for other tools??? who knows.


