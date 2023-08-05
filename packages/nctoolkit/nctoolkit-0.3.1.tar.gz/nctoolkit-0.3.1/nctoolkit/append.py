import os
import warnings
from nctoolkit.session import nc_safe, append_safe, remove_safe


def append(self, x=None):
    """
    Add new file(s) to a dataset.

    Parameters
    -------------
    x: str or list
     File path(s) to add to the dataset


    Examples
    ------------
    If you want to add a dataset data2 to another dataset data1, do the following:

    >>> data1.append(data2)

    If you want to add a new file to a dataset, do this:

    >>> data.append("infile.nc")


    """

    # run, as it makes no sense to add files while commands are waiting to run
    self.run()
    if "api.DataSet" in str(type(x)):
        x.run()

    if x is None:
        raise TypeError("Please supply files")

    if type(x) is str:
        x = [x]
    len_x = len(x)

    x = list(set(x))

    if len(x) < len_x:
        warnings.warn("Duplicates removed from files")

    # check files are not already in the dataset

    check_list = self.current

    for ff in x:
        if ff in check_list:
            raise ValueError(
                "You are trying to add a file that is already in the dataset"
            )

    for ff in x:
        if os.path.exists(ff) is False:
            raise ValueError(f"{ff} does not exist!")

    for ff in x:
        append_safe(ff)
        self.current.append(ff)


def remove(self, x=None):
    """
    Remove file(s) from a dataset

    Parameters
    -------------
    x: str or list
     File path(s) to remove from a dataset


    """

    if x is None:
        raise ValueError("Please provide files to remove!")

    if type(x) is str:
        x = [x]

    for ff in x:
        if ff not in self:
            raise ValueError(f"{x} is not a member of the dataset!")

    for ff in x:
        self.current.remove(ff)
        remove_safe(ff)
