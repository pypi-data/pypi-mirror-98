import copy
import subprocess

from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_this, run_cdo, tidy_command
from nctoolkit.temp_file import temp_file
from nctoolkit.session import nc_safe, remove_safe


def cdo_version():
    cdo_check = subprocess.run(
        "cdo --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    cdo_check = str(cdo_check.stderr).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()
    return cdo_check.split("(")[0].strip().split(" ")[-1]


def fldstat(self, stat="mean"):
    """Method to calculate the spatial stat from a dataset"""
    # This cannot be chained in cdo version 1.9.3
    if cdo_version() in ["1.9.3"]:
        self.run()

    cdo_command = f"cdo -fld{stat}"

    run_this(cdo_command, self, output="ensemble")
    if cdo_version() in ["1.9.3"]:
        self.run()


def spatial_mean(self):
    """
    Calculate the area weighted spatial mean for all variables
    This is performed for each time step.

    Examples
    ------------

    If you want to calculate the spatial mean for a dataset, just do the following:

    >>> data.spatial_mean()

    Note that this calculation will calculate the average using weights based on each cell's
    area. If cell areas cannot be calculated, it will take a straight average, and a warning
    will say this.

    """
    fldstat(self, stat="mean")


def spatial_min(self):
    """
    Calculate the spatial minimum for all variables
    This is performed for each time step.

    Examples
    ------------

    If you want to calculate the spatial minimum for a dataset, just do the following:

    >>> data.spatial_min()

    """
    fldstat(self, stat="min")


def spatial_max(self):
    """
    Calculate the spatial maximum for all variables
    This is performed for each time step.

    Examples
    ------------
    If you want to calculate the spatial maximum for a dataset, just do the following:

    >>> data.spatial_max()

    """
    fldstat(self, stat="max")


def spatial_range(self):
    """
    Calculate the spatial range for all variables
    This is performed for each time step.

    Examples
    ------------
    If you want to calculate the range of each variable across space for a dataset, just do the following:

    >>> data.spatial_max()
    """
    fldstat(self, stat="range")


def spatial_sum(self, by_area=False):
    """
    Calculate the spatial sum for all variables
    This is performed for each time step.

    Parameters
    --------------
    by_area : boolean
        Set to True if you want to multiply the values by the grid cell area
        before summing over space. Default is False.

    Examples
    ------------
    If you want to calculate the spatial sum each variable across space for a dataset, just do the following:

    >>> data.spatial_sum()

    By default, this method simply sums up each grid cell value. In some cases this is not suitable. For example,
    the values in each cell may concentrations or values per square metre etc. In this case multiplying each cell
    value by the cell area is more suitable. Do the following:

    >>> data.spatial_sum(by_area = True)

    Each cell's value will be multiplied by the area of the cell (in square metres) prior to calculating the
    spatial sum.


    """

    if isinstance(by_area, bool) is False:
        raise TypeError("by_area is not boolean")

    # fldstats cannot be chained in cdo version 1.9.3, so run everything
    if cdo_version() in ["1.9.3"]:
        self.run()

    if len(self) == 1 or (by_area is False):

        if by_area:
            self.run()

            if cdo_version() in ["1.9.3"]:

                new_commands = []
                target1 = temp_file("nc")

                cdo_command = f"cdo -gridarea {self.current[0]} {target1}"
                cdo_command = tidy_command(cdo_command)
                new_commands.append(cdo_command)
                target1 = run_cdo(cdo_command, target=target1)

                target2 = temp_file("nc")

                cdo_command = f"cdo -mul {self.current[0]} {target1} {target2}"
                cdo_command = tidy_command(cdo_command)
                new_commands.append(cdo_command)

                target2 = run_cdo(cdo_command, target=target2)

                target = temp_file("nc")

                cdo_command = f"cdo -fldsum {target2} {target}"
                cdo_command = tidy_command(cdo_command)
                target = run_cdo(cdo_command, target=target)
                self.history += new_commands
                self._hold_history = copy.deepcopy(self.history)

                self.current = target
                remove_safe(target)
                remove_safe(target1)
                remove_safe(target2)

                cleanup()

                return None
            else:
                cdo_command = f"cdo -fldsum -mul {self.current[0]} -gridarea "
        else:
            cdo_command = "cdo -fldsum"

        run_this(cdo_command, self, output="ensemble")

        return None

    new_files = []
    new_commands = []
    for ff in self:
        if cdo_version() in ["1.9.3"]:

            target1 = temp_file("nc")

            cdo_command = f"cdo -gridarea {ff} {target1}"
            cdo_command = tidy_command(cdo_command)
            new_commands.append(cdo_command)
            target1 = run_cdo(cdo_command, target=target1)

            target2 = temp_file("nc")

            cdo_command = f"cdo -mul {ff} {target1} {target2}"
            cdo_command = tidy_command(cdo_command)
            new_commands.append(cdo_command)

            target2 = run_cdo(cdo_command, target=target2)

            target = temp_file("nc")

            cdo_command = f"cdo -fldsum {target2} {target}"
            cdo_command = tidy_command(cdo_command)
            target = run_cdo(cdo_command, target=target)
            remove_safe(target1)
            remove_safe(target2)
            new_files.append(target)
            new_commands.append(cdo_command)

        else:

            target = temp_file("nc")

            cdo_command = f"cdo -fldsum -mul {ff} -gridarea {ff} {target}"
            cdo_command = tidy_command(cdo_command)
            target = run_cdo(cdo_command, target=target)
            new_files.append(target)
            new_commands.append(cdo_command)

    self.history += new_commands
    self._hold_history = copy.deepcopy(self.history)

    self.current = new_files

    for ff in new_files:
        remove_safe(ff)

    cleanup()
    self.disk_clean()


def spatial_percentile(self, p=None):
    """
    Calculate the spatial sum for all variables
    This is performed for each time step.
    Parameters
    -------------
    p: int or float
        Percentile to calculate. 0<=p<=100.

    Examples
    ------------
    If you want to calculate the median of each variable across space for a dataset, just do the following:

    >>> data.spatial_percentile(50)
    """

    if p is None:
        raise ValueError("Please supply a percentile")

    if type(p) not in (int, float):
        raise ValueError(f"{str(p)} is not a valid percentile")
    if (p < 0) or (p > 100):
        raise ValueError(f"p: {str(p)} is not between 0 and 100!")

    cdo_command = f"cdo -fldpctl,{str(p)}"

    run_this(cdo_command, self, output="ensemble")
