"""
Run known pulsar parameter estimation using bilby.
"""

import ast
import configparser
import glob
import json
import os
import signal
import sys
import warnings
from argparse import ArgumentParser

import bilby
import cwinpy
import numpy as np
from bilby_pipe.bilbyargparser import BilbyArgParser
from bilby_pipe.input import Input
from bilby_pipe.job_creation.dag import Dag
from bilby_pipe.job_creation.node import Node
from bilby_pipe.utils import (
    CHECKPOINT_EXIT_CODE,
    BilbyPipeError,
    check_directory_exists_and_if_not_mkdir,
    convert_string_to_dict,
    parse_args,
)
from configargparse import DefaultConfigFileParser
from lalpulsar.PulsarParametersWrapper import PulsarParametersPy

from ..data import HeterodynedData, MultiHeterodynedData
from ..likelihood import TargetedPulsarLikelihood
from ..utils import is_par_file


def sighandler(signum, frame):
    # perform periodic eviction with exit code 77
    # see https://git.ligo.org/lscsoft/bilby_pipe/-/commit/c63c3e718f20ce39b0340da27fb696c49409fcd8  # noqa: E501
    sys.exit(CHECKPOINT_EXIT_CODE)


def create_pe_parser():
    """
    Create the argument parser.
    """

    description = """\
A script to use Bayesian inference to estimate the parameters of a \
continuous gravitational-wave signal from a known pulsar."""

    parser = BilbyArgParser(
        prog=sys.argv[0],
        description=description,
        ignore_unknown_config_file_keys=False,
        allow_abbrev=False,
    )
    parser.add("--config", type=str, is_config_file=True, help="Configuration ini file")
    parser.add(
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=cwinpy.__version__),
    )
    parser.add(
        "--periodic-restart-time",
        default=43200,
        type=int,
        help=(
            "Time after which the job will be self-evicted with code 77. "
            "After this, condor will restart the job. Default is 43200s. "
            "This is used to decrease the chance of HTCondor hard evictions."
        ),
    )

    pulsarparser = parser.add_argument_group("Pulsar inputs")
    pulsarparser.add(
        "--par-file",
        required=True,
        type=str,
        help=("The path to a TEMPO(2) style file containing the pulsar parameters."),
    )

    dataparser = parser.add_argument_group("Data inputs")
    dataparser.add(
        "-d",
        "--detector",
        action="append",
        help=(
            "The abbreviated name of a detector to analyse. "
            "Multiple detectors can be passed with multiple "
            "arguments, e.g., --detector H1 --detector L1."
        ),
    )
    dataparser.add(
        "--data-file",
        action="append",
        help=(
            "The path to a heterodyned data file for a given "
            "detector. The format should be of the form "
            '"DET:PATH",  where DET is the detector name. '
            "Multiple files can be passed with multiple "
            "arguments, e.g., --data-file H1:H1data.txt "
            "--data-file L1:L1data.txt. This data will be assumed "
            "to be that in a search for a signal from the l=m=2 "
            "mass quadrupole and therefore heterodyned at twice "
            "the source's rotation frequency. To add data "
            "explicitly setting the heterodyned frequency at twice "
            'the rotation frequency use "--data-file-2f", or for '
            'data at the rotation frequency use "--data-file-1f".'
        ),
    )
    dataparser.add(
        "--data-file-2f",
        action="append",
        help=(
            "The path to a data file for a given detector where "
            "the data is explicitly given as being heterodyned at "
            "twice the source's rotation frequency. The inputs "
            "should be in the same format as those given to the "
            '"--data-file" flag. This flag should generally be '
            'preferred over the use of "--data-file".'
        ),
    )
    dataparser.add(
        "--data-file-1f",
        action="append",
        help=(
            "The path to a data file for a given detector where "
            "the data is explicitly given as being heterodyned at "
            "the source's rotation frequency. The inputs should "
            "be in the same format as those given to the "
            '"--data-file" flag.'
        ),
    )
    dataparser.add(
        "--data-kwargs",
        help=(
            "A Python dictionary containing keywords to pass to "
            "the HeterodynedData object."
        ),
    )

    simparser = parser.add_argument_group("Simulated data")
    simparser.add(
        "--inj-par",
        type=str,
        help=(
            "The path to a TEMPO(2) style file containing the "
            'parameters of a simulated signal to "inject" into the '
            "data."
        ),
    )
    simparser.add(
        "--inj-times",
        help=(
            "A Python list of pairs of times between which to add "
            'the simulated signal (specified by the "--inj-par" '
            "flag) to the data. By default the signal is added into "
            "the whole data set."
        ),
    )
    simparser.add(
        "--show-truths",
        action="store_true",
        default=False,
        help=(
            "If plotting the results, setting this flag will "
            'overplot the "true" signal values. If adding a '
            "simulated signal then these parameter values will be "
            'taken from the file specified by the "--inj-par" flag, '
            "otherwise the values will be taken from the file "
            'specified by the "--par-file" flag.'
        ),
    )
    simparser.add(
        "--fake-asd",
        action="append",
        help=(
            "This flag sets the code to perform the analysis on "
            "simulated Gaussian noise, with data samples drawn from "
            "a Gaussian distribution defined by a given amplitude "
            "spectral density. The flag is set in a similar way to "
            'the "--data-file" flag. The argument can either be a '
            "float giving an ASD value, or a string containing a "
            "detector alias to produce noise from the design curve "
            "for that detector, or a string containing a path to a "
            "file with the noise curve for a detector. This can be "
            'used in conjunction with the "--detector" flag, e.g., '
            '"--detector H1 --fake-asd 1e-23", or without the '
            '"--detector" flag, e.g., "--fake-asd H1:1e-23". Values '
            "for multiple detectors can be passed by repeated use "
            "of the flag, noting that if used in conjunction with "
            'the "--detector" flag detectors and ASD values should '
            'be added in the same order, e.g., "--detector H1 '
            '--fake-asd H1 --detector L1 --fake-asd L1". This flag '
            'is ignored if "--data-file" values for the same '
            "detector have already been passed. The fake data that "
            "is produced is assumed to be that for a signal at "
            "twice the source rotation frequency. To explicitly set "
            "fake data at once or twice the rotation frequency "
            'use the "--fake-asd-1f" and "--fake-asd-2f" flags '
            "instead."
        ),
    )
    simparser.add(
        "--fake-asd-1f",
        action="append",
        help=(
            "This flag sets the data to be Gaussian noise "
            "explicitly for a source emitting at the rotation "
            'frequency. See the documentation for "--fake-asd" for '
            "details of its use."
        ),
    )
    simparser.add(
        "--fake-asd-2f",
        action="append",
        help=(
            "This flag sets the data to be Gaussian noise "
            "explicitly for a source emitting at twice the rotation "
            'frequency. See the documentation for "--fake-asd" for '
            "details of its use."
        ),
    )
    simparser.add(
        "--fake-sigma",
        action="append",
        help=(
            'This flag is equivalent to "--fake-asd", but '
            "instead of taking in an amplitude spectral density "
            "value it takes in a noise standard deviation."
        ),
    )
    simparser.add(
        "--fake-sigma-1f",
        action="append",
        help=(
            'This flag is equivalent to "--fake-asd-1f", but '
            "instead of taking in an amplitude spectral density "
            "value it takes in a noise standard deviation."
        ),
    )
    simparser.add(
        "--fake-sigma-2f",
        action="append",
        help=(
            'This flag is equivalent to "--fake-asd-2f", but '
            "instead of taking in an amplitude spectral density "
            "value it takes in a noise standard deviation."
        ),
    )
    simparser.add(
        "--fake-start",
        action="append",
        help=(
            "The GPS start time for generating simulated noise "
            "data. This be added for each detector in the same way "
            'as used in the "--fake-asd" command (default: '
            "1000000000)."
        ),
    )
    simparser.add(
        "--fake-end",
        action="append",
        help=(
            "The GPS end time for generating simulated noise data. "
            "This be added for each detector in the same way as "
            'used in the "--fake-asd" command (default: '
            "1000086400)"
        ),
    )
    simparser.add(
        "--fake-dt",
        action="append",
        help=(
            "The time step for generating simulated noise data. "
            "This be added for each detector in the same way as "
            'used in the "--fake-asd" command (default: 60)'
        ),
    )
    simparser.add(
        "--fake-seed",
        type=int,
        help=(
            "A positive integer random number generator seed used "
            "when generating the simulated data noise."
        ),
    )

    outputparser = parser.add_argument_group("Output")
    outputparser.add("-o", "--outdir", help="The output directory for the results")
    outputparser.add("-l", "--label", help="The output filename label for the results")
    outputparser.add(
        "--output-snr",
        action="store_true",
        default=False,
        help=(
            "Set this flag to output the maximum likelihood and maximum "
            "a-posteriori recovered signal-to-noise ratio. If adding "
            "an injection this will also output the injected signal SNR. "
            "These values will be output to a JSON file in the supplied "
            "output directory, and using the supplied label, with a file "
            "extension of '.snr'."
        ),
    )

    samplerparser = parser.add_argument_group("Sampler inputs")
    samplerparser.add(
        "-s",
        "--sampler",
        default="dynesty",
        help=("The sampling algorithm to use bilby (default: " "%(default)s)"),
    )
    samplerparser.add(
        "--sampler-kwargs",
        help=(
            "The keyword arguments for running the sampler. This should be in "
            "the format of a standard Python dictionary and must be given "
            "within quotation marks, e.g., \"{'Nlive':1000}\"."
        ),
    )
    samplerparser.add(
        "--likelihood",
        default="studentst",
        help=(
            "The name of the likelihood function to use. This can be either "
            '"studentst" or "gaussian".'
        ),
    )
    samplerparser.add(
        "--numba",
        action="store_true",
        default=False,
        help=("Set this flag to use enable to likelihood calculation using " "numba."),
    )
    samplerparser.add(
        "--prior",
        type=str,
        required=True,
        help=(
            "The path to a bilby-style prior file defining the parameters to "
            "be estimated and their prior probability distributions."
        ),
    )
    samplerparser.add(
        "--grid",
        action="store_true",
        default=False,
        help=(
            "Set this flag to evaluate the posterior over a grid rather than "
            "using a stochastic sampling method."
        ),
    )
    samplerparser.add(
        "--grid-kwargs",
        help=(
            "The keyword arguments for running the posterior evaluation over "
            "a grid. This should be a the format of a standard Python "
            "dictionary, and must be given within quotation marks, "
            "e.g., \"{'grid_size':100}\"."
        ),
    )

    ephemparser = parser.add_argument_group("Solar System Ephemeris inputs")
    ephemparser.add(
        "--ephem-earth",
        type=str,
        help=(
            "The path to a file providing the Earth ephemeris. If "
            "not supplied, the code will attempt to automatically "
            "find the appropriate file."
        ),
    )
    ephemparser.add(
        "--ephem-sun",
        type=str,
        help=(
            "The path to a file providing the Sun ephemeris. If not "
            "supplied, the code will attempt to automatically find "
            "the appropriate file."
        ),
    )

    return parser


