"""
Handles abstract LineList data
Implementation of a specific source (e.g. Vald) should be in its own file

Uses a pandas dataframe under the hood to handle the data
"""
import io
import json
import logging

import numpy as np
import pandas as pd

from flex.extensions.tabledata import JSONTableExtension

from ..persistence import IPersist
from ..util import air2vac, vac2air

logger = logging.getLogger(__name__)


class LineListError(Exception):
    """Raise when attempt to read a line data file fails"""


class LineList(IPersist):
    """Atomic data for a list of spectral lines
    """

    _base_columns = [
        "species",
        "wlcent",
        "excit",
        "gflog",
        "gamrad",
        "gamqst",
        "gamvw",
        "atom_number",
        "ionization",
    ]
    string_columns = ["species", "term_lower", "term_upper", "reference"]

    # Citations are added in the submodule (e.g. ValdFile)
    citation_info = ""

    @staticmethod
    def parse_line_error(error_flags, values=None):
        """Transform Line Error flags into relative error values

        Parameters
        ----------
        error_flags : list(str)
            Error Flags as defined by various references
        values : float
            depths of the lines, to convert absolute to relative errors

        Returns
        -------
        errors : list(float)
            relative errors for each line
        """
        if values is None:
            values = np.ones(len(error_flags))

        nist = {
            "AAA": 0.003,
            "AA": 0.01,
            "A+": 0.02,
            "A": 0.03,
            "B+": 0.07,
            "B": 0.1,
            "C+": 0.18,
            "C": 0.25,
            "C-": 0.3,
            "D+": 0.4,
            "D": 0.5,
            "D-": 0.6,
            "E": 0.7,
        }
        error = np.ones(len(error_flags), dtype=float)
        for i, (flag, _) in enumerate(zip(error_flags, values)):
            if len(flag) == 0:
                error[i] = 0.5
            elif flag[0] in [" ", "_", "P"]:
                # undefined or predicted
                error[i] = 0.5
            elif flag[0] == "E":
                # absolute error in dex
                # TODO absolute?
                error[i] = 10 ** float(flag[1:])
            elif flag[0] == "C":
                # Cancellation Factor, i.e. relative error
                try:
                    error[i] = abs(float(flag[1:]))
                except ValueError:
                    error[i] = 0.5
            elif flag[0] == "N":
                # NIST quality class
                flag = flag[1:5].strip()
                try:
                    error[i] = nist[flag]
                except KeyError:
                    error[i] = 0.5
        return error

    @staticmethod
    def guess_format(kwargs):
        short_line_format = kwargs.pop(
            "short_line_format", kwargs.pop("short_format", None)
        )
        if short_line_format is not None:
            return short_line_format

        keys = kwargs.keys()
        if (
            "line_extra" in keys
            and "line_lulande" in keys
            and "line_term_low" in keys
            and "line_term_upp" in keys
        ):
            return 2
        return 1

    @classmethod
    def from_IDL_SME(cls, **kwargs):
        """ extract LineList from IDL SME structure keywords """
        species = kwargs.pop("species").astype("U")
        atomic = np.asarray(kwargs.pop("atomic"), dtype="<f8")
        lande = np.asarray(kwargs.pop("lande"), dtype="<f8")
        depth = np.asarray(kwargs.pop("depth"), dtype="<f8")
        lineref = kwargs.pop("lineref").astype("U")
        short_line_format = cls.guess_format(kwargs)
        if short_line_format == 2:
            line_extra = np.asarray(kwargs.pop("line_extra"), dtype="<f8")
            line_lulande = np.asarray(kwargs.pop("line_lulande"), dtype="<f8")
            line_term_low = kwargs.pop("line_term_low").astype("U")
            line_term_upp = kwargs.pop("line_term_upp").astype("U")

        # If there is only one line, it is 1D in the IDL structure, but we expect 2D
        atomic = np.atleast_2d(atomic)

        data = {
            "species": species,
            "atom_number": atomic[:, 0],
            "ionization": atomic[:, 1],
            "wlcent": atomic[:, 2],
            "excit": atomic[:, 3],
            "gflog": atomic[:, 4],
            "gamrad": atomic[:, 5],
            "gamqst": atomic[:, 6],
            "gamvw": atomic[:, 7],
            "lande": lande,
            "depth": depth,
            "reference": lineref,
        }

        if short_line_format == 1:
            lineformat = "short"
        if short_line_format == 2:
            lineformat = "long"
            error = [s[0:11].strip() for s in lineref]
            error = LineList.parse_line_error(error, depth)
            data["error"] = error
            data["lande_lower"] = line_lulande[:, 0]
            data["lande_upper"] = line_lulande[:, 1]
            data["j_lo"] = line_extra[:, 0]
            data["e_upp"] = line_extra[:, 1]
            data["j_up"] = line_extra[:, 2]
            data["term_lower"] = [t[10:].strip() for t in line_term_low]
            data["term_upper"] = [t[10:].strip() for t in line_term_upp]

        linedata = pd.DataFrame.from_dict(data)

        return (linedata, lineformat)

    def __init__(self, linedata=None, lineformat="short", medium=None, **kwargs):
        if linedata is None or len(linedata) == 0:
            if isinstance(linedata, pd.DataFrame):
                linedata = pd.DataFrame(data=linedata, columns=self._base_columns)
            elif "atomic" in kwargs.keys():
                # everything is in the kwargs (usually by loading from old SME file)
                linedata, lineformat = LineList.from_IDL_SME(**kwargs)
            else:
                linedata = pd.DataFrame(data=[], columns=self._base_columns)
        else:
            if isinstance(linedata, LineList):
                linedata = linedata._lines
                lineformat = linedata.lineformat
                medium = linedata._medium
            else:
                if isinstance(linedata, (list, np.ndarray)):
                    # linedata = np.atleast_2d(linedata)
                    linedata = pd.DataFrame(
                        data=[[*linedata, 0, 0]], columns=self._base_columns
                    )

                if "atom_number" in kwargs.keys():
                    linedata["atom_number"] = kwargs["atom_number"]
                elif "atom_number" not in linedata:
                    linedata["atom_number"] = np.ones(len(linedata), dtype=float)

                if "ionization" in kwargs.keys():
                    linedata["ionization"] = kwargs["ionization"]
                elif "ionization" not in linedata and "species" in linedata:
                    linedata["ionization"] = np.array(
                        [int(s[-1]) for s in linedata["species"]], dtype=float
                    )

                if "term_upper" in kwargs.keys():
                    linedata["term_upper"] = kwargs["term_upper"]
                if "term_lower" in kwargs.keys():
                    linedata["term_lower"] = kwargs["term_lower"]
                if "reference" in kwargs.keys():
                    linedata["reference"] = kwargs["reference"]
                if "error" in kwargs.keys():
                    linedata["error"] = kwargs["error"]

        #:{"short", "long"}: Defines how much information is available
        self.lineformat = lineformat
        #:pandas.DataFrame: DataFrame that contains all the data
        self._lines = linedata  # should have all the fields (20)
        if medium in ["air", "vac", None]:
            self._medium = medium
        else:
            raise ValueError(
                f"Medium not recognized, expected one of ['air', 'vac'] , but got {medium} instead."
            )

        self.citation_info = ""
        if "citation_info" in kwargs.keys():
            self.citation_info = kwargs["citation_info"]

    def __len__(self):
        return len(self._lines)

    def __str__(self):
        return str(self._lines)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return self._lines.itertuples(index=False)

    def __getitem__(self, index):
        if isinstance(index, (list, str)):
            if len(index) == 0:
                return LineList(
                    self._lines.iloc[[]], lineformat=self.lineformat, medium=self.medium
                )
            values = self._lines[index].values
            if index in self.string_columns:
                values = values.astype(str)
            return values
        else:
            if isinstance(index, int):
                index = slice(index, index + 1)
            # just pass on a subsection of the linelist data, but keep it a linelist object
            return LineList(
                self._lines.iloc[index], self.lineformat, medium=self.medium
            )

    def __getattribute__(self, name):
        if name[0] != "_" and name not in dir(self):
            return self._lines[name].values
        return super().__getattribute__(name)

    @property
    def columns(self):
        return self._lines.columns

    @property
    def medium(self):
        return self._medium

    @medium.setter
    def medium(self, value):
        if self._medium is None:
            logger.warning(
                "No medium was defined for the linelist."
                " The new value of %s is assumed to be the native medium of the linelist. No conversion was performed"
            )
            self._medium = value
        if self._medium == value:
            return
        else:
            if self._medium == "air" and value == "vac":
                self._lines["wlcent"] = air2vac(self._lines["wlcent"])
                self._medium = "vac"
            elif self._medium == "vac" and value == "air":
                self._lines["wlcent"] = vac2air(self._lines["wlcent"])
                self._medium = "air"
            else:
                raise ValueError(
                    f"Type of medium not undertstood. Expected one of [vac, air], but got {value} instead"
                )

    @property
    def species(self):
        """list(str) of size (nlines,): Species name of each line """
        return self._lines["species"].values.astype("U")

    @property
    def lulande(self):
        """list(float) of size (nlines, 2): Lower and Upper Lande factors """
        if self.lineformat == "short":
            raise AttributeError(
                "Lower and Upper Lande Factors are only available in the long line format"
            )

            # additional data arrays for sme
        names = ["lande_lower", "lande_upper"]
        return self._lines.reindex(columns=names).values

    @property
    def extra(self):
        """list(float) of size (nlines, 3): additional line level information for NLTE calculation """
        if self.lineformat == "short":
            raise AttributeError("Extra is only available in the long line format")
        names = ["j_lo", "e_upp", "j_up"]
        return self._lines.reindex(columns=names).values

    @property
    def atomic(self):
        """list(float) of size (nlines, 8): Data array passed to C library, should only be used for this purpose """
        names = [
            "atom_number",
            "ionization",
            "wlcent",
            "excit",
            "gflog",
            "gamrad",
            "gamqst",
            "gamvw",
        ]
        # Select fields
        return self._lines.reindex(columns=names).values

    def sort(self, field="wlcent", ascending=True):
        """Sort the linelist

        The underlying datastructure will be replaced, 
        i.e. any references will not be sorted or updated

        Parameters
        ----------
        field : str, optional
            Field to use for sorting (default: "wlcent")
        ascending : bool, optional
            Wether to sort in ascending or descending order (default: True)

        Returns
        -------
        self : LineList
            The sorted LineList object
        """

        self._lines = self._lines.sort_values(by=field, ascending=ascending)
        return self

    def add(self, species, wlcent, excit, gflog, gamrad, gamqst, gamvw):
        """Add a new line to the existing linelist

        This replaces the underlying datastructure, 
        i.e. any references (atomic, etc.) will not be updated

        Parameters
        ----------
        species : str
            Name of the element and ionization
        wlcent : float
            central wavelength
        excit : float
            excitation energy in eV
        gflog : float
            gf logarithm
        gamrad : float
            broadening factor radiation
        gamqst : float
            broadening factor qst
        gamvw : float
            broadening factor van der Waals
        """

        linedata = {
            "species": species,
            "wlcent": wlcent,
            "excit": excit,
            "gflog": gflog,
            "gamrad": gamrad,
            "gamqst": gamqst,
            "gamvw": gamvw,
        }
        self._lines = self._lines.append([linedata])

    def _save(self):
        header = {
            "lineformat": self.lineformat,
            "medium": self.medium,
            "citation_info": self.citation_info,
        }
        data = self._lines
        ext = JSONTableExtension(header, data)
        return ext

    @classmethod
    def _load(cls, ext: JSONTableExtension):
        ll = cls(ext.data, **ext.header)
        return ll

    def _save_v1(self, file, folder="linelist"):
        if folder != "" and folder[-1] != "/":
            folder = folder + "/"

        info = {
            "format": self.lineformat,
            "medium": self.medium,
            "citation_info": self.citation_info,
        }
        file.writestr(f"{folder}info.json", json.dumps(info))

        lines = self._lines.reset_index(drop=True)
        # Eventually feather should be stable, at that point we can use this
        # Until then use JSON?
        # b = io.BytesIO()
        # lines.to_feather(b)
        # file.writestr(f"{folder}data.feather", b.getvalue())
        linedata = lines.to_json(orient="records")
        file.writestr(f"{folder}data.json", linedata)

    @staticmethod
    def _load_v1(file, names, folder=""):
        for name in names:
            if name.endswith("info.json"):
                info = file.read(name)
                info = json.loads(info)
                lineformat = info["format"]
                medium = info.get("medium")
                citation_info = info.get("citation_info", "")
            elif name.endswith("data.feather"):
                b = io.BytesIO(file.read(name))
                linedata = pd.read_feather(b)
            elif name.endswith("data.json"):
                b = io.BytesIO(file.read(name))
                linedata = pd.read_json(b, orient="records")
            elif name.endswith("data.npy"):
                b = io.BytesIO(file.read(name))
                linedata = np.load(b)
                linedata = pd.DataFrame.from_records(linedata)

        return LineList(
            linedata, lineformat=lineformat, medium=medium, citation_info=citation_info
        )
