---
title: "Back to the __future__ and import annotations"
published: true
published_at: "2024-06-30T22:56:25"
description: "After last week, I thought I was done with module import errors. Turns out, I had only just started with them."
tags: ["Architecture", "Python", "Testing"]
---

After last week, I thought I was done with module import errors. Turns out, I had only just started with them.

After months of hard work, I have finally written all of the code for my LoreBinders project. Now to see if it works!

So I wrote tests for everything, typed `pytest` into the terminal and hit enter.

```
ImportError while importing test module 'vscode\ProsePal\lorebinders\tests\test_ai_factory.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
 from lorebinders._managers import EmailManager, RateLimitManager
src\lorebinders\_managers.py:4: in 
from _types import AIModelRegistry, APIProvider, Model, ModelFamily
src\lorebinders_types.py:12: in
from _managers import AIProviderManager, EmailManager, ErrorManager
src\lorebinders_managers.py:4: in
from _types import AIModelRegistry, APIProvider, Model, ModelFamily
E ImportError: cannot import name 'AIModelRegistry' from partially initialized module '_types' (most likely due to a circular import)
```

15 times. Different modules, same problem.

Oops!

I created a problem of circular imports by trying to avoid circular imports.

The \_types module exists to be a central repository for all of the abstract classes, Generics, dataclasses, TypedDicts, etc that are being used as a type hint somewhere in my code base. To avoid circular imports, my idea was to import them all into a central file, and then import the ones I need in a given module.

But then I had situations like this one, where \_managers neeeded to import some dataclasses as types from \_types, but \_types was importing abstract classes to be used as types from the \_managers module. And when the Python interpreter went back to \_types, if found itself needing to go back to \_managers, which sent it back to \_types, until it quite and shouted, make up your mind!

if TYPE\_CHECKING to the rescue
-------------------------------

Since the whole issue only happens because be are using type hints for type checkers, the typing module provides a convenient way of sidestepping the problem.

If you import the constant TYPE\_CHECKING from the typing module and add the conditional ``if TYPE_CHECKING:`` static type checkers will evaluate this conditional as True, and run the code inside the conditional block. But the runtime will evaluate as False, and the code inside will not run.  
  
So we've gone from this:

```
from typing import Literal, TypeVar

from openai.types.chat import (
ChatCompletion,
ChatCompletionAssistantMessageParam,
ChatCompletionSystemMessageParam,
ChatCompletionUserMessageParam
)
from openai.types.chat.completion_create_params import ResponseFormat

from lorebinders._managers import (
AIProviderManager,
EmailManager,
ErrorManager,
RateLimitManager
)
from lorebinders.binders import Binder
from lorebinders.book import Book, Chapter
from lorebinders.book_dict import BookDict

T = TypeVar("T", dict, list, str)

FinishReason = Literal[
"stop", "length", "tool_calls", "content_filter", "function_call"
]

__all__ = [
"FinishReason",
"ChatCompletion",
"ChatCompletionAssistantMessageParam",
"ChatCompletionSystemMessageParam",
"ChatCompletionUserMessageParam",
"ResponseFormat",
"BookDict",
"Book",
"Chapter",
"Binder",
"AIProviderManager",
"EmailManager",
"ErrorManager",
"RateLimitManager",
"T",
]
```

to this:

```
from typing import TYPE_CHECKING Literal, TypeVar

from openai.types.chat import (
ChatCompletion,
ChatCompletionAssistantMessageParam,
ChatCompletionSystemMessageParam,
ChatCompletionUserMessageParam
)
from openai.types.chat.completion_create_params import ResponseFormat

if TYPE_CHECKING:
from lorebinders._managers import (
AIProviderManager,
EmailManager,
ErrorManager,
RateLimitManager
)
from lorebinders.binders import Binder
from lorebinders.book import Book, Chapter
from lorebinders.book_dict import BookDict

T = TypeVar("T", dict, list, str)

FinishReason = Literal[
"stop", "length", "tool_calls", "content_filter", "function_call"
]

__all__ = [
"FinishReason",
"ChatCompletion",
"ChatCompletionAssistantMessageParam",
"ChatCompletionSystemMessageParam",
"ChatCompletionUserMessageParam",
"ResponseFormat",
"BookDict",
"Book",
"Chapter",
"Binder",
"AIProviderManager",
"EmailManager",
"ErrorManager",
"RateLimitManager",
"T",
]
```

