from pelican import signals
from pelican.settings import configure_settings, get_settings_from_file

# This is mostly ripped fomr Pelican.settings
# It makes some of the relative urls in the subsite settings files absolute
# And also does osme over the top validation that I didnt want to remove

'''
def relativise_path(local_settings, path):
    for p in ['PATH', 'OUTPUT_PATH', 'THEME', 'CACHE_PATH']:
        if p in local_settings and local_settings[p] is not None \
                and not os.path.isabs(local_settings[p]):
            absp = os.path.abspath(os.path.normpath(os.path.join(
                os.path.dirname(path), local_settings[p])))
            if p not in ('THEME') or os.path.exists(absp):
                local_settings[p] = absp

    if 'PLUGIN_PATH' in local_settings:
        logger.warning('PLUGIN_PATH setting has been replaced by '
                       'PLUGIN_PATHS, moving it to the new setting name.')
        local_settings['PLUGIN_PATHS'] = local_settings['PLUGIN_PATH']
        del local_settings['PLUGIN_PATH']
    if isinstance(local_settings['PLUGIN_PATHS'], six.string_types):
        logger.warning("Defining PLUGIN_PATHS setting as string "
                       "has been deprecated (should be a list)")
        local_settings['PLUGIN_PATHS'] = [local_settings['PLUGIN_PATHS']]
    elif local_settings['PLUGIN_PATHS'] is not None:
        def getabs(path, pluginpath):
            if os.path.isabs(pluginpath):
                return pluginpath
            else:
                path_dirname = os.path.dirname(path)
                path_joined = os.path.join(path_dirname, pluginpath)
                path_normed = os.path.normpath(path_joined)
                path_absolute = os.path.abspath(path_normed)
                return path_absolute

        pluginpath_list = [getabs(path, pluginpath)
                           for pluginpath
                           in local_settings['PLUGIN_PATHS']]
        local_settings['PLUGIN_PATHS'] = pluginpath_list
    return local_settings


def subsites(pelican_obj):
    # Copy the main site's settings
    basesettings = pelican_obj.settings.copy()
    baseoutput = basesettings["OUTPUT_PATH"]
    basesite = basesettings["SITEURL"]
    # Run through the list of subsites
    for subsite in basesettings["SUBSITES"]:
        logging.debug('Subsite {}: Started.'.format(subsite.replace('_', '').capitalize()))
        # Turn the settings file into a dictionary and make the relative paths
        # absolute
        newsettings = relativise_path(
            get_settings_from_file(subsite + "/settings.py", basesettings), subsite + "/settings.py")
        # Ensure that the output is a subdirectory of the main site
        newsettings["OUTPUT_PATH"] = baseoutput + \
            "/" + newsettings["SUBSITE_PATH"]
        # Ensure that the subsite knows its url
        newsettings["SITEURL"] = basesite + \
            "/" + newsettings["SUBSITE_PATH"]
        newsettings["BASEURL"] = basesite
        # Pelican magic settings checker
        settings = configure_settings(newsettings)
        # This is a bit hacky. It removes the plugin to signal mapping. For
        # reason even in a new pelican object the signals are still mapped
        # to the old plugins.
        # iterate through module's attributes
        for name, val in signals.__dict__.items():
            if hasattr(val, 'receivers'):
                val.receivers = {}
        # Set up a pelican class
        cls = basesettings['PELICAN_CLASS']
        # I think this is some python2/3 compatibility thing
        # I'm scared to remove.
        if isinstance(cls, six.string_types):
            module, cls_name = cls.rsplit('.', 1)
            module = __import__(module)
            cls = getattr(module, cls_name)
        # Create a new pelican instance for the subsite and run!
        new_pelican_obj = cls(settings)
        new_pelican_obj.run()
        for name, val in signals.__dict__.items():
            if hasattr(val, 'receivers'):
                val.receivers = {}
        logging.debug('Subsite {}: Completed.'.format(subsite.replace('_', '').capitalize()))
'''

from pelican import signals
from pelican.readers import MarkdownReader

# Create a new reader class, inheriting from the pelican.reader.BaseReader
class BetterMarkdownReader(MarkdownReader):
    def read(self, filename):
        content, metadata = super(BetterMarkdownReader, self).read(filename)
        print(content)
        return content, metadata

def add_reader(readers):
    readers.reader_classes['md'] = BetterMarkdownReader

# This is how pelican works.
def register():
    signals.readers_init.connect(add_reader)
