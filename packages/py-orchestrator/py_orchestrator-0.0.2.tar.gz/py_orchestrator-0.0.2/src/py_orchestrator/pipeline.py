from py_orchestrator.stage import Stage


class Pipeline:
    def __init__(self, name, configs):
        self.name = name
        self.stages = []
        self.configs = configs

    def add_stage(self, stage: Stage.__class__):
        self.stages.append(stage(self.configs))

    def run(self):
        state = None
        for stage in self.stages:
            state = stage.perform(state)

        return state
