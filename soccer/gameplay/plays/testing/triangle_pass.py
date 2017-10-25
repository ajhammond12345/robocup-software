import robocup
import play
import behavior
import skills.move
import skills.capture
import tactics.coordinated_pass
import constants
import main
import enum
import role_assignment

# Goals
# 1. Move robots into the shape of a triangle
# 2. Pass around the triangle

## A demo play written during a teaching session to demonstrate play-writing
# Three robots form a triangle on the field and pass the ball A->B->C->A and so on.
class TrianglePass(play.Play):
    class State(enum.Enum):
        ## 2 robots get on the corners of a triangle,
        # while a third fetches the ball
        setup = 1

        ## The robots continually pass to each other
        passing = 2

    def __init__(self):
        super().__init__(continuous=True)

        # register states - they're both substates of "running"
        # Feel free to modify these transitions if you would like to use the state
        
        # machine system to your advantage!
        self.add_state(TrianglePass.State.setup,
                       behavior.Behavior.State.running)
        self.add_state(TrianglePass.State.passing,
                       behavior.Behavior.State.running)

        self.add_transition(behavior.Behavior.State.start,
                            TrianglePass.State.setup, lambda: True,
                            'immediately')
        self.add_transition(TrianglePass.State.setup,
                            TrianglePass.State.passing,
                            lambda: self.all_subbehaviors_completed(),
                            'all subbehaviors completed')

        # This play runs forever, so it dosen't need a transition out of 'passing'

        # Define any member variables you need here:
        # Eg:
        self.triangle_points = [robocup.Point(-1.0, 2.0), robocup.Point(1.0, 2.0), robocup.Point(0.0, 3.0)]
        self.point_to_pass = 0

    def on_enter_setup(self):
        # Add subbehaviors to place robots in a triangle
        #
        # Send two robots to corners of triangle, and one to 'capture' the ball
        p1 = self.add_subbehavior(skills.move.Move(self.triangle_points[0]), 'move1')
        p2 = self.add_subbehavior(skills.move.Move(self.triangle_points[1]), 'move2')
        #c1 =self.add_subbehavior(skills.capture.Capture(), 'capture')
        pass

    def on_exit_setup(self):
        # Remove all subbehaviors, so we can add new ones for passing
        self.remove_all_subbehaviors()

    def execute_passing(self):
        # Remember this function is getting called continuously, so we don't want to add subbehaviors
        # if they are already present

        shouldAdd = 0
        # <Check to see if subbehaviors are done, if they are, remove them, so we can kick again>

        # Don't add subbehaviors if we have added them in the previous loop
        if not self.has_subbehaviors():
            # Add a subbehavior to pass the ball to another robot!
            if shouldAdd == 0:
                self.add_subbehavior(tactics.coordinated_pass.CoordinatedPass(self.triangle_points[self.point_to_pass]), 'pass')
                self.point_to_pass += 1
                if self.point_to_pass == 3:
                    self.point_to_pass = 0
                shouldAdd = 1
            pass
        else:
            if self.all_subbehaviors()[0].is_done_running():
                self.remove_all_subbehaviors()
                shouldAdd = 0
            

    def on_exit_passing(self):
        # clean up!
        self.remove_all_subbehaviors()

    def role_requirements(self):
        reqs = super().role_requirements()
        print(reqs)
        for req in role_assignment.iterate_role_requirements_tree_leaves(reqs):
            req.robot_change_cost = 1.0
        return reqs