class PERunner(object):
    """
    Set up and run the known pulsar parameter estimation.

    Parameters
    ----------
    kwargs: dict
        A dictionary of analysis setup parameters.
    """

    def __init__(self, kwargs):
        self.set_parameters(kwargs)
        self.set_likelihood()

    def set_parameters(self, kwargs):
        """
        Set the run parameters and their defaults.

        Parameters
        ----------
        kwargs: dict
            Dictionary of run parameters.
        """

        if not isinstance(kwargs, dict):
            raise TypeError("Argument must be a dictionary")

        # remove any None keyword values
        for key in list(kwargs.keys()):
            if kwargs[key] is None:
                kwargs.pop(key)

        # keyword arguments for creating the HeterodynedData objects
        self.datakwargs = kwargs.get("data_kwargs", {})

        if "par_file" not in kwargs:
            raise KeyError("A pulsar parameter file must be provided")
        else:
            self.datakwargs["par"] = kwargs["par_file"]

        # injection parameters
        self.datakwargs.setdefault("injpar", kwargs.get("inj_par", None))
        self.datakwargs.setdefault(
            "inject", (False if self.datakwargs["injpar"] is None else True)
        )

        # get list of times at which to inject the signal
        self.datakwargs.setdefault("injtimes", kwargs.get("inj_times", None))
        try:
            self.datakwargs["injtimes"] = ast.literal_eval(self.datakwargs["injtimes"])
        except (ValueError, SyntaxError):
            pass

        if self.datakwargs["injtimes"] is not None:
            if not isinstance(self.datakwargs["injtimes"], (list, np.ndarray)):
                raise TypeError("Injection times must be a list")

        # get solar system ephemeris information if provided
        self.datakwargs.setdefault("ephemearth", kwargs.get("ephem_earth", None))
        self.datakwargs.setdefault("ephemsun", kwargs.get("ephem_sun", None))

        # data parameters
        if "detector" in kwargs:
            if isinstance(kwargs["detector"], str):
                detectors = [kwargs["detector"]]
            elif isinstance(kwargs["detector"], list):
                detectors = []
                for det in kwargs["detector"]:
                    try:
                        thisdet = det
                    except (ValueError, SyntaxError):
                        thisdet = det

                    if isinstance(det, str):
                        detectors.append(det)
                    else:
                        raise TypeError("Detector must be a string")
        else:
            detectors = None

        # empty heterodyned data object
        self.hetdata = MultiHeterodynedData()

        # set the heterodyned data structure
        resetdetectors = True if detectors is None else False
        if (
            "data_file" in kwargs
            or "data_file_1f" in kwargs
            or "data_file_2f" in kwargs
        ):
            data2f = []
            for kw in ["data_file", "data_file_2f"]:
                if kw in kwargs:
                    try:
                        data2f = convert_string_to_dict(kwargs[kw][0], kw)
                    except (
                        ValueError,
                        SyntaxError,
                        BilbyPipeError,
                        TypeError,
                        IndexError,
                        KeyError,
                    ):
                        data2f = kwargs[kw]
                    break

            data1f = []
            if "data_file_1f" in kwargs:
                try:
                    data1f = convert_string_to_dict(
                        kwargs["data_file_1f"][0], "data_file_1f"
                    )
                except (
                    ValueError,
                    SyntaxError,
                    BilbyPipeError,
                    TypeError,
                    IndexError,
                    KeyError,
                ):
                    data1f = kwargs["data_file_1f"]

            if isinstance(data2f, str):
                # make into a list
                data2f = [data2f]

            if isinstance(data1f, str):
                # make into a list
                data1f = [data1f]

            for freq, data in zip([1.0, 2.0], [data1f, data2f]):
                self.datakwargs["freqfactor"] = freq

                if isinstance(data, dict):
                    # make into a list
                    if detectors is None:
                        detectors = list(data.keys())
                    else:
                        for det in data.keys():
                            if det not in detectors:
                                data.pop(det)

                    data = list(data.values())

                if isinstance(data, list):
                    # pass through list and check strings
                    for i, dfile in enumerate(data):
                        detdata = dfile.split(":")  # split detector and path

                        if len(detdata) == 2:
                            if detectors is not None:
                                if detdata[0] not in detectors:
                                    raise ValueError(
                                        "Data file does not have consistent detector"
                                    )
                            thisdet = detdata[0]
                            thisdata = detdata[1]
                        elif len(detdata) == 1 and detectors is not None:
                            try:
                                thisdet = detectors[i]
                            except Exception as e:
                                raise ValueError(
                                    "Detectors is not a list: {}".format(e)
                                )
                            thisdata = dfile
                        else:
                            raise ValueError(
                                "Data string must be of the form 'DET:FILEPATH'"
                            )

                        self.hetdata.add_data(
                            HeterodynedData(
                                data=thisdata, detector=thisdet, **self.datakwargs
                            )
                        )
                else:
                    raise TypeError("Data files are not of a recognised type")

                # remove any detectors than are not requested
                if detectors is not None:
                    for det in list(self.hetdata.detectors):
                        if det not in detectors:
                            self.hetdata.pop(det)

        # set fake data
        detectors = None if resetdetectors else detectors
        if (
            "fake_asd" in kwargs
            or "fake_asd_1f" in kwargs
            or "fake_asd_2f" in kwargs
            or "fake_sigma" in kwargs
            or "fake_sigma_1f" in kwargs
            or "fake_sigma_2d" in kwargs
        ):

            starts = kwargs.get("fake_start", 1000000000)  # default start time
            ends = kwargs.get("fake_end", 1000086400)  # default end time
            dts = kwargs.get("fake_dt", 60)  # default time step
            ftimes = kwargs.get("fake_times", None)  # time array(s)
            fseed = kwargs.get("fake_seed", None)  # data seed

            fakeasd2f = []
            issigma2f = False
            for kw in ["fake_asd", "fake_asd_2f", "fake_sigma", "fake_sigma_2f"]:
                if kw in kwargs:
                    try:
                        fakeasd2f = convert_string_to_dict(kwargs[kw][0], kw)
                    except (
                        ValueError,
                        SyntaxError,
                        BilbyPipeError,
                        TypeError,
                        IndexError,
                        KeyError,
                    ):
                        fakeasd2f = kwargs[kw]
                    if "sigma" in kw:
                        issigma2f = True
                        break

            fakeasd1f = []
            issigma1f = False
            for kw in ["fake_asd_1f", "fake_sigma_1f"]:
                if kw in kwargs:
                    try:
                        fakeasd1f = convert_string_to_dict(kwargs[kw][0], kw)
                    except (
                        ValueError,
                        SyntaxError,
                        BilbyPipeError,
                        TypeError,
                        IndexError,
                        KeyError,
                    ):
                        fakeasd1f = kwargs[kw]
                    if "sigma" in kw:
                        issigma1f = True
                        break

            if isinstance(starts, str):
                try:
                    starts = convert_string_to_dict(starts[0], "fake_start")
                except (
                    ValueError,
                    SyntaxError,
                    BilbyPipeError,
                    TypeError,
                    IndexError,
                    KeyError,
                ):
                    pass

            if isinstance(ends, str):
                try:
                    ends = convert_string_to_dict(ends[0], "fake_end")
                except (
                    ValueError,
                    SyntaxError,
                    BilbyPipeError,
                    TypeError,
                    IndexError,
                    KeyError,
                ):
                    pass

            if isinstance(dts, str):
                try:
                    dts = convert_string_to_dict(dts[0], "fake_dt")
                except (
                    ValueError,
                    SyntaxError,
                    BilbyPipeError,
                    TypeError,
                    IndexError,
                    KeyError,
                ):
                    pass

            if isinstance(starts, int):
                if detectors is None:
                    starts = [starts]
                else:
                    starts = len(detectors) * [starts]

            if isinstance(ends, int):
                if detectors is None:
                    ends = [ends]
                else:
                    ends = len(detectors) * [ends]

            if isinstance(dts, int):
                if detectors is None:
                    dts = [dts]
                else:
                    dts = len(detectors) * [dts]

            if isinstance(ftimes, (np.ndarray, list)) or ftimes is None:
                if len(np.shape(ftimes)) == 1 or ftimes is None:
                    if detectors is None:
                        ftimes = [ftimes]
                    else:
                        ftimes = len(detectors) * [ftimes]

            if isinstance(fakeasd2f, (str, float)):
                # make into a list
                if detectors is None:
                    fakeasd2f = [fakeasd2f]
                else:
                    fakeasd2f = len(detectors) * [fakeasd2f]

            if isinstance(fakeasd1f, (str, float)):
                # make into a list
                if detectors is None:
                    fakeasd1f = [fakeasd1f]
                else:
                    fakeasd1f = len(detectors) * [fakeasd1f]

            # set random seed
            rstate = None
            if fseed is not None:
                rstate = np.random.RandomState(fseed)

            for freq, fakedata, issigma in zip(
                [1.0, 2.0], [fakeasd1f, fakeasd2f], [issigma1f, issigma2f]
            ):
                self.datakwargs["freqfactor"] = freq
                self.datakwargs["issigma"] = issigma
                self.datakwargs["fakeseed"] = rstate

                if isinstance(fakedata, dict):
                    # make into a list
                    if detectors is None:
                        detectors = list(fakedata.keys())
                    else:
                        for det in fakedata.keys():
                            if det not in detectors:
                                fakedata.pop(det)

                    fakedata = list(fakedata.values())

                if isinstance(starts, dict):
                    # make into a list
                    if list(starts.keys()) != detectors:
                        raise ValueError(
                            "Fake data start times do not "
                            "contain consistent detectors"
                        )
                    else:
                        starts = list(starts.values())

                if isinstance(ends, dict):
                    # make into a list
                    if list(ends.keys()) != detectors:
                        raise ValueError(
                            "Fake data end times do not contain consistent detectors"
                        )
                    else:
                        ends = list(ends.values())

                if isinstance(dts, dict):
                    # make into a list
                    if list(dts.keys()) != detectors:
                        raise ValueError(
                            "Fake data time steps do not "
                            "contain consistent detectors"
                        )
                    else:
                        dts = list(dts.values())

                if isinstance(ftimes, dict):
                    # make into a list
                    if list(ftimes.keys()) != detectors:
                        raise ValueError(
                            "Fake data time arrays do not "
                            "contain consistent detectors"
                        )
                    else:
                        ftimes = list(ftimes.values())

                if len(fakedata) > 0:
                    if len(starts) == 1 and len(fakedata) > 1:
                        starts = len(fakedata) * starts

                    if len(ends) == 1 and len(fakedata) > 1:
                        ends = len(fakedata) * ends

                    if len(dts) == 1 and len(fakedata) > 1:
                        dts = len(fakedata) * dts

                    if len(ftimes) == 1 and len(fakedata) > 1:
                        ftimes = len(fakedata) * ftimes

                    if (
                        len(fakedata) != len(starts)
                        or len(fakedata) != len(ends)
                        or len(fakedata) != len(dts)
                        or len(fakedata) != len(ftimes)
                    ):
                        raise ValueError(
                            "Fake data values and times are not consistent"
                        )

                if isinstance(fakedata, list):
                    # parse through list
                    detidx = 0
                    for fdata, start, end, dt, ftime in zip(
                        fakedata, starts, ends, dts, ftimes
                    ):
                        try:
                            # make sure value is a string so it can be "split"
                            detfdata = (
                                str(fdata).replace("'", "").replace('"', "").split(":")
                            )
                        except Exception as e:
                            raise TypeError(
                                "Fake data value is the wrong type: {}".format(e)
                            )

                        if ftime is None:
                            try:
                                # make sure values are strings so they can be
                                # "split"
                                detstart = str(start).split(":")
                                detend = str(end).split(":")
                                detdt = str(dt).split(":")
                            except Exception as e:
                                raise TypeError(
                                    "Fake time value is the wrong type: {}".format(e)
                                )

                        if len(detfdata) == 2:
                            if detectors is not None:
                                if detfdata[0] not in detectors:
                                    raise ValueError(
                                        "Fake data input does not have "
                                        "consistent detector"
                                    )

                            try:
                                asdval = float(detfdata[1])
                            except ValueError:
                                asdval = detfdata[1]

                            thisdet = detfdata[0]

                            # check if actual data already exists
                            if thisdet in self.hetdata.detectors:
                                for het in self.hetdata[thisdet]:
                                    if het.freq_factor == freq:
                                        # data already exists
                                        continue

                            if ftime is None:
                                for detcheck in [detstart, detend, detdt]:
                                    if len(detcheck) == 2:
                                        if detcheck[0] != thisdet:
                                            raise ValueError("Inconsistent detectors!")

                                try:
                                    int(detcheck[-1])
                                except ValueError:
                                    raise TypeError("Problematic type!")

                                ftime = np.arange(
                                    int(detstart[-1]), int(detend[-1]), int(detdt[-1])
                                )
                        elif len(detfdata) == 1:
                            if detectors is not None:
                                try:
                                    asdval = float(detfdata[0])
                                except ValueError:
                                    asdval = detfdata[0]

                                try:
                                    thisdet = detectors[detidx]
                                    detidx += 1
                                except Exception as e:
                                    raise ValueError(
                                        "Detectors is not a list: {}".format(e)
                                    )
                            else:
                                thisdet = detfdata[0]
                                asdval = detfdata[0]  # get ASD for the given detector

                            # check if actual data already exists
                            if thisdet in self.hetdata.detectors:
                                for het in self.hetdata[thisdet]:
                                    if het.freq_factor == freq:
                                        # data already exists
                                        continue

                            if ftime is None:
                                for detcheck in [detstart, detend, detdt]:
                                    if len(detcheck) == 2:
                                        if detcheck[0] != thisdet:
                                            raise ValueError("Inconsistent detectors!")

                                try:
                                    int(detcheck[-1])
                                except ValueError:
                                    raise TypeError("Problematic type!")

                                ftime = np.arange(
                                    int(detstart[-1]), int(detend[-1]), int(detdt[-1])
                                )
                        else:
                            raise ValueError(
                                "Fake data string must be of the form 'DET:ASD'"
                            )

                        self.hetdata.add_data(
                            HeterodynedData(
                                fakeasd=asdval,
                                detector=thisdet,
                                times=ftime,
                                **self.datakwargs
                            )
                        )
                else:
                    raise TypeError("Fake data not of the correct type")

        if len(self.hetdata) == 0:
            raise ValueError("No data has been supplied!")

        # sampler parameters
        self.sampler = kwargs.get("sampler", "dynesty")
        self.sampler_kwargs = kwargs.get("sampler_kwargs", {})
        if isinstance(self.sampler_kwargs, str):
            try:
                self.sampler_kwargs = ast.literal_eval(self.sampler_kwargs)
            except (ValueError, SyntaxError):
                raise ValueError("Unable to parse sampler keyword arguments")
        self.use_grid = kwargs.get("grid", False)
        self.grid_kwargs = kwargs.get("grid_kwargs", {})
        if isinstance(self.grid_kwargs, str):
            try:
                self.grid_kwargs = ast.literal_eval(self.grid_kwargs)
            except (ValueError, SyntaxError):
                raise ValueError("Unable to parse grid keyword arguments")
        self.likelihoodtype = kwargs.get("likelihood", "studentst")
        self.numba = kwargs.get("numba", False)
        self.prior = kwargs.get("prior", None)
        if not isinstance(self.prior, (str, dict, bilby.core.prior.PriorDict)):
            raise ValueError("The prior is not defined")
        else:
            try:
                self.prior = bilby.core.prior.PriorDict.from_json(self.prior)
            except Exception as e1:
                try:
                    self.prior = bilby.core.prior.PriorDict(self.prior)
                except Exception as e2:
                    raise RuntimeError(
                        "Problem setting prior dictionary: {}\n{}".format(e1, e2)
                    )

        # output parameters
        if "outdir" in kwargs:
            self.sampler_kwargs.setdefault("outdir", kwargs.get("outdir"))
        if "label" in kwargs:
            self.sampler_kwargs.setdefault("label", kwargs.get("label"))

        self.outputsnr = kwargs.get("output_snr", False)

        show_truths = kwargs.get("show_truths", False)
        if show_truths or self.outputsnr:
            # don't overwrite 'injection_parameters' is they are already defined
            if "injection_parameters" not in self.sampler_kwargs:
                if self.datakwargs["injpar"] is not None:
                    injpartmp = self.hetdata.to_list[0].injpar
                else:
                    injpartmp = self.hetdata.to_list[0].par

                # get "true" values of any parameters in the prior
                injtruths = {}
                for key in self.prior:
                    injtruths[key] = injpartmp[key.upper()]

                    # check iota and theta
                    if key.lower() in ["iota", "theta"]:
                        if (
                            injtruths[key] is None
                            and injpartmp["COS{}".format(key.upper())] is not None
                        ):
                            injtruths[key] = np.arccos(
                                injpartmp["COS{}".format(key.upper())]
                            )
                    elif key.lower() in ["cosiota", "costheta"]:
                        if (
                            injtruths[key] is None
                            and injpartmp[key[3:].upper()] is not None
                        ):
                            injtruths[key] = np.cos(injpartmp[key[3:].upper()])

                self.sampler_kwargs.update({"injection_parameters": injtruths})

        # set use_ratio to False by default
        if "use_ratio" not in self.sampler_kwargs:
            self.sampler_kwargs["use_ratio"] = False

        # turn off check_point_plot for dynesty by default
        if self.sampler == "dynesty" and "check_point_plot" not in self.sampler_kwargs:
            self.sampler_kwargs["check_point_plot"] = False

        # default restart time to 1000000 seconds if not running through CLI
        self.periodic_restart_time = kwargs.get("periodic_restart_time", 10000000)

    def set_likelihood(self):
        """
        Set the likelihood function.
        """

        self.likelihood = TargetedPulsarLikelihood(
            data=self.hetdata,
            priors=self.prior,
            likelihood=self.likelihoodtype,
            numba=self.numba,
        )

    def run_sampler(self):
        """
        Run bilby to sample the posterior.

        Returns
        -------
        res
            A bilby Results object.
        """

        # restart the job after 10800 seconds (for if running on Condor to
        # prevent hard evictions)
        signal.signal(signal.SIGALRM, handler=sighandler)
        signal.alarm(self.periodic_restart_time)

        self.result = bilby.run_sampler(
            sampler=self.sampler,
            priors=self.prior,
            likelihood=self.likelihood,
            **self.sampler_kwargs
        )

        # output SNRs
        if self.outputsnr:
            snrs = {}

            if self.datakwargs["inject"]:
                snrs["Injected SNR"] = self.hetdata.injection_snr

            # set recovered parameters
            sourcepars = PulsarParametersPy(self.datakwargs["par"])
            maxlikeidx = self.result.posterior.log_likelihood.idxmax()
            maxpostidx = (
                self.result.posterior.log_likelihood + self.result.posterior.log_prior
            ).idxmax()
            for snrstr, idx in zip(
                ["Maximum likelihood SNR", "Maximum a-posteriori SNR"],
                [maxlikeidx, maxpostidx],
            ):
                for item in self.prior:
                    # NOTE: at the moment this will not work correctly if you
                    # have searched over parameters that are converted to their
                    # SI uints
                    sourcepars[item.upper()] = self.result.posterior[item][idx]

                snrs[snrstr] = self.hetdata.signal_snr(sourcepars)

            with open(
                os.path.join(
                    self.sampler_kwargs["outdir"],
                    "{}.snr".format(self.sampler_kwargs["label"]),
                ),
                "w",
            ) as fp:
                json.dump(snrs, fp, indent=2)

        return self.result

    def run_grid(self):
        """
        Run the sampling over a grid in parameter space.

        Returns
        -------
        grid
            A bilby Grid object.
        """

        self.grid = bilby.core.grid.Grid(
            likelihood=self.likelihood, priors=self.prior, **self.grid_kwargs
        )

        return self.grid


