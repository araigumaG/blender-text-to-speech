import pyttsx3
import os
import time
import bpy
from sys import platform
import string

not_allowed = ['/', '"', '\'', " "]
if platform == "win32":
    not_allowed = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

def sound_strip_from_text(context, text, pitch, start_frame, gender, audio_channel, rate):

    tmp_ident = text[0:45]
    
    text_ident = ""
    for char in tmp_ident:
        if char in not_allowed:
            pass
        else:
            text_ident += char

    time_now = time.strftime("%Y%m%d%H%M%S")
    identifier = f"{text_ident}{time_now}.wav"
    output_name = os.path.join(bpy.context.scene.render.filepath, identifier)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 

    if platform.startswith("linux"): # english
        engine.setProperty('voice', voices[11].id)
    else:
        engine.setProperty('voice', voices[int(gender)].id)

    engine.setProperty('rate', int(rate))
    engine.save_to_file(text, output_name)
    engine.runAndWait()
    
    _scene = context.scene
    
    if not _scene.sequence_editor:
        _scene.sequence_editor_create()
    seq = _scene.sequence_editor

    obj = seq.sequences.new_sound(identifier, filepath=output_name, channel=audio_channel, frame_start=start_frame)
    obj.pitch = pitch
    
    return (obj, identifier)