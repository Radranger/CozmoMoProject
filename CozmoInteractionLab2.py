import cozmo
import asyncio
import time

# FROM HELLO WORLD:
def cozmo_program(robot: cozmo.robot.Robot):
    robot.say_text("Hello World").wait_for_completed()

# FROM PLAY SONG:
def cozmo_program(robot: cozmo.robot.Robot):

    # Create an array of SongNote objects, consisting of all notes from C2 to C3_Sharp
    notes = [
        cozmo.song.SongNote(cozmo.song.NoteTypes.C2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C2_Sharp, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.D2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.D2_Sharp, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.E2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.F2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.F2_Sharp, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.G2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.G2_Sharp, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.A2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.A2_Sharp, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.B2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C3, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C3_Sharp, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.Rest, cozmo.song.NoteDurations.Quarter) ]

    # Play the ascending notes
    robot.play_song(notes, loop_count=1).wait_for_completed()

    # Create an array of SongNote objects, consisting of the C3 pitch with varying durations
    notes = [
        cozmo.song.SongNote(cozmo.song.NoteTypes.C3, cozmo.song.NoteDurations.Half),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C3, cozmo.song.NoteDurations.ThreeQuarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.Rest, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C3, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C3, cozmo.song.NoteDurations.Whole) ]

    # Play the notes with varying durations
    robot.play_song(notes, loop_count=1).wait_for_completed()

cozmo.run_program(cozmo_program)
# OUR CODE Comments with SDK references below found at:
# https://data.bit-bots.de/cozmo_sdk_doc/cozmosdk.anki.com/docs/generated/cozmo.robot.html

# Step 1: Make Cozmo angry when seeing cube.
#   Once a cube is spotted by Cozmo:
#    class cozmo.objects.EvtObjectAppeared(**kwargs)
#   Look around in place and find human face:
#    class cozmo.behavior.BehaviorTypes
#    FindFaces= _BehaviorType(name='FindFaces', id=1)

# Facial expression angry:
#cozmo.faces.FACIAL_EXPRESSION_ANGRY= 'angry'
'''
def make_cozmo_angry(robot: cozmo.robot.Robot):
    try:
        # Step 1: Spot cube
        cube = robot.world.wait_for_observed_light_cube(timeout=10)
        if cube:
            robot.play_anim(name="anim_reacttoblock_happydetermined").wait_for_completed()
        
        # Step 2: Look for a human face
        robot.say_text("Who did this?").wait_for_completed()
        found_face = None
        for _ in range(4):  # Rotate in place up to 360 degrees
            robot.turn_in_place(degrees(90)).wait_for_completed()
            found_face = robot.world.wait_for_observed_face(timeout=3)
            if found_face:
                break
        
        if found_face:
            robot.play_anim(name="anim_greeting_happy_01").wait_for_completed()
            robot.say_text("I am angry!").wait_for_completed()
        else:
            robot.say_text("No human found!").wait_for_completed()

    except cozmo.exceptions.RobotBusy:
        print("Cozmo is busy, retrying...")

#Step 2: Make Cozmo go and pick up the cube.
def pick_up_cube(robot: cozmo.robot.Robot):
    try:
        cube = robot.world.wait_for_observed_light_cube(timeout=10)
        if cube:
            robot.go_to_object(cube, distance_mm(50)).wait_for_completed()
            robot.pickup_object(cube).wait_for_completed()
        else:
            robot.say_text("No cube found!").wait_for_completed()
    except cozmo.exceptions.RobotBusy:
        print("Cozmo is busy, retrying...")

#Step 3: Make Cozmo drop the cube in a specific location "bin".
'''