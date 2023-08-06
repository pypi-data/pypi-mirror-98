from collections import defaultdict

import pandas as pd
import numpy as np
from fractions import Fraction as frac

from .logger import get_logger, function_logger, LoggedClass

class MeasureList(LoggedClass):
    """ Turns a _MSCX_bs4._measures DataFrame into a measure list and performs a couple of consistency checks on the score.

    Attributes
    ----------
    df : :obj:`pandas.DataFrame`
        The input DataFrame from _MSCX_bs4.raw_measures
    sections : :obj:`bool`, default True
        By default, section breaks allow for several anacrusis measures within the piece (relevant for `mc_offset` column)
        and make it possible to omit a repeat sign in the following bar (relevant for `next` column).
        Set to False if you want to ignore section breaks.
    secure : :obj:`bool`, default False
        By default, measure information from lower staves is considered to contain only redundant information.
        Set to True if you want to be warned about additional measure information from lower staves that is not taken into account.
    reset_index : :obj:`bool`, default True
        By default, the original index of `df` is replaced. Pass False to keep original index values.

    cols : :obj:`dict`
        Dictionary of the relevant columns in `df` as present after the parse.
    ml : :obj:`pandas.DataFrame`
        The measure list in the making; the final result.
    volta_structure : :obj:`dict`
        Keys are first MCs of volta groups, values are dictionaries of {volta_no: [mc1, mc2 ...]}

    """

    def __init__(self, df, sections=True, secure=False, reset_index=True, columns={}, logger_cfg={}):
        """

        Parameters
        ----------
        df
        sections : :obj:`bool`, optional
            By default, pieces containing section breaks (where counting MNs restarts) receive two more columns in the measures
            list, namely ``section`` and ``ambiguous_mn`` to grant access to MNs as shown in MuseScore. Pass False to not
            add such columns.
        secure
        reset_index
        logger_cfg : :obj:`dict`, optional
            The following options are available:
            'name': LOGGER_NAME -> by default the logger name is based on the parsed file(s)
            'level': {'W', 'D', 'I', 'E', 'C', 'WARNING', 'DEBUG', 'INFO', 'ERROR', 'CRITICAL'}
            'file': PATH_TO_LOGFILE to store all log messages under the given path.
        """
        super().__init__(subclass='MeasureList', logger_cfg=logger_cfg)
        self.df = df
        self.ml = pd.DataFrame()
        self.sections = sections
        self.secure = secure
        self.reset_index = reset_index
        self.volta_structure = {}
        self.cols = {'barline': 'voice/BarLine/subtype',
                     'breaks': 'LayoutBreak/subtype',
                     'dont_count': 'irregular',
                     'endRepeat': 'endRepeat',
                     'jump_bwd': 'Jump/jumpTo',
                     'jump_fwd': 'Jump/continueAt',
                     'keysig_col': 'voice/KeySig/accidental',
                     'len_col': 'Measure:len',
                     'markers': 'Marker/label',
                     'mc': 'mc',
                     'numbering_offset': 'noOffset',
                     'play_until': 'Jump/playUntil',
                     'sigN_col': 'voice/TimeSig/sigN',
                     'sigD_col': 'voice/TimeSig/sigD',
                     'staff': 'staff',
                     'startRepeat': 'startRepeat',
                     'volta_start': 'voice/Spanner/Volta/endings',
                     'volta_length': 'voice/Spanner/next/location/measures',
                     'volta_frac': 'voice/Spanner/next/location/fractions'}
        col_names = list(self.cols.keys())
        if any(True for c in columns if c not in col_names):
            wrong = [c for c in columns if c not in col_names]
            plural_s = 's' if  len(wrong) > 1 else ''
            logger.warning(f"Wrong column name{plural_s} passed: {wrong}. Only {col_names} permitted.")
            columns = {k: v for k, v in columns.items() if k in col_names}
        self.cols.update(columns)
        self.make_ml()



    def make_ml(self, section_breaks=True, secure=False, reset_index=True, logger_cfg={}):
        if logger_cfg != {}:
            self.update_logger_cfg(logger_cfg=logger_cfg)
        self.sections = section_breaks
        self.secure = secure
        self.reset_index = reset_index

        self.ml = self.get_unique_measure_list()
        info_cols = ['barline', 'breaks', 'dont_count', 'endRepeat', 'jump_bwd', 'jump_fwd', 'len_col', 'markers', 'numbering_offset',
                   'play_until', 'sigD_col', 'sigN_col', 'startRepeat', 'volta_start', 'volta_length']
        for col in [self.cols[col] for col in info_cols]:
            if not col in self.ml.columns:
                self.ml[col] = np.nan
        self.ml.rename(columns={self.cols[c]: c for c in ['mc', 'breaks', 'jump_bwd', 'jump_fwd', 'markers', 'play_until']}, inplace=True)
        if self.ml.jump_fwd.notna().any():
            self.ml.jump_fwd = self.ml.jump_fwd.replace({'/': None})
        def get_cols(l):
            return {col: self.cols[col] for col in l}
        volta_cols = get_cols(['mc', 'volta_start', 'volta_length'])
        if self.cols['volta_frac'] in self.ml.columns:
            volta_cols['frac_col'] = self.cols['volta_frac']
        self.volta_structure = get_volta_structure(self.ml, **volta_cols, logger=self.logger)
        func_params = {
            make_mn_col: get_cols(['dont_count', 'numbering_offset']),
            make_keysig_col: get_cols(['keysig_col']),
            make_timesig_col: dict(get_cols(['sigN_col', 'sigD_col']), logger=self.logger),
            make_actdur_col: get_cols(['len_col']),
            make_repeat_col: get_cols(['startRepeat', 'endRepeat']),
            make_volta_col: {'volta_structure': self.volta_structure},
            make_next_col: {'volta_structure': self.volta_structure,
                            'logger': self.logger, 'sections': self.sections},
            make_offset_col: {'mc_col': self.cols['mc'], 'section_breaks': 'breaks', 'logger': self.logger},
        }
        for func, params in func_params.items():
            self.add_col(func, **params)
        if reset_index:
            self.ml.reset_index(drop=True, inplace=True)
        rn = {self.cols[col]: col for col in ['barline', 'dont_count', 'numbering_offset']}
        self.ml.rename(columns=rn, inplace=True)
        ml_cols = ['mc', 'mn', 'keysig', 'timesig', 'act_dur', 'mc_offset', 'volta', 'numbering_offset', 'dont_count',
                   'barline', 'breaks', 'repeats']
        remove_if_empty = ['markers', 'jump_bwd', 'jump_fwd', 'play_until']
        if self.ml[remove_if_empty].isna().all().all():
            ml_cols += ['next']
        else:
            ml_cols += remove_if_empty + ['next']
        self.ml = self.ml[ml_cols]
        self.ml[['numbering_offset', 'dont_count']] = self.ml[['numbering_offset', 'dont_count']].apply(pd.to_numeric).astype('Int64')
        self.check_measure_numbers()



    def add_col(self, func, **kwargs):
        """ Inserts or appends a column created by `func(df, **kwargs)`
        """
        new_cols = func(self.ml, **kwargs)
        self.ml = pd.concat([self.ml, new_cols], axis=1)


    def get_unique_measure_list(self, **kwargs):
        """ Keep only the measure information from the first staff.
        Uses: keep_one_row_each()

        Parameters
        ----------
        mc_col, staff_col : :obj:`str`, optional
            DataFrame columns where MC and staff can be found. Staff is to be dropped.
        secure : :obj:`bool`
            If the dropped rows contain additional information, set `secure` to True to
            be informed about the information being lost by the function keep_one_row_each().
        **kwargs: Additional parameter passed on to keep_one_row_each(). Ignored if `secure=False`.
        """
        if not self.secure:
            return self.df.drop_duplicates(subset=self.cols['mc']).drop(columns=self.cols['staff'])
        return keep_one_row_each(self.df, compress_col=self.cols['mc'], differentiating_col=self.cols['staff'], logger=self.logger)


    def check_measure_numbers(self, mc_col='mc', mn_col='mn', act_dur='act_dur', mc_offset='mc_offset',
                              dont_count='dont_count', numbering_offset='numbering_offset'):
        def ordinal(i):
            if i == 1:
                return '1st'
            elif i == 2:
                return '2nd'
            elif i == 3:
                return '3rd'
            return f'{i}th'
        mc2mn = dict(self.ml[[mc_col, mn_col]].itertuples(index=False))
        # Check measure numbers in voltas
        for volta_group in self.volta_structure.values():
            for i, t in enumerate(zip(*volta_group.values()), start=1):
                m = t[0]
                mn = mc2mn[m]
                for j, mc in enumerate(t[1:], start=2):
                    current_mn = mc2mn[mc]
                    if current_mn != mn:
                        self.logger.warning(
                            f"MC {mc}, the {ordinal(i)} measure of a {ordinal(j)} volta, should have MN {mn}, not MN {current_mn}.")

        # Check measure numbers for split measures
        error_mask = (self.ml[mc_offset] > 0) & self.ml[dont_count].isna() & self.ml[numbering_offset].isna()
        n_errors = error_mask.sum()
        if n_errors > 0:
            mcs = ', '.join(self.ml.loc[error_mask, mc_col].astype(str))
            context_mask = error_mask | error_mask.shift(-1).fillna(False) | error_mask.shift().fillna(False)
            context = self.ml.loc[context_mask, [mc_col, mn_col, act_dur, mc_offset, dont_count, numbering_offset]]
            plural = n_errors > 1
            self.logger.warning(
                f"MC{'s' if plural else ''} {mcs} seem{'' if plural else 's'} to be offset from the MN's beginning but ha{'ve' if plural else 's'} not been excluded from barcount. Context:\n{context}")


