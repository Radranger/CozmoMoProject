import cozmo
import asyncio
import time
from cozmo.util import degrees, distance_mm
import speech_recognition as sr


# FROM PLAY SONG:
def cozmo_sing(robot: cozmo.robot.Robot):

    notes = [
        cozmo.song.SongNote(cozmo.song.NoteTypes.C2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.D2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.D2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.F2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.F2, cozmo.song.NoteDurations.Half),
        cozmo.song.SongNote(cozmo.song.NoteTypes.E2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.G2, cozmo.song.NoteDurations.ThreeQuarter),
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
        cube = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=10)
        lookaround.stop()
        
        if len(cube) >= 2:
            robot.play_anim_trigger(cozmo.anim.Triggers.DriveStartAngry).wait_for_completed()
            robot.play_anim_trigger(cozmo.anim.Triggers.DriveLoopAngry).wait_for_completed()

            # Step 2: Look for a human face
            robot.say_text("Whoa whoa whoa whoa").wait_for_completed()

            #robot.move_lift(-3)
            robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()

            
            face_to_follow = None  # Start with no face detected
            followCnt = 0
            while True:
                turn_action = None
                if(followCnt == 3):
                    break

                if face_to_follow:
                    if face_to_follow.is_visible:
                        # Turn towards the visible face
                        print("Following the face...")
                        turn_action = robot.turn_towards_face(face_to_follow)
                        followCnt = followCnt+1
                    else:
                        # If the face is no longer visible, reset and search again
                        print("Lost the face. Searching again...")
                        face_to_follow = None

                if not face_to_follow:
                    # If no face is detected, turn and search for one
                    try:
                        print("Searching for a face...")
                        robot.turn_in_place(degrees(-30)).wait_for_completed()  # Turn 30 degrees
                        face_to_follow = robot.world.wait_for_observed_face(timeout=30)  # Look for a face

                        if face_to_follow:
                            print("Face found! Starting to follow.")

                    except cozmo.exceptions.CozmoSDKException:
                        print("No face detected yet. Continuing search...")

                if turn_action:
                    # Complete any ongoing turn action
                    turn_action.wait_for_completed()

                # Add a small delay to avoid overloading the CPU
                time.sleep(1)


            if face_to_follow:
                robot.say_text("Was it you?").wait_for_completed()
                speech = listen()
                if(speech == 'not me'):
                    robot.say_text("Liar!").wait_for_completed()
                elif(speech == 'yes'):
                    robot.say_text("I knew it!").wait_for_completed()
            print(len(cube))
            if(len(cube) == 2):
                pick_up_cube(robot, cube)
                robot.play_anim_trigger(cozmo.anim.Triggers.DriveEndAngry).wait_for_completed()
            elif(len(cube) == 3):
                build_pyrimad(robot, cube)
                robot.play_anim_trigger(cozmo.anim.Triggers.DriveEndAngry).wait_for_completed()



        elif len(cube) < 2:
            cozmo_sing(robot)

        else: 
            return
    
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

def build_pyrimad(robot: cozmo.robot.Robot, cube):
    current_action = robot.pickup_object(cube[0], num_retries=3, in_parallel = True)
    current_action.wait_for_completed()
    if current_action.has_failed:
        code, reason = current_action.failure_reason
        result = current_action.result
        print("Pickup Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
        return
   
    current_action = robot.place_on_object(cube[1], num_retries=3)
    current_action.wait_for_completed()
    if current_action.has_failed:
        code, reason = current_action.failure_reason
        result = current_action.result
        print("Place On Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
        return

    current_action = robot.pickup_object(cube[2], num_retries=3, in_parallel = True)
    current_action.wait_for_completed()
    if current_action.has_failed:
        code, reason = current_action.failure_reason
        result = current_action.result
        print("Pickup Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
        return

    target_cube = cube[1]
    robot.go_to_object(target_cube, distance_mm(120)).wait_for_completed()

    robot.place_object_on_ground_here(target_cube, num_retries=3).wait_for_completed()
    print("Placed the cube next to the target cube.")


def build_pyrimad2(robot: cozmo.robot.Robot, cubes):
    try:
        # Step 2: Pick up the first cube and start the pyramid
        current_action = robot.pickup_object(cubes[0], num_retries=3)
        current_action.wait_for_completed()
        if current_action.has_failed:
            raise Exception(f"Failed to pick up the first cube: {current_action.failure_reason}")

        print("Successfully picked up the first cube.")

        # Step 3: Use the first animation to place the first cube on the side of the second cube
        robot.play_anim_trigger(BuildPyramidFirstBlockOnSide).wait_for_completed()

        print("First cube placed on the side of the second cube.")

        # Step 4: Pick up the second cube and place it on the side of the first cube
        current_action = robot.pickup_object(cubes[1], num_retries=3)
        current_action.wait_for_completed()
        if current_action.has_failed:
            raise Exception(f"Failed to pick up the second cube: {current_action.failure_reason}")

        print("Successfully picked up the second cube.")

        robot.play_anim_trigger(BuildPyramidSecondBlockOnSide).wait_for_completed()

        print("Second cube placed on the side of the first cube.")

        # Step 5: Pick up the third cube and place it upright on top
        current_action = robot.pickup_object(cubes[2], num_retries=3)
        current_action.wait_for_completed()
        if current_action.has_failed:
            raise Exception(f"Failed to pick up the third cube: {current_action.failure_reason}")

        print("Successfully picked up the third cube.")

        robot.play_anim_trigger(BuildPyramidThirdBlockUpright).wait_for_completed()

        print("Third cube placed upright on top. Pyramid complete!")

    except Exception as e:
        print(f"An error occurred: {e}")

#cozmo.run_program(follow_faces)

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)

    try:
        print("You said: " + recognizer.recognize_google(audio))
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Request error: {e}")

cozmo.run_program(make_cozmo_angry)