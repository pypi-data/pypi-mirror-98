# -*- coding: utf-8 -*-
"""
Command line interface for ms3.
"""

import argparse, os

from ms3 import Parse
from ms3.utils import convert_folder, resolve_dir

__author__ = "johentsch"
__copyright__ = "Êcole Polytechnique Fédérale de Lausanne"
__license__ = "gpl3"



def check(args):
    labels_cfg = {'decode': True}
    log = args.log
    if log is not None:
        log = os.path.expanduser(log)
        if not os.path.isabs(log):
            log = os.path.join(os.getcwd(), log)
    logger_cfg = {
        'level': args.level,
        'file': log,
    }
    if args.regex is None:
        args.regex = r'\.mscx$'
    p = Parse(args.dir, paths=args.file, file_re=args.regex, exclude_re=args.exclude, recursive=args.nonrecursive,
              index=['key', 'fnames'], labels_cfg=labels_cfg, logger_cfg=logger_cfg)
    if '.mscx' not in p.count_extensions():
        p.logger.warning("No MSCX files to check.")
        return
    p.parse_mscx()
    res = True
    if not args.scores_only:
        wrong = p.check_labels()
        if wrong is None:
            res = None
        if len(wrong) == 0:
            p.logger.info("No syntactical errors.")
        else:
            if not args.assertion:
                p.logger.warning(f"The following labels don't match the regular expression:\n{wrong.to_string()}")
            res = False
    if args.assertion:
        assert res, "Contains syntactical errors:\n" + wrong.to_string()
    return res


def compare(args):
    logger_cfg = {
        'level': args.level,
    }
    if args.regex is None:
        args.regex = r'\.mscx$'
    p = Parse(args.dir, paths=args.file, file_re=args.regex, exclude_re=args.exclude, recursive=args.nonrecursive,
                  key='compare', index='fnames', logger_cfg=logger_cfg)
    if len(p._score_ids()) == 0:
        p.logger.warning(f"Your selection does not include any scores.")
        return
    p.add_rel_dir(args.annotations, suffix=args.suffix, score_extensions=args.extensions, new_key='old')
    p.parse_mscx()
    p.add_detached_annotations()
    p.compare_labels('old', store_with_suffix='_reviewed')


def extract(args):
    labels_cfg = {
        'positioning': args.positioning,    # default=False
        'decode': args.raw,                 # default=True
    }
    if sum([True for arg in [args.notes, args.labels, args.measures, args.rests, args.events, args.chords, args.expanded] if arg is not None]) == 0:
        print("Pass at least one of the following arguments: -N (notes), -L (labels), -M (measures), -R (rests), -E (events), -C (chords), -X (expanded)")
        return
    if args.suffix is not None:
        l_suff = len(args.suffix)
        params = ['notes', 'labels', 'measures', 'rests', 'events', 'chords', 'expanded']
        if l_suff == 0:
            suffixes = {f"{p}_suffix": f"_{p}" for p in params}
        elif l_suff == 1:
            suffixes = {f"{p}_suffix": args.suffix[0] for p in params}
        else:
            suffixes = {f"{p}_suffix": args.suffix[i] if i < l_suff else f"_{p}" for i, p in enumerate(params)}
    else:
        suffixes = {}

    logger_cfg = {
        'level': args.level,
        'file': args.logfile,
        'path': args.logpath,
    }

    p = Parse(args.dir, paths=args.file, file_re=args.regex, exclude_re=args.exclude, recursive=args.nonrecursive, labels_cfg=labels_cfg,
              logger_cfg=logger_cfg, simulate=args.test, ms=args.musescore)
    p.parse_mscx(simulate=args.test)
    p.store_lists(root_dir=args.out,
                  notes_folder=args.notes,
                  labels_folder=args.labels,
                  measures_folder=args.measures,
                  rests_folder=args.rests,
                  events_folder=args.events,
                  chords_folder=args.chords,
                  expanded_folder=args.expanded,
                  simulate=args.test,
                  unfold=args.unfold,
                  **suffixes)


def check_and_create(d):
    """ Turn input into an existing, absolute directory path.
    """
    if not os.path.isdir(d):
        d = resolve_dir(os.path.join(os.getcwd(), d))
        if not os.path.isdir(d):
            if input(d + ' does not exist. Create? (y|n)') == "y":
                os.mkdir(d)
            else:
                raise argparse.ArgumentTypeError(d + ' needs to be an existing directory')
    return resolve_dir(d)

