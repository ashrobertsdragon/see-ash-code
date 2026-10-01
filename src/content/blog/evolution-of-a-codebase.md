---
title: "Evolution of a codebase"
published: true
published_at: "2024-07-15T04:27:52"
description: "When I wrote the first version of Lorebinders, I hadn't yet started exploring object oriented programming. v1 has comprised by a series of functions strung i..."
tags: ["Architecture"]
---

When I wrote the first version of Lorebinders, I hadn't yet started exploring object oriented programming. v1 has comprised by a series of functions strung in a row, one, calling the next.

Unfortunately (or maybe fortunately!), that code was gone before I discovered version control. It is gone for ever.

For the first refactoring, I organized it a little better, but still depended sole on functions like these:

```
def search_names(chapters: list, folder_name: str, num_chapters: int, character_lists: list, character_lists_index: int) -> list:

  character_lists_path = os.path.join(folder_name, "character_lists.json")
  role_script = ner_role_script(folder_name)
  model = "gpt_three"
  max_tokens = 1000
  temperature = 0.2

  with tqdm(total = num_chapters, unit = "Chapter", ncols = 40, bar_format = "|{l_bar}{bar}|", position = 0, leave = True) as progress_bar:
    for chapter_index, chapter in enumerate(chapters):
      progress_bar.set_description(f"\033[92mProcessing chapter {chapter_index + 1} of {num_chapters}", refresh = True)
      if chapter_index < character_lists_index:
        progress_bar.update(1)
        continue
      chapter_number = chapter_index + 1
      prompt = f"Text: {chapter}"
      character_list = cf.call_gpt_api(model, prompt, role_script, temperature, max_tokens)
      chapter_tuple = (chapter_number, character_list)
      character_lists.append(chapter_tuple)
      cf.append_json_file(chapter_tuple, character_lists_path)
      progress_bar.update(1)
  cf.clear_screen()
  return character_lists
```

When I started v2, leaning into object oriented programing principles, I quickly learned that classes don't make dependency and coupling any simpler. I needed to initialize the API class, get the text from the chapter, and save the response to the chapter. It looked easy to organize when each class was was separate.

```
class NameTools(ABC):
    """
    Abstract class for name classes
    """

    def __init__(
        self,
        book: Book,
        chapter: Chapter,
        provider: str,
        ai_models: dict,
        ai_quality: bool = False,
    ) -> None:
        """
        Initialize the NameTools class with a Book object and an instance of
        the
        OpenAIAPI class.
        Args:
            chapter (Chapter): The Chapter object representing the chapter.
        Raises:
            TypeError: If book is not an instance of the Book class.
        """
        self.book = book
        self.chapter = chapter
        self._prompt = f"Text: {self.chapter.text}"

        self._ai_config = AIModelConfig(provider, ai_models, ai_quality)
        self._ai = self._ai_config.initialize_api()

        self._categories_base = ["Characters", "Settings"]
        self._role_scripts: List[RoleScript] = []

    def get_info(self) -> str:
        """
        Iterate over the Chapter objects stored in the Book object, send the
        text as prompts to the AI model, and fetch the response. For use with
        simpler prompts.
        """

        responses = []
        for script in self._role_scripts:
            payload = self._ai.create_payload(script.script, script.max_tokens)
            response = self._ai.call_api(payload)
        if response:
            responses.append(response)
        return "".join(response)

    @abstractmethod
    def parse_response(self, response: str) -> Union[list, dict]:
        """
        Abstract method to parse the AI response.
        Raises:
            NotImplementedError: If the method is not implemented in the child
                class.
        """
        raise NotImplementedError(
            "Method _parse_response must be implemented in child class."
        )

    @abstractmethod
    def build_role_script(self) -> None:
        """
        Abstract method to build the role script
        Raises:
            NotImplementedError: If the method is not implemented in the child
                class.
        """
        raise NotImplementedError(
            "Method _build_role_script must be implemented in child class."
        )
```

```
class Binder:
    """
    Class representing the book analysis binder.
    """

    def __init__(self, book: Book, ai_model: APIProvider) -> None:
        self.book = book
        self.ai_models = ai_model
        self.binder_type = __name__.lower()
        self._book_name: str | None = None
        self._temp_file: str | None = None

    def __str__(self) -> str:
        return f"Binder for {self.book_name} - {self.book.author}"

    @property
    def book_name(self) -> str:
        if self._book_name is None:
            self._book_name = self.book.name
        return self._book_name

    @property
    def metadata(self) -> BookDict:
        return self.book.metadata

    @property
    def binder_tempfile(self) -> str:
        if self._temp_file is None:
            self._temp_file = f"{self.book_name}-{self.binder_type}.json"
        return self._temp_file

    def add_binder(self, binder: dict) -> None:
        if not isinstance(binder, dict):
            raise TypeError("Binder must be a dictionary")
        self._binder = binder
        write_json_file(self._binder, self.binder_tempfile)

    def update_binder(self, binder: dict) -> None:
        if not isinstance(binder, dict):
            raise TypeError("Binder must be a dictionary")
        if self._binder != binder:
            self.add_binder(binder)

    @property
    def binder(self) -> dict:
        return self._binder

    def perform_ner(
        self, ner: NameExtractor, metadata: BookDict, chapter: Chapter
    ) -> None:
        ner.initialize_chapter(metadata, chapter)
        ner.build_role_script()
        names = ner.extract_names()
        chapter.add_names(names)

    def analyze_names(
        self, analyzer: NameAnalyzer, metadata: BookDict, chapter: Chapter
    ) -> None:
        analyzer.initialize_chapter(metadata, chapter)
        analyzer.build_role_script()
        analysis = analyzer.analyze_names()
        chapter.add_analysis(analysis)

    def summarize(self, summarizer: NameSummarizer) -> None:
        summarizer.build_role_script()
        self._binder = summarizer.summarize_names(self._binder)

    def build_binder(self) -> None:
        ner = NameExtractor(self.ai_models)
        analyzer = NameAnalyzer(self.ai_models)
        summarizer = NameSummarizer(self.ai_models)

        for chapter in self.book.chapters:
            self.perform_ner(ner, self.metadata, chapter)
            self.analyze_names(analyzer, self.metadata, chapter)
        self.summarize(summarizer)
```

