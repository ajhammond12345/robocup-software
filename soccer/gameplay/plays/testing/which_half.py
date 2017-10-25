import robocup
import constants
import play
import enum
import behavior
import main

# Slides and other materials can be found here:
# https://github.com/RoboJackets/robocup-training
#
# Field Documentation can be found here:
# https://robojackets.github.io/robocup-software/struct_field___dimensions.html
#
# Ball Documentation can be found here:
# https://robojackets.github.io/robocup-software/class_ball.html


# Maintains the state of the ball's position by keeping track of which
# half the ball is on and prints on both entering a given state and
# continously during the execution of a given state.
class WhichHalf(play.Play):
    class State(enum.Enum):
        start = 0
        top = 1
        bottom = 2

        # Define your states here.
        # eg: some_state = 0
        # -----------------------
        pass  # remove this once you have put in your states

    def __init__(self):
        super().__init__(continuous=True)

        self.add_state(WhichHalf.State.top,
            behavior.Behavior.State.running)
        self.add_state(WhichHalf.State.bottom,
            behavior.Behavior.State.running)

        self.add_transition(behavior.Behavior.State.start, 
            self.State.bottom,
            lambda: True,
            'immediately')
        self.add_transition(self.State.bottom, 
            self.State.top,
            lambda: main.ball().pos.y > constants.Field.Length / 2,
            'Ball went to top')
        self.add_transition(self.State.top, 
            self.State.bottom,
            lambda: main.ball().pos.y < constants.Field.Length / 2,
            'Ball went to bottom')


    def on_enter_top(self):
        print("Entering Top")
    def on_enter_bottom(self):
        print("Entering Bottom")

    def execute_top(self):
        print("Ball Y cor: ", main.ball().pos.y)
        # Register the states you defined using 'add_state'.
        # eg: self.add_state(WhichHalf.State.<???>,
        #                    behavior.Behavior.State.running)
        # ----------------------------------------------------

        # Add your state transitions using 'add_transition'.
        # eg: self.add_transition(behavior.Behavior.State.start,
        #                         self.State.<???>, lambda: True,
        #                         'immediately')
        # eg: self.add_transition(self.State.<???>, self.State.<???>,
        #                         lambda: <???>,
        #                         'state change message')
        # ------------------------------------------------------------

        # Define your own 'on_enter' and 'execute' functions here.
        # eg: def on_enter_<???>(self):
        #         print('Something?')
        # eg: def execute_<???>(self):
        #         print('Something?')
        # ---------------------------------------------------------