@function_logger
def make_next_col(df, volta_structure={}, sections=True, columns={}, name='next'):
    """ Uses a `NextColumnMaker` object to create a column with all MCs that can follow each MC (e.g. due to repetitions).

    Parameters
    ----------
    df : :obj:`pandas.DataFrame`
        Raw measure list.
    volta_structure : :obj:`dict`, optional
        This parameter can be computed by get_volta_structure(). It is empty if
        there are no voltas in the piece.
    sections : :obj:`bool`, optional
        By default, pieces containing section breaks (where counting MNs restarts) receive two more columns in the measures
        list, namely ``section`` and ``ambiguous_mn`` to grant access to MNs as shown in MuseScore. Pass False to not
        add such columns.
    """
    if sections and (df['breaks'].fillna('') == 'section').sum() == 0:
        sections = False

    # col_names = ['mc', 'breaks', 'jump_bwd', 'jump_fwd', 'markers', 'play_until', 'repeats', 'volta']
    col_names = ['mc', 'repeats', 'breaks']
    sel = df[col_names[1:]].notna().any(axis=1)

    ncm = NextColumnMaker(df, volta_structure, sections=sections, logger_cfg={'name': logger.name})
    for mc, repeats, breaks in df.loc[sel, col_names].itertuples(index=False):
        ncm.treat_input(mc, repeats, breaks == 'section')

    for mc, has_repeat in ncm.check_volta_repeats.items():
        if not has_repeat:
            logger.warning(f"MC {mc} is missing an endRepeat.")

    try:
        nxt_col = df['mc'].map(ncm.next).map(tuple)
    except:
        print(df['mc'])
        print(ncm.next)
        raise
    return nxt_col.rename(name)


