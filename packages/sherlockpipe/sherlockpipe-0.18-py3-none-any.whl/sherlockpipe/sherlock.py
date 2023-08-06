import logging
import math
import multiprocessing
import shutil
import sys
import pandas
import wotan
import matplotlib.pyplot as plt
import transitleastsquares as tls
import lightkurve as lk
import numpy as np
import os
import sys

from scipy.ndimage import uniform_filter1d
from sherlockpipe.star.starinfo import StarInfo
from astropy import units as u
from sherlockpipe.curve_preparer.Flattener import Flattener
from sherlockpipe.curve_preparer.Flattener import FlattenInput
from sherlockpipe.objectinfo.MissionObjectInfo import MissionObjectInfo
from sherlockpipe.objectinfo.InputObjectInfo import InputObjectInfo
from sherlockpipe.objectinfo.MissionFfiIdObjectInfo import MissionFfiIdObjectInfo
from sherlockpipe.objectinfo.MissionInputObjectInfo import MissionInputObjectInfo
from sherlockpipe.objectinfo.MissionFfiCoordsObjectInfo import MissionFfiCoordsObjectInfo
from sherlockpipe.objectinfo.preparer.MissionFfiLightcurveBuilder import MissionFfiLightcurveBuilder
from sherlockpipe.objectinfo.preparer.MissionInputLightcurveBuilder import MissionInputLightcurveBuilder
from sherlockpipe.objectinfo.preparer.MissionLightcurveBuilder import MissionLightcurveBuilder
from sherlockpipe.objectinfo.InvalidNumberOfSectorsError import InvalidNumberOfSectorsError
from sherlockpipe.scoring.BasicSignalSelector import BasicSignalSelector
from sherlockpipe.scoring.SnrBorderCorrectedSignalSelector import SnrBorderCorrectedSignalSelector
from sherlockpipe.scoring.QuorumSnrBorderCorrectedSignalSelector import QuorumSnrBorderCorrectedSignalSelector
from sherlockpipe.ois.OisManager import OisManager
from sherlockpipe.search_zones.HabitableSearchZone import HabitableSearchZone
from sherlockpipe.search_zones.OptimisticHabitableSearchZone import OptimisticHabitableSearchZone
from sherlockpipe.star.HabitabilityCalculator import HabitabilityCalculator
from sherlockpipe.transitresult import TransitResult
from multiprocessing import Pool
from scipy.signal import argrelextrema, savgol_filter
from scipy.ndimage.interpolation import shift
from scipy import stats, signal
from wotan import flatten

from sherlockpipe.update import Updater


