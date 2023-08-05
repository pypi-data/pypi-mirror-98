from statemachine import StateMachine, State

from pkg_trainmote.actions.actionInterface import ActionInterface
from .models.Program import Program
from .models.Action import Action
from typing import Optional

class ProgramMachine(StateMachine):

    __program: Program
    __action_index: int = 0
    __actionInterface: Optional[ActionInterface] = None

    def start(self, program: Program):
        if self.is_readyForAction:
            self.__program = program
            self.startProgram()

    readyForAction = State('readyForAction', initial=True)
    runningAction = State('RunningAction')
    actionFinished = State('ActionFinished')
    preparingAction = State('preparingAction')

    startProgram = readyForAction.to(preparingAction)
    cancelProgram = runningAction.to(readyForAction)
    endAction = runningAction.to(actionFinished)
    prepareForAction = actionFinished.to(preparingAction)
    startAction = preparingAction.to(runningAction)
    endProgram = preparingAction.to(readyForAction)

    def on_startProgram(self):
        print('startProgram')

    def on_startAction(self):
        print('startAction')
        
        def actionCallback():
            print("action finished")
            self.endAction()
        self.__actionInterface.runAction(actionCallback)

    def on_cancelProgram(self):
        print('startAction')

    def on_endAction(self):
        print('startAction')

    def on_prepareForAction(self):
        print('on_prepareForAction')
        if self.__action_index < len(self.__program.actions):
            action = self.__program.actions[self.__action_index]
            self.__actionInterface = action.getProgramAction()
            if self.__actionInterface is not None:
                self.startAction()
                return
        self.endProgram()