class NextColumnMaker(LoggedClass):

    def __init__(self, df, volta_structure, sections=True, logger_cfg={}):
        super().__init__(subclass='NextColumnMaker', logger_cfg=logger_cfg)
        self.sections = sections
        self.mc = df.mc  # Series
        if self.mc.isna().any():
            self.logger.warning(f"MC column contains NaN which will lead to an incorrect 'next' column.")
        nxt = self.mc.shift(-1).astype('Int64').map(lambda x: [x] if not pd.isnull(x) else [-1])
        last_row = df.iloc[-1]
        end_mc = last_row.mc
        self.next = {mc: nx for mc, nx in zip(self.mc, nxt)}
        fines = df.markers.fillna('').str.contains('fine')
        if fines.any():
            if fines.sum() > 1:
                self.logger.warning(f"ms3 currently does not deal with more than one Fine. Using last measure as Fine.")
            elif last_row.repeats != 'end' and pd.isnull(last_row.jump_bwd):
                self.logger.warning(
                    f"Piece has a Fine but the last MC is missing a repeat sign or a D.C. (da capo) or D.S. (dal segno). Ignoring Fine.")
            else:
                fine_mc = df[fines].iloc[0].mc
                volta_mcs = dict(df.loc[df.volta.notna(), ['mc', 'volta']].values)
                if fine_mc in volta_mcs:
                    self.next[fine_mc] = [-1]
                else:
                    self.next[fine_mc].append(-1)
                end_mc = fine_mc
                self.next[last_row.mc] = []
                self.logger.debug(f"Set the Fine in MC {fine_mc} as final measure.")

        if df.jump_bwd.notna().any():
            #jumps = dict(map(lambda row: (row[0], tuple(row[1:])), df.loc[df.jump_bwd.notna(), ['mc', 'jump_bwd', 'jump_fwd', 'play_until']].values))
            markers = defaultdict(list)
            for t in df.loc[df.markers.notna(), ['mc', 'markers']].itertuples(index=False):
                for marker in t.markers.split(' & '):
                    markers[marker].append(t.mc)
            # markers = {marker: mcs.to_list() for marker, mcs in df.groupby('markers').mc}

            def jump2marker(from_mc, marker, untill=None):

                def get_marker_mc(m, untilll=False):
                    mcs = markers[m]
                    if len(mcs) > 1:
                        if untilll:
                            self.logger.warning(
f"After jumping from MC {mc} to {marker}, the music is supposed to play until label {m} but there are {len(mcs)} of them: {mcs}. Picking the first one.")
                        else:
                            self.logger.warning(
                            f"MC {mc} is supposed to jump to label {m} but there are {len(mcs)} of them: {mcs}. Picking the first one.")
                    return mcs[0]

                if marker == 'start':
                    jump_to_mc = 1
                elif marker in markers:
                    jump_to_mc = get_marker_mc(marker)
                else:
                    self.logger.warning(
                        f"MC {from_mc} is supposed to jump to label {marker} but there is no corresponding marker in the score. Ignoring.")
                    return None, None

                if pd.isnull(untill):
                    end_of_jump_mc = None
                elif untill == 'end':
                    end_of_jump_mc = end_mc
                elif untill in markers:
                    end_of_jump_mc = get_marker_mc(untill, True)
                else:
                    end_of_jump_mc = None
                    self.logger.warning(
                        f"After jumping from MC {from_mc} to {marker}, the music is supposed to play until label {untill} but there is no corresponding marker in the score. Ignoring.")
                return jump_to_mc, end_of_jump_mc

            bwd_jumps = df.loc[df.jump_bwd.notna(), ['mc', 'jump_bwd', 'jump_fwd', 'play_until']] #.copy()
            #bwd_jumps.jump_fwd = bwd_jumps.jump_fwd.replace({'/': None})
            for mc, jumpb, jumpf, until in bwd_jumps.itertuples(name=None, index=False):
                jump_to_mc, end_of_jump_mc = jump2marker(mc, jumpb, until)
                self.next[mc] = [jump_to_mc]
                self.logger.debug(f"Included backward jump from MC {mc} to the {jumpb} in MC {jump_to_mc}.")
                if not pd.isnull(jumpf):
                    if end_of_jump_mc is None:
                        if jumpf in markers:
                            reason = f"{until} was not found in the score."
                        else:
                            reason = "neither of them was found in the score."
                        self.logger.warning(f"The jump from MC {mc} to {self.next[mc][0]} is supposed to jump forward from {until} to {jumpf}, but {reason}")
                    else:
                        to_mc, _ = jump2marker(end_of_jump_mc, jumpf)
                        self.next[jump_to_mc].append(to_mc)
                        self.logger.debug(f"Included forward jump from the {jumpb} in MC {jump_to_mc} to the {jumpf} in MC {to_mc} ")
                
        self.repeats = dict(df[['mc', 'repeats']].values)
        self.start = None
        self.potential_start = None
        self.potential_ending = None
        self.check_volta_repeats = {}
        self.wasp_nest = {}
        for first_mc, group in volta_structure.items():
            firsts = []
            lasts = []
            last_volta = max(group)
            mc_after_voltas = max(group[last_volta]) + 1
            if mc_after_voltas not in self.next:
                mc_after_voltas = None
            for volta, mcs in group.items():
                # every volta except the last needs will have the `next` value replaced either by the startRepeat MC or
                # by the first MC after the last volta
                if volta < last_volta:
                    lasts.append(mcs[-1])
                # the bar before the first volta will have first bar of every volta as `next`
                firsts.append(mcs[0])
            self.next[first_mc - 1] = firsts + self.next[first_mc - 1][1:]
            # check_volta_repeats keys are last MCs of all voltas except last voltas, values are all False at the beginning
            # and they are set to True if
            lasts_with_repeat = [l for l in lasts if self.repeats[l] == 'end']
            for l in lasts:
                if not pd.isnull(self.repeats[l]):
                    if self.repeats[l] == 'end':
                        self.check_volta_repeats[l] = False
                        self.wasp_nest[l] = lasts_with_repeat
                    else:
                        self.logger.warning(f"MC {l}, which is the last MC of a volta, has a different repeat sign than 'end': {self.repeats[l]}")
                elif mc_after_voltas is None:
                    if l not in bwd_jumps.mc.values:
                        self.logger.warning(f"MC {l} is the last MC of a volta but has neither a repeat sign or jump, nor is there a MC after the volta group where to continue.")
                else:
                    self.next[l] = [mc_after_voltas]




    def start_section(self, mc):
        if self.start is not None:
            if self.potential_ending is None:
                self.logger.warning(f"""The startRepeat in MC {self.start} is missing its endRepeat.
For correction, MC {mc - 1} is interpreted as such because it precedes the next startRepeat.""")
                self.end_section(mc - 1)
            else:
                ending, reason = self.potential_ending
                self.logger.warning(f"""The startRepeat in MC {self.start} is missing its endRepeat.
For correction, MC {ending} is interpreted as such because it {reason}.""")
                self.end_section(ending)
        self.start = mc
        self.potential_start = None
        self.potential_ending = None

    def end_section(self, mc):
        if self.start is not None:
            start = self.start
        elif self.potential_start is not None:
            start, reason = self.potential_start
            if reason == 'firstMeasure':
                self.logger.debug(
                    f"MC {start} has been inferred as startRepeat for the endRepeat in MC {mc} because it is the first bar of the piece.")
            else:
                msg = f"""The endRepeat in MC {mc} is missing its startRepeat.
For correction, MC {start} is interpreted as such because it {reason}."""
                if "section break" in msg:
                    self.logger.debug(msg)
                else:
                    self.logger.warning(msg)
        else:
            start = None

        if mc in self.check_volta_repeats:
            self.check_volta_repeats[mc] = True
            if mc in self.wasp_nest:
                if start is None:
                    self.logger.error(
                        f"No starting point for the repeatEnd in MC {mc} could be determined. It is being ignored.")
                else:
                    volta_endings = self.wasp_nest[mc]
                    for e in volta_endings:
                        self.next[e] = [start]
                        del (self.wasp_nest[e])
                    self.start = None
        elif start is None:
            self.logger.error(f"No starting point for the repeatEnd in MC {mc} could be determined. It is being ignored.")
        else:
            self.next[mc] = [start] + self.next[mc]
            if self.potential_start is not None:
                pot_mc, reason = self.potential_start
                if pot_mc == mc + 1:
                    self.potential_start = (pot_mc, reason + ' and the previous endRepeat')
                else:
                    self.potential_start = (mc + 1, 'is the first bar after the previous endRepeat')
            else:
                self.potential_start = (mc + 1, 'is the first bar after the previous endRepeat')
            self.start = None

    def treat_input(self, mc, repeat, section_break=False):
        if section_break:
            self.potential_ending = (mc, 'precedes a section break')
            self.potential_start = (mc + 1, 'follows a section break')

        if repeat == 'firstMeasure':
            self.potential_start = (mc, 'firstMeasure')
        elif repeat == 'start':
            self.start_section(mc)
        elif repeat == 'startend':
            self.start_section(mc)
            self.end_section(mc)
        elif repeat == 'end':
            self.end_section(mc)
        elif repeat == 'lastMeasure':
            if self.start is not None:
                self.potential_ending = (mc, 'is the last bar of the piece.')
                self.start_section(mc + 1)
                self.start = None