def pe(**kwargs):
    """
    Run PE within Python.

    Parameters
    ----------
    par_file: str
        The path to a TEMPO(2) style pulsar parameter file for the source.
    inj_par: str
        The path to a TEMPO(2) style pulsar parameter file containing the
        parameters of a simulated signal to be injected into the data. If
        this is not given a simulated signal will not be added.
    detector: str, list
        A string, or list of strings, containing the abbreviated names for
        the detectors being analysed (e.g., "H1", "L1", "V1").
    data_file: str, list, dict
        A string, list, or dictionary contain paths to the heterodyned data
        to be used in the analysis. For a single detector this can be a single
        string. For multiple detectors a list can be passed with the file path
        for each detector given in the same order as the list passed to the
        ``detector`` argument, or as a dictionary with each file path keyed to
        the associated detector. in the latter case the ``detector`` keyword
        argument is not required, unless wanting to analyse fewer detectors
        than passed. This data is assumed to have been heterodyned at twice the
        source's rotation frequency - to explicitly add data heterodyned at
        once or twice the source's rotation frequency use the ``data_file_1f``
        and ``data_file_2f`` arguments.
    data_file_2f: str, list, dict
        Data files that have been heterodyned at twice the source's rotation
        frequency. See the documentation for ``data_file`` above for usage.
    data_file_1f: str, list, dict
        Data files that have been heterodyned at the source's rotation
        frequency. See the documentation for ``data_file`` above for usage.
    fake_asd: float, str, list, dict
        This specifies the creation of fake Gaussian data drawn from a
        distribution with a given noise amplitude spectral density (ASD). If
        passing a float (and set of ``detector``'s are specified), then this
        value is used when generating the noise for all detectors. If this is
        a string then it should give a detector alias, which specifies using
        the noise ASD for the design sensitivity curve of that detector, or it
        should give a path to a file containing a frequency series of the
        ASD. If a list, then this should be a different float or string for
        each supplied detector. If a dictionary, then this should be a set
        of floats or strings keyed to detector names. The simulated noise
        produced with this argument is assumed to be at twice the source
        rotation frequency. To explicitly specify fake data generation at once
        or twice the source rotation frequency use the equivalent
        ``fake_asd_1f`` and ``fake_asd_2f`` arguments respectively. If wanting
        to supply noise standard deviations rather than ASD use the
        ``fake_sigma`` arguments instead. This argument is ignored if
        ``data_file``'s are supplied.
    fake_asd_1f: float, str, list, dict
        Set the amplitude spectral density for fake noise generation at the
        source rotation frequency. See the ``fake_asd`` argument for usage.
    fake_asd_2f: float, str, list, dict
        Set the amplitude spectral density for fake noise generation at twice
        the source rotation frequency. See the ``fake_asd`` argument for usage.
    fake_sigma: float, str, list, dict
        Set the standard deviation for generating fake Gaussian noise. See the
        ``fake_asd`` argument for usage. The simulated noise produced with this
        argument is assumed to be at twice the source rotation frequency. To
        explicitly specify fake data generation at once or twice the source
        rotation frequency use the equivalent ``fake_sigma_1f`` and
        ``fake_sigma_2f`` arguments respectively.
    fake_sigma_1f: float, str, list, dict
        Set the noise standard deviation for fake noise generation at the
        source rotation frequency. See the ``fake_sigma`` argument for usage.
    fake_sigma_2f: float, str, list, dict
        Set the noise standard deviation for fake noise generation at twice
        the source rotation frequency. See the ``fake_sigma`` argument for usage.
    fake_start: int, list, dict
        The GPS start time for generating fake data. If requiring data at once
        and twice the rotation frequency for the same detector, then the same
        start time will be used for both frequencies.
    fake_end: int, list, dict
        The GPS end time for generating fake data. If requiring data at once
        and twice the rotation frequency for the same detector, then the same
        end time will be used for both frequencies.
    fake_dt: int, list, dict:
        The time step in seconds for generating fake data. If requiring data at
        once and twice the rotation frequency for the same detector, then the
        same time step will be used for both frequencies.
    fake_times: dict, array_like
        Instead of passing start times, end times and time steps for the fake
        data generation, an array of GPS times (or a dictionary of arrays keyed
        to the detector) can be passed instead.
    fake_seed: int, :class:`numpy.random.RandomState`
        A seed for random number generation for the creation of fake data.
    data_kwargs: dict
        A dictionary of keyword arguments to pass to the
        :class:`cwinpy.data.HeterodynedData` objects.
    inj_times: list
        A list of pairs of times between which the simulated signal (if given
        with the ``inj_par`` argument) will be added to the data.
    sampler: str
        The sampling algorithm to use within bilby. The default is "dynesty".
    sampler_kwargs: dict
        A dictionary of keyword arguments to be used by the given sampler
        method.
    grid: bool
        If True then the posterior will be evaluated on a grid.
    grid_kwargs: dict
        A dictionary of keyword arguments to be used by the grid sampler.
    outdir: str
        The output directory for the results.
    label: str
        The name of the output file (excluding the '.json' extension) for the
        results.
    output_snr: bool,
        Set this flag to output the maximum likelihood and maximum a-posteriori
        recovered signal-to-noise ratio. If adding an injection this will also
        output the injected signal SNR. These values will be output to a JSON
        file in the supplied output directory, and using the supplied label,
        with a file extension of '.snr'. This defaults to False.
    likelihood: str
        The likelihood function to use. At the moment this can be either
        'studentst' or 'gaussian', with 'studentst' being the default.
    numba: bool
        Set whether to use the likelihood with numba enabled. Defaults to
        False.
    show_truths: bool
        If plotting the results, setting this argument will overplot the
        "true" signal values. If adding a simulated signal then these parameter
        values will be taken from the file specified by the "inj_par" argument,
        otherwise the values will be taken from the file specified by the
        "par_file" argument.
    prior: str, PriorDict
        A string to a bilby-style
        `prior <https://lscsoft.docs.ligo.org/bilby/prior.html>`_ file, or a
        bilby :class:`~bilby.core.prior.PriorDict` object. This defines the
        parameters that are to be estimated and their prior distributions.
    config: str
        The path to a configuration file containing the analysis arguments.
    periodic_restart_time: int
        The number of seconds after which the run will be evicted with a
        ``77`` exit code. This prevents hard evictions if running under
        HTCondor. For running via the command line interface, this defaults to
        43200 seconds (12 hours), at which point the job will be stopped (and
        then restarted if running under HTCondor). If running directly within
        Python this defaults to 10000000.
    ephem_earth: str, dict
        The path to a file providing the Earth ephemeris. If not supplied, the
        code will attempt to automatically find the appropriate file.
    ephem_sun: str, dict
        The path to a file providing the Sun ephemeris. If not supplied, the
        code will attempt to automatically find the appropriate file.
    """

    if "cli" in kwargs or "config" in kwargs:
        if "cli" in kwargs:
            kwargs.pop("cli")

        # get command line arguments
        parser = create_pe_parser()

        # parse config file or command line arguments
        if "config" in kwargs:
            cliargs = ["--config", kwargs["config"]]
        else:
            cliargs = sys.argv[1:]

        try:
            args, unknown_args = parse_args(cliargs, parser)
        except BilbyPipeError as e:
            raise IOError("{}".format(e))

        # convert args to a dictionary
        dargs = vars(args)

        if "config" in kwargs:
            # update with other keyword arguments
            dargs.update(kwargs)
    else:
        dargs = kwargs

    # set up the run
    runner = PERunner(dargs)

    # run the sampler (expect in testing)
    if runner.use_grid:
        runner.run_grid()
    elif not hasattr(cwinpy, "_called_from_test"):
        runner.run_sampler()

    return runner


