# Load the native modules and other dependencies.
from ..plugins.PyScript import FileImporter, FileSource, PipelineStatus
from ..data import DataCollection
import sys
import ovito
try:
    # Python 3.x
    import collections.abc as collections
except ImportError:
    # Python 2.x
    import collections

# Implementation of FileSource.load() method:
def _FileSource_load(self, location, **params):
    """ Sets a new input file, from which this data source will retrieve its data from.

        The function accepts additional keyword arguments, which are forwarded to the format-specific file importer.
        For further information, please see the documentation of the :py:func:`~ovito.io.import_file` function,
        which has the same function interface as this method.

        :param str location: The local file(s) or remote URL to load.
    """

    # Process input parameter
    if isinstance(location, str if sys.version_info[0] >= 3 else basestring):
        location_list = [location]
    elif isinstance(location, collections.Sequence):
        location_list = list(location)
    else:
        raise TypeError("Invalid input file location. Expected string or sequence of strings.")
    first_location = location_list[0]

    # Importing a file is a long-running operation, which is not permitted during viewport rendering or pipeline evaluation.
    # In these situations, the following function call will raise an exception.
    ovito.scene.request_long_operation()

    # Determine the file's format.
    importer = FileImporter.autodetect_format(self.dataset, first_location)
    if not importer:
        raise RuntimeError("Could not detect the file format. The format might not be supported.")

    # Re-use existing importer if compatible.
    if self.importer and type(self.importer) == type(importer):
        importer = self.importer

    # Forward user parameters to the importer.
    for key in params:
        if not hasattr(importer, key):
            raise RuntimeError("Importer object %s does not have an attribute '%s'." % (importer, key))
        importer.__setattr__(key, params[key])

    # Load new data file.
    if not self.set_source(location_list, importer, False):
        raise RuntimeError("Operation has been canceled by the user.")

    # Block execution until data has been loaded.
    if not self.wait_until_ready(self.dataset.anim.time):
        raise RuntimeError("Operation has been canceled by the user.")

    # Raise Python error if loading failed.
    if self.status.type == PipelineStatus.Type.Error:
        raise RuntimeError(self.status.text)

    # Block until list of animation frames has been loaded
    if not self.wait_for_frames_list():
        raise RuntimeError("Operation has been canceled by the user.")

FileSource.load = _FileSource_load

# Implementation of FileSource.source_path property.
def _get_FileSource_source_path(self):
    """ This read-only attribute returns the path(s) or URL(s) of the file(s) where this :py:class:`!FileSource` retrieves its input data from.
        You can change the source path by calling :py:meth:`.load`. """
    path_list = self.get_source_paths()
    if len(path_list) == 1: return path_list[0]
    elif len(path_list) == 0: return ""
    else: return path_list
FileSource.source_path = property(_get_FileSource_source_path)

def _FileSource_compute(self, frame = None):
    """ Requests data from this data source. The :py:class:`!FileSource` will load it from the external file if needed.

        The optional *frame* parameter determines the frame to retrieve, which must be in the range 0 through (:py:attr:`num_frames`-1).
        If no frame number is specified, the current time slider position is used (will always be frame 0 for scripts not running in the context of an interactive OVITO session).

        The :py:class:`!FileSource` uses a caching mechanism to keep the data for one or more frames in memory. Thus, invoking :py:meth:`!compute`
        repeatedly to retrieve the same frame will typically be very fast.

        :param int frame: The source frame to retrieve.
        :return: A new :py:class:`~ovito.data.DataCollection` containing the loaded data.
    """
    if frame is not None:
        time = self.source_frame_to_anim_time(frame)
    else:
        time = self.dataset.anim.time

    state = self._evaluate(time)
    if state.status.type == PipelineStatus.Type.Error:
        raise RuntimeError("Data source evaluation failed: %s" % state.status.text)
    if not state.data:
        raise RuntimeError("Data pipeline did not yield any output DataCollection.")

    # Wait for worker threads to finish.
    # This is to avoid warning messages 'QThreadStorage: Thread exited after QThreadStorage destroyed'
    # during Python program exit.
#    if not hasattr(sys, '__OVITO_BUILD_MONOLITHIC'):
#        import PySide2.QtCore
#        PySide2.QtCore.QThreadPool.globalInstance().waitForDone(0)

    return state.mutable_data

FileSource.compute = _FileSource_compute