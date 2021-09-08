#
# sys_info ds ChRIS plugin app
#
# (c) 2021 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

from chrisapp.base import ChrisApp
import os
import platform
import socket


Gstr_title = r"""
                 _        __      
                (_)      / _|     
 ___ _   _ ___   _ _ __ | |_ ___  
/ __| | | / __| | | '_ \|  _/ _ \ 
\__ \ |_| \__ \ | | | | | || (_) |
|___/\__, |___/ |_|_| |_|_| \___/ 
      __/ | ______                
     |___/ |______|               
"""

Gstr_synopsis = """

(Edit this in-line help for app specifics. At a minimum, the 
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS and TS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       sys_info

    SYNOPSIS

        docker run --rm fnndsc/pl-sys_info sys_info                     \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            docker run --rm -u $(id -u)                             \
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
                fnndsc/pl-sys_info sys_info                        \
                /incoming /outgoing

    DESCRIPTION

        `sys_info` ...

    ARGS

        [-h] [--help]
        If specified, show help message and exit.
        
        [--json]
        If specified, show json representation of app and exit.
        
        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.
        
        [--savejson <DIR>] 
        If specified, save json representation file to DIR and exit. 
        
        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.
        
        [--version]
        If specified, print version number and exit. 
"""


class Sys_info(ChrisApp):
    """
    An app to display systen information
    """
    PACKAGE                 = __package__
    TITLE                   = 'An app to display systen information'
    CATEGORY                = ''
    TYPE                    = 'ds'
    ICON                    = ''   # url of an icon image
    MIN_NUMBER_OF_WORKERS   = 1    # Override with the minimum number of workers as int
    MAX_NUMBER_OF_WORKERS   = 1    # Override with the maximum number of workers as int
    MIN_CPU_LIMIT           = 1000 # Override with millicore value as int (1000 millicores == 1 CPU core)
    MIN_MEMORY_LIMIT        = 200  # Override with memory MegaByte (MB) limit as int
    MIN_GPU_LIMIT           = 0    # Override with the minimum number of GPUs as int
    MAX_GPU_LIMIT           = 0    # Override with the maximum number of GPUs as int

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())
        # Architecture
        print("Architecture: " + platform.architecture()[0])

        # machine
        print("Machine: " + platform.machine())

        # node
        #print("Node: " + platform.node())
        print("Node: " + socket.gethostname())

        # processor
        print("Processors: ")
        with open("/proc/cpuinfo", "r")  as f:
            info = f.readlines()

        cpuinfo = [x.strip().split(":")[1] for x in info if "model name"  in x]
        for index, item in enumerate(cpuinfo):
            print("    " + str(index) + ": " + item)

        # system
        print("System: " + platform.system())

        # distribution
        #dist = platform.dist()
        #dist = " ".join(x for x in dist)
        #print("Distribution: " + dist)

        # Load
        with open("/proc/loadavg", "r") as f:
            print("Average Load: " + f.read().strip())

        # Memory
        print("Memory Info: ")
        with open("/proc/meminfo", "r") as f:
            lines = f.readlines()

        print("     " + lines[0].strip())
        print("     " + lines[1].strip())

        # uptime
        uptime = None
        with open("/proc/uptime", "r") as f:
            uptime = f.read().split(" ")[0].strip()
        uptime = int(float(uptime))
        uptime_hours = uptime // 3600
        uptime_minutes = (uptime % 3600) // 60
        print("Uptime: " + str(uptime_hours) + ":" + str(uptime_minutes) + " hours")

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