def pe_cli(**kwargs):  # pragma: no cover
    """
    Entry point to ``cwinpy_pe script``. This just calls :func:`cwinpy.pe.pe`,
    but does not return any objects.
    """

    kwargs["cli"] = True  # set to show use of CLI
    _ = pe(**kwargs)


class PEDAGRunner(object):
    """
    Set up and run the known pulsar parameter estimation DAG.

    Parameters
    ----------
    config: :class:`configparser.ConfigParser`
          A :class:`configparser.ConfigParser` object with the analysis setup
          parameters.
    """

    def __init__(self, config, **kwargs):
        # create and build the dag
        self.create_dag(config, **kwargs)

    def create_dag(self, config, **kwargs):
        """
        Create the HTCondor DAG from the configuration parameters.

        Parameters
        ----------
        config: :class:`configparser.ConfigParser`
            A :class:`configparser.ConfigParser` object with the analysis setup
            parameters.
        """

        if not isinstance(config, configparser.ConfigParser):
            raise TypeError("'config' must be a ConfigParser object")

        inputs = PEInput(config)

        if "dag" in kwargs:
            # get a previously created DAG if given (for example for a full
            # analysis pipeline)
            self.dag = kwargs["dag"]
        else:
            self.dag = Dag(inputs)

        # get whether to build the dag
        self.build = config.getboolean("dag", "build", fallback=True)

        # get whether to automatically submit the dag
        self.submitdag = config.getboolean("dag", "submitdag", fallback=False)

        # get any additional submission options
        self.submit_options = config.get("dag", "submit_options", fallback=None)

        # create configurations for each cwinpy_pe job
        if config.has_section("pe"):
            # get the paths to the pulsar parameter files
            parfiles = config.get("pe", "pulsars", fallback=None)

            if parfiles is None:
                raise ValueError(
                    "Configuration must contain a set of pulsar parameter files"
                )

            # the "pulsars" option in the [pe] section can either be:
            #  - the path to a single file
            #  - a list of parameter files
            #  - a directory (or glob-able directory pattern) containing parameter files
            #  - a combination of a list of directories and/or files
            # All files must have the extension '.par'
            parfiles = self.eval(parfiles)
            if not isinstance(parfiles, list):
                parfiles = [parfiles]

            pulsars = []
            for parfile in parfiles:
                # add "*.par" wildcard to any directories
                if os.path.isdir(parfile):
                    parfile = os.path.join(parfile, "*.par")

                # get all parameter files
                pulsars.extend(
                    [
                        par
                        for par in glob.glob(parfile)
                        if os.path.splitext(par)[1] == ".par"
                    ]
                )

            # get names of all the pulsars
            pulsardict = {}
            for pulsar in list(pulsars):
                if is_par_file(pulsar):
                    psr = PulsarParametersPy(pulsar)

                    # try names with order of precedence
                    names = [
                        psr[name]
                        for name in ["PSRJ", "PSRB", "PSR", "NAME"]
                        if psr[name] is not None
                    ]
                    if len(names) > 0:
                        pulsardict[names[0]] = pulsar
                    else:
                        warnings.warn(
                            "Parameter file '{}' has no name, so it will be "
                            "ignored".format(pulsar)
                        )

            # the "injections" option in the [pe] section can be specified
            # in the same way as the "pulsars" option
            # get paths to pulsar injection files
            injfiles = config.get("pe", "injections", fallback=None)
            if injfiles is not None:
                injfiles = self.eval(injfiles)
                if not isinstance(injfiles, list):
                    injfiles = [injfiles]

                injections = []
                for injfile in injfiles:
                    # add "*.par" wildcard to any directories
                    if os.path.isdir(injfile):
                        injfile = os.path.join(injfile, "*.par")

                    # get all parameter files
                    injections.extend(
                        [
                            inj
                            for inj in glob.glob(injfile)
                            if os.path.splitext(inj)[1] == ".par"
                        ]
                    )

                injdict = {}
                for inj in injections:
                    if is_par_file(inj):
                        psr = PulsarParametersPy(inj)

                        # try names with order or precedence
                        names = [
                            psr[name]
                            for name in ["PSRJ", "PSRB", "PSR", "NAME"]
                            if psr[name] is not None
                        ]
                        if len(names) > 0:
                            injdict[names[0]] = inj
                        else:
                            warnings.warn(
                                "Parameter file '{}' has no name, so it will "
                                "be ignored".format(inj)
                            )

            # the "data-file-1f" and "data-file-2f" options in the [pe]
            # section specify the locations of heterodyned data files at the
            # rotation frequency and twice the rotation frequency of each
            # source. It is expected that the heterodyned file names
            # contain the name of the pulsar (based on the "PSRJ" name in the
            # associated parameter file). The option should be a dictionary
            # with keys being the detector name for the data sets. If a
            # "data-file" option is given it is assumed to be for data at twice
            # the rotation frequency.
            datafiles1f = config.get("pe", "data-file-1f", fallback=None)
            datafiles2fdefault = config.get("pe", "data-file", fallback=None)
            datafiles2f = config.get("pe", "data-file-2f", fallback=datafiles2fdefault)

            # the "fake-asd-1f" and "fake-asd-2f" options in the [pe]
            # section specify amplitude spectral densities with which to
            # generate simulated Gaussian data for a given detector. If this is
            # a list of detectors then the design ASDs for the given detectors
            # will be used, otherwise it should be a dictionary keyed to
            # detector names, each giving an ASD value, or file from which the
            # ASD can be read. If a "fake-asd" option is given it is assumed to
            # be for data at twice the rotation frequency.
            fakeasd1f = config.get("pe", "fake-asd-1f", fallback=None)
            fakeasd2fdefault = config.get("pe", "fake-asd", fallback=None)
            fakeasd2f = config.get("pe", "fake-asd-2f", fallback=fakeasd2fdefault)
            simdata = {}

            if datafiles1f is not None or datafiles2f is not None:
                detectors1f = None
                if datafiles1f is not None:
                    datafiles1f = self.eval(datafiles1f)

                    if not isinstance(datafiles1f, dict):
                        raise TypeError("Data files must be specified in a dictionary")

                    detectors1f = sorted(list(datafiles1f.keys()))

                detectors2f = None
                if datafiles2f is not None:
                    datafiles2f = self.eval(datafiles2f)

                    if not isinstance(datafiles2f, dict):
                        raise TypeError("Data files must be specified in a dictionary")

                    detectors2f = sorted(list(datafiles2f.keys()))

                if detectors1f != detectors2f and datafiles1f and datafiles2f:
                    raise IOError("Inconsistent detectors given for data sets")

                detectors = detectors2f if detectors2f else detectors1f

                # get lists of data files. For each detector the passed files could
                # be a single file, a list of files, a glob-able directory path
                # containing the files, or a dictionary keyed to the pulsar names.
                datadict = {pname: {} for pname in pulsardict.keys()}

                for datafilesf, freqfactor in zip(
                    [datafiles1f, datafiles2f], ["1f", "2f"]
                ):
                    if datafilesf is None:
                        continue
                    else:
                        for pname in pulsardict.keys():
                            datadict[pname][freqfactor] = {}

                    for det in detectors:
                        dff = []
                        datafiles = datafilesf[det]

                        if isinstance(datafiles, dict):
                            # dictionary of files, with one for each pulsar
                            for pname in pulsardict.keys():
                                if pname in datafiles:
                                    datadict[pname][freqfactor][det] = datafiles[pname]
                            continue

                        if not isinstance(datafiles, list):
                            datafiles = [datafiles]

                        for datafile in datafiles:
                            # add "*" wildcard to any directories
                            if os.path.isdir(datafile):
                                datafile = os.path.join(datafile, "*")

                            # get all data files
                            dff.extend(
                                [
                                    dat
                                    for dat in glob.glob(datafile)
                                    if os.path.isfile(dat)
                                ]
                            )

                        if len(dff) == 0:
                            raise ValueError("No data files found!")

                        # check file name contains the name of a supplied pulsar
                        for pname in pulsardict:
                            for datafile in dff:
                                if pname in datafile:
                                    if det not in datadict[pname][freqfactor]:
                                        datadict[pname][freqfactor][det] = datafile
                                    else:
                                        print(
                                            "Duplicate pulsar '{}' data. Ignoring "
                                            "duplicate.".format(pname)
                                        )
            elif fakeasd1f is not None or fakeasd2f is not None:
                # set to use simulated data
                if fakeasd1f is not None:
                    simdata["1f"] = self.eval(fakeasd1f)

                if fakeasd2f is not None:
                    simdata["2f"] = self.eval(fakeasd2f)
            else:
                raise IOError("No data set for use")

            if simdata:
                # get the start time, end time and time step if given
                fakestart = config.get("pe", "fake-start", fallback=None)
                fakeend = config.get("pe", "fake-end", fallback=None)
                fakedt = config.get("pe", "fake-dt", fallback=None)

            # set some default bilby-style priors
            DEFAULTPRIORS2F = (
                "h0 = Uniform(minimum=0.0, maximum=1.0e-22, name='h0', latex_label='$h_0$')\n"
                "phi0 = Uniform(minimum=0.0, maximum={pi}, name='phi0', latex_label='$\\phi_0$', unit='rad')\n"
                "iota = Sine(minimum=0.0, maximum={pi}, name='iota', latex_label='$\\iota$, unit='rad')\n"
                "psi = Uniform(minimum=0.0, maximum={pi_2}, name='psi', latex_label='$\\psi$, unit='rad')\n"
            ).format(**{"pi": np.pi, "pi_2": (np.pi / 2.0)})

            DEFAULTPRIORS1F = (
                "c21 = Uniform(minimum=0.0, maximum=1.0e-22, name='c21', latex_label='$C_{{21}}$')\n"
                "phi21 = Uniform(minimum=0.0, maximum={2pi}, name='phi21', latex_label='$\\Phi_{{21}}$', unit='rad')\n"
                "iota = Sine(minimum=0.0, maximum={pi}, name='iota', latex_label='$\\iota$, unit='rad')\n"
                "psi = Uniform(minimum=0.0, maximum={pi_2}, name='psi', latex_label='$\\psi$, unit='rad')\n"
            ).format(**{"2pi": 2.0 * np.pi, "pi": np.pi, "pi_2": (np.pi / 2.0)})

            DEFAULTPRIORS1F2F = (
                "c21 = Uniform(minimum=0.0, maximum=1.0e-22, name='c21', latex_label='$C_{{21}}$')\n"
                "c22 = Uniform(minimum=0.0, maximum=1.0e-22, name='c22', latex_label='$C_{{22}}$')\n"
                "phi21 = Uniform(minimum=0.0, maximum={2pi}, name='phi21', latex_label='$\\Phi_{{21}}$', unit='rad')\n"
                "phi22 = Uniform(minimum=0.0, maximum={2pi}, name='phi22', latex_label='$\\Phi_{{22}}$', unit='rad')\n"
                "iota = Sine(minimum=0.0, maximum={pi}, name='iota', latex_label='$\\iota$, unit='rad')\n"
                "psi = Uniform(minimum=0.0, maximum={pi_2}, name='psi', latex_label='$\\psi$, unit='rad')\n"
            ).format(**{"2pi": 2.0 * np.pi, "pi": np.pi, "pi_2": (np.pi / 2.0)})

            # get priors (if none are specified use the defaults)
            priors = config.get("pe", "priors", fallback=None)

            # "priors" can be a file, list of files, directory containing files,
            # glob-able path pattern to a set of files, or a dictionary of files
            # keyed to pulsar names. If all case bar a single file, or a
            # dictionary of keyed files, it is expected that the prior file name
            # contains the PSRJ name of the associated pulsar.
            if priors is not None:
                priors = self.eval(priors)

                if isinstance(priors, dict):
                    priorfiles = priors
                else:
                    if isinstance(priors, list):
                        allpriors = []
                        for priorfile in priors:
                            # add "*" wildcard to directories
                            if os.path.isdir(priorfile):
                                priorfile = os.path.join(priorfile, "*")

                            # get all prior files
                            allpriors.extend([pf for pf in glob.glob(priorfile)])

                        # sort allpriors by base filename (to hopefully avoid clashes)
                        allpriors = [
                            pfs[1]
                            for pfs in sorted(
                                zip(
                                    [os.path.basename(pf) for pf in allpriors],
                                    allpriors,
                                )
                            )
                        ]

                        priorfiles = {}
                        for pname in pulsardict.keys():
                            for i, priorfile in enumerate(list(allpriors)):
                                if pname in priorfile:
                                    if pname not in priorfiles:
                                        priorfiles[pname] = priorfile
                                        del allpriors[i]
                                        break
                                    else:
                                        warnings.warn(
                                            "Duplicate prior '{}' data. Ignoring "
                                            "duplicate.".format(pname)
                                        )
                    elif isinstance(priors, str):
                        if os.path.isfile(priors):
                            priorfiles = {psr: priors for psr in pulsardict.keys()}
                        elif os.path.isdir(priors):
                            # add * wildcard to directories (if not already present)
                            if priors[-1] != "*":
                                priorfile = os.path.join(priors, "*")
                            else:
                                priorfile = priors
                            allpriors = [pf for pf in glob.glob(priorfile)]

                            # sort allpriors by base filename (to hopefully avoid clashes)
                            allpriors = [
                                pfs[1]
                                for pfs in sorted(
                                    zip(
                                        [os.path.basename(pf) for pf in allpriors],
                                        allpriors,
                                    )
                                )
                            ]

                            priorfiles = {}
                            for pname in pulsardict.keys():
                                for i, priorfile in enumerate(list(allpriors)):
                                    if pname in priorfile:
                                        if pname not in priorfiles:
                                            priorfiles[pname] = priorfile
                                            del allpriors[i]
                                            break
                                        else:
                                            warnings.warn(
                                                "Duplicate prior '{}' data. Ignoring "
                                                "duplicate.".format(pname)
                                            )
                        else:
                            raise ValueError(
                                "Prior file '{}' does not exist".format(priors)
                            )
                    else:
                        raise TypeError("Prior type is no recognised")
            else:
                # use default priors
                priorfile = os.path.join(inputs.outdir, "prior.txt")

                with open(priorfile, "w") as fp:
                    if datafiles1f is not None and datafiles2f is not None:
                        fp.write(DEFAULTPRIORS1F2F)
                    elif datafiles2f is not None:
                        fp.write(DEFAULTPRIORS2F)
                    else:
                        fp.write(DEFAULTPRIORS1F)

                priorfiles = {psr: priorfile for psr in pulsardict.keys()}

            # check prior and data exist for the same pulsar, if not remove
            priornames = list(priorfiles.keys())
            datanames = list(datadict.keys()) if not simdata else priornames

            for pname in list(pulsardict.keys()):
                if pname in priornames and pname in datanames:
                    continue
                else:
                    print(
                        "Removing pulsar '{}' as either no data, or no prior "
                        "is given".format(pname)
                    )
                    if pname in datanames:
                        datadict.pop(pname)
                    if pname in priornames:
                        priorfiles.pop(pname)

                    if pname in pulsardict:
                        pulsardict.pop(pname)

            # output the SNRs (injected and recovered)
            outputsnr = config.getboolean("pe", "output_snr", fallback=False)

            # get the sampler (default is dynesty)
            sampler = config.get("pe", "sampler", fallback="dynesty")

            # get the sampler keyword arguments
            samplerkwargs = config.get("pe", "sampler_kwargs", fallback=None)

            # get whether to use numba
            numba = config.getboolean("pe", "numba", fallback=False)

            # get ephemeris files if given
            earthephem = self.eval(config.get("pe", "ephem-earth", fallback=None))
            sunephem = self.eval(config.get("pe", "ephem-sun", fallback=None))
        else:
            raise IOError("Configuration file must have a [pe] section.")

        if len(pulsardict) == 0:
            raise ValueError("No pulsars have been specified!")

        # create jobs (output and label set using pulsar name)
        for pname in pulsardict:
            # create dictionary of configuration outputs
            configdict = {}

            configdict["par_file"] = pulsardict[pname]

            # data file(s)
            for freqfactor in ["1f", "2f"]:
                if not simdata:
                    try:
                        configdict["data_file_{}".format(freqfactor)] = datadict[pname][
                            freqfactor
                        ]
                    except KeyError:
                        pass
                else:
                    try:
                        configdict["fake_asd_{}".format(freqfactor)] = str(
                            ["{}".format(det) for det in simdata[freqfactor]]
                        )
                    except KeyError:
                        pass

            # add injection if given
            if injfiles is not None:
                if pname in injdict:
                    configdict["inj_par"] = injdict[pname]

            configdict["prior"] = priorfiles[pname]
            configdict["sampler"] = sampler
            configdict["numba"] = numba

            if samplerkwargs is not None:
                configdict["sampler_kwargs"] = samplerkwargs

            if outputsnr:
                configdict["output_snr"] = "True"

            for ephem, ephemname in zip(
                [earthephem, sunephem], ["ephem_earth", "ephem_sun"]
            ):
                if ephem is not None:
                    if isinstance(ephem, dict):
                        if pname in ephem:
                            configdict[ephemname] = ephem[pname]
                    elif isinstance(ephem, str):
                        configdict[ephemname] = ephem
                    else:
                        raise TypeError(
                            "Ephemeris file for {} is not a string".format(pname)
                        )

            if simdata and inputs.n_parallel > 1:
                # set a fake seed, so all parallel runs produce the same data
                seed = np.random.randint(1, 2 ** 32 - 1)
                configdict["fake_seed"] = str(seed)

            if simdata:
                if (fakestart is None and fakeend is not None) or (
                    fakestart is not None and fakeend is None
                ):
                    raise ValueError("'fake-start' and 'fake-end' must both be set")
                else:
                    if fakestart is not None:
                        configdict["fake_start"] = fakestart
                    if fakeend is not None:
                        configdict["fake_end"] = fakeend
                if fakedt is not None:
                    configdict["fake_dt"] = fakedt

            parallel_node_list = []
            for idx in range(inputs.n_parallel):
                penode = PulsarPENode(inputs, configdict.copy(), pname, idx, self.dag)
                parallel_node_list.append(penode)

            if inputs.n_parallel > 1:
                _ = MergeNode(inputs, parallel_node_list, self.dag)

        if self.build:
            self.dag.build()

    def eval(self, arg):
        """
        Try and evaluate a string using :func:`ast.literal_eval`.

        Parameters
        ----------
        arg: str
            A string to be evaluated.

        Returns
        -------
        object:
            The evaluated object, or original string, if not able to be evaluated.
        """

        # copy of string
        newobj = str(arg)

        try:
            newobj = ast.literal_eval(newobj)
        except (ValueError, SyntaxError):
            pass

        return newobj


