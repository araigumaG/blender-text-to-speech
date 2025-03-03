import os
import sys
from pathlib import Path
import importlib

import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.app.handlers import persistent
from bpy.props import StringProperty, EnumProperty, BoolProperty

from . import blender_time as b_time
from . import caption as c
from .imports import txt as txt_import
from .imports import srt as srt_import
from .imports import sbv as sbv_import
from .imports import csv as csv_import
from .exports import txt as txt_export
from .exports import srt as srt_export
from .exports import sbv as sbv_export
from .exports import csv as csv_export
from . import codecs as codec_list
from . import text_strip
importlib.reload(b_time)
importlib.reload(c)
importlib.reload(txt_import)
importlib.reload(srt_import)
importlib.reload(sbv_import)
importlib.reload(csv_import)
importlib.reload(txt_export)
importlib.reload(srt_export)
importlib.reload(sbv_export)
importlib.reload(csv_export)
importlib.reload(codec_list)
importlib.reload(text_strip)

global global_captions
global_captions = []
global template_strip
template_strip = None

def remove_deleted_strips():
    global global_captions

    context = bpy.context
    scene = context.scene
    seq = scene.sequence_editor
    bpy.ops.sequencer.refresh_all()
    
    if not len(seq.sequences_all):
        global_captions.clear()

    it = 0
    end = len(global_captions)

    while(it < end):

        found = False
        for strip in seq.sequences_all:
            
            if global_captions[it].filename == strip.name:
                found = True
                global_captions[it].sound_strip = strip

        if not found:
            del global_captions[it]
            end -= 1
            it -= 1
        else:
            it += 1

def sort_strips_by_time():
    global global_captions
    bpy.ops.sequencer.refresh_all()
    for caption in global_captions:
        caption.update_timecode()
    
    global_captions.sort(key=lambda caption: caption.frame_start, reverse=False)

@persistent
def btts_load_handler(_scene):
    global global_captions
    if bpy.context.scene.text_to_speech.persistent_string:
        context = bpy.context
        scene = context.scene
        seq = scene.sequence_editor
        captions_raw = bpy.context.scene.text_to_speech.persistent_string.split('`')
        captions_raw.pop()

        for caption in captions_raw:
            caption_meta = caption.split('|')
            filename = caption_meta[0]
            cc_type = int(caption_meta[1])
            voice = int(caption_meta[2])
            name = caption_meta[3]
            channel = int(caption_meta[4])
            strip_text = caption_meta[5]
            pitch = float(caption_meta[6])
            rate = int(caption_meta[7])
            caption_strip = -1

            for strip in seq.sequences_all:
                if strip.name == filename:
                    caption_strip = strip

            if caption_strip != -1:
                new_cap = c.Caption(context, cc_type, name, strip_text,
                        b_time.Time(-1, -1, -1, -1), b_time.Time(-1, -1, -1, -1),
                        voice, channel, pitch, rate, 0, True, False, reconstruct=True)
                new_cap.sound_strip = caption_strip
                new_cap.filename = filename
                new_cap.update_timecode()
                global_captions.append(new_cap)

@persistent
def btts_save_handler(_scene):
    global global_captions
    remove_deleted_strips()
    sort_strips_by_time()
    string_to_save = ""

    # TODO refresh caption channel and pitch
    
    for caption in global_captions:
        string_to_save += f"{caption.sound_strip.name}|{caption.cc_type}|{caption.voice}|{caption.name}|{caption.channel}|{caption.text}|{caption.pitch}|{caption.rate}`"

    bpy.context.scene.text_to_speech.persistent_string = string_to_save

class TextToSpeechOperator(bpy.types.Operator):
    bl_idname = 'text_to_speech.speak'
    bl_label = 'speak op'
    bl_options = {'INTERNAL'}
    bl_description = "turns text into audio strip at current playhead"

    def execute(self, context):
        global global_captions
        seconds = bpy.context.scene.frame_current / bpy.context.scene.render.fps
        tts_props = context.scene.text_to_speech

        if not tts_props.string_field:
            self.report({'INFO'}, "no text to convert")
            return {'FINISHED'}

        else:
            global_captions.append(
                    c.Caption(context, 0, "", tts_props.string_field,
                        b_time.Time(0, 0, seconds, 0), b_time.Time(-1, -1, -1, -1),
                        tts_props.voice_enumerator, tts_props.channel, tts_props.pitch, tts_props.rate,
                        tts_props.text_channel, True, False))

            self.report({'INFO'}, "FINISHED")
            return {'FINISHED'}