def check_dir(d):
    if not os.path.isdir(d):
        d = resolve_dir(os.path.join(os.getcwd(), d))
        if not os.path.isdir(d):
            raise argparse.ArgumentTypeError(d + ' needs to be an existing directory')
    return resolve_dir(d)


def convert(args):
    dir, target = resolve_dir(args.dir), resolve_dir(args.target)
    #assert target[:len(
    #    dir)] != dir, "TARGET_DIR cannot be identical with nor a subfolder of DIR.\nDIR:        " + dir + '\nTARGET_DIR: ' + target
    convert_folder(dir, target,
                   extensions=args.extensions,
                   target_extension=args.format,
                   regex=args.regex,
                   suffix=args.suffix,
                   recursive=args.nonrecursive,
                   ms=args.musescore,
                   overwrite=args.overwrite,
                   parallel=args.nonparallel)


def repair(args):
    print(args.dir)


def run():
    # reusable argument sets
    input_args = argparse.ArgumentParser(add_help=False)
    input_args.add_argument('-d', '--dir', metavar='DIR', nargs='+', type=check_dir,
                                help='Folder(s) that will be scanned for input files. Defaults to current working directory if no individual files are passed via -f.')
    input_args.add_argument('-n', '--nonrecursive', action='store_false',
                                help="Don't scan folders recursively, i.e. parse only files in DIR.")
    input_args.add_argument('-r', '--regex', metavar="REGEX", default=r'(\.mscx|\.mscz)$',
                                help="Select only file names including this string or regular expression.")
    input_args.add_argument('-e', '--exclude', metavar="regex", default=r'^(\.|_)',
                                help="Any files or folders (and their subfolders) including this regex will be disregarded.")
    input_args.add_argument('-f', '--file', metavar='PATHs', nargs='+',
                                help='Add path(s) of individual file(s) to be checked.')
    input_args.add_argument('-l', '--level', metavar='{c, e, w, i, d}', default='i',
                                help="Choose how many log messages you want to see: c (none), e, w, i, d (maximum)")

    # main argument parser
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='''\
--------------------------
| Welcome to ms3 parsing |
--------------------------

The library offers you the following commands. Add the flag -h to one of them to learn about its parameters. 
''')
    subparsers = parser.add_subparsers(help='The action that you want to perform.', dest='action')

    extract_parser = subparsers.add_parser('extract', help="Extract selected information from MuseScore files and store it in TSV files.",
                                           parents=[input_args])
    extract_parser.add_argument('-N', '--notes', metavar='folder', help="Folder where to store TSV files with notes.")
    extract_parser.add_argument('-L', '--labels', metavar='folder', help="Folder where to store TSV files with annotation labels.")
    extract_parser.add_argument('-M', '--measures', metavar='folder', help="Folder where to store TSV files with measure information.")
    extract_parser.add_argument('-R', '--rests', metavar='folder', help="Folder where to store TSV files with rests.")
    extract_parser.add_argument('-E', '--events', metavar='folder', help="Folder where to store TSV files with events (notes, rests, articulation, etc.).")
    extract_parser.add_argument('-C', '--chords', metavar='folder', help="Folder where to store TSV files with chords, including lyrics, slurs, and other markup.")
    extract_parser.add_argument('-X', '--expanded', metavar='folder', help="Folder where to store TSV files with expanded DCML labels.")
    extract_parser.add_argument('-s', '--suffix', nargs='*',  metavar='SUFFIX',
                        help="Pass -s to use standard suffixes or -s SUFFIX to choose your own.")
    extract_parser.add_argument('-o', '--out', metavar='ROOT_DIR', type=check_and_create,
                                help="""Make all relative folder paths relative to ROOT_DIR rather than to MSCX_DIR.
This setting has no effect on absolute folder paths.""")
    extract_parser.add_argument('-m', '--musescore', default='auto', help="""Command or path of MuseScore executable. Defaults to 'auto' (attempt to use standard path for your system).
Other standard options are -m win, -m mac, and -m mscore (for Linux).""")
    extract_parser.add_argument('-t', '--test', action='store_true', help="No data is written to disk.")
    extract_parser.add_argument('-p', '--positioning', action='store_true', help="When extracting labels, include manually shifted position coordinates in order to restore them when re-inserting.")
    extract_parser.add_argument('--raw', action='store_false', help="When extracting labels, leave chord symbols encoded instead of turning them into a single column of strings.")
    extract_parser.add_argument('-u', '--unfold', action='store_true', help="Unfold the repeats for all stored DataFrames.")
    extract_parser.add_argument('--logfile', metavar='file path or file name', help="""Either pass an absolute file path to store all logging data in that particular file
or pass just a file name and the argument --logpath to create several log files of the same name in a replicated folder structure.
In the former case, --logpath will be disregarded.""")
    extract_parser.add_argument('--logpath', type=check_and_create, help="""If you define a path for storing log files, the original folder structure of the parsed
MuseScore files is recreated there. Additionally, you can pass a filename to --logfile to combine logging data for each 
subdirectory; otherwise, an individual log file is automatically created for each MuseScore file.""")
    extract_parser.set_defaults(func=extract)


    check_parser = subparsers.add_parser('check', help="""Parse MSCX files and look for errors.
In particular, check DCML harmony labels for syntactic correctness.""", parents=[input_args])
    check_parser.add_argument('-s', '--scores_only', action='store_true',
                              help="Don't check DCML labels for syntactic correctness.")
    check_parser.add_argument('--assertion', action='store_true', help="If you pass this argument, an error will be thrown if there are any mistakes.")
    check_parser.add_argument('--log', metavar='NAME', help='Can be a an absolute file path or relative to the current directory.')
    check_parser.set_defaults(func=check)


    compare_parser = subparsers.add_parser('compare',
        help="For MSCX files for which annotation tables exist, create another MSCX file with a coloured label comparison.",
        parents = [input_args])
    compare_parser.add_argument('-a', '--annotations', metavar='PATH', default='../harmonies',
                                help='Path relative to the score file(s) where to look for existing annotation tables.')
    compare_parser.add_argument('-s', '--suffix', metavar='SUFFIX', default='',
                                help='If existing annotation tables have a particular suffix, pass this suffix.')
    compare_parser.add_argument('-x', '--extensions', metavar='EXT', nargs='+',
                                help='If you only want to compare scores with particular extensions, pass these extensions.')
    compare_parser.set_defaults(func=compare)


    convert_parser = subparsers.add_parser('convert',
                                           help="Use your local install of MuseScore to convert MuseScore files.")
    convert_parser.add_argument('dir', metavar='DIR', type=check_dir,
                                help='Path to folder with files to convert; can be relative to the folder where the script is located.')
    convert_parser.add_argument('target', metavar='TARGET_DIR', type=check_and_create, default=os.getcwd(),
                                help='Path to folder for converted files. Defaults to current working directory.')
    convert_parser.add_argument('-x', '--extensions', nargs='+', default=['mscx', 'mscz'],
                                help="List, separated by spaces, the file extensions that you want to convert. Defaults to mscx mscz")
    convert_parser.add_argument('-f', '--format', default='mscx',
                                help="You may choose one out of {png, svg, pdf, mscz, mscx, wav, mp3, flac, ogg, xml, mxl, mid}")
    convert_parser.add_argument('-m', '--musescore', default='mscore', help="""Path to MuseScore executable. Defaults to the command 'mscore' (standard on *nix systems).
    To use standard paths on commercial systems, try -m win, or -m mac.""")
    convert_parser.add_argument('-r', '--regex', default=r'.*',
                                help="Convert only files containing this regular expression (or a simple search string).")
    convert_parser.add_argument('-n', '--nonrecursive', action='store_false',
                                help="Don't scan folders recursively, i.e. parse only files in DIR.")
    convert_parser.add_argument('-o', '--overwrite', action='store_true',
                                help="Set true if existing files are to be overwritten.")
    convert_parser.add_argument('-p', '--nonparallel', action='store_false',
                                help="Do not use all available CPU cores in parallel to speed up batch jobs.")
    convert_parser.add_argument('-s', '--suffix', metavar='SUFFIX', help='Add this suffix to the filename of every new file.')
    convert_parser.set_defaults(func=convert)

    repair_parser = subparsers.add_parser('repair',
                                          help="Apply automatic repairs to your uncompressed MuseScore files.",
                                          parents=[input_args])
    repair_parser.set_defaults(func=repair)

    args = parser.parse_args()
    if args.file is None and args.dir is None:
        args.dir = os.getcwd()
    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()





if __name__ == "__main__":
    run()