def pe_dag(**kwargs):
    """
    Run pe_dag within Python. This will create a `HTCondor <https://research.cs.wisc.edu/htcondor/>`_
    DAG for running multiple ``cwinpy_pe`` instances on a computer cluster.

    Parameters
    ----------
    config: str
        A configuration file, or :class:`configparser:ConfigParser` object,
        for the analysis.

    Returns
    -------
    dag:
        The pycondor :class:`pycondor.Dagman` object.
    """

    if "config" in kwargs:
        configfile = kwargs.pop("config")
    else:  # pragma: no cover
        parser = ArgumentParser(
            description=(
                "A script to create a HTCondor DAG to run Bayesian inference to "
                "estimate the parameters of continuous gravitational-wave signals "
                "from a selection of known pulsars."
            )
        )
        parser.add_argument("config", help=("The configuration file for the analysis"))

        args = parser.parse_args()
        configfile = args.config

    if isinstance(configfile, configparser.ConfigParser):
        config = configfile
    else:
        config = configparser.ConfigParser()

        try:
            config.read_file(open(configfile, "r"))
        except Exception as e:
            raise IOError(
                "Problem reading configuration file '{}'\n: {}".format(configfile, e)
            )

    return PEDAGRunner(config, **kwargs)


def pe_dag_cli(**kwargs):  # pragma: no cover
    """
    Entry point to the cwinpy_pe_dag script. This just calls
    :func:`cwinpy.pe.pe_dag`, but does not return any objects.
    """

    _ = pe_dag(**kwargs)


