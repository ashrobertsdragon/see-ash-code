---
title: "How to fix 'module' could not be resolved from source Python linter errors"
published: true
published_at: "2024-06-17T04:00:51"
description: "Last week, I mentioned that I had [put aside the problem of MyPy not being able to follow my module imports](https://see-ash.codes/know-when-to-quit/) becaus..."
tags: ["Python"]
---

Last week, I mentioned that I had [put aside the problem of MyPy not being able to follow my module imports](https://see-ash.codes/know-when-to-quit/) because it was dragging down my productivity and I couldn't find someone to ask.

I found someone to ask, and it took longer to ask than to get a fix.

If you are having a similar problem where your linter can't resolve module imports here's the fix:

Project root vs package root
----------------------------

When you start a new project in VS Code and start saving files, the directory you are in is your project root. On my Windows laptop, I always put everything in a vscode folder of my user folder, so for my LoreBinders project, the project root is

```
users\ash\vscode\lorebinders\
```

In this directory, I have my configuration files, virtual environment and cache folders, and the files GitHub needs, such as the readme and license files.

There's also a stubs folder, a test folder, and src. Inside the src folder there is a folder called 'lorebinders' where the actual code for the program lives.

This is a pretty common setup, called the '*src layout*.' In fact, some modern linters are even programmed to check a src folder automatically when following imports.

In technical language this is called the path, and is set with the PYTHONPATH variable in VS Code. When you activate a virtual environment that interpreter and the lib directory is added to the path so that Python and all of your IDE tools can detect the installed packages.

The other common layout is known as a *flat layout*.

```
example flat layout  
.  
├── README.md  
├── pyproject.toml  
├── my_package/  
│   ├── __init__.py  
│   └── module.py  
└── tests/  
    └── test_module.py
```

```
example src layout  
.  
├── README.md  
├── pyproject.toml  
├── src/  
│    └── my_package/  
│       ├── __init__.py  
│       └── module.py  
└── tests/  
    └── test_module.py
```

The entire point of having a src layout instead of a flat layout is to create an additional layer of separation between the project root and the package root. The src folder isn't a package. It doesn't have an \_\_init\_\_.py file. So when the interpreter, or linters see it, it gets skipped over as unimportant.

Except that VS Code knows this is happening. There's a setting to include the src folder in your PATH. I have it enabled, but that that didn't do the trick.

I don't know if something is implemented incorrectly somewhere, or what. But what I had to do was add the package root directly as an extra path.

Extra paths
-----------

This is a setting that will need to be set at the workspace level for VS Code, instead of the user level. Why? Because, unless every project you work on is named the same thing, the package folder is going to have a different name.

Go to:

```
Preferences -> Settings
```

Click on Workspace in the top left corner

```
Python -> Analysis -> Extra Paths
```

and click the Add path button.

Then enter:

```
${WorkspaceFolder}/src/my_package
```

Where my\_package is the name of the folder where the code lives. Leave *workspaceFolder* as is. That's a variable, but it's a variable for VS Code to interpret.


![Screenshot of VS Code settings reads:
Python > Anlysis: Extra Paths
Additional import search resolution paths
${workspaceFolder}/src/lorebinders
Yellow button with text "Add item"](https://see-ash.codes/wp-content/uploads/2024/06/Screenshot-2024-06-16-155445.png)

Or alternatively, you can create a .vscode folder in the project root if one doesn't exist already, and a settings.json file in that folder if that doesn't exist already. This is the file where workspace settings are stored. Then add this line:

```
"terminal.integrated.env.windows": {
    "PYTHONPATH": "${workspaceFolder}/src:${workspaceFolder}/src/my_projrct"}
```

Editable install
----------------

Of course, all we have now done is completely bypass the entire point of having a src layout in the first place. Because we have just redefined what Python sees when it looks in the src folder. Basically, The interpreter gets redirected to the project root as if the src folder wasn't there at all. We've basically made a flat layout with extra steps.

### What is the point of a src layout anyway?

By creating a separation between the code and the project root, you ensure that nothing in the project root is accidentally accessible to your codebase. One place this is important is if you have, say, a config file in the project root and then another one in the package root. When you are importing the package config file, you want to make sure you are getting the package config file and not the project config file.

Of course, if you give your files unique file names, you won't have this problem. When I asked different chatbots what other advantages a src layout had over a flat layout, none of the technical answers were very convincing. Every obstacle was easily overcome by observing other best practices, like installing to a clean virtual environment when done will trump installing to the same environment you developed in. Somehow it "promotes better organization" but I'm not buying it.

The only real argument for a src layout that it gave me that was remotely believable was that it was popular and therefore you are going to need to be prepared to be able to work with it at some point.

But if you don't want to turn the src layout into a flat layout, perhaps because you are in someone else's project and they do have multiple files named the same thing, you can do what is called an editable install. Basically, you are installing the package using pip, but with the -e flag to make it "editable" which means that changes you make are immediately reflected in the installation.

So once you have enough code, or at least enough boilerplate to have something to install, all you need is this:

```
pip install -e .
```

The period at the end tells pip to install the current project to the environment it is in, which should be your virtual environment. As an editable install (the -e flag) it won't have an actual presence in the lib folder of your virtual environment, just a link will exist back to your project, essentially adding it to the Python interpreter's path without access to the project root.

Either the editable install or adding an extra path will get your linter to work with a project with src layout. The choice is really up to you.