@function_logger
def get_volta_structure(df, mc, volta_start, volta_length, frac_col=None):
    """
        Uses: treat_group()
    """
    cols = [mc, volta_start, volta_length]
    sel = df[volta_start].notna()
    voltas = (df.loc[sel, cols])
    if voltas[volta_length].isna().sum() > 0:
        rows = voltas[voltas[volta_length].isna()]
        logger.debug(f"The volta in MC {rows[mc].values} has no length: A standard length of 1 is supposed.")
        voltas[volta_length] = voltas[volta_length].fillna(0)
    voltas = voltas.astype(int)
    if len(voltas) == 0:
        return {}
    if frac_col is not None:
        voltas[volta_length] += df.loc[sel, frac_col].notna()
    voltas.loc[voltas[volta_start] == 1, 'group'] = 1
    voltas.group = voltas.group.fillna(0).astype(int).cumsum()
    groups = {v[mc].iloc[0]: v[cols].to_numpy() for _, v in voltas.groupby('group')}
    res = {mc: treat_group(mc, group, logger=logger) for mc, group in groups.items()}
    logger.debug(f"Inferred volta structure: {res}")
    return res




@function_logger
def keep_one_row_each(df, compress_col, differentiating_col, differentiating_val=None, ignore_columns=None, fillna=True,
                      drop_differentiating=True):
    """ Eliminates duplicates in `compress_col` but warns about values within the
        dropped rows which diverge from those of the remaining rows. The `differentiating_col`
        serves to identify places where information gets lost during the process.

    The result of this function is the same as `df.drop_duplicates(subset=[compress_col])`
    if `differentiating_val` is None, and `df[df[compress_col] == differentiating_val]` otherwise
    but with the difference that only adjacent duplicates are eliminated.

    Parameters
    ----------
    compress_col : :obj:`str`
        Column with duplicates (e.g. measure counts).
    differentiating_col : :obj:`str`
        Column that differentiates duplicates (e.g. staff IDs).
    differentiating_val : value, optional
        If you want to keep rows with a certain `differentiating_col` value, pass that value (e.g. a certain staff).
        Otherwise, the first row of every `compress_col` value is kept.
    ignore_columns : :obj:`Iterable`, optional
        These columns are not checked.
    fillna : :obj:`bool`, optional
        By default, missing values of kept rows are filled if the dropped rows contain
        one unique value in that particular column. Pass False to keep rows as they are.
    drop_differentiating : :obj:`bool`, optional
        By default, the column that differentiates the `compress_col` is dropped.
        Pass False to prevent that.
    """
    if ignore_columns is None:
        ignore_columns = [differentiating_col]
    else:
        ignore_columns.append(differentiating_col)
    consider_for_notna = [col for col in df.columns if not col in ignore_columns + [compress_col]]
    consider_for_duplicated = consider_for_notna + [compress_col]
    empty_rows = df[consider_for_duplicated].isnull().all(axis=1)
    if differentiating_val is not None:
        keep_rows = df[differentiating_col] == differentiating_val
    else:
        keep_rows = df[compress_col] != df[compress_col].shift()
    drop_rows = ~keep_rows & empty_rows
    result = df.drop(df[drop_rows].index)

    def compress(df):
        if len(df) == 1:
            return df.iloc[0]
        if differentiating_val is None:
            keep_row = df.iloc[[0]].copy()
            remaining = df.iloc[1:].drop_duplicates(subset=consider_for_duplicated)
        else:
            keep = df[differentiating_col] == differentiating_val
            keep_row = df[keep].copy()
            assert len(keep_row) == 1, "The column designated by `differentiating_col` needs to be unique."
            remaining = df[~keep].drop_duplicates(subset=consider_for_duplicated)
        if len(remaining) == 1:
            return keep_row
        which = keep_row[compress_col]
        for val, (col_name, col) in zip(*keep_row[consider_for_notna].itertuples(index=False, name=None),
                                        remaining[consider_for_notna].items()):
            if col.isna().all():
                continue
            vals = col[col.notna()].unique()
            if len(vals) == 1:
                if vals[0] == val:
                    continue
                new_val = vals[0]
                if pd.isnull(val) and fillna:
                    keep_row[col_name] = new_val
                    logger.warning(
                        f"{compress_col} {which}: The missing value in '{col_name}' was replaced by '{new_val}', present in {differentiating_col} {remaining.loc[remaining[col_name] == new_val, differentiating_col].values}.")
                    continue
                logger.warning(
                    f"{compress_col} {which}: The value '{new_val}' in '{col_name}' of {differentiating_col} {remaining.loc[remaining[col_name] == new_val, differentiating_col].values} is lost.")
                continue
            logger.warning(
                f"{compress_col} {which}: The values {vals} in '{col_name}' of {differentiating_col} {remaining.loc[col.notna(), differentiating_col].values} are lost.")
        return keep_row

    result = result.groupby(compress_col, group_keys=False).apply(compress)
    return result.drop(columns=differentiating_col) if drop_differentiating else result


