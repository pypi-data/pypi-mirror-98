import random

from .command import Command
from .argument import Argument


class CommandWithArgs(Command):

    def __init__(self, parent, task_manager):
        super(CommandWithArgs, self).__init__(parent, task_manager)
        self.user_config_tag = 'other'
        self.complete = False
        self.children = []

    def forward(self, text, context):
        user_expertise = context['user_config']['commands']
        user_expertise[self.user_config_tag] += .01
        # normalize other commands user preferences
        for key, value in user_expertise.items():
            user_expertise[key] = value / 1.01

        for child in self.children:
            if not child.complete:
                return child.forward(text, context)

        # wrong_params = self.verify_params(context)
        # while len(wrong_params)>0:
        #     error = wrong_params[0]
        #     return error.node, error.tag, error.message

        self.complete = True

        # self.run(context)
        self.task_manager.add_task({
            'fn': self.run,
            'args': {
                'context': context,
            }
        })

        response = random.choice(self.responses)
        return self.parent.backward(self.tag, response, context)

    def backward(self, tag, text, context):
        return self.forward(text, context)

    def add_argument(self, arg):
        self.children.append(arg)

    def create_argument(self, name, trigger):
        setattr(self, name, Argument({
            'parent': self,
            'name': name,
            'trigger': trigger,
            'position': 1
        }))
        self.add_argument(getattr(self,name))

