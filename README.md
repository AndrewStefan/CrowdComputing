# CrowdComputing

## Abstract
The ever-growing popularity of discussion, criticism, and praise regarding artificial intelligence (AI) in modern media can influence the public's opinion about what AI can do or even about what it is to begin with. In an attempt to shed some light on the matter, a survey was conducted, polling for opinions about AI in European countries which heavily invest into research in this domain. The survey targeted people's perception about the capabilities and complexity of systems which involve some form of artificial intelligence. The systems included are ones that are more or less used in everyday life, and the aim is to find if these people know these systems as well as they think they do. The results, though too few to be considered statistically significant, show that people generally consider systems containing AI to be more intelligent compared to ones that do not. Systems without AI are also perceived as better at their specific tasks than humans, while ones containing AI can make mistakes and seem random at times. In terms of complexity, the results somewhat aligned with the expected answers, with the exception of search engines (rated rather low), which suggests that frequent use might condition people to believe the system is less complex.

## Code Overview

### Template Builder ([toloka_template_builder.json](toloka_template_builder.json))
The survey was deployed on the [Toloka](https://toloka.ai/tolokers/) platform, which includes a template builder functionality for ease of developing the tasks for crowdsourcing. The json file [toloka_template_builder.json](toloka_template_builder.json) represents the template used for our survey.

### Annotations ([annotator.py](annotator.py))
This script was used to annotate the responses obtained for the open question of our survey (*i.e. "What do you consider to fall into the domain of Artificial Intelligence? One or two short sentences should suffice."*). In particular, three members of our group annotated the responses as *Non-informative*, *Neutral*, and *Informative*, using the following guidelines:
- **Non-informative (0)**: Responses that are irrelevant to the question, or contain no information related to AI (*e.g.* "I don't know", "Systems I use")
- **Neutral (1)**: Responses that are relevant to the question, but didn't showcase knowledge of the AI domain (*e.g.* "Machines that replace humans", "Computer systems")
- **Informative (2)**: Responses that convey knowledge about what AI is, or what is user for (*e.g.* "Algorithms that learn to perform a task from data", "Face recognition, self-driving cars")
```
$ python annotator.py -h
usage: annotator.py [-h] -f F

options:
  -h, --help          show this help message and exit
  -f F, --filename F  Path to Toloka's file with the responses.
```

### Majority Voting ([majority_voting.py](majority_voting.py))
This script was used to generate the majority voting result of annotations from three annotators for each open question answer and calculate the Fleiss' kappa. For the situation where annotators have distinct answers, the fourth annotator is asked to break the tie. Fleiss' kappa coefficient is a number between 0-1 and the extent of agreement of corresponding Fleiss' kappa coefficient can be found [here](https://pubmed.ncbi.nlm.nih.gov/15883903/).

```
$ python majority_voting.py
usage: majority_voting.py

```

### Statistics ([statistics.py](statistics.py))
This script was used to generate statistics (mean, median, std, count) for the responses in the system-specific and non system-specific questions. The aforementioned statistics are calculated with respect to two different variables:
- The contributors' **familiarity** with the corresponding systems
- The contributors' knowledge of whether these systems fall **into the AI domain**
```
$ python statistics.py -h
usage: statistics.py [-h] --filename FILENAME --save SAVE [--variable {familiarity,inAIdomain}]
                     [--statistic {mean,median,std,count}]

options:
  -h, --help            show this help message and exit
  --filename FILENAME, -f FILENAME
                        Path to results file in Toloka's format
  --save SAVE, -s SAVE  Path to save the statistics.
  --variable {familiarity,inAIdomain}, -v {familiarity,inAIdomain}
                        Variable to calculate statistics for.
  --statistic {mean,median,std,count}
                        Statistic to calculate.
```

### Complexity ([complexity.py](complexity.py))
This script was used to generate statistics (mean, median, std) for the responses in the final question of the survey about complexity. The aforementioned statistics are again calculated with respect to two different variables:
- The contributors' **familiarity** with the corresponding systems
- The contributors' knowledge of whether these systems fall **into the AI domain**
```
$ python complexity.py -h
usage: complexity.py [-h] --filename FILENAME --save SAVE [--variable {familiarity,inAIdomain}]
                     [--statistic {mean,median,std}]

options:
  -h, --help            show this help message and exit
  --filename FILENAME, -f FILENAME
                        Path to results file in Toloka's format
  --save SAVE, -s SAVE  Path to save the statistics.
  --variable {familiarity,inAIdomain}, -v {familiarity,inAIdomain}
                        Variable to calculate statistics for.
  --statistic {mean,median,std}
                        Statistic to calculate.
```

### Tic-Tac-Toe ([tic-tac-toe](tic-tac-toe))
This directory contains an implementation of a web app for the infamous game Tic-Tac-Toe that we used in our survey. This is based on [Cledersonbc's](https://github.com/Cledersonbc/tic-tac-toe-minimax/) application, but the code is modified to allow for different levels of difficulty. In particular,
there are three levels:
- Level 1: Computer performs random moves
- Level 2: Computer performs optimal moves with a 0.3 chance of performing
		   a random move
- Level 3: Computer performs optimal moves only (unbeatable)

It contains the following files:
- [index.html](tic-tac-toe/index.html): HTHML code for the user interface of the application
- [script.js](tic-tac-toe/script.js): JavaScript file that contains the game logic and an implementation of the MiniMax algorithm.
- [style.css](tic-tac-toe/style.css): Cascading Style Sheet for the user interface of the application

In order to interact with the system, you only need to open the [index.html](tic-tac-toe/index.html) file using your favorite browser.
