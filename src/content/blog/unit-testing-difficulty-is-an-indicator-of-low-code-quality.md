---
title: "Unit Testing Difficulty is an Indicator of (Low) Code Quality"
published: true
published_at: "2024-08-26T23:01:24"
description: "When I first read about unit testing, I’ll admit, it sounded like one of those things that only seasoned developers would bother with. It seemed like a maze ..."
tags: ["Architecture", "Python", "Testing"]
---

When I first read about unit testing, I’ll admit, it sounded like one of those things that only seasoned developers would bother with. It seemed like a maze of confusing terms and intimidating processes that only experts could navigate.  I didn’t write my first test for over a year after I started my coding journey. Until then, my version of testing was typing `python my\_project.py` in the terminal. Or, I will sheepishly admit, just hitting the “Run” button in VS Code (and Replit before that). Then waiting for it to crash and debugging from there. It was my version of compiled languages developers who claim that if the code compiles, it must be free of errors.

*(As an aside, I had to take a C++ course in college. Or rather, I had to take a BASIC course in college and somehow wound up in an intro C++ class instead. The final for the class was a kind of employee scheduler application, and mine had an error that whoever was named in the third row always showed a schedule start time of 9:15am on Tuesdays, regardless of what data was entered. Never did figure out why, and the professor didn’t really care enough to try to help. But the code compiled just fine… eventually.)*

When I finally started to delve into the world of unit testing, the first thing I discovered was that it wasn't *tedious* so much as it was *hard*. Like, really hard. My tests were failing left and right and the reason wasn't always very clear.

It turns out it was because I just wasn't writing very good code. When I started writing better code, I my tests were easier to write, and more likely to pass on the first try.

What I'm trying to say here is that unit testing should not be difficult, past the first couple days of learning to write them. So, when it is, that’s a red flag indicating something might be wrong under the hood. If you find yourself struggling to write tests, or if those tests are constantly failing for reasons that are difficult to diagnose, it’s likely not the tests that are the issue. Instead, it’s a sign that your code might be too complex, poorly structured, or trying to do too much at once. Recognizing this early on can save you a lot of headaches down the road and lead to better, more maintainable code.

At its simplest, unit testing involves isolating a specific section of code—typically a method or function—and verifying that it works as intended. In Python, this often means using a testing framework like `pytest` to write test cases that call these methods with various inputs and then check the outputs against expected results. Each test should focus on one small part of the code, making it easier to identify problems and understand where things are going wrong.

However, simplicity can be deceptive. If your code is not well-structured, even the smallest units can become difficult to test. For example, if a method is doing too much—handling multiple responsibilities, interacting with external systems, or depending on too many other parts of the code—writing a unit test for it can become an exercise in frustration. The tests might become overly complex, requiring intricate setups or mocking of dependencies, and when they fail, the failure messages might not clearly indicate what went wrong. This complexity is not just a testing problem; it’s a sign that the code itself needs to be reevaluated.

Easy unit testing requires on good code design. The easier it is to test a piece of code, the more likely it is that the code is well-designed, modular, and focused. When tests are difficult to write, it’s usually a symptom of code that needs to be broken down into smaller, more manageable pieces. By using testing difficulty as a guide, you can identify areas of your code that need improvement and take steps to refactor them into more testable and more maintainable components.

Over the next couple days, I will be posting a series aimed at demystifying unit testing by showing how test difficulty can be used as a valuable metric for code quality. By the end, you’ll see how simplifying your code not only makes it easier to test but also results in a more robust and maintainable codebase.

Next I’m going to introduce you to a class that I had ChatGPT create – it was surprisingly hard to get it to generate purposely bad code, considering how easily it does it accidentally. This class `DocumentHandler` is intentionally a mess, designed specifically to demonstrate common code smells and violations of SOLID principles and show how its initial complexity makes testing difficult. From there, I’ll add some tests, some that pass and some that fail, and explain why they failing tests are failing any how it could have been simple to write that failing test when you weren’t trying.

In the following post, I will walk you through refactoring the class to make it cleaner, more modular, and overall better. And then show how the tests just get easier to write on their own.