class PEInput(Input):
    def __init__(self, cf):
        """
        Class that sets inputs for the DAG and analysis node generation.

        Parameters
        ----------
        cf: :class:`configparser.ConfigParser`
            The configuration file for the DAG set up.
        """

        self.config = cf
        self.submit = cf.getboolean("dag", "submitdag", fallback=False)
        self.transfer_files = cf.getboolean("dag", "transfer-files", fallback=True)
        self.osg = cf.getboolean("dag", "osg", fallback=False)
        self.label = cf.get("dag", "name", fallback="cwinpy_pe")

        # see bilby_pipe MainInput class
        self.scheduler = cf.get("dag", "scheduler", fallback="condor")
        self.scheduler_args = cf.get("dag", "scheduler_args", fallback=None)
        self.scheduler_module = cf.get("dag", "scheduler_module", fallback=None)
        self.scheduler_env = cf.get("dag", "scheduler_env", fallback=None)
        self.scheduler_analysis_time = cf.get(
            "dag", "scheduler_analysis_time", fallback="7-00:00:00"
        )

        self.outdir = cf.get("run", "basedir", fallback=os.getcwd())

        self.universe = cf.get("job", "universe", fallback="vanilla")
        self.getenv = cf.getboolean("job", "getenv", fallback=False)
        self.pe_log_directory = cf.get(
            "job", "log", fallback=os.path.join(os.path.abspath(self._outdir), "log")
        )
        self.request_memory = cf.get("job", "request_memory", fallback="4 GB")
        self.request_cpus = cf.getint("job", "request_cpus", fallback=1)
        self.accounting = cf.get(
            "job", "accounting_group", fallback="cwinpy"
        )  # cwinpy is a dummy tag
        self.accounting_user = cf.get("job", "accounting_group_user", fallback=None)
        requirements = cf.get("job", "requirements", fallback=None)
        self.requirements = [requirements] if requirements else []
        self.retry = cf.getint("job", "retry", fallback=0)
        self.notification = cf.get("job", "notification", fallback="Never")
        self.email = cf.get("job", "email", fallback=None)
        self.condor_job_priority = cf.getint("job", "condor_job_priority", fallback=0)

        # number of parallel runs for each job
        self.n_parallel = cf.getint("pe", "n_parallel", fallback=1)
        self.sampler_kwargs = cf.get("pe", "sampler_kwargs", fallback=None)

        # needs to be set for the bilby_pipe Node initialisation, but is not a
        # requirement for cwinpy_pe
        self.online_pe = False
        self.extra_lines = []
        self.run_local = False

    @property
    def submit_directory(self):
        subdir = self.config.get(
            "dag", "submit", fallback=os.path.join(self._outdir, "submit")
        )
        check_directory_exists_and_if_not_mkdir(subdir)
        return subdir

    @property
    def initialdir(self):
        if hasattr(self, "_initialdir"):
            if self._initialdir is not None:
                return self._initialdir
            else:
                return os.getcwd()
        else:
            return os.getcwd()

    @initialdir.setter
    def initialdir(self, initialdir):
        if isinstance(initialdir, str):
            self._initialdir = initialdir
        else:
            self._initialdir = None


