---
title: "How to become a programmer with dyslexia"
published: true
published_at: "2024-06-13T21:57:29"
description: "I was first diagnosed with dyslexia in my mid-thirties. I have what would be considered \"stealth\" or \"mild\" dyslexia which is how I managed to not realize it..."
tags: ["Accessibility", "Career", "Python"]
---

I was first diagnosed with dyslexia in my mid-thirties. I have what would be considered "stealth" or "mild" dyslexia which is how I managed to not realize it for three decades.

What is dyslexia like? It's a little different for everyone, and there are different types. In fact, nobody can quite agree what the different types are. Some researchers will classify dyslexia by deficit, while others by brain activity. Confusing isn't it?

For me, it's a little like this:


![distorted text that reads "Examples of distorted text"](/images/l_distortedtext02.jpg)

Swirled text example from http://www.defeat-dyslexia.com/2016/03/6-types-of-dyslexic-visual-distortion/

This is a gross over-exaggeration of what it feels like, but when I first start to focus on text, and also when I focus on it for too long, it starts to go a bit wavy on me.


![doubled text that reads "Examples of distortion"](/images/l_distortedtext01.jpg)

Doubled text example from <http://www.defeat-dyslexia.com/2016/03/6-types-of-dyslexic-visual-distortion/>

I don't experience doubled text that much, except in cases of very high contrast, such as pure black on pure white or vice versa (more on that later). And again, I also don't have it anywhere quite as bad as this example shows.

So what does a girl with dyslexia like to do for fun?  
She writes books and programs, of course!

Luckily there are several things you can do as a programmer to make your setup more dyslexia friendly.

Dyslexia-friendly text
----------------------

Since dyslexia is a disability related to reading text, it makes sense to start with talking about how to make text dyslexia friendly.

### Fonts:

#### OpenDyslexia

Since I first discovered it on the Kindle, I've been a big fan of OpenDyslexic. It is an open source font that uses distinct shapes for each letter with a focus on increasing the "gravity" of the letter (useful for those who experience rotation or swirling).


![screenshot of OpenDyslexic About page. Text reads: "OpenDyslexic is a new open sourced font created to increase readability for readers with dyslexia. The typeface includes regular, bold, italic, and bold-italic styles, and 2 typefaces: OpenDyslexic, and OpenDyslexic-Alta. It was created to help with my reading, and is being updated continually and improved based on input from other dyslexic users. There are no restrictions on using OpenDyslexic."](/images/Screenshot-2024-06-13-104710.png)

screenshot from OpenDyslexic "About" page

They also have a monospace font that you can then use in VSCode. You can find instructions for setting that up here: <https://dev.to/deadlybyte/have-dyslexia-make-coding-easier-in-visual-studio-code-4kmg>

#### Other fonts for coding with dyslexia

Not everyone is a fan of OpenDyslexic, or the proprietary alternative Dyslexie (its a little nicer looking but no monospace version).

The British Dyslexia Association recommends fonts that designers would call "clean and simple" or "readable." Their highest recommendations go to Arial and Comic Sans. Yes, Comic Sans.

*Fun fact: Reading about the hate that surrounds Comic Sans, and the counter-argument that it is considered dyslexic-friendly is the thing that started me down the rabbit hole of seeking a diagnosis.*

Other fonts that make their list are Verdana, Tahoma, Century Gothic, Trebuchet, Calibri, Open Sans.

Of course, none of those fonts are monospace, are they? Well, technically, you don't have to use a monospace font in your IDE. But if you really want to use a monospace font, most of these have alternatives:

* Arial -> Arial Monospaced
* Verdana/Tahoma (very similar fonts with Tahoma having tighter letter spacing - more on that later) -> Andale Mono
* Trebuchet -> N/A
* Calibri -> Consolas (the default in VSCode)
* Open Sans -> Noto Sans

### Text size:

The British Dyslexia Association recommends size 12-14 font. Personally, I prefer size 16. The next couple sections will have a recurring theme of "give your characters room to breathe on the screen." The more space they have, within reason, the easier they are to read. Larger font size is going to have more weight while also having more space between the "ink", which is where bold text can suffer. Bold can cause the letters to bleed together because it upsets the text to space ratio.

Speaking of…

### Letter spacing for dyslexia:

You want more space between the letters inside the words. The technical word for this is *kerning*. Monospace fonts have the same kerning between each letter, proportional fonts have kerning that can vary from letter to letter. But in most text editors, and VSCode is no exception, you can add additional space that occurs between each character.

This is one of of the reasons I like OpenDyslexic, because it has a wider kerning than most fonts. I don't need to add any additional letter spacing in the editor, but for the terminal, which is more text heavy, I find having an extra pixel of spacing helps.


