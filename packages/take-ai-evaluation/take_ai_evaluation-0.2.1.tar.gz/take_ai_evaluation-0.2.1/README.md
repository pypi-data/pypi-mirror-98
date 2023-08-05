# TakeAiEvaluation 

TakeAiEvaluation is a tool to _provide metrics and visualizations for evaluating a chatbot's AI utilization._
This currently addresses two types of evaluation: Knowledge Base Quality and Message Base Information.


## Installation

The `take_ai_evaluation` package can be installed from PyPI:
```bash
pip install take_ai_evaluation
```

## Usage

As input, either a `pandas.DataFrame` or a `CSV` file path can be used.

1. Matrix all vs all
```python
import matplotlib.pyplot as plt
from take_ai_evaluation import AiEvaluation

ai_evaluation = AiEvaluation(analysed_base='knowledge-base.csv', 
                             sentence_col='id', 
                             intent_col='intent', 
                             predict_col='predicted')

ai_evaluation.get_all_vs_all_confusion_matrix(title='All vs All')

plt.show()
```

2. Matrix one vs all
```python
import matplotlib.pyplot as plt
from take_ai_evaluation import AiEvaluation

ai_evaluation = AiEvaluation(analysed_base='knowledge-base.csv', 
                             sentence_col='id', 
                             intent_col='intent', 
                             predict_col='predicted')

ai_evaluation.get_one_vs_all_confusion_matrix(intent='Intent', title='All vs All')

plt.show()
```

3. Best intent
- Just the values for the default metric, which is 'accuracy'
```python
import matplotlib.pyplot as plt
from take_ai_evaluation import AiEvaluation

ai_evaluation = AiEvaluation(analysed_base='knowledge-base.csv', 
                             sentence_col='id', 
                             intent_col='intent', 
                             predict_col='predicted')

ai_evaluation.get_best_intent()

plt.show()
```

- Just the values for 'recall' metric
```python
import matplotlib.pyplot as plt
from take_ai_evaluation import AiEvaluation

ai_evaluation = AiEvaluation(analysed_base='knowledge-base.csv', 
                             sentence_col='id', 
                             intent_col='intent', 
                             predict_col='predicted')

ai_evaluation.get_best_intent(metric='recall')

plt.show()
```

- As graph
```python
import matplotlib.pyplot as plt
from take_ai_evaluation import AiEvaluation

ai_evaluation = AiEvaluation(analysed_base='knowledge-base.csv', 
                             sentence_col='id', 
                             intent_col='intent', 
                             predict_col='predicted')

ai_evaluation.get_best_intent(as_graph=True)

plt.show()
```

4. Worst intent
- Just the values for the default metric, which is 'accuracy'
```python
import matplotlib.pyplot as plt
from take_ai_evaluation import AiEvaluation

ai_evaluation = AiEvaluation(analysed_base='knowledge-base.csv', 
                             sentence_col='id', 
                             intent_col='intent', 
                             predict_col='predicted')

ai_evaluation.get_worst_intent()

plt.show()
```

- Just the values for 'recall' metric
```python
import matplotlib.pyplot as plt
from take_ai_evaluation import AiEvaluation

ai_evaluation = AiEvaluation(analysed_base='knowledge-base.csv', 
                             sentence_col='id', 
                             intent_col='intent', 
                             predict_col='predicted')

ai_evaluation.get_worst_intent(metric='recall')

plt.show()
```

- As graph
```python
import matplotlib.pyplot as plt
from take_ai_evaluation import AiEvaluation

ai_evaluation = AiEvaluation(analysed_base='knowledge-base.csv', 
                             sentence_col='id', 
                             intent_col='intent', 
                             predict_col='predicted')

ai_evaluation.get_worst_intent(as_graph=True)

plt.show()
```

5. Classification Report
```python
from take_ai_evaluation import AiEvaluation

ai_evaluation = AiEvaluation(analysed_base='knowledge-base.csv', 
                             sentence_col='id', 
                             intent_col='intent', 
                             predict_col='predicted')

ai_evaluation.get_classification_report()
```

- As pandas DataFrame
```python
from take_ai_evaluation import AiEvaluation

ai_evaluation = AiEvaluation(analysed_base='knowledge-base.csv', 
                             sentence_col='id', 
                             intent_col='intent', 
                             predict_col='predicted')

ai_evaluation.get_classification_report(as_dataframe=True)
```

## Author
Take Blip Data&Analytics Research (ROps)