def make_actdur_col(df, len_col, timesig_col='timesig', name='act_dur'):
    actdur = df[len_col]
    actdur = actdur.fillna(df[timesig_col])
    try:
        return actdur.map(frac).rename(name)
    except:
        print(df.to_dict())
        raise



def make_keysig_col(df, keysig_col, name='keysig'):
    if keysig_col in df:
        return df[keysig_col].fillna(method='ffill').fillna(0).astype(int).rename(name)
    return pd.Series(0, index=df.index).rename(name)


def make_mn_col(df, dont_count, numbering_offset, name='mn'):
    """ Compute measure numbers where one or two columns can influence the counting.

    Parameters
    ----------
    df : :obj:`pd.DataFrame`
        If no other parameters are given, every row is counted, starting from 1.
    dont_count : :obj:`str`, optional
        This column has notna() for measures where the option "Exclude from bar count" is activated, NaN otherwise.
    numbering_offset : :obj:`str`, optional
        This column has values of the MuseScore option "Add to bar number", which adds
        notna() values to this and all subsequent measures.
    """
    if dont_count is None:
        mn = pd.Series(range(1, len(df) + 1), index=df.index)
    else:
        excluded = df[dont_count].fillna(0).astype(bool)
        mn = (~excluded).cumsum()
    if numbering_offset is not None:
        offset = df[numbering_offset]
        if offset.notna().any():
            offset = offset.fillna(0).astype(int).cumsum()
            mn += offset
    return mn.rename(name)