class PulsarPENode(Node):
    def __init__(
        self, inputs, configdict, psrname, parallel_idx, dag, generation_node=None
    ):
        super().__init__(inputs)
        self.dag = dag

        self.parallel_idx = parallel_idx
        self.request_cpus = inputs.request_cpus
        self.retry = inputs.retry
        self.getenv = inputs.getenv
        self._universe = inputs.universe

        self.psrname = psrname

        resdir = inputs.config.get("pe", "results", fallback="results")
        self.psrbase = os.path.join(inputs.outdir, resdir, psrname)
        if self.inputs.n_parallel > 1:
            self.resdir = os.path.join(self.psrbase, "par{}".format(parallel_idx))
        else:
            self.resdir = self.psrbase

        check_directory_exists_and_if_not_mkdir(self.resdir)
        configdict["outdir"] = self.resdir

        # job name prefix
        jobname = inputs.config.get("job", "name", fallback="cwinpy_pe")

        # replace any "+" in the pulsar name for the job name as Condor does
        # not allow "+"s in the name
        self.label = "{}_{}".format(jobname, psrname)
        self.base_job_name = "{}_{}".format(jobname, psrname.replace("+", "plus"))
        if inputs.n_parallel > 1:
            self.job_name = "{}_{}".format(self.base_job_name, parallel_idx)
            self.label = "{}_{}".format(self.label, parallel_idx)
        else:
            self.job_name = self.base_job_name

        configdict["label"] = self.label

        # output the configuration file
        configdir = inputs.config.get("pe", "config", fallback="configs")
        configlocation = os.path.join(inputs.outdir, configdir)
        check_directory_exists_and_if_not_mkdir(configlocation)
        if inputs.n_parallel > 1:
            configfile = os.path.join(
                configlocation, "{}_{}.ini".format(psrname, parallel_idx)
            )
        else:
            configfile = os.path.join(configlocation, "{}.ini".format(psrname))

        self.setup_arguments(
            add_ini=False, add_unknown_args=False, add_command_line_args=False
        )

        # add files for transfer
        if self.inputs.transfer_files or self.inputs.osg:
            tmpinitialdir = self.inputs.initialdir

            self.inputs.initialdir = self.resdir

            input_files_to_transfer = [
                self._relative_topdir(configfile, self.inputs.initialdir)
            ]

            # make paths relative
            for key in ["par_file", "inj_par", "data_file_1f", "data_file_2f", "prior"]:
                if key in list(configdict.keys()):
                    if key in ["data_file_1f", "data_file_2f"]:
                        for detkey in configdict[key]:
                            input_files_to_transfer.append(
                                self._relative_topdir(
                                    configdict[key][detkey], self.inputs.initialdir
                                )
                            )

                            # set to use only file as the transfer directory is flat
                            configdict[key][detkey] = os.path.basename(
                                configdict[key][detkey]
                            )
                    else:
                        input_files_to_transfer.append(
                            self._relative_topdir(
                                configdict[key], self.inputs.initialdir
                            )
                        )

                        # set to use only file as the transfer directory is flat
                        configdict[key] = os.path.basename(configdict[key])

            configdict["outdir"] = "results/"

            # add output directory to inputs in case resume file exists
            input_files_to_transfer.append(".")

            self.extra_lines.extend(
                self._condor_file_transfer_lines(
                    list(set(input_files_to_transfer)), [configdict["outdir"]]
                )
            )

            self.arguments.add("config", os.path.basename(configfile))
        else:
            tmpinitialdir = None
            self.arguments.add("config", configfile)

        self.extra_lines.extend(self._checkpoint_submit_lines())

        # add accounting user
        if self.inputs.accounting_user is not None:
            self.extra_lines.append(
                "accounting_group_user = {}".format(self.inputs.accounting_user)
            )

        parseobj = DefaultConfigFileParser()
        with open(configfile, "w") as fp:
            fp.write(parseobj.serialize(configdict))

        self.process_node()

        # reset initial directory
        if tmpinitialdir is not None:
            self.inputs.initialdir = tmpinitialdir

        if generation_node is not None:
            # This is for the future when implementing a full pipeline
            # the generation node will be, for example, a heterodyning job
            self.job.add_parent(generation_node.job)

    @property
    def executable(self):
        jobexec = self.inputs.config.get("job", "executable", fallback="cwinpy_pe")
        return self._get_executable_path(jobexec)

    @property
    def request_memory(self):
        return self.inputs.request_memory

    @property
    def log_directory(self):
        check_directory_exists_and_if_not_mkdir(self.inputs.pe_log_directory)
        return self.inputs.pe_log_directory

    @property
    def result_directory(self):
        """ The path to the directory where result output will be stored """
        check_directory_exists_and_if_not_mkdir(self.resdir)
        return self.resdir

    @property
    def result_file(self):
        extension = self.inputs.sampler_kwargs.get("save", "json")
        gzip = self.inputs.sampler_kwargs.get("gzip", False)
        return bilby.core.result.result_file_name(
            self.result_directory, self.label, extension=extension, gzip=gzip
        )

    @staticmethod
    def _relative_topdir(path, reference):
        """Returns the top-level directory name of a path relative
        to a reference
        """
        try:
            return os.path.relpath(path, reference)
        except ValueError as exc:
            exc.args = ("cannot format {} relative to {}".format(path, reference),)
            raise