class Sherlock:
    """
    Main SHERLOCK PIPEline class to be used for loading input, setting up the running parameters and launch the
    analysis of the desired TESS, Kepler, K2 or csv objects light curves.
    """
    TOIS_CSV_URL = 'https://exofop.ipac.caltech.edu/tess/download_toi.php?sort=toi&output=csv'
    CTOIS_CSV_URL = 'https://exofop.ipac.caltech.edu/tess/download_ctoi.php?sort=ctoi&output=csv'
    KOIS_LIST_URL = 'https://exofop.ipac.caltech.edu/kepler/targets.php?sort=num-pc&page1=1&ipp1=100000&koi1=&koi2='
    KOI_TARGET_URL = 'https://exofop.ipac.caltech.edu/kepler/edit_target.php?id={$id}'
    KOI_TARGET_URL_NEW = 'https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=cumulative'
    EPIC_TARGET_URL_NEW = 'https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=k2candidates'
    MASK_MODES = ['mask', 'subtract']
    RESULTS_DIR = './'
    VALID_DETREND_METHODS = ["biweight", "gp"]
    VALID_PERIODIC_DETREND_METHODS = ["biweight", "gp", "cosine", "cofiam"]
    VALID_SIGNAL_SELECTORS = ["basic", "border-correct", "quorum"]
    NUM_CORES = multiprocessing.cpu_count() - 1
    TOIS_CSV = RESULTS_DIR + 'tois.csv'
    CTOIS_CSV = RESULTS_DIR + 'ctois.csv'
    KOIS_CSV = RESULTS_DIR + 'kois.csv'
    VERSION = 14
    OBJECT_ID_REGEX = "^(KIC|TIC|EPIC)[-_ ]([0-9]+)$"
    NUMBERS_REGEX = "[0-9]+$"
    MISSION_ID_KEPLER = "KIC"
    MISSION_ID_KEPLER_2 = "EPIC"
    MISSION_ID_TESS = "TIC"
    transits_min_count = {}
    wl_min = {}
    wl_max = {}
    report = {}
    ois = None
    config_step = 0
    ois_manager = OisManager()
    use_ois = False
    user_transit_template = None

    def __init__(self, update_ois: bool, object_infos: list, explore=False):
        """
        Initializes a Sherlock object, loading the OIs from the csvs, setting up the detrend and transit configurations,
        storing the provided object_infos list and initializing the builders to be used to prepare the light curves for
        the provided object_infos.
        @param update_ois: Flag to signal SHERLOCK for updating the TOIs, KOIs and EPICs
        @param object_infos: a list of objects information to be analysed
        @param explore: whether to only run the prepare stage for all objects
        @type object_infos: a list of ObjectInfo implementations to be resolved and analysed
        """
        self.explore = explore
        self.setup_files(update_ois)
        self.setup_detrend()
        self.object_infos = object_infos
        self.lightcurve_builders = {InputObjectInfo: MissionInputLightcurveBuilder(),
                                    MissionInputObjectInfo: MissionInputLightcurveBuilder(),
                                    MissionObjectInfo: MissionLightcurveBuilder(),
                                    MissionFfiIdObjectInfo: MissionFfiLightcurveBuilder(),
                                    MissionFfiCoordsObjectInfo: MissionFfiLightcurveBuilder()}
        self.search_zones_resolvers = {'hz': HabitableSearchZone(),
                                       'ohz': OptimisticHabitableSearchZone()}
        self.habitability_calculator = HabitabilityCalculator()
        self.setup_transit_adjust_params()

    def setup_files(self, refresh_ois, results_dir=RESULTS_DIR):
        """
        Loads the objects of interest data from the downloaded CSVs.
        @param refresh_ois: Flag update the TOIs, KOIs and EPICs
        @param results_dir: Stores the directory to be used for the execution.
        @return: the Sherlock object itself
        """
        self.results_dir = results_dir
        self.load_ois(refresh_ois)
        return self

    def setup_detrend(self, initial_smooth=True, initial_rms_mask=True, initial_rms_threshold=1.5,
                      initial_rms_bin_hours=3, n_detrends=6, detrend_method="biweight", detrend_wl_min=None,
                      detrend_wl_max=None, cores=1, auto_detrend_periodic_signals=False, auto_detrend_ratio=1/4,
                      auto_detrend_method="biweight", user_prepare=None):
        """
        Configures the values for the detrends steps.
        @param initial_smooth: whether to execute an initial local noise reduction before the light curve analysis
        @param initial_rms_mask: whether to execute high RMS areas masking before the light curve analysis
        @param initial_rms_threshold: the high RMS areas limit to be applied multiplied by the RMS median
        @param initial_rms_bin_hours: the high RMS areas binning
        @param n_detrends: the number of detrends to be applied to the PDCSAP_FLUX curve for each run.
        @param detrend_method: the type of algorithm to be used for the detrending
        @param cores: the number of CPU cores to be used for the detrending process
        @param auto_detrend_periodic_signals: whether to search for intense periodicities from the LS periodogram and
        perform an initial detrending based on them.
        @param auto_detrend_ratio: the factor to apply to the highest periodicity found in the LS periodogram which will
        be used for the initial detrend.
        @param auto_detrend_method: the detrend method to be applied with the highest periodicity found in the LS
        periodogram
        @param user_prepare: custom algorithm from user to be applied.
        @return: the Sherlock object itself
        @rtype: Sherlock
        """
        if detrend_method not in self.VALID_DETREND_METHODS:
            raise ValueError("Provided detrend method '" + detrend_method + "' is not allowed.")
        if auto_detrend_method not in self.VALID_PERIODIC_DETREND_METHODS:
            raise ValueError("Provided periodic detrend method '" + auto_detrend_method + "' is not allowed.")
        self.initial_rms_mask = initial_rms_mask
        self.initial_rms_threshold = initial_rms_threshold
        self.initial_rms_bin_hours = initial_rms_bin_hours
        self.initial_smooth = initial_smooth
        self.n_detrends = n_detrends
        self.detrend_method = detrend_method
        self.detrend_wl_min = detrend_wl_min
        self.detrend_wl_max = detrend_wl_max
        self.detrend_cores = cores
        self.auto_detrend_periodic_signals = auto_detrend_periodic_signals
        self.auto_detrend_ratio = auto_detrend_ratio
        self.auto_detrend_method = auto_detrend_method
        self.detrend_plot_axis = [[1, 1], [2, 1], [3, 1], [2, 2], [3, 2], [3, 2], [3, 3], [3, 3], [3, 3], [4, 3],
                                  [4, 3], [4, 3], [4, 4], [4, 4], [4, 4], [4, 4], [5, 4], [5, 4], [5, 4], [5, 4],
                                  [6, 4], [6, 4], [6, 4], [6, 4]]
        self.detrend_plot_axis.append([1, 1])
        self.detrend_plot_axis.append([2, 1])
        self.detrend_plot_axis.append([3, 1])
        self.user_prepare = user_prepare
        return self

    def setup_transit_adjust_params(self, max_runs=10, min_sectors=1, max_sectors=999999, period_protec=10,
                                    search_zone=None, user_search_zone=None, period_min=0.5, period_max=20,
                                    bin_minutes=10, run_cores=NUM_CORES, snr_min=5, sde_min=5, fap_max=0.1,
                                    mask_mode="mask", best_signal_algorithm='border-correct', quorum_strength=1,
                                    min_quorum=0, user_selection_algorithm=None, fit_method="tls",
                                    oversampling=None, t0_fit_margin=0.05, duration_grid_step=1.1,
                                    custom_transit_template=None):
        """
        Configures the values to be used for the transit fitting and the main run loop.
        @param max_runs: the max number of runs to be executed for each object.
        @param min_sectors: the minimum number of sectors/quarters for an object to be analysed
        @param max_sectors: the maximum number of sectors/quarters for an object to be analysed
        @param period_protec: the maximum period to be used to calculate the minimum transit duration
        @param search_zone: the zone where sherlock should be searching transits for. If set, period_min and period_max
        are to be ignored because they will be generated for the selected zone.
        @param user_search_zone: custom defined user class to be used for constraining the periods search.
        @param period_min: the minimum period to search transits for
        @param period_max: the maximum period to search transits for
        @param bin_minutes:
        @param run_cores: the number of CPU cores to use for the transit fitting
        @param snr_min: the minimum SNR accepted to continue the analysis for an object
        @param sde_min: the minimum SDE accepted to continue the analysis for an object
        @param fap_max: the maximum FAP accepted to continue the analysis for an object
        @param mask_mode: the way to remove every run-selected transit influence in the light curve. 'mask' and
        'subtract' are available
        @param best_signal_algorithm: the way to calculate the best signal for each object run. 'basic', 'border-correct'
        and 'quorum' are available.
        @param quorum_strength: if quorum is selected as best_signal_algorithm this value will be used for the votes
        weight.
        @param min_quorum: used to decide when SHERLOCK should be stopped because of lack of persistence in the found
        signals of the last executed run.
        @param user_selection_algorithm: selection algorithm provided by the user to be used by SHERLOCK.
        @param fit_method: selection algorithm provided by the user to be used by SHERLOCK.
        @param oversampling: from 1 to 10, the oversampling size to be used by TLS.
        @param t0_fit_margin: from 0.01 to 0.1, the percent of T0 to be shifted for the T0 fit.
        @param duration_grid_step: from 1.0 to 1.1, how fast should the duration be iterated by TLS.
        @param custom_transit_template: User provided TransitTemplateGenerator extension, which in case of being
        provided, overrides the fit_method.
        @return: the Sherlock object itself
        @rtype: Sherlock
        """
        if mask_mode not in self.MASK_MODES:
            raise ValueError("Provided mask mode '" + mask_mode + "' is not allowed.")
        if best_signal_algorithm not in self.VALID_SIGNAL_SELECTORS:
            raise ValueError("Provided best signal algorithm '" + best_signal_algorithm + "' is not allowed.")
        self.max_runs = max_runs
        self.min_sectors = min_sectors
        self.max_sectors = max_sectors
        self.run_cores = run_cores
        self.mask_mode = mask_mode
        self.period_protec = period_protec
        self.period_min = period_min
        self.period_max = period_max
        self.bin_minutes = bin_minutes
        self.snr_min = snr_min
        self.sde_min = sde_min
        self.fap_max = fap_max
        self.search_zone = search_zone if user_search_zone is None else "user"
        if user_search_zone is not None:
            self.search_zones_resolvers["user"] = user_search_zone
        self.signal_score_selectors = {self.VALID_SIGNAL_SELECTORS[0]: BasicSignalSelector(),
                                       self.VALID_SIGNAL_SELECTORS[1]: SnrBorderCorrectedSignalSelector(),
                                       self.VALID_SIGNAL_SELECTORS[2]: QuorumSnrBorderCorrectedSignalSelector(
                                           quorum_strength, min_quorum),
                                       "user": user_selection_algorithm}
        self.best_signal_algorithm = best_signal_algorithm if user_selection_algorithm is None else "user"
        self.user_selection_algorithm = user_selection_algorithm
        self.fit_method = "default"
        if fit_method is not None and fit_method.lower() == 'bls':
            self.fit_method = "box"
        elif fit_method is not None and fit_method.lower() == 'grazing':
            self.fit_method = "grazing"
        elif fit_method is not None and fit_method.lower() == 'comet':
            self.fit_method = "comet"
        self.oversampling = oversampling
        if self.oversampling is not None:
            self.oversampling = int(self.oversampling)
        self.t0_fit_margin = t0_fit_margin
        self.duration_grid_step = duration_grid_step
        if custom_transit_template is not None:
            self.fit_method = "custom"
            self.user_transit_template = custom_transit_template

        return self

    def refresh_ois(self):
        """
        Downloads the TOIs, KOIs and EPIC OIs into csv files.
        @return: the Sherlock object itself
        @rtype: Sherlock
        """
        self.ois_manager.update_tic_csvs()
        self.ois_manager.update_kic_csvs()
        self.ois_manager.update_epic_csvs()
        return self

    def load_ois(self, refresh_ois):
        """
        Loads the csv OIs files into memory
        @return: the Sherlock object itself
        @rtype: Sherlock
        """
        if refresh_ois:
            Updater().update(False, True, True)
        self.ois = self.ois_manager.load_ois()
        return self

    def filter_hj_ois(self):
        """
        Filters the in-memory OIs given some basic filters associated to hot jupiters properties. This method is added
        as an example
        @return: the Sherlock object itself
        @rtype: Sherlock
        """
        self.use_ois = True
        self.ois = self.ois[self.ois["Disposition"].notnull()]
        self.ois = self.ois[self.ois["Period (days)"].notnull()]
        self.ois = self.ois[self.ois["Planet Radius (R_Earth)"].notnull()]
        self.ois = self.ois[self.ois["Planet Insolation (Earth Flux)"].notnull()]
        self.ois = self.ois[self.ois["Depth (ppm)"].notnull()]
        self.ois = self.ois[(self.ois["Disposition"] == "KP") | (self.ois["Disposition"] == "CP")]
        self.ois = self.ois[self.ois["Period (days)"] < 10]
        self.ois = self.ois[self.ois["Planet Radius (R_Earth)"] > 5]
        self.ois = self.ois[self.ois["Planet Insolation (Earth Flux)"] > 4]
        self.ois.sort_values(by=['Object Id', 'OI'])
        return self

    def filter_ois(self, function):
        """
        Applies a function accepting the Sherlock objects of interests dataframe and stores the result into the
        Sherlock same ois dataframe.
        @param function: the function to be applied to filter the Sherlock OIs.
        @return: the Sherlock object itself
        @rtype: Sherlock
        """
        self.use_ois = True
        self.ois = function(self.ois)
        return self

    def limit_ois(self, offset=0, limit=0):
        """
        Limits the in-memory loaded OIs given an offset and a limit (like a pagination)
        @param offset:
        @param limit:
        @return: the Sherlock object itself
        @rtype: Sherlock
        """
        if limit == 0:
            limit = len(self.ois.index)
        self.ois = self.ois[offset:limit]
        return self

    def run(self):
        """
        Entrypoint of Sherlock which launches the main execution for all the input object_infos
        """
        self.__setup_logging()
        logging.info('SHERLOCK (Searching for Hints of Exoplanets fRom Lightcurves Of spaCe-base seeKers)')
        logging.info('Version %s', self.VERSION)
        logging.info('MODE: %s', "ANALYSE" if not self.explore else "EXPLORE")
        if len(self.object_infos) == 0 and self.use_ois:
            self.object_infos = [MissionObjectInfo(object_id, 'all')
                                 for object_id in self.ois["Object Id"].astype('string').unique()]
        for object_info in self.object_infos:
            self.__run_object(object_info)

    def __run_object(self, object_info):
        """
        Performs the analysis for one object_info
        @param object_info: The object to be analysed.
        @type object_info: ObjectInfo
        """
        sherlock_id = object_info.sherlock_id()
        mission_id = object_info.mission_id()
        try:
            time, flux, flux_err, star_info, transits_min_count, cadence, sectors = self.__prepare(object_info)
            id_run = 1
            best_signal_score = 1
            self.report[sherlock_id] = []
            logging.info('================================================')
            logging.info('SEARCH RUNS')
            logging.info('================================================')
            lcs, wl = self.__detrend(time, flux, star_info)
            lcs = np.concatenate(([flux], lcs), axis=0)
            wl = np.concatenate(([0], wl), axis=0)
            while not self.explore and best_signal_score == 1 and id_run <= self.max_runs:
                self.__setup_object_logging(sherlock_id, False)
                object_report = {}
                logging.info("________________________________ run %s________________________________", id_run)
                transit_results, signal_selection = \
                    self.__analyse(object_info, time, lcs, flux_err, star_info, id_run, transits_min_count, cadence,
                                   self.report[sherlock_id], wl)
                best_signal_score = signal_selection.score
                object_report["Object Id"] = mission_id
                object_report["run"] = id_run
                object_report["score"] = best_signal_score
                object_report["curve"] = str(signal_selection.curve_index)
                object_report["snr"] = transit_results[signal_selection.curve_index].snr
                object_report["sde"] = transit_results[signal_selection.curve_index].sde
                object_report["fap"] = transit_results[signal_selection.curve_index].fap
                object_report["border_score"] = transit_results[signal_selection.curve_index].border_score
                object_report["harmonic"] = transit_results[signal_selection.curve_index].harmonic
                object_report["period"] = transit_results[signal_selection.curve_index].period
                object_report["per_err"] = transit_results[signal_selection.curve_index].per_err
                object_report["duration"] = transit_results[signal_selection.curve_index].duration * 60 * 24
                object_report["t0"] = transit_results[signal_selection.curve_index].t0
                object_report["depth"] = transit_results[signal_selection.curve_index].depth
                object_report['rp_rs'] = transit_results[signal_selection.curve_index].results.rp_rs
                real_transit_args = np.argwhere(~np.isnan(transit_results[signal_selection.curve_index]
                                                          .results.transit_depths))
                object_report["transits"] = np.array(transit_results[signal_selection.curve_index]
                                                          .results.transit_times)[real_transit_args.flatten()]
                object_report["transits"] = ','.join(map(str, object_report["transits"]))
                object_report["sectors"] = ','.join(map(str, sectors)) if sectors is not None and len(sectors) > 0 else None
                object_report["ffi"] = isinstance(object_info, MissionFfiIdObjectInfo) or \
                                       isinstance(object_info, MissionFfiCoordsObjectInfo)

                object_report["oi"] = self.__find_matching_oi(object_info, object_report["period"])
                if best_signal_score == 1:
                    logging.info('New best signal is good enough to keep searching. Going to the next run.')
                    time, lcs = self.__apply_mask_from_transit_results(time, lcs, transit_results,
                                                                        signal_selection.curve_index)
                    id_run += 1
                    if id_run > self.max_runs:
                        logging.info("Max runs limit of %.0f is reached. Stopping.", self.max_runs)
                else:
                    logging.info('New best signal does not look very promising. End')
                self.report[sherlock_id].append(object_report)
                self.__setup_object_report_logging(sherlock_id, True)
                object_dir = self.__init_object_dir(object_info.sherlock_id())
                logging.info("Listing most promising candidates for ID %s:", sherlock_id)
                logging.info("%-12s%-10s%-10s%-10s%-8s%-8s%-8s%-8s%-10s%-14s%-14s%-12s%-25s%-10s%-18s%-20s", "Detrend no.", "Period",
                             "Per_err", "Duration", "T0", "Depth", "SNR", "SDE", "FAP", "Border_score", "Matching OI", "Harmonic",
                             "Planet radius (R_Earth)", "Rp/Rs", "Semi-major axis", "Habitability Zone")
                if sherlock_id in self.report:
                    candidates_df = pandas.DataFrame(columns=['curve', 'period', 'per_err', 'duration', 't0', 'depth',
                                                              'snr', 'sde', 'fap', 'border_score', 'oi', 'rad_p', 'rp_rs',
                                                              'a', 'hz'])
                    i = 1
                    for report in self.report[sherlock_id]:
                        a, habitability_zone = self.habitability_calculator\
                            .calculate_hz_score(star_info.teff, star_info.mass, star_info.lum, report["period"])
                        report['a'] = a
                        report['hz'] = habitability_zone
                        if star_info.radius_assumed:
                            report['rad_p'] = np.nan
                            report['rp_rs'] = np.nan
                        else:
                            report['rad_p'] = self.__calculate_planet_radius(star_info, report["depth"])
                        logging.info("%-12s%-10.4f%-10.5f%-10.2f%-8.2f%-8.3f%-8.2f%-8.2f%-10.6f%-14.2f%-14s%-12s%-25.5f%-10.5f%-18.5f%-20s",
                                     report["curve"], report["period"], report["per_err"],
                                     report["duration"], report["t0"], report["depth"], report["snr"], report["sde"],
                                     report["fap"], report["border_score"], report["oi"], report["harmonic"],
                                     report['rad_p'], report['rp_rs'], a, habitability_zone)
                        candidates_df = candidates_df.append(report, ignore_index=True)
                        i = i + 1
                    candidates_df.to_csv(object_dir + "candidates.csv", index=False)
        except InvalidNumberOfSectorsError as e:
            logging.exception(str(e))
            print(e)
            self.__remove_object_dir(sherlock_id)
        except Exception as e:
            logging.exception(str(e))
            print(e)

    def __init_object_dir(self, object_id, clean_dir=False):
        dir = self.results_dir + str(object_id)
        dir = dir.replace(" ", "_")
        if clean_dir:
            self.__remove_object_dir(object_id)
        if not os.path.exists(dir):
            os.makedirs(dir)
        return dir + "/"

    def __remove_object_dir(self, object_id):
        dir = self.results_dir + str(object_id)
        dir = dir.replace(" ", "_")
        if os.path.exists(dir) and os.path.isdir(dir):
            shutil.rmtree(dir, ignore_errors=True)

    def __init_object_run_dir(self, object_id, run_no, clean_dir=False):
        dir = self.results_dir + str(object_id) + "/" + str(run_no)
        dir = dir.replace(" ", "_")
        if clean_dir and os.path.exists(dir) and os.path.isdir(dir):
            shutil.rmtree(dir, ignore_errors=True)
        if not os.path.exists(dir):
            os.makedirs(dir)
        return dir + "/"

    def __setup_logging(self):
        formatter = logging.Formatter('%(message)s')
        logger = logging.getLogger()
        while len(logger.handlers) > 0:
            logger.handlers.pop()
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def __setup_object_logging(self, object_id, clean_dir=True):
        object_dir = self.__init_object_dir(object_id, clean_dir)
        logger = logging.getLogger()
        while len(logger.handlers) > 1:
            logger.handlers.pop()
        formatter = logging.Formatter('%(message)s')
        handler = logging.FileHandler(object_dir + str(object_id) + "_report.log")
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return object_dir

    def __setup_object_report_logging(self, object_id, clean=False):
        object_dir = self.__setup_object_logging(object_id, False)
        logger = logging.getLogger()
        logger.handlers.pop()
        formatter = logging.Formatter('%(message)s')
        file = object_dir + str(object_id) + "_candidates.log"
        if clean and os.path.exists(file):
            os.remove(file)
        handler = logging.FileHandler(file)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def __complete_star_info(self, input_star_info, catalogue_star_info):
        if catalogue_star_info is None:
            catalogue_star_info = StarInfo()
        result_star_info = catalogue_star_info
        if input_star_info is None:
            input_star_info = StarInfo()
        if input_star_info.radius is not None:
            result_star_info.radius = input_star_info.radius
            result_star_info.radius_assumed = False
        if input_star_info.radius_min is not None:
            result_star_info.radius_min = input_star_info.radius_min
        if input_star_info.radius_max is not None:
            result_star_info.radius_max = input_star_info.radius_max
        if input_star_info.mass is not None:
            result_star_info.mass = input_star_info.mass
            result_star_info.mass_assumed = False
        if input_star_info.mass_min is not None:
            result_star_info.mass_min = input_star_info.mass_min
        if input_star_info.mass_max is not None:
            result_star_info.mass_max = input_star_info.mass_max
        if input_star_info.ra is not None:
            result_star_info.ra = input_star_info.ra
        if input_star_info.dec is not None:
            result_star_info.dec = input_star_info.dec
        if input_star_info.teff is not None:
            result_star_info.teff = input_star_info.teff
        if input_star_info.lum is not None:
            result_star_info.lum = input_star_info.lum
        if input_star_info.logg is not None:
            result_star_info.logg = input_star_info.logg
        if input_star_info.ld_coefficients is not None:
            result_star_info.ld_coefficients = input_star_info.ld_coefficients
        return result_star_info

    def __prepare(self, object_info):
        sherlock_id = object_info.sherlock_id()
        object_dir = self.__setup_object_logging(sherlock_id)
        logging.info('ID: %s', sherlock_id)
        lc, lc_data, star_info, transits_min_count, sectors, quarters = self.lightcurve_builders[type(object_info)].build(object_info, object_dir)
        star_info = self.__complete_star_info(object_info.star_info, star_info)
        if star_info is not None:
            logging.info('================================================')
            logging.info('STELLAR PROPERTIES FOR THE SIGNAL SEARCH')
            logging.info('================================================')
            logging.info("Star catalog info downloaded.")
            if star_info.mass is None or np.isnan(star_info.mass):
                logging.info("Star catalog doesn't provide mass. Assuming M=0.1Msun")
                star_info.assume_model_mass()
            if star_info.radius is None or np.isnan(star_info.radius):
                logging.info("Star catalog doesn't provide radius. Assuming R=0.1Rsun")
                star_info.assume_model_radius()
            logging.info('limb-darkening estimates using quadratic LD (a,b)= %s', star_info.ld_coefficients)
            logging.info('mass = %.6f', star_info.mass)
            logging.info('mass_min = %.6f', star_info.mass_min)
            logging.info('mass_max = %.6f', star_info.mass_max)
            logging.info('radius = %.6f', star_info.radius)
            logging.info('radius_min = %.6f', star_info.radius_min)
            logging.info('radius_max = %.6f', star_info.radius_max)
            logging.info('teff = %.6f', star_info.teff)
            logging.info('lum = %.6f', star_info.lum)
            logging.info('logg = %.6f', star_info.logg)
        if not star_info.radius_assumed and not star_info.mass_assumed and star_info.teff is not None:
            star_df = pandas.DataFrame(columns=['ra', 'dec', 'R_star', 'R_star_lerr', 'R_star_uerr', 'M_star',
                                                'M_star_lerr', 'M_star_uerr', 'Teff_star', 'Teff_star_lerr',
                                                'Teff_star_uerr', 'ld_a', 'ld_b'])
            star_df = star_df.append({'ra': star_info.ra, 'dec': star_info.dec, 'R_star': star_info.radius,
                                      'R_star_lerr': star_info.radius - star_info.radius_min,
                            'R_star_uerr': star_info.radius_max - star_info.radius,
                            'M_star': star_info.mass, 'M_star_lerr': star_info.mass - star_info.mass_min,
                            'M_star_uerr': star_info.mass_max - star_info.mass,
                            'Teff_star': star_info.teff, 'Teff_star_lerr': 200, 'Teff_star_uerr': 200,
                                      'ld_a': star_info.ld_coefficients[0], 'ld_b': star_info.ld_coefficients[1]},
                           ignore_index=True)
            star_df.to_csv(object_dir + "params_star.csv", index=False)
        logging.info('================================================')
        logging.info('USER DEFINITIONS')
        logging.info('================================================')
        if self.detrend_method == "gp":
            logging.info('Detrend method: Gaussian Process Matern 2/3')
        else:
            logging.info('Detrend method: Bi-Weight')
        logging.info('No of detrend models applied: %s', self.n_detrends)
        logging.info('Minimum number of transits: %s', transits_min_count)
        logging.info('Period planet protected: %.1f', self.period_protec)
        lightcurve_timespan = lc.time[len(lc.time) - 1] - lc.time[0]
        if self.search_zone is not None and not (star_info.mass_assumed or star_info.radius_assumed):
            logging.info("Selected search zone: %s. Minimum and maximum periods will be calculated.", self.search_zone)
            min_and_max_period = self.search_zones_resolvers[self.search_zone].calculate_period_range(star_info)
            if min_and_max_period is None:
                logging.info("Selected search zone was %s but cannot be calculated. Defaulting to minimum and " +
                             "maximum input periods", self.search_zone)
            else:
                logging.info("Selected search zone periods are [%.2f, %.2f] days", min_and_max_period[0], min_and_max_period[1])
                if min_and_max_period[0] > lightcurve_timespan or min_and_max_period[1] > lightcurve_timespan:
                    logging.info("Selected search zone period values are greater than lightcurve dataset. " +
                                 "Defaulting to minimum and maximum input periods.")
                else:
                    self.period_min = min_and_max_period[0]
                    self.period_max = min_and_max_period[1]
        elif self.search_zone is not None:
            logging.info("Selected search zone was %s but star catalog info was not found or wasn't complete. " +
                         "Defaulting to minimum and maximum input periods.", self.search_zone)
        logging.info('Minimum Period (d): %.1f', self.period_min)
        logging.info('Maximum Period (d): %.1f', self.period_max)
        logging.info('Binning size (min): %.1f', self.bin_minutes)
        if object_info.initial_mask is not None:
            logging.info('Mask: yes')
        else:
            logging.info('Mask: no')
        if object_info.initial_transit_mask is not None:
            logging.info('Transit Mask: yes')
        else:
            logging.info('Transit Mask: no')
        logging.info('Threshold limit for SNR: %.1f', self.snr_min)
        logging.info('Threshold limit for SDE: %.1f', self.sde_min)
        logging.info('Threshold limit for FAP: %.1f', self.fap_max)
        logging.info("Fit method: %s", self.fit_method)
        if self.oversampling is not None:
            logging.info('Oversampling: %.3f', self.oversampling)
        if self.duration_grid_step is not None:
            logging.info('Duration step: %.3f', self.duration_grid_step)
        if self.t0_fit_margin is not None:
            logging.info('T0 Fit Margin: %.3f', self.t0_fit_margin)
        logging.info('Signal scoring algorithm: %s', self.best_signal_algorithm)
        if self.best_signal_algorithm == self.VALID_SIGNAL_SELECTORS[2]:
            logging.info('Quorum algorithm vote strength: %.2f',
                         self.signal_score_selectors[self.VALID_SIGNAL_SELECTORS[2]].strength)
        if sectors is not None:
            sectors_count = len(sectors)
            logging.info('================================================')
            logging.info('SECTORS INFO')
            logging.info('================================================')
            logging.info('Sectors : %s', sectors)
            logging.info('No of sectors available: %s', len(sectors))
            if sectors_count < self.min_sectors or sectors_count > self.max_sectors:
                raise InvalidNumberOfSectorsError("The object " + sherlock_id + " contains " + str(sectors_count) +
                                                  " sectors and the min and max selected are [" +
                                                  str(self.min_sectors) + ", " + str(self.max_sectors) + "].")
        if quarters is not None:
            sectors_count = len(quarters)
            logging.info('================================================')
            logging.info('QUARTERS INFO')
            logging.info('================================================')
            logging.info('Quarters : %s', quarters)
            if sectors_count < self.min_sectors or sectors_count > self.max_sectors:
                raise InvalidNumberOfSectorsError("The object " + sherlock_id + " contains " + str(sectors_count) +
                                                  " quarters and the min and max selected are [" +
                                                  str(self.min_sectors) + ", " + str(self.max_sectors) + "].")
        flux = lc.flux
        flux_err = lc.flux_err
        time = lc.time
        logging.info('================================================')
        logging.info("Detrend Window length / Kernel size")
        logging.info('================================================')
        if self.detrend_wl_min is not None and self.detrend_wl_max is not None:
            logging.info("Using user input WL / KS")
            if self.detrend_method == 'gp':
                self.wl_min[sherlock_id] = self.detrend_wl_min
                self.wl_max[sherlock_id] = self.detrend_wl_max
            else:
                self.wl_min[sherlock_id] = self.detrend_wl_min
                self.wl_max[sherlock_id] = self.detrend_wl_max
        else:
            logging.info("Using transit duration based WL or fixed KS")
            transit_duration = wotan.t14(R_s=star_info.radius, M_s=star_info.mass, P=self.period_protec,
                                         small_planet=True)  # we define the typical duration of a small planet in this star
            if self.detrend_method == 'gp':
                self.wl_min[sherlock_id] = 1
                self.wl_max[sherlock_id] = 12
            else:
                self.wl_min[sherlock_id] = 3 * transit_duration  # minimum transit duration
                self.wl_max[sherlock_id] = 20 * transit_duration  # maximum transit duration
        logging.info("wl/ks_min: %.2f", self.wl_min[sherlock_id])
        logging.info("wl/ks_min: %.2f", self.wl_max[sherlock_id])
        logging.info('================================================')
        time_float = lc.time.value
        flux_float = lc.flux.value
        flux_err_float = lc.flux_err.value
        lc = lk.LightCurve(time=time_float, flux=flux_float, flux_err=flux_err_float)
        lc_df = pandas.DataFrame(columns=['#time', 'flux', 'flux_err'])
        lc_df['#time'] = time_float
        lc_df['flux'] = flux_float
        lc_df['flux_err'] = flux_err_float
        lc_df.to_csv(object_dir + "lc.csv", index=False)
        lc = lc.remove_outliers(sigma_lower=float('inf'), sigma_upper=3)  # remove outliers over 3sigma
        time_float = lc.time.value
        flux_float = lc.flux.value
        flux_err_float = lc.flux_err.value
        cadence_array = np.diff(time_float) * 24 * 60
        cadence_array = cadence_array[~np.isnan(cadence_array)]
        cadence_array = cadence_array[cadence_array > 0]
        cadence = np.nanmedian(cadence_array)
        clean_time, flatten_flux, clean_flux_err = self.__clean_initial_flux(object_info, time_float, flux_float,
                                                                             flux_err_float, star_info, cadence)
        lc = lk.LightCurve(time=clean_time, flux=flatten_flux, flux_err=clean_flux_err)
        self.rotator_period = None
        periodogram = lc.to_periodogram(minimum_period=0.05, maximum_period=15, oversample_factor=10)
        # power_norm = self.running_median(periodogram.power.value, 20)
        periodogram.plot(view='period', scale='log')
        plt.title(str(sherlock_id) + " Lightcurve periodogram")
        plt.savefig(object_dir + "Periodogram_" + str(sherlock_id) + ".png")
        plt.clf()
        # power_mod = periodogram.power.value - power_norm
        # power_mod = power_mod / np.mean(power_mod)
        # periodogram.power = power_mod * u.d / u.d
        # periodogram.plot(view='period', scale='log')
        # plt.title(str(sherlock_id) + " Lightcurve normalized periodogram")
        # plt.savefig(object_dir + "PeriodogramNorm_" + str(sherlock_id) + ".png")
        # plt.clf()
        if object_info.initial_detrend_period is not None:
            self.rotator_period = object_info.initial_detrend_period
        elif self.auto_detrend_periodic_signals:
            self.rotator_period = self.__calculate_max_significant_period(lc, periodogram)
        if self.rotator_period is not None:
            logging.info('================================================')
            logging.info('AUTO-DETREND EXECUTION')
            logging.info('================================================')
            logging.info("Period = %.3f", self.rotator_period)
            lc.fold(self.rotator_period).scatter()
            plt.title("Phase-folded period: " + format(self.rotator_period, ".2f") + " days")
            plt.savefig(object_dir + "Phase_detrend_period_" + str(sherlock_id) + "_" + format(self.rotator_period, ".2f") + "_days.png")
            plt.clf()
            flatten_flux, lc_trend = self.__detrend_by_period(clean_time, flatten_flux, self.rotator_period * self.auto_detrend_ratio)
            if not self.period_min:
                self.period_min = self.rotator_period * 4
                logging.info("Setting Min Period to %.3f", self.period_min)
        if object_info.initial_mask is not None:
            logging.info('================================================')
            logging.info('INITIAL MASKING')
            logging.info('================================================')
            initial_mask = object_info.initial_mask
            logging.info('** Applying ordered masks to the lightcurve **')
            for mask_range in initial_mask:
                mask = [(clean_time < mask_range[0] if not math.isnan(mask_range[1]) else False) |
                        (clean_time > mask_range[1] if not math.isnan(mask_range[1]) else False)]
                clean_time = clean_time[mask]
                flatten_flux = flatten_flux[mask]
        if object_info.initial_transit_mask is not None:
            logging.info('================================================')
            logging.info('INITIAL TRANSIT MASKING')
            logging.info('================================================')
            initial_transit_mask = object_info.initial_transit_mask
            logging.info('** Applying ordered transit masks to the lightcurve **')
            for transit_mask in initial_transit_mask:
                logging.info('* Transit mask with P=%.2f d, T0=%.2f d, Dur=%.2f min**', transit_mask["P"],
                             transit_mask["T0"], transit_mask["D"])
                mask = tls.transit_mask(clean_time, transit_mask["P"], transit_mask["D"] / 60 / 24, transit_mask["T0"])
                clean_time = clean_time[~mask]
                flatten_flux = flatten_flux[~mask]
                clean_flux_err = clean_flux_err[~mask]
        return clean_time, flatten_flux, clean_flux_err, star_info, transits_min_count, cadence, \
               sectors if sectors is not None else quarters

    def running_median(self, data, kernel):
        """Returns sliding median of width 'kernel' and same length as data """
        idx = np.arange(kernel) + np.arange(len(data) - kernel + 1)[:, None]
        med = np.percentile(data[idx], 90, axis=1)

        # Append the first/last value at the beginning/end to match the length of
        # data and returned median
        first_values = med[0]
        last_values = med[-1]
        missing_values = len(data) - len(med)
        values_front = int(missing_values * 0.5)
        values_end = missing_values - values_front
        med = np.append(np.full(values_front, first_values), med)
        med = np.append(med, np.full(values_end, last_values))
        return med

    def __clean_initial_flux(self, object_info, time, flux, flux_err, star_info, cadence):
        clean_time = time
        clean_flux = flux
        clean_flux_err = flux_err
        is_short_cadence = round(cadence) <= 5
        if self.user_prepare is not None:
            clean_time, clean_flux, clean_flux_err = self.user_prepare.prepare(object_info, clean_time, clean_flux, clean_flux_err)
        if (is_short_cadence and self.initial_smooth) or (self.initial_rms_mask and object_info.initial_mask is None):
            logging.info('================================================')
            logging.info('INITIAL FLUX CLEANING')
            logging.info('================================================')
        if self.initial_rms_mask and object_info.initial_mask is None:
            logging.info('Masking high RMS areas by a factor of %.2f with %.1f hours binning',
                         self.initial_rms_threshold, self.initial_rms_bin_hours)
            bins_per_day = 24 / self.initial_rms_bin_hours
            before_flux = clean_flux
            fig, axs = plt.subplots(2, 1, figsize=(8, 8), constrained_layout=True)
            axs[1].scatter(time, before_flux, color='gray', alpha=0.5, rasterized=True, label="Flux")
            bins = (clean_time[len(clean_time) - 1] - clean_time[0]) * bins_per_day
            bin_stds, bin_edges, binnumber = stats.binned_statistic(clean_time, clean_flux, statistic='std', bins=bins)
            stds_median = np.nanmedian(bin_stds[bin_stds > 0])
            stds_median_array = np.full(len(bin_stds), stds_median)
            rms_threshold_array = stds_median_array * self.initial_rms_threshold
            too_high_bin_stds_indexes = np.argwhere(bin_stds > rms_threshold_array)
            high_std_mask = np.array([bin_id - 1 in too_high_bin_stds_indexes for bin_id in binnumber])
            clean_time = clean_time[~high_std_mask]
            clean_flux = clean_flux[~high_std_mask]
            clean_flux_err = flux_err[~high_std_mask]
            bin_width = (bin_edges[1] - bin_edges[0])
            bin_centers = bin_edges[1:] - bin_width / 2
            axs[0].plot(bin_centers, bin_stds, color='black', alpha=0.75, rasterized=True, label="RMS")
            axs[0].plot(bin_centers, rms_threshold_array, color='red', rasterized=True, label='Mask Threshold')
            axs[0].set_title(str(self.initial_rms_bin_hours) + " hours binned RMS")
            axs[0].legend(loc="upper right")
            axs[1].scatter(time[high_std_mask], before_flux[high_std_mask], linewidth=1, color='red', alpha=1.0, label="High RMS")
            axs[1].legend(loc="upper right")
            axs[1].set_title("Total and masked high RMS flux")
            fig.suptitle(str(star_info.object_id) + " High RMS Mask")
            axs[0].set_xlabel('Time')
            axs[0].set_ylabel('Flux RMS')
            axs[1].set_xlabel('Time')
            axs[1].set_ylabel('Flux')
            plot_dir = self.__init_object_dir(star_info.object_id)
            fig.savefig(plot_dir + 'High_RMS_Mask_' + str(star_info.object_id) + '.png', dpi=200)
            fig.clf()
        if is_short_cadence and self.initial_smooth:
            #logging.info('Applying Smooth phase (savgol + weighted average)')
            logging.info('Applying Smooth phase (savgol)')
            clean_flux = self.smooth(clean_flux)
            # TODO to use convolve we need to remove the borders effect
            # clean_flux = np.convolve(clean_flux, [0.025, 0.05, 0.1, 0.155, 0.34, 0.155, 0.1, 0.05, 0.025], "same")
            # clean_flux = np.convolve(clean_flux, [0.025, 0.05, 0.1, 0.155, 0.34, 0.155, 0.1, 0.05, 0.025], "same")
            # clean_flux[0:5] = 1
            # clean_flux[len(clean_flux) - 6: len(clean_flux) - 1] = 1
            #clean_flux = uniform_filter1d(clean_flux, 11)
            #clean_flux = self.flatten_bw(self.FlattenInput(clean_time, clean_flux, 0.02))[0]
        return clean_time, clean_flux, clean_flux_err

    def smooth(self, flux, window_len=11, window='blackman'):
        clean_flux = savgol_filter(flux, window_len, 3)
        # if window_len < 3:
        #     return flux
        # if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        #     raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")
        # s = np.r_[np.ones(window_len//2), clean_flux, np.ones(window_len//2)]
        # # print(len(s))
        # if window == 'flat':  # moving average
        #     w = np.ones(window_len, 'd')
        # else:
        #     w = eval('np.' + window + '(window_len)')
        # # TODO probably problematic with big gaps in the middle of the curve
        # clean_flux = np.convolve(w / w.sum(), s, mode='valid')
        return clean_flux

    def __calculate_max_significant_period(self, lc, periodogram):
        #max_accepted_period = (lc.time[len(lc.time) - 1] - lc.time[0]) / 4
        max_accepted_period = np.float64(10)
        # TODO related to https://github.com/franpoz/SHERLOCK/issues/29 check whether this fits better
        max_power_index = np.argmax(periodogram.power)
        period = periodogram.period[max_power_index]
        if max_power_index > 0.0008:
            period = period.value
            logging.info("Auto-Detrend found the strong period: " + str(period) + ".")
        else:
            logging.info("Auto-Detrend did not find relevant periods.")
            period = None
        return period

    def __detrend_by_period(self, time, flux, period_window):
        if self.auto_detrend_method == 'gp':
            flatten_lc, lc_trend = flatten(time, flux, method=self.detrend_method, kernel='matern',
                                   kernel_size=period_window, return_trend=True, break_tolerance=0.5)
        else:
            flatten_lc, lc_trend = flatten(time, flux, window_length=period_window, return_trend=True,
                                           method=self.auto_detrend_method, break_tolerance=0.5)
        return flatten_lc, lc_trend

    def __analyse(self, object_info, time, lcs, flux_err, star_info, id_run, transits_min_count, cadence, report, wl):
        logging.info('=================================')
        logging.info('SEARCH OF SIGNALS - Run %s', id_run)
        logging.info('=================================')
        transit_results = self.__identify_signals(object_info, time, lcs, flux_err, star_info, transits_min_count, wl, id_run, cadence, report)
        signal_selection = self.signal_score_selectors[self.best_signal_algorithm]\
            .select(transit_results, self.snr_min, self.detrend_method, wl)
        logging.info(signal_selection.get_message())
        return transit_results, signal_selection

    def __detrend(self, time, lc, star_info):
        wl_min = self.wl_min[star_info.object_id]
        wl_max = self.wl_max[star_info.object_id]
        bins = len(time) * 2 / self.bin_minutes
        bin_means, bin_edges, binnumber = stats.binned_statistic(time, lc, statistic='mean', bins=bins)
        logging.info('=================================')
        logging.info('MODELS IN THE DETRENDING')
        logging.info('=================================')
        logging.info("%-25s%-17s%-15s%-11s%-15s", "light_curve", "Detrend_method", "win/ker_size", "RMS (ppm)",
                     "RMS_10min (ppm)")
        logging.info("%-25s%-17s%-15s%-11.2f%-15.2f", "PDCSAP_FLUX", "---", "---", np.std(lc) * 1e6,
                     np.std(bin_means[~np.isnan(bin_means)]) * 1e6)
        wl_step = (wl_max - wl_min) / self.n_detrends
        wl = np.arange(wl_min, wl_max, wl_step)  # we define all the posibles window_length that we apply
        final_lcs = np.zeros((len(wl), len(lc)))
        ## save in a plot all the detrendings and all the data to inspect visually.
        figsize = (8, 8)  # x,y
        rows = self.detrend_plot_axis[self.n_detrends - 1][0]
        cols = self.detrend_plot_axis[self.n_detrends - 1][1]
        shift = 2 * (1.0 - (np.min(lc)))  # shift in the between the raw and detrended data
        fig, axs = plt.subplots(rows, cols, figsize=figsize, constrained_layout=True)
        if self.n_detrends > 1:
            axs = self.__trim_axs(axs, len(wl))
        flatten_inputs = []
        flattener = Flattener()
        if self.detrend_cores > 1:
            for i in range(0, len(wl)):
                flatten_inputs.append(FlattenInput(time, lc, wl[i], self.bin_minutes))
            if self.detrend_method == 'gp':
                flatten_results = self.run_multiprocessing(self.run_cores, flattener.flatten_gp, flatten_inputs)
            else:
                flatten_results = self.run_multiprocessing(self.run_cores, flattener.flatten_bw, flatten_inputs)
        else:
            flatten_results = []
            for i in range(0, len(wl)):
                if self.detrend_method == 'gp':
                    flatten_results.append(flattener.flatten_gp(FlattenInput(time, lc, wl[i], self.bin_minutes)))
                else:
                    flatten_results.append(flattener.flatten_bw(FlattenInput(time, lc, wl[i], self.bin_minutes)))
        i = 0
        plot_axs = axs
        for flatten_lc_detrended, lc_trend, bin_centers, bin_means, flatten_wl in flatten_results:
            if self.n_detrends > 1:
                plot_axs = axs[i]
            final_lcs[i] = flatten_lc_detrended
            logging.info("%-25s%-17s%-15.4f%-11.2f%-15.2f", 'flatten_lc & trend_lc ' + str(i), self.detrend_method,
                         flatten_wl, np.std(flatten_lc_detrended) * 1e6, np.std(bin_means[~np.isnan(bin_means)]) * 1e6)
            if self.detrend_method == 'gp':
                plot_axs.set_title('ks=%s' % str(np.around(flatten_wl, decimals=4)))
            else:
                plot_axs.set_title('ws=%s' % str(np.around(flatten_wl, decimals=4)))
            plot_axs.plot(time, lc, linewidth=0.05, color='black', alpha=0.75, rasterized=True)
            plot_axs.plot(time, lc_trend, linewidth=1, color='orange', alpha=1.0)
            i = i + 1

        plot_dir = self.__init_object_dir(star_info.object_id)
        plt.savefig(plot_dir + 'Detrends_' + str(star_info.object_id) + '.png', dpi=200)
        fig.clf()
        plt.close(fig)
        return final_lcs, wl

    def __identify_signals(self, object_info, time, lcs, flux_err, star_info, transits_min_count, wl, id_run, cadence, report):
        detrend_logging_customs = 'ker_size' if self.detrend_method == 'gp' else "win_size"
        logging.info("%-12s%-12s%-10s%-8s%-18s%-14s%-14s%-12s%-12s%-14s%-16s%-14s%-12s%-25s%-10s%-18s%-20s",
                     detrend_logging_customs, "Period", "Per_err", "N.Tran", "Mean Depth (ppt)", "T. dur (min)", "T0",
                     "SNR", "SDE", "FAP", "Border_score", "Matching OI", "Harmonic", "Planet radius (R_Earth)", "Rp/Rs",
                     "Semi-major axis", "Habitability Zone")
        transit_results = {}
        run_dir = self.__init_object_run_dir(object_info.sherlock_id(), id_run)
        lc_df = pandas.DataFrame(columns=['#time', 'flux', 'flux_err'])
        args = np.argwhere(~np.isnan(lcs[0])).flatten()
        lc_df['#time'] = time[args]
        lc_df['flux'] = lcs[0][args]
        lc_df['flux_err'] = flux_err[args]
        lc_df.to_csv(run_dir + "/lc_0.csv", index=False)
        transit_result = self.__adjust_transit(time, lcs[0], star_info, transits_min_count, transit_results, report, cadence)
        transit_results[0] = transit_result
        r_planet = self.__calculate_planet_radius(star_info, transit_result.depth)
        rp_rs = transit_result.results.rp_rs
        a, habitability_zone = self.habitability_calculator \
            .calculate_hz_score(star_info.teff, star_info.mass, star_info.lum, transit_result.period)
        oi = self.__find_matching_oi(object_info, transit_result.period)
        logging.info('%-12s%-12.5f%-10.6f%-8s%-18.3f%-14.1f%-14.4f%-12.3f%-12.3f%-14s%-16.2f%-14s%-12s%-25.5f%-10.5f%-18.5f%-20s',
                     "PDCSAP_FLUX", transit_result.period,
                     transit_result.per_err, transit_result.count, transit_result.depth,
                     transit_result.duration * 24 * 60, transit_result.t0, transit_result.snr, transit_result.sde,
                     transit_result.fap, transit_result.border_score, oi, transit_result.harmonic, r_planet, rp_rs, a,
                     habitability_zone)
        plot_title = 'Run ' + str(id_run) + 'PDCSAP_FLUX # P=' + \
                     format(transit_result.period, '.2f') + 'd # T0=' + format(transit_result.t0, '.2f') + \
                     ' # Depth=' + format(transit_result.depth, '.4f') + 'ppt # Dur=' + \
                     format(transit_result.duration * 24 * 60, '.0f') + 'm # SNR:' + \
                     str(format(transit_result.snr, '.2f')) + ' # SDE:' + str(format(transit_result.sde, '.2f')) + \
                     ' # FAP:' + format(transit_result.fap, '.6f')
        plot_file = 'Run_' + str(id_run) + '_PDCSAP-FLUX_' + str(star_info.object_id) + '.png'
        self.__save_transit_plot(star_info.object_id, plot_title, plot_file, time, lcs[0], transit_result, cadence,
                                 id_run)
        for i in range(1, len(wl)):
            lc_df = pandas.DataFrame(columns=['#time', 'flux', 'flux_err'])
            args = np.argwhere(~np.isnan(lcs[i])).flatten()
            lc_df['#time'] = time[args]
            lc_df['flux'] = lcs[i][args]
            lc_df['flux_err'] = flux_err[args]
            lc_df.to_csv(run_dir + "/lc_" + str(i) + ".csv", index=False)
            transit_result = self.__adjust_transit(time, lcs[i], star_info, transits_min_count, transit_results, report, cadence)
            transit_results[i] = transit_result
            r_planet = self.__calculate_planet_radius(star_info, transit_result.depth)
            rp_rs = transit_result.results.rp_rs
            a, habitability_zone = self.habitability_calculator \
                .calculate_hz_score(star_info.teff, star_info.mass, star_info.lum, transit_result.period)
            oi = self.__find_matching_oi(object_info, transit_result.period)
            logging.info('%-12.4f%-12.5f%-10.6f%-8s%-18.3f%-14.1f%-14.4f%-12.3f%-12.3f%-14s%-16.2f%-14s%-12s%-25.5f%-10.5f%-18.5f%-20s',
                         wl[i], transit_result.period,
                     transit_result.per_err, transit_result.count, transit_result.depth,
                     transit_result.duration * 24 * 60, transit_result.t0, transit_result.snr, transit_result.sde,
                     transit_result.fap, transit_result.border_score, oi, transit_result.harmonic, r_planet, rp_rs, a,
                     habitability_zone)
            detrend_file_title_customs = 'ker_size' if self.detrend_method == 'gp' else 'win_size'
            detrend_file_name_customs = 'ks' if self.detrend_method == 'gp' else 'ws'
            title = 'Run ' + str(id_run) + '# ' + detrend_file_title_customs + ':' + str(format(wl[i], '.4f')) + \
                    ' # P=' + format(transit_result.period, '.2f') + 'd # T0=' + \
                    format(transit_result.t0, '.2f') + ' # Depth=' + format(transit_result.depth, '.4f') + "ppt # Dur=" + \
                    format(transit_result.duration * 24 * 60, '.0f') + 'm # SNR:' + \
                    str(format(transit_result.snr, '.2f')) + ' # SDE:' + str(format(transit_result.sde, '.2f')) + \
                    ' # FAP:' + format(transit_result.fap, '.6f')
            file = 'Run_' + str(id_run) + '_' + detrend_file_name_customs + '=' + str(format(wl[i], '.4f')) + '_' + \
                   str(star_info.object_id) + '.png'
            self.__save_transit_plot(star_info.object_id, title, file, time, lcs[i], transit_result, cadence, id_run)
        return transit_results

    def __find_matching_oi(self, object_info, period):
        if self.ois is not None:
            existing_period_in_object = self.ois[(self.ois["Object Id"] == object_info.mission_id()) &
                                                 (0.95 < self.ois["Period (days)"] / period) &
                                                 (self.ois["Period (days)"] / period < 1.05)]
            existing_period_in_oi = existing_period_in_object[existing_period_in_object["OI"].notnull()]
            oi = existing_period_in_oi["OI"].iloc[0] if len(
                existing_period_in_oi.index) > 0 else np.nan
        else:
            oi = ""
        return oi

    def __adjust_transit(self, time, lc, star_info, transits_min_count, run_results, report, cadence):
        oversampling = self.oversampling
        if oversampling is None:
            time_lapse = time[len(time) - 1] - time[0]
            oversampling = int(600 // time_lapse)
            if oversampling < 3:
                oversampling = 3
            elif oversampling > 10:
                oversampling = 10
        model = tls.transitleastsquares(time, lc)
        power_args = {"transit_template": self.fit_method, "period_min": self.period_min, "period_max": self.period_max,
                      "n_transits_min": transits_min_count, "T0_fit_margin": self.t0_fit_margin,
                      "show_progress_bar": False, "use_threads": self.run_cores, "oversampling_factor": oversampling,
                      "duration_grid_step": self.duration_grid_step}
        if star_info.ld_coefficients is not None:
            power_args["u"] = star_info.ld_coefficients
        if not star_info.radius_assumed:
            power_args["R_star"] = star_info.radius
            power_args["R_star_min"] = star_info.radius_min
            power_args["R_star_max"] = star_info.radius_max
        if not star_info.mass_assumed:
            power_args["M_star"] = star_info.mass
            power_args["M_star_min"] = star_info.mass_min
            power_args["M_star_max"] = star_info.mass_max
        if self.user_transit_template is not None:
            power_args["transit_template_generator"] = self.user_transit_template
        results = model.power(**power_args)
        if results.T0 != 0:
            depths = results.transit_depths[~np.isnan(results.transit_depths)]
            depth = (1. - np.mean(depths)) * 100 / 0.1  # change to ppt units
        else:
            depths = results.transit_depths
            depth = results.transit_depths
        in_transit = tls.transit_mask(time, results.period, results.duration, results.T0)
        transit_count = results.distinct_transit_count
        border_score = self.__compute_border_score(time, results, in_transit, cadence)
        # Recalculating duration because of tls issue https://github.com/hippke/tls/issues/83
        intransit_folded_model = np.where(results['model_folded_model'] < 1.)[0]
        if len(intransit_folded_model) > 0:
            duration = results['period'] * (results['model_folded_phase'][intransit_folded_model[-1]]
                                            - results['model_folded_phase'][intransit_folded_model[0]])
        else:
            duration = results['duration']
        harmonic = self.__is_harmonic(results, run_results, report)
        return TransitResult(results, results.period, results.period_uncertainty, duration,
                             results.T0, depths, depth, transit_count, results.snr,
                             results.SDE, results.FAP, border_score, in_transit, harmonic)

    def __calculate_planet_radius(self, star_info, depth):
        rp = np.nan
        try:
            rp = star_info.radius * math.sqrt(depth / 1000) / 0.0091577
        except ValueError as e:
            logging.error("Planet radius could not be calculated: depth=%s, star_radius=%s", depth, star_info.radius)
            logging.exception(str(e))
            print(e)
        return rp

    def __compute_border_score(self, time, result, intransit, cadence):
        shift_cadences = 60 / cadence
        edge_limit_days = 0.05
        transit_depths = np.nan_to_num(result.transit_depths)
        transit_depths = np.zeros(1) if type(transit_depths) is not np.ndarray else transit_depths
        transit_depths = transit_depths[transit_depths > 0] if len(transit_depths) > 0 else []
        # a=a[np.where([i for i, j in groupby(intransit)])]
        border_score = 0
        if len(transit_depths) > 0:
            shifted_transit_points = shift(intransit, shift_cadences, cval=np.nan)
            inverse_shifted_transit_points = shift(intransit, -shift_cadences, cval=np.nan)
            intransit_shifted = intransit | shifted_transit_points | inverse_shifted_transit_points
            time_edge_indexes = np.where(abs(time[:-1] - time[1:]) > edge_limit_days)[0]
            time_edge = np.full(len(time), False)
            time_edge[time_edge_indexes] = True
            time_edge[0] = True
            time_edge[len(time_edge) - 1] = True
            transits_in_edge = intransit_shifted & time_edge
            transits_in_edge_count = len(transits_in_edge[transits_in_edge])
            border_score = 1 - transits_in_edge_count / len(transit_depths)
        return border_score if border_score >= 0 else 0

    def __is_harmonic(self, tls_results, run_results, report):
        scales = [0.25, 0.5, 1, 2, 4]
        if self.rotator_period is not None:
            rotator_scale = round(tls_results.period / self.rotator_period, 2)
            rotator_harmonic = np.array(np.argwhere((np.array(scales) > rotator_scale - 0.02) & (np.array(scales) < rotator_scale + 0.02))).flatten()
            if len(rotator_harmonic) > 0:
                return str(scales[rotator_harmonic[0]]) + "*source"
        period_scales = [tls_results.period / round(item["period"], 2) for item in report]
        for key, period_scale in enumerate(period_scales):
            period_harmonic = np.array(np.argwhere((np.array(scales) > period_scale - 0.02) & (np.array(scales) < period_scale + 0.02))).flatten()
            if len(period_harmonic) > 0:
                period_harmonic = scales[period_harmonic[0]]
                return str(period_harmonic) + "*SOI" + str(key + 1)
        period_scales = [round(tls_results.period / run_results[key].period, 2) for key in run_results]
        for key, period_scale in enumerate(period_scales):
            period_harmonic = np.array(np.argwhere(
                (np.array(scales) > period_scale - 0.02) & (np.array(scales) < period_scale + 0.02))).flatten()
            if len(period_harmonic) > 0 and period_harmonic[0] != 2:
                period_harmonic = scales[period_harmonic[0]]
                return str(period_harmonic) + "*this(" + str(key) + ")"
        return "-"

    def __trim_axs(self, axs, N):
        [axis.remove() for axis in axs.flat[N:]]
        return axs.flat[:N]

    def __save_transit_plot(self, object_id, title, file, time, lc, transit_result, cadence, run_no):
        # start the plotting
        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(10, 10), constrained_layout=True)
        fig.suptitle(title)
        # 1-Plot all the transits
        in_transit = transit_result.in_transit
        tls_results = transit_result.results
        ax1.scatter(time[in_transit], lc[in_transit], color='red', s=2, zorder=0)
        ax1.scatter(time[~in_transit], lc[~in_transit], color='black', alpha=0.05, s=2, zorder=0)
        ax1.plot(tls_results.model_lightcurve_time, tls_results.model_lightcurve_model, alpha=1, color='red', zorder=1)
        # plt.scatter(time_n, flux_new_n, color='orange', alpha=0.3, s=20, zorder=3)
        plt.xlim(time.min(), time.max())
        # plt.xlim(1362.0,1364.0)
        ax1.set(xlabel='Time (days)', ylabel='Relative flux')
        # phase folded plus binning
        bins_per_transit = 8
        half_duration_phase = transit_result.duration / 2 / transit_result.period
        if np.isnan(transit_result.period) or np.isnan(transit_result.duration):
            bins = 200
            folded_plot_range = 0.05
        else:
            bins = transit_result.period / transit_result.duration * bins_per_transit
            folded_plot_range = half_duration_phase * 10
        binning_enabled = round(cadence) <= 5
        ax2.plot(tls_results.model_folded_phase, tls_results.model_folded_model, color='red')
        scatter_measurements_alpha = 0.05 if binning_enabled else 0.8
        ax2.scatter(tls_results.folded_phase, tls_results.folded_y, color='black', s=10,
                    alpha=scatter_measurements_alpha, zorder=2)
        ax2.set_xlim(0.5 - folded_plot_range, 0.5 + folded_plot_range)
        ax2.set(xlabel='Phase', ylabel='Relative flux')
        plt.ticklabel_format(useOffset=False)
        bins = 80
        if binning_enabled and tls_results.SDE != 0:
            folded_phase_zoom_mask = np.where((tls_results.folded_phase > 0.5 - folded_plot_range) &
                                              (tls_results.folded_phase < 0.5 + folded_plot_range))
            folded_phase = tls_results.folded_phase[folded_phase_zoom_mask]
            folded_y = tls_results.folded_y[folded_phase_zoom_mask]
            bin_means, bin_edges, binnumber = stats.binned_statistic(folded_phase, folded_y, statistic='mean',
                                                                     bins=bins)
            bin_stds, _, _ = stats.binned_statistic(folded_phase, folded_y, statistic='std', bins=bins)
            bin_width = (bin_edges[1] - bin_edges[0])
            bin_centers = bin_edges[1:] - bin_width / 2
            bin_size = int(folded_plot_range * 2 / bins * transit_result.period * 24 * 60)
            ax2.errorbar(bin_centers, bin_means, yerr=bin_stds / 2, xerr=bin_width / 2, marker='o', markersize=4,
                         color='darkorange', alpha=1, linestyle='none', label='Bin size: ' + str(bin_size) + "m")
            ax2.legend(loc="upper right")
        ax3 = plt.gca()
        ax3.axvline(transit_result.period, alpha=0.4, lw=3)
        plt.xlim(np.min(tls_results.periods), np.max(tls_results.periods))
        for n in range(2, 10):
            ax3.axvline(n * tls_results.period, alpha=0.4, lw=1, linestyle="dashed")
            ax3.axvline(tls_results.period / n, alpha=0.4, lw=1, linestyle="dashed")
        ax3.set(xlabel='Period (days)', ylabel='SDE')
        ax3.plot(tls_results.periods, tls_results.power, color='black', lw=0.5)
        ax3.set_xlim(0., max(tls_results.periods))
        plot_dir = self.__init_object_run_dir(object_id, run_no)
        plt.savefig(plot_dir + file, bbox_inches='tight', dpi=200)
        fig.clf()
        plt.close(fig)

    def __apply_mask_from_transit_results(self, time, lcs, transit_results, best_signal_index):
        intransit = tls.transit_mask(time, transit_results[best_signal_index].period,
                                     2 * transit_results[best_signal_index].duration, transit_results[best_signal_index].t0)
        if self.mask_mode == 'subtract':
            model_flux, model_flux_edges, model_flux_binnumber = stats.binned_statistic(
                transit_results[best_signal_index].results.model_lightcurve_time,
                transit_results[best_signal_index].results.model_lightcurve_model, statistic='mean', bins=len(intransit))
            for flux in lcs:
                flux[intransit] = flux[intransit] + np.full(len(flux[intransit]), 1) - model_flux[intransit]
                flux[intransit] = np.full(len(flux[intransit]), 1)
            clean_time = time
            clean_lcs = lcs
        else:
            clean_lcs = []
            for key, flux in enumerate(lcs):
                flux[intransit] = np.nan
                clean_time, clean_flux = tls.cleaned_array(time, flux)
                clean_lcs.append(clean_flux)
        return clean_time, np.array(clean_lcs)

    def run_multiprocessing(self, n_processors, func, func_input):
        with Pool(processes=n_processors) as pool:
            return pool.map(func, func_input)

    class KoiInput:
        def __init__(self, star_id, kic_id):
            self.star_id = star_id
            self.kic_id = kic_id
