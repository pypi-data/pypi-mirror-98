# orchestrator

## Installation
`pip install py-orchestrator`

## Example
```
from py_orchestrator.pipeline import Pipeline
from py_orchestrator.stage import Stage


class ActorOne(Stage):
    def perform(self, state):
        if not state:
            state = 0
        return self.configs['a'] + self.configs['b'] + state


class ActorTwo(Stage):
    def perform(self, state):
        if not state:
            state = 0
        return self.configs['c'] + self.configs['d'] + state


class TestPipeline:
    def test_pipeline(self):
        configs = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        pipeline = Pipeline('test_pipeline', configs)
        pipeline.add_stage(ActorOne)
        pipeline.add_stage(ActorTwo)
        assert pipeline.run() == 10
```