class MergeNode(Node):
    def __init__(self, inputs, parallel_node_list, dag):
        super().__init__(inputs)
        self.dag = dag

        self.job_name = "{}_merge".format(parallel_node_list[0].base_job_name)

        jobname = inputs.config.get("job", "name", fallback="cwinpy_pe")
        self.label = "{}_{}".format(jobname, parallel_node_list[0].psrname)
        self.request_cpus = 1
        self.setup_arguments(
            add_ini=False, add_unknown_args=False, add_command_line_args=False
        )
        self.arguments.append("--result")
        for pn in parallel_node_list:
            self.arguments.append(pn.result_file)
        self.arguments.add("outdir", parallel_node_list[0].psrbase)
        self.arguments.add("label", self.label)
        self.arguments.add_flag("merge")

        extension = self.inputs.sampler_kwargs.get("save", "json")
        gzip = self.inputs.sampler_kwargs.get("gzip", False)
        self.arguments.add("extension", extension)
        if gzip:
            self.arguments.add_flag("gzip")

        self.process_node()
        for pn in parallel_node_list:
            self.job.add_parent(pn.job)

    @property
    def executable(self):
        return self._get_executable_path("bilby_result")

    @property
    def request_memory(self):
        return "16 GB"

    @property
    def log_directory(self):
        return self.inputs.pe_log_directory

    @property
    def result_file(self):
        extension = self.inputs.sampler_kwargs.get("save", "json")
        gzip = self.inputs.sampler_kwargs.get("gzip", False)
        return bilby.core.result.result_file_name(
            self.inputs.result_directory, self.label, extension=extension, gzip=gzip
        )