![Screenshot of letter spacing setting in VSCode](/images/Screenshot-2024-06-12-214327.png)

You don't want to go too far, or else the words starts to lose their cohesion. Ideal letter spacing is 35% of the letter width. That said, monospace fonts don't really advertise their width or even their height-width ratio, so it's kind of hard to actually calculate that. Adjust it until it feels right.

### Line height:

Ideal line height is 1.5x the font size. That one is pretty easy. Just like letter spacing, you want to have enough space to make individual letters easy to differentiate, but not so much that tracking becomes difficult.

Tracking is eye movement while reading, and specifically moving from one line to the next. When lines are too far apart, they become difficult to keep track of your place.

In settings, just search for line height (two words). A number between 0-8 is going to be a ratio of the font size. A number greater than 8 is considered a pixel value if you want to set it manually.


![Screenshot of line height setting in VSCode](/images/Screenshot-2024-06-12-214554.png)

That's pretty much it about the actual qualities of the font. Next, let's talk about colors

Colors and VSCode Themes for dyslexia
-------------------------------------

### Contrast:

Just like with the font, there is a balance in the contrast between the text color and background color. More is better, but only up to a point. The British Dyslexia Association recommends black text on a fixed, off-white background.

When the text/background is pure black & white, hex 000/FFF, that's when I'm most likely to experience doubling. When I set the theme I was using when I took the screenshots in this post, I hadn't realized that the settings page was white text on black background. It gave me a headache trying to focus on the text.

Most resources will recommend dark text on light background, because it turns out that most dyslexics' eyes have a harder time detecting differences in contrast at lower light levels. But programmers love our dark themes, right? When using a dark theme, look for a theme marked as being higher contrast. We need more contrast in dark mode than we need in light mode.

### Semantic highlighting:

Modern IDE utilize what is known as "semantic highlighting of tokens." What this means is that different *things* in a programming language will look different, to make it easy to differentiate at a glance a variable vs a function vs a keyword, etc. This reduces the cognitive load of reading code. This is good for everyone. It's great for dyslexics.

Some VSCode themes do a better job of setting the semantic highlighting than others. My continued frustration is that dark themes that are particularly good at semantic highlighting tend to be bad at contrast.


![screenshot of Python class using Microsoft's Dark Modern theme for VSCode](/images/DarkModern.png)

Dark Modern by Microsoft: great semantic highlighting, mediocre contrast

![screenshot of Python class using Frantic Contrast theme from Rainglow in VSCode](/images/FranticContrast.png)

Frantic Contrast by Rainglow: good contrast, mediocre semantic highlighting

If you know of a high contrast dark theme that utilizes semantic highlighting to its full extent, please let me know!

Tooling and workflows to help write code with dyslexia
------------------------------------------------------

No matter how much you try to minimize how much dyslexia affects your ability to read the code on your screen, it always will. Affect it, that is. So let's move on to supports to help you overcome the obstacles.

#### Spell check

How did we live before spellcheck? My spelling ability in, I'll say medium, but when typing, it becomes remedial, at best. Fortunately, there's a spell checking extension for VSCode called Code Spell Checker by Side Street Software. It works just like regular spellcheck, except that it doesn't get caught up by snake\_case or camelCase

#### Linters & Formatters

Linters are the grammar check of code syntax, in my mind. For Python, I use Isort, Ruff, Flake8, and MyPy. If you use a different language, check out what tools are available for you.

#### Pre-commit

Pre-commit is a really nifty tool that I recently discovered. It's a python library that runs pre-commit hooks that have been configured in a yaml file whenever you commit a file to your git repo. The hooks, and YAML especially, can be a little complex to set up, but there are dozens of repos with example files. Some hooks that can be set up are checks for valid TOML, YAML, or JSON files, checks that .env or other files aren't being uploaded, and running linters and formatters. So before my code is uploaded to GitHub, all of the syntax errors and typos have been caught.

#### GitHub Actions

I haven't explored this space much yet, but you can think of GitHub Actions as kind of "post-commit." Any pre-commit hook you can run before commit can also be run as a GitHub Action, plus some other things. Have an existing codebase that you want to make sure you don't mess up with your new code? You can create a GitHub Action to run regression tests when you commit. You can push new versions to PyPi or wherever. Once this stuff is set up, you don't have to worry about typos getting in your way of doing it any more.

#### Cursorless

I'll be honest. I don't use this one myself. I'm just not a fan of voice controls. But Cursorless lets you use dictation and voice editing in the IDE. Less to read this way.

*What are some of the ways you've found to help program with dyslexia or other other disabilities?*