@function_logger
def make_offset_col(df, mc_col='mc', timesig='timesig', act_dur='act_dur', next_col='next', section_breaks=None, name='mc_offset'):
    """ If one MN is composed of two MCs, the resulting column indicates the second MC's offset from the MN's beginning.

    Parameters
    ----------
    mc_col, timesig, act_dur, next_col : :obj:`str`, optional
        Names of the required columns.
    section_breaks : :obj:`str`, optional
        If you pass the name of a column, the string 'section' is taken into account
        as ending a section and therefore potentially ending a repeated part even when
        the repeat sign is missing.
    """
    nom_dur = df[timesig].map(frac)
    sel = df['act_dur'] < nom_dur
    if sel.sum() == 0:
        return pd.Series(0, index=df.index, name=name)

    if section_breaks is not None and len(df[df[section_breaks].fillna('') == 'section']) == 0:
        section_breaks = None
    cols = [mc_col, next_col]
    if section_breaks is not None:
        cols.append(section_breaks)
        last_mc = df[mc_col].max()
        offsets = {m: 0 for m in df[df[section_breaks].fillna('') == 'section'].mc + 1 if m <= last_mc}
        # offset == 0 is a neutral value but the presence of mc in offsets indicates that it could potentially be an
        # (incomplete) pickup measure which can be offset even if the previous measure is complete
    else:
        offsets = {}
    nom_durs = dict(df[[mc_col]].join(nom_dur).itertuples(index=False))
    act_durs = dict(df[[mc_col, act_dur]].itertuples(index=False))

    def missing(mc):
        return nom_durs[mc] - act_durs[mc]

    def add_offset(mc, val=None):
        if val is None:
            val = missing(mc)
        offsets[mc] = val


    irregular = df.loc[sel, cols]
    if irregular[mc_col].iloc[0] == 1:
        # Check whether first MC is an anacrusis and mark accordingly
        if len(irregular) > 1 and irregular[mc_col].iloc[1] == 2:
            if not missing(1) + act_durs[2] == nom_durs[1]:
                add_offset(1)
            else:
                # regular divided measure, no anacrusis
                pass
        else:
            # is anacrusis
            add_offset(1)
    for t in irregular.itertuples(index=False):
        if section_breaks:
            mc, nx, sec = t
            if sec == 'section':
                nxt = [i for i in nx if i <= mc]
                if len(nxt) == 0:
                    logger.debug(f"MC {mc} ends a section with an incomplete measure.")
            else:
                nxt = [i for i in nx]
        else:
            mc, nx = t
            nxt = [i for i in nx]
        if mc not in offsets:
            completions = {m: act_durs[m] for m in nxt if m > -1}
            expected = missing(mc)
            errors = sum(True for c in completions.values() if c != expected)
            if errors > 0:
                logger.warning(
                    f"The incomplete MC {mc} (timesig {nom_durs[mc]}, act_dur {act_durs[mc]}) is completed by {errors} incorrect duration{'s' if errors > 1 else ''} (expected: {expected}):\n{completions}")
            for compl in completions.keys():
                add_offset(compl)
        elif offsets[mc] == 0:
            add_offset(mc)
    mc2ix = {m: ix for ix, m in df.mc.iteritems()}
    result = {mc2ix[m]: offset for m, offset in offsets.items()}
    return pd.Series(result, name=name).reindex(df.index, fill_value=0)


