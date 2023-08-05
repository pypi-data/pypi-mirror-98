import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "resources")
src = "https://github.com/lowRISC/opentitan"

# Module version
version_str = "0.0.post5324"
version_tuple = (0, 0, 5324)
try:
    from packaging.version import Version as V
    pversion = V("0.0.post5324")
except ImportError:
    pass

# Data version info
data_version_str = "0.0.post5229"
data_version_tuple = (0, 0, 5229)
try:
    from packaging.version import Version as V
    pdata_version = V("0.0.post5229")
except ImportError:
    pass
data_git_hash = "da341bfe385c6aca906ead47ba7110bd9a8273f6"
data_git_describe = "v0.0-5229-gda341bfe3"
data_git_msg = """\
commit da341bfe385c6aca906ead47ba7110bd9a8273f6
Author: Rupert Swarbrick <rswarbrick@lowrisc.org>
Date:   Wed Mar 10 15:45:25 2021 +0000

    [ibex] Just take the bottom 32 bits of dm::FooAddress
    
    The pulp_riscv_dbg module is presumably designed to support 64-bit
    systems, so its addresses are 64 bits wide. Slice out the bottom 32
    bits explicitly, avoiding width mismatch warnings for the addition and
    then for setting a 32-bit parameter with the 64-bit result.
    
    Signed-off-by: Rupert Swarbrick <rswarbrick@lowrisc.org>

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
