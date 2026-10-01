---
title: "Know when to quit"
published: true
published_at: "2024-06-11T03:47:59"
description: "*How's that for a first post?*"
tags: ["Python"]
---

*How's that for a first post?*

New developers will often spend too much time trying to figure out a problem they are stuck on, long past the point they should have asked for help. I recently found myself in that position and wasted an entire week.

The worst part? It wasn't even code itself that I was stuck on, but a *tool*.

I started implementing type hints in my code fairly early on, in an endeavor to make it more readable, if to myself if to no one else. But they were just that. I didn't have any tooling in place to take advantage of them. But I've been slowly adding DevOps tooling into my workflow, building out the CI/CD pipelines that will help make me a better developer. DevOps is apparently a controversial topic in the programming world, but I can't imagine why I wouldn't want automated tools that help improve the quality of the code I put out into the world.

One of the tools I've added is MyPy, a static type checker for Python. There are a few different types checkers, but MyPy is the one most developers are talking about when they are talking about static type checking in Python. It's also apparently the strictest at interpreting types. If that's for good or ill, I'll leave up to you.

The first time I ran it, I discovered I hadn't done half as good a job of annotating my code as I'd thought I had. Approximately 75% of the errors fell into the category of "MyPy doesn't infer type like that"

For instance:

/code

```
def func(arg1: str, ar2: Union[list, str] -> None:
    try:
        arg2.append(arg1)
    except TypeError:
        combined = arg1 + arg2
```

This is a classic example of Python's *Easier to Ask for Forgiveness than Permission* (EAFP) style. Try a list method, and if that fails, we know it's a string. But MyPy does **NOT** like that.

So I spent a good while cleaning up my code to make it pass MyPy's checks, while maintaining a Pythonic structure. I like to think it made the code better, for the most part. Although some of it was just plain frustrating to be able to push through it. But I did.

For the most part.

I don't know why, but none of my imports are getting parsed properly by MyPy. I'm getting ridiculous errors such as this:


![](/images/1000004377.png)

How can it not exist if Intellisense is showing me the documentation?

I spent a week trying to figure it out. Reading documentation. Asking ChatGPT. Asking for help. I was stuck.

I still am. It's an unsolved problem. But I gave up. It's an unsolved problem for another time. If Intellisense can see the code, it will run. And I'm going to test it. It just won't pass all of MyPy's checks unless someone else can figure out the problem.