class ClosedCaptionSet(): # translates cc files into a list of caption.Captions
    captions = []
    people = []

    def get(self):
        return(self.captions)

    def arrange_captions_by_time(self, with_text=False): # when timecode not provided
        bpy.ops.sequencer.select_all(action='DESELECT')
        frame_pointer = self.captions[0].sound_strip.frame_duration + bpy.context.scene.render.fps
        bpy.context.scene.tool_settings.sequencer_tool_settings.overlap_mode = 'SHUFFLE'

        for caption in range(1, len(self.captions)):
            
            self.captions[caption].sound_strip.select = True
            if with_text:
                self.text_caps[caption].select = True
            bpy.ops.transform.seq_slide(value=(frame_pointer, 0.0))
            # TODO there is a bug here where seq_slide doesn't always move the strips by exactly frame_pointer + 1sec
            self.captions[caption].sound_strip.select = False
            if with_text:
                self.text_caps[caption].select = False
            frame_pointer += self.captions[caption].sound_strip.frame_duration + bpy.context.scene.render.fps

    def __init__(self, context, text, filename, gender, pitch, rate, channel, text_channel, tts_flag, text_flag):
        ext = filename[-3:len(filename)]
        self.finished = False

        if ext == 'csv':
            self.captions = csv_import.import_cc(context, filename)
            print(self.captions)
            print(len(self.captions))
            if len(self.captions) > 0:
                self.finished = True
            else:
                print("csv file error")
                self.finished = False

        elif ext == 'txt':
            self.captions, self.text_caps = txt_import.import_cc(context, text, gender, pitch, rate, channel,
                                                text_channel, tts_flag, text_flag)

            if self.text_caps:
                self.arrange_captions_by_time(with_text=True)
            else:
                self.arrange_captions_by_time()

            self.finished = True
            
        elif ext == 'srt':
            self.captions = srt_import.import_cc(context, text, gender, pitch, rate, channel,
                                                text_channel, tts_flag, text_flag)
            self.finished = True

        elif ext == 'sbv':
            self.captions = sbv_import.import_cc(context, text, gender, pitch, rate, channel,
                                                text_channel, tts_flag, text_flag)
            self.finished = True


class ImportClosedCapFile(Operator, ImportHelper):
    bl_idname = "_import.cc_file"
    bl_label = "Import CC Data"

    codec: EnumProperty(
        name="File Encoding",
        description="Choose File Encoding",
        items = codec_list.items,
        default='95')

    tts_flag : bpy.props.BoolProperty(
        name="Text to speech",
        description="Option to create text to speech audio strips",
        default=True)

    text_strip_flag : bpy.props.BoolProperty(
        name="Text strips",
        description="Option to create text strips",
        default=False)

    def execute(self, context):
        global global_captions
        f = Path(bpy.path.abspath(self.filepath))
        tts_props = context.scene.text_to_speech

        if f.exists():
            enc = codec_list.items[int(self.codec)][1]
            captions =  ClosedCaptionSet(context, f.read_text(encoding=enc).split("\n"), self.filepath,
                                        tts_props.voice_enumerator, tts_props.pitch, tts_props.rate,
                                        tts_props.channel, tts_props.text_channel, self.tts_flag, self.text_strip_flag)
            if captions.finished:
                global_captions += captions.get()
                return {'FINISHED'}

            else:
                self.report({'INFO'}, 'Please try .txt, .srt, .sbv or csv file')
                return {'CANCELLED'}

class LoadFileButton(Operator):
    bl_idname = 'text_to_speech.load'
    bl_label = 'load op'
    bl_options = {'INTERNAL'}
    bl_description = "loads closed captions from txt, srt or sbv file"

    def execute(self, context):
        bpy.ops._import.cc_file('INVOKE_DEFAULT')
        return {'FINISHED'}

def export_cc_file(context, filepath, file_type):
    global global_captions
    remove_deleted_strips()
    sort_strips_by_time()

    if file_type == 'txt':
        return(txt_export.export(filepath, global_captions))

    if file_type == 'srt':
        return(srt_export.export(filepath, global_captions))

    if file_type == 'sbv':
        return(sbv_export.export(filepath, global_captions))

    if file_type == 'csv':
        return(csv_export.export(filepath, global_captions))

class ExportFileName(Operator, ExportHelper):
    bl_idname = "_export.cc_file"
    bl_label = "Export CC Data"
    filename_ext = ""
    
    filetype: EnumProperty(
        name="Filetype",
        description="Choose File Type",
        items=(
            ("txt", "txt", "text file"),
            ("srt", "srt", "srt file"),
            ("sbv", "sbv", "sbv file"),
            ("csv", "csv", "csv file"),
        ),
        default="txt",
    )
  
    def execute(self, context):

        if export_cc_file(context, self.filepath, self.filetype):
            return {'FINISHED'}

        else:
            self.report({'INFO'}, 'File already exists.')
            return {'CANCELLED'}

class ExportFileButton(Operator):
    bl_idname = 'text_to_speech.export'
    bl_label = 'export op'
    bl_options = {'INTERNAL'}
    bl_description = "exports closed caption file to a filepath"
    
    def execute(self, context):
        bpy.ops._export.cc_file('INVOKE_DEFAULT')
        return {'FINISHED'} 

class ConvertToTextStrip(Operator):
    bl_idname = 'text_to_speech.speech_to_strip'
    bl_label = 'convert to text strip'
    bl_options = {'INTERNAL'}
    bl_description = "convert selected audio captions to text strips"
    
    def execute(self, context):
        global global_captions
        global template_strip

        remove_deleted_strips()
        tts_props = context.scene.text_to_speech
        template = text_strip.check_for_template(context)

        for cap in global_captions:
            if cap.sound_strip.select:
                text_strip.text_strip(context, cap.text, cap.sound_strip.frame_start,
                                    cap.sound_strip.frame_final_end, tts_props.text_channel, template)

        return {'FINISHED'}

class CreateTemplateStrip(Operator):
    bl_idname = 'text_to_speech.create_template'
    bl_label = 'create template text strip'
    bl_options = {'INTERNAL'}
    bl_description = "create template for text strip creation"
    
    def execute(self, context):
        global template_strip
        _scene = context.scene
        tts_props = context.scene.text_to_speech

        if not _scene.sequence_editor:
            _scene.sequence_editor_create()
        seq = _scene.sequence_editor

        f_start = context.scene.frame_current
        f_end = f_start + context.scene.render.fps

        template_strip = seq.sequences.new_effect(
            name="Template_strip",
            type='TEXT',
            frame_start=f_start,
            frame_end=f_end,
            channel=tts_props.text_channel)

        return {'FINISHED'}