But we are only halfway there.

Forward references
------------------

Next, I also had to add the TYPE\_CHECKING conditional to the import of \_types in every module that imports from the \_types module.

The only problem is that by doing that, when the application is run, the types aren't imported (which is what we wanted), meaning they aren't defined when referenced in a function signature.

What we need is a forward reference.

A forward reference is when we refence a variable before we define it. Normally, that's a big no-no. Linters hate that. But there are ways of getting around that limitation.

When I enclosed each object in the \_\_all\_\_ list in the \_types module in quotes, I was using a string annotation, which is one way of making a a forward reference.

If I used string annotations for every type hint in every function signature for a type imported from \_types, that would have taken forever.

The \_\_**future**\_\_ is here
------------------------------

Since Python 3.7, we haven't had to resort to string annotations for forward referencing. Instead, we can import annotations from the \_\_future\_\_ module.

When we use a string annotation for a type hint in a function signature, the interpreter ignores it, because it is now a string instead of a variable, and just adds it to the \_\_annotations\_\_ dictionary for type checkers to use. Eventually, the interpreter won't try to interpret a type hint at all and just do it by default. But to avoid breaking a lot of codebases, this is a change that is going to happen slowly over a period of years. Step was was adding the \_\_annotations\_\_ dictionary to the \_\_future\_\_ module.

\_\_future\_\_ is home to features in Python that are optional for now but will be default in the future. Like not interpreting the type hint in a function signature.

So when we import annotations from \_\_future\_\_, Python pretends that there is a string annotation, adds the type hint to the \_\_annotations\_\_ dict, and otherwise ignores it. Without us doing any work beyond typing from 34 characters at the top of a module.

So now, in addition to the \_types module shown above, \_managers has gone from:

```
from abc import ABC, abstractmethod

from _types import (
AIModelRegistry,
APIProvider,
Model,
ModelFamily
)

class AIProviderManager(ABC):
_registry: AIModelRegistry | None = None

@property
def registry(self) -> AIModelRegistry:
if not self._registry:
self._registry = self._load_registry()
return self._registry

@abstractmethod
def _load_registry(self) -> AIModelRegistry:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def get_all_providers(self) -> list[APIProvider]:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def get_provider(self, provider: str) -> APIProvider:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def add_provider(self, provider: APIProvider) -> None:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def delete_provider(self, provider: str) -> None:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def get_model_family(self, provider: str, family: str) -> ModelFamily:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def add_model_family(
self, provider: str, model_family: ModelFamily
) -> None:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def delete_model_family(self, provider: str, family: str) -> None:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def add_model(self, provider: str, family: str, model: Model) -> None:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def replace_model(
self, model: Model, model_id: int, family: str, provider: str
) -> None:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def delete_model(self, provider: str, family: str, model_id: int) -> None:
raise NotImplementedError("Must be implemented by child class")
```

to:

```
from __future__ import annotations

from abc import ABC, abstractmethod

from _types import (
AIModelRegistry,
APIProvider,
Model,
ModelFamily
)

class AIProviderManager(ABC):
_registry: AIModelRegistry | None = None

@property
def registry(self) -> AIModelRegistry:
if not self._registry:
self._registry = self._load_registry()
return self._registry

@abstractmethod
def _load_registry(self) -> AIModelRegistry:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def get_all_providers(self) -> list[APIProvider]:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def get_provider(self, provider: str) -> APIProvider:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def add_provider(self, provider: APIProvider) -> None:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def delete_provider(self, provider: str) -> None:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def get_model_family(self, provider: str, family: str) -> ModelFamily:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def add_model_family(
self, provider: str, model_family: ModelFamily
) -> None:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def delete_model_family(self, provider: str, family: str) -> None:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def add_model(self, provider: str, family: str, model: Model) -> None:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def replace_model(
self, model: Model, model_id: int, family: str, provider: str
) -> None:
raise NotImplementedError("Must be implemented by child class")

@abstractmethod
def delete_model(self, provider: str, family: str, model_id: int) -> None:
raise NotImplementedError("Must be implemented by child class")
```

And now my tests are failing for a different reason!
