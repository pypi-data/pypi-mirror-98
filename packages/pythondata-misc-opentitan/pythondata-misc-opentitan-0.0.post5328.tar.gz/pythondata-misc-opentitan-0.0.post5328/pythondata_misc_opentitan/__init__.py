import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "resources")
src = "https://github.com/lowRISC/opentitan"

# Module version
version_str = "0.0.post5328"
version_tuple = (0, 0, 5328)
try:
    from packaging.version import Version as V
    pversion = V("0.0.post5328")
except ImportError:
    pass

# Data version info
data_version_str = "0.0.post5233"
data_version_tuple = (0, 0, 5233)
try:
    from packaging.version import Version as V
    pdata_version = V("0.0.post5233")
except ImportError:
    pass
data_git_hash = "54a509970b6499f63f7e98198b17535e64449b9f"
data_git_describe = "v0.0-5233-g54a509970"
data_git_msg = """\
commit 54a509970b6499f63f7e98198b17535e64449b9f
Author: Michael Schaffner <msf@opentitan.org>
Date:   Tue Mar 9 17:12:43 2021 -0800

    [sram_ctrl] Fix potential back-to-back partial write bug
    
    Signed-off-by: Michael Schaffner <msf@opentitan.org>

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