def make_repeat_col(df, startRepeat, endRepeat, name='repeats'):
    repeats = df[startRepeat].copy()
    ends = df[endRepeat]
    sel = dict(
        start=repeats.notna() & ends.isna(),
        startend=repeats.notna() & ends.notna(),
        end=repeats.isna() & ends.notna()
    )
    for case, arr in sel.items():
        repeats.loc[arr] = case
    if pd.isnull(repeats.iloc[0]):
        repeats.iloc[0] = 'firstMeasure'
    if pd.isnull(repeats.iloc[-1]):
        repeats.iloc[-1] = 'lastMeasure'
    return repeats.rename(name)


@function_logger
def make_timesig_col(df, sigN_col, sigD_col, name='timesig'):
    if pd.isnull(df[sigN_col].iloc[0]):
        logger.warning("No time signature defined in MC 1: Wild-guessing it's 4/4")
        sigN_pos, sigD_pos = df.columns.get_loc(sigN_col), df.columns.get_loc(sigD_col)
        df.iloc[0, [sigN_pos, sigD_pos]] = '4'
    n = pd.to_numeric(df[sigN_col].fillna(method='ffill')).astype(str)
    d = pd.to_numeric(df[sigD_col].fillna(method='ffill')).astype(str)
    return (n + '/' + d).rename(name)


