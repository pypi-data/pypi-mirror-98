import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "resources")
src = "https://github.com/lowRISC/opentitan"

# Module version
version_str = "0.0.post5314"
version_tuple = (0, 0, 5314)
try:
    from packaging.version import Version as V
    pversion = V("0.0.post5314")
except ImportError:
    pass

# Data version info
data_version_str = "0.0.post5219"
data_version_tuple = (0, 0, 5219)
try:
    from packaging.version import Version as V
    pdata_version = V("0.0.post5219")
except ImportError:
    pass
data_git_hash = "44ab47bf0c323a02d59c39ce6c98162338db819e"
data_git_describe = "v0.0-5219-g44ab47bf0"
data_git_msg = """\
commit 44ab47bf0c323a02d59c39ce6c98162338db819e
Author: Cindy Chen <chencindy@google.com>
Date:   Mon Mar 8 12:22:02 2021 -0800

    [dv/alert] Add fatal alert check if scb is disabled
    
    This PR addes a fatal alert check (check if fatal alert continuously
    triggered until reset in a nonblocking task).
    This can be used in aes shadow reg tests and keymgr tests where the scb
    is disabled.
    
    Signed-off-by: Cindy Chen <chencindy@google.com>

"""

# Tool version info
tool_version_str = "0.0.post95"
tool_version_tuple = (0, 0, 95)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post95")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_misc_opentitan."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_misc_opentitan".format(f))
    return fn
