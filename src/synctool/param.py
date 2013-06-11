#
#	synctool.param.py	WJ111
#
#   synctool by Walter de Jong <walter@heiho.net> (c) 2003-2013
#
#   synctool COMES WITH NO WARRANTY. synctool IS FREE SOFTWARE.
#   synctool is distributed under terms described in the GNU General Public
#   License.
#

import os
import sys

VERSION = '6.0-beta'

# location of default config file on the master node
# synctool-client generally runs with -c $masterdir/synctool-client.conf
DEFAULT_CONF = '/etc/synctool.conf'
CONF_FILE = DEFAULT_CONF

BOOLEAN_VALUE_TRUE = ('1', 'on', 'yes', 'true')
BOOLEAN_VALUE_FALSE = ('0', 'off', 'no', 'false')

#
# config variables
#
# The prefix is initialized by init(),
# and may be overridden in the config file
# Also note that setting a default for masterdir is probably a bad idea
#
PREFIX = None
MASTERDIR = None
OVERLAY_DIR = None
DELETE_DIR = None
TEMP_DIR = '/tmp/synctool'
HOSTNAME = None
NODENAME = None
HOST_ID = None

DIFF_CMD = 'diff -u'
PING_CMD = 'ping -q -c 1 -t 1'
SSH_CMD = 'ssh -o ConnectTimeout=10 -x -q'
SCP_CMD = 'scp -o ConnectTimeout=10 -p'
RSYNC_CMD = ("rsync -ar --numeric-ids --delete --delete-excluded "
			"-e 'ssh -o ConnectTimeout=10 -x -q' -q")
SYNCTOOL_CMD = None
PKG_CMD = None

PACKAGE_MANAGER = None

LOGFILE = None
NUM_PROC = 16				# use sensible default

# default symlink mode
# Linux makes them 0777 no matter what umask you have ...
# but how do you like them on a different platform?
#
# The symlink mode can be set in the config file
# with keyword symlink_mode
#
# Changing this value here has no effect ...
# By default, detect_root() will set it to 0777 on Linux and 0755 otherwise
SYMLINK_MODE = 0755

REQUIRE_EXTENSION = True
FULL_PATH = False
TERSE = False
BACKUP_COPIES = True
IGNORE_DOTFILES = False
IGNORE_DOTDIRS = False
IGNORE_FILES = []
IGNORE_FILES_WITH_WILDCARDS = []

DEFAULT_NODESET = ['all']

NODES = {}
IPADDRESSES = {}
HOSTNAMES = {}
HOSTNAMES_BY_NODE = {}

GROUP_DEFS = {}

IGNORE_GROUPS = []

# to be initialized externally ... (see synctool.py)
# these are lists of group names
MY_GROUPS = None
ALL_GROUPS = None

# string length of the 'MASTERDIR' variable
# although silly to keep this in a var,
# it makes it easier to print messages
MASTER_LEN = 0

# colorize output
COLORIZE = True
COLORIZE_FULL_LINE = False
COLORIZE_BRIGHT = True

TERSE_COLORS = {
	'info'   : 'default',
	'warn'   : 'magenta',
	'error'  : 'red',
	'fail'   : 'red',
	'sync'   : 'default',
	'link'   : 'cyan',
	'mkdir'  : 'blue',		# I'd use yellow on a black background,
							# blue on white
	'rm'     : 'yellow',
	'chown'  : 'cyan',
	'chmod'  : 'cyan',
	'exec'   : 'green',
	'upload' : 'magenta',
	'new'    : 'default',
	'type'   : 'magenta',
	'dryrun' : 'default',
	'fixing' : 'default',
	'ok'     : 'default',
}

# list of supported package managers
KNOWN_PACKAGE_MANAGERS = (
	'apt-get', 'yum', 'zypper', 'brew', 'pacman', 'bsdpkg',
#	'urpmi', 'portage', 'port', 'swaret',
)


def init():
	'''detect my prefix and set default symlink mode'''

	base = os.path.abspath(os.path.dirname(sys.argv[0]))
	if not base:
		raise RuntimeError, 'unable to determine base dir'

	(prefix, bindir) = os.path.split(base)

	reset_prefix(prefix)

	# detect symlink mode
	if sys.platform[:5] == 'linux':
		SYMLINK_MODE = 0777
	else:
		SYMLINK_MODE = 0755


def reset_prefix(prefix):
	'''reset dirs that are relative to the prefix'''

	global PREFIX, SYNCTOOL_CMD, PKG_CMD

	PREFIX = prefix

	# FIXME what if synctool_cmd was already set in the cfg file?
	SYNCTOOL_CMD = os.path.join(prefix, 'bin/synctool-client')
	PKG_CMD = os.path.join(prefix, 'bin/synctool-pkg')


def reset_masterdir(masterdir):
	global MASTERDIR, MASTER_LEN, OVERLAY_DIR, DELETE_DIR

	MASTERDIR = masterdir
	MASTER_LEN = len(MASTERDIR) + 1
	OVERLAY_DIR = os.path.join(MASTERDIR, 'overlay')
	DELETE_DIR = os.path.join(MASTERDIR, 'delete')


# EOB
