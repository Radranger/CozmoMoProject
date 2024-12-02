import cozmo
import asyncio
import time
from cozmo.util import degrees, distance_mm


# FROM PLAY SONG:
def cozmo_sing(robot: cozmo.robot.Robot):

    notes = [
        cozmo.song.SongNote(cozmo.song.NoteTypes.C2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.G2, cozmo.song.NoteDurations.Half),
        cozmo.song.SongNote(cozmo.song.NoteTypes.G2, cozmo.song.NoteDurations.Half),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C3, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.D2, cozmo.song.NoteDurations.Half),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C2, cozmo.song.NoteDurations.ThreeQuarter)
    ]

    # Play the ascending notes
    robot.play_song(notes, loop_count=1).wait_for_completed()


# OUR CODE Comments with SDK references below found at:
# https://data.bit-bots.de/cozmo_sdk_doc/cozmosdk.anki.com/docs/generated/cozmo.robot.html

# Step 1: Make Cozmo angry when seeing cube.
#   Once a cube is spotted by Cozmo:
#    class cozmo.objects.EvtObjectAppeared(**kwargs)
#   Look around in place and find human face:
#    class cozmo.behavior.BehaviorTypes
#    FindFaces= _BehaviorType(name='FindFaces', id=1)


def make_cozmo_angry(robot: cozmo.robot.Robot):

    robot.say_text("Mmo").wait_for_completed()
    try:
        # Step 1: Spot cube
        lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        cube = robot.world.wait_until_observe_num_objects(num=2, object_type=cozmo.objects.LightCube, timeout=10)
        lookaround.stop()
        
        if len(cube) == 2:
            robot.play_anim_trigger(cozmo.anim.Triggers.DriveStartAngry).wait_for_completed()
            robot.play_anim_trigger(cozmo.anim.Triggers.DriveLoopAngry).wait_for_completed()

            # Step 2: Look for a human face
            robot.say_text("Whoa whoa whoa whoa").wait_for_completed()

            #robot.move_lift(-3)
            robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
            face = None
            
            while True:
                if face and face.is_visible:
                    robot.set_all_backpack_lights(cozmo.lights.red_light)
                    break
                else:
                    robot.set_backpack_lights_off()

                    # Wait until we we can see another face
                    try:
                        face = robot.world.wait_for_observed_face(timeout=30)
                    except asyncio.TimeoutError:
                        print("Didn't find a face.")
                        return

                time.sleep(.1)
            
            if face:
                robot.say_text("You!").wait_for_completed()
                
            pick_up_cube(robot, cube)
            robot.play_anim_trigger(cozmo.anim.Triggers.DriveEndAngry).wait_for_completed()


        else:
            cozmo_sing(robot)
    
    except cozmo.exceptions.RobotBusy:
        print("Cozmo is busy, retrying...")

#Step 2: Make Cozmo stack cube.
def pick_up_cube(robot: cozmo.robot.Robot, cube):
    
    if len(cube) < 2:
        print("Error: need 2 Cubes but only found", len(cube), "Cube(s)")
    else:
        # Try and pickup the 1st cube
        current_action = robot.pickup_object(cube[0], num_retries=3, in_parallel = True)
        current_action.wait_for_completed()
        if current_action.has_failed:
            code, reason = current_action.failure_reason
            result = current_action.result
            print("Pickup Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
            return

        # Now try to place that cube on the 2nd one
        current_action = robot.place_on_object(cube[1], num_retries=3)
        current_action.wait_for_completed()
        if current_action.has_failed:
            code, reason = current_action.failure_reason
            result = current_action.result
            print("Place On Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
            return

        print("Cozmo successfully stacked 2 blocks!")



def detect_face(robot: cozmo.robot.Robot):
    robot.move_lift(-3)
    robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()

    face = None
     
    while True:
        if face and face.is_visible:
            robot.set_all_backpack_lights(cozmo.lights.blue_light)
        else:
            robot.set_backpack_lights_off()

            # Wait until we we can see another face
            try:
                face = robot.world.wait_for_observed_face(timeout=30)
            except asyncio.TimeoutError:
                print("Didn't find a face.")
                return

        time.sleep(.1)

#cozmo.run_program(follow_faces)

cozmo.run_program(make_cozmo_angry)