So now I'm passing the AI configuration information to the Binder class, which is then passing it to each of the NameTools sub classes, which will be using a different model. And then the NameTools classes were calling the AIModelConfig class, which was then initializing an instance of the correct API class.

THAT'S PASSING THE APIProvider FOUR TIMES!


![](/images/holy-coupling.jpg)

Where I'm at now, NameTools is no longer an abstract class, but a mixin that gives the other name classes access to the AIModelConfig, and the Binder class is gone split up between the build module and the Book class.

```
class NameTools:
    """
    Mixin class for providing interface for AI to Name classes.
    """

    def __init__(
        self,
        provider: APIProvider,
        family: str,
        model_id: int,
        rate_limiter: RateLimitManager,
    ) -> None:
        self.initialize_api(provider, rate_limiter)
        self.set_family(family)
        self.set_model(model_id)

        self._categories_base: list[str] = ["Characters", "Settings"]
        self.temperature: float = 0.7
        self.json_mode: bool = False

    def initialize_api(
        self, provider: APIProvider, rate_limiter: RateLimitManager
    ) -> None:
        """
        Initialize the AI API with the provided schema.

        Args:
            provider (APIProvider): A dataclass of the AI API information.
            rate_limiter (RateLimitManager): An implementation of the
            abstract rate limiter.
        """

        self._ai_config = AIModelConfig(provider)
        self._ai = self._ai_config.initialize_api(rate_limiter)

    def set_family(self, family: str) -> None:
        """
        Set the model family for the AI implementation.
        """
        self._ai.set_family(family)

    def set_model(self, model_id: int) -> None:
        """
        Retrieve model dictionary from configuration and pass it to the AI.
        """
        self._ai.set_model(self._ai_config, model_id)

    def get_model(self, family: str, model_id: int) -> Model:
        """
        Retrieve the Model object for the given family and model_id.
        """
        ai_family = self._ai.api_provider.get_ai_family(family)
        return ai_family.get_model_by_id(model_id)

    def _get_instruction_text(
        self, file_name: str, *, prompt_type: str | None = None
    ) -> str:
        if prompt_type is not None:
            os.path.join("instructions", prompt_type, file_name)
        else:
            file_path = os.path.join("instructions", file_name)
        return file_handling.read_text_file(file_path)

    def _get_ai_response(self, role_script: RoleScript, prompt: str) -> str:
        """
        Create the payload to send to the AI and send it.
        """
        payload = self._ai.create_payload(
            prompt,
            role_script.script,
            self.temperature,
            role_script.max_tokens,
        )
        return self._ai.call_api(payload, self.json_mode)
```

There's still too much coupling. The next step is to initialize the API class in the build module and pass it to the Name class.

```
def initialize_ai(
    provider: APIProvider, family: str, model_id: int, rate_limiter
) -> AIInterface:
    ai_config = AIModelConfig(provider)
    ai = ai_config.initialize_api(rate_limiter)
    ai.set_family(ai_config, family)
    ai.set_model(model_id)
    return ai


def initializer_ner(
    provider: APIProvider, rate_limiter: RateLimitManager
) -> NameExtractor:
    ai = initialize_ai(
        provider=provider,
        family="openai",
        model_id=1,
        rate_limiter=rate_limiter,
    )
    return NameExtractor(ai)


def initializer_analyzer(
    provider: APIProvider, rate_limiter: RateLimitManager
) -> NameAnalyzer:
    model_id = 2
    ai = initialize_ai(
        provider=provider,
        family="openai",
        model_id=model_id,
        rate_limiter=rate_limiter,
    )
    model = ai.get_model(model_id)
    absolute_max_tokens = model.absolute_max_tokens
    return NameAnalyzer(
        ai,
        instruction_type="markdown",
        absolute_max_tokens=absolute_max_tokens,
    )


def initializer_summarizer(
    provider: APIProvider, rate_limiter: RateLimitManager
) -> NameSummarizer:
    ai = initialize_ai(
        provider=provider,
        family="openai",
        model_id=1,
        rate_limiter=rate_limiter,
    )
    return NameSummarizer(ai)
```

Of course, the build module is up to 500 lines of functions, so the next step is going to be to split it up into separate modules