def make_volta_col(df, volta_structure, mc='mc', name='volta'):
    """ Create the input for `volta_structure` using get_volta_structure()
    """
    mc2volta = {mc: volta for group in volta_structure.values() for volta, mcs in group.items() for mc in mcs}
    return df[mc].map(mc2volta).astype('Int64').rename(name)



@function_logger
def treat_group(mc, group):
    """ Helper function for make_volta_col()
        Input example: array([[93,  1,  1], [94,  2,  2], [96,  3,  1]])
        where columns are (MC, volta number, volta length).
    """
    n = group.shape[0]
    mcs, numbers, lengths = group.T
    # check volta numbers
    expected = np.arange(1, n + 1)
    if (numbers != expected).any():
        logger.warning(f"Volta group of MC {mc} should have voltas {expected.tolist()} but has {numbers.tolist()}")
    # check volta lengths
    frst = lengths[0]
    if (lengths != frst).any():
        logger.warning(
            f"Volta group of MC {mc} contains voltas with different lengths: {lengths.tolist()} Check for correct computation of MNs.")
    # check for overlaps and holes
    boundaries = np.append(mcs, mcs[-1] + group[-1, 2])
    correct = {i: np.arange(fro, to).tolist() for i, (fro, to) in
               enumerate(zip(boundaries[:-1], boundaries[1:]), start=1)}
    in_score = {i: [row[0] + i for i in range(row[2])] for i, row in enumerate(group, start=1)}
    if in_score != correct:
        logger.warning(
            f"The incorrect structure {in_score} of the volta groupa of MC {mc} has been corrected to {correct}.")
    return correct