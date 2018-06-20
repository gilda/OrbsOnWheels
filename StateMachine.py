# just interface class for all states to inherit from
class State:
    def __init__(self, *args):
        pass
    def run(self, *args):
        pass
    def next(self, *args):
        pass
        
# class for controlling the eventflow of States
class StateMachine:
    def __init__(self, init, initInp):
        # initialize the first state
        self.currState = init
        
        # run the first state for setup
        self.currState.run(initInp)
        
    
    def runAll(self, inputs):
        # loop over all inputs
        for i in inputs:
            # calc next state using some input
            self.currState = self.currState.next(i)
            # run next step and keep looping
            self.currState.run()
