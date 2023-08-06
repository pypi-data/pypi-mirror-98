"""
Contexts for performing long or delicate functions.
"""
import os
import re
from contextlib import contextmanager
import tempfile
import shutil
import ix
from ciocore.gpath import Path


FILE_ATTR_HINTS = [
    ix.api.OfAttr.VISUAL_HINT_FILENAME_SAVE,
    ix.api.OfAttr.VISUAL_HINT_FILENAME_OPEN,
    ix.api.OfAttr.VISUAL_HINT_FOLDER,
]


class ConductorError(Exception):
    pass


@contextmanager
def waiting_cursor():
    """
    Perform some function with the wait cursor showing.
    """
    clarisse_win = ix.application.get_event_window()
    old_cursor = clarisse_win.get_mouse_cursor()
    clarisse_win.set_mouse_cursor(ix.api.Gui.MOUSE_CURSOR_WAIT)
    yield
    clarisse_win.set_mouse_cursor(old_cursor)


@contextmanager
def disabled_app():
    """
    Disble the app to perform some function.
    """
    app = ix.application
    app.disable()
    yield
    app.enable()


def is_windows():
    return os.name == "nt"


def conductor_temp_dir():
    return os.path.join(
        ix.application.get_factory().get_vars().get("CTEMP").get_string(),
        "conductor",
    )


def linuxify(filename):
    """
    Adjust reference pasths for windows.
    """
    path_regex = _get_path_line_regex()

    temp_path = tempfile.mktemp()

    shutil.copy2(filename, temp_path)
    os.remove(filename)
    with open(filename, "w+") as outfile:
        with open(temp_path, "r+") as infile:
            for line in infile:
                match = re.match(path_regex, line)
                if match:
                    path = Path(match.group(1), no_expand=True).posix_path(
                        with_drive=False)
                    outfile.write(line.replace(match.group(1), path))
                else:
                    outfile.write(line)


def _get_path_line_regex():
    """
    Generate a regex to help identify filepath attributes.

    As we scan project files to replace windows paths, we use this regex which
    will be something like: r'\s+(?:filename|filename_sys|save_as)\s+"(.*)"\s+'
    only longer.
    """
    classes = ix.application.get_factory().get_classes()
    file_attrs = []
    for klass in classes.get_classes():
        attr_count = klass.get_attribute_count()
        for i in xrange(attr_count):
            attr = klass.get_attribute(i)
            hint = attr.get_visual_hint()
            if hint in FILE_ATTR_HINTS:
                file_attrs.append(attr.get_name())

    return r"\s+(?:" + "|".join(sorted(set(file_attrs))) + r')\s+"(.*)"\s+'


# a = {
#     'environment': {
#         u'PATH': u'/opt/isotropix/clarisse/4/clarisse4.0.sp10/clarisse', 
#         u'ILISE_SERVER': u'conductor_ilise:40500', 
#         'CONDUCTOR_PATHHELPER': 0, 
#         'PYTHONHOME': '/opt/silhouettefx/silhouette/7/silhouette-7.5.2', 
#         'LD_LIBRARY_PATH': '/usr/lib/python2.7/config-x86_64-linux-gnu'
#     }, 
#     'local_upload': False, 
#     'upload_paths': [
#     '/Users/Shared/tmp/conductor/ciocnode', 
#     '/Users/Shared/tmp/conductor/cioprep.py', 
#     '/Users/Shared/tmp/conductor/clarisse.cfg', 
#     '/Volumes/xtr/gd/arches/arch_shot.debugjobAMacOS.cio.project', 
#     '/Volumes/xtr/gd/arches/bugs_seq/bugs.0120.jpg', 
#     '/Volumes/xtr/gd/arches/bugs_seq/bugs.0121.jpg', 
#     '/Volumes/xtr/gd/arches/bugs_seq/bugs.0122.jpg', 
#     '/Volumes/xtr/gd/arches/bugs_seq/bugs.0123.jpg', 
#     '/Volumes/xtr/gd/arches/bugs_seq/bugs.0124.jpg', 
#     '/Volumes/xtr/gd/arches/bugs_seq/bugs.0125.jpg', 
#     '/Volumes/xtr/gd/arches/bugs_seq/bugs.0126.jpg', 
#     '/Volumes/xtr/gd/arches/bugs_seq/bugs.0127.jpg', 
#     '/Volumes/xtr/gd/arches/bugs_seq/bugs.0128.jpg', 
#     '/Volumes/xtr/gd/arches/bugs_seq/bugs.0129.jpg', 
#     '/Volumes/xtr/gd/arches/bugs_seq/bugs.0130.jpg', 
#     '/Volumes/xtr/gd/fish_100.abc', 
#     '/Volumes/xtr/gd/image_maps/alcazar.jpg', 
#     '/Volumes/xtr/gd/image_maps/dd.jpg', 
#     '/Volumes/xtr/gd/image_maps/wall.jpeg'], 
#     'autoretry_policy': {
#     'preempted': {'max_retries': 3}},
#     'software_package_ids': [u'2f5b4ca59da29c2ae0ab42bfdcb5b19e'], 
#     'preemptible': True, 'upload_only': False, 
#     'project': u'default', 'instance_type': u'n1-highmem-4', 
#     'scout_frames': '120', 'output_path': '/Users/julian/dev/fish/clarisse/renders/jobA', 
#     'notify': None, 
#     'chunk_size': 1, 
#     'tasks_data': [
#         {'frames': '120', 'command': '/Users/Shared/tmp/conductor/ciocnode "/Volumes/xtr/gd/arches/arch_shot.debugjobAMacOS.cio.project" -image project://scene/image1 -image_frames_list 120 -tile_rendering 1 1 -license_server conductor_ilise:40500'}, 
#         {'frames': '121', 'command': '/Users/Shared/tmp/conductor/ciocnode "/Volumes/xtr/gd/arches/arch_shot.debugjobAMacOS.cio.project" -image project://scene/image1 -image_frames_list 121 -tile_rendering 1 1 -license_server conductor_ilise:40500'}
#         ],
#     'job_title': 'debug_jobA_MacOS'
#     }
