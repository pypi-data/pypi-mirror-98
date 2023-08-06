import argparse
import csv
import logging
import os
import shutil
import sys
from collections import defaultdict
from typing import List, Dict
from pathlib import Path

from .songs import SongRecord, SongTags, RecordTagLink


logging.basicConfig(format='%(levelname)s %(message)s')
logger = logging.getLogger(__name__)


def fuse_main_csv(full_path: Path) -> List[Dict[str, str]]:
    csv_filenames = full_path.glob('*.csv')
    lines = []
    for csv_filename in csv_filenames:
        with open(csv_filename.absolute(), 'r') as csv_in:
            reader = csv.DictReader(
                csv_in,
                fieldnames=['title', 'album', 'artist', 'duration_ms', 'rating', 'play_count', 'removed'],
            )
            try:
                next(reader)
                lines.extend([SongRecord(original_csv_name=csv_filename.name, **line) for line in reader])
            except StopIteration:
                logger.error('All csv files must begin with header')
                return None
            except TypeError:
                logger.error('CSV files are not in expected format.')
                return None
    return lines


def output_main_csv(main_csv: List[SongRecord], full_path: Path):
    {'Title': '05 - I Shot The Sheriff.mp3',
     'Album': 'Burnin&#39;',
     'Artist': 'Bob Marley',
     'Duration (ms)': '282000',
     'Rating': '0',
     'Play Count': '0',
     'Removed': ''}
    with open(full_path / 'main_csv.csv', 'w') as outfile:
        header = ['Title,Album,Artist,Duration (ms),Rating,Play Count,Removed']
        lines = '\n'.join(header + [str(line) for line in main_csv])
        outfile.writelines(lines)


def move_audio_files(target_path: Path,
                     tagged_data: List[RecordTagLink],
                     copy: bool = True,
                     dry_run: bool = False):
    '''
    Actually move or copy files.
    Loops twice despite being possible to do in one loop to prevent data loss
    '''
    existing_directories = set()
    if dry_run:
        def shutil_command(*args, **kwargs):
            pass
    else:
        shutil_command = shutil.copyfile if copy else shutil.move

    origins = []
    targets = []
    duplicate_origins = []
    duplicate_targets = []
    for data in tagged_data:
        target_directory = target_path / data.tags.artist / data.tags.album
        if target_directory not in existing_directories:
            try:
                if not dry_run:
                    os.makedirs(target_directory)
            except FileExistsError:
                pass
            existing_directories.add(target_directory)

        origin = data.tags.filepath
        target = target_directory / data.target_filename
        if origin in origins:
            duplicate_origins.append(origin)
        if target in targets:
            duplicate_targets.append(target)
        origins.append(origin)
        targets.append(target)

    if duplicate_targets:
        logger.error('Duplicates targets found. File copy (or move) cannot continue until '
                     'the duplicates are addressed manually. Targets with multiple sources include: %s',
                     str(duplicate_targets))
        return

    elif duplicate_origins:
        raise ValueError(
            'Duplicate origins found. This is a programming error, '
            'as each file should only be processed once.')

    for origin, target in zip(origins, targets):
        shutil_command(origin, target)


def merge_csv_with_filetags(full_path: Path, main_csv: List[SongRecord], dry_run: bool):
    lines_by_artist_album = defaultdict(dict)
    lost_lines = []
    for line in main_csv:
        if not line.artist or not line.album:
            lost_lines.append(line)
        else:
            if not lines_by_artist_album[line.artist].get(line.album):
                lines_by_artist_album[line.artist][line.album] = {}

            lines_by_artist_album[line.artist][line.album][line.title] = line

    lost_audiofiles = []
    unmatched_audiofiles = []
    matched_audiofiles = []
    for audiofile in full_path.glob('*.mp3'):
        tags = SongTags(filepath=audiofile)
        if not tags.artist or not tags.album:
            lost_audiofiles.append(audiofile)
            continue
        corresponding_line = lines_by_artist_album[tags.artist].get(tags.album, {}).get(tags.title)
        if not corresponding_line:
            unmatched_audiofiles.append(tags)
            continue

        matched_audiofiles.append(RecordTagLink(songrecord=corresponding_line, tags=tags, dry_run=dry_run))
    if any([lost_lines, lost_audiofiles, unmatched_audiofiles]):
        return lost_lines, lost_audiofiles, unmatched_audiofiles
    else:
        return matched_audiofiles


def main():
    parser = argparse.ArgumentParser(
        description='Convert google music takeout results to plex-friendly structure')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument(
        '-i',
        '--takeout-tracks-directory',
        type=str,
        required=True,
        help='The full path to the directory containing the flat list of tracks and corresponding csv files.',
    )
    parser.add_argument(
        '--dry-run',
        type=bool,
        default=False,
        nargs='?',
        help=('Prevent the renaming, removal, or creation of any actual audio files. '
              'Will still output the combined CSV file for manul confirmation'),
    )
    parser.add_argument(
        '--move-files',
        type=bool,
        default=False,
        nargs='?',
        help=('In order to save space during operation, actually move files instead of copying them. '
              'If something goes wrong during the command, rolling back will not be possible.'),
    )
    parser.add_argument(
        '--main-csv',
        type=str,
        default='',
        nargs='?',
        help=('Specify the google takeout csv file to use for operating on audio files. '
              'This can be generated by running with dry-run first. '
              'Specifying it will skip the csv file scrape step.'),
    )
    parser.add_argument(
        '--output-directory',
        type=str,
        default='out',
        nargs='?',
        help=('Specify the parent directory under which to create the '
              'new artist/album directories in to which to move the audio files.'),
    )
    cmd_args = vars(parser.parse_args())

    # Validate tracks directory is actually a directory.
    full_path = Path(cmd_args['takeout_tracks_directory'])
    if not full_path.is_dir():
        logger.error(
            'Takeout tracks directory must be a directory. %s is not a directory.',
            str(full_path.absolute()),
        )
        sys.exit(1)

    # Validate the main csv is actually a file if it was specified
    main_csv = Path(cmd_args['main_csv']) if cmd_args.get('main_csv') else None
    if main_csv:
        if not main_csv.is_file():
            logger.error('Main CSV file must be a csv file. %s is not a csv file.', str(main_csv.absolute()))
            sys.exit(1)

    if not main_csv:
        main_csv = fuse_main_csv(full_path)
        if not main_csv:
            sys.exit(1)
        output_main_csv(main_csv, full_path)

    fused_with_tags = merge_csv_with_filetags(full_path, main_csv, cmd_args.get('dry_run'))
    if isinstance(fused_with_tags, tuple):
        lost_lines, lost_files, unmatched = fused_with_tags
        for songrecord in lost_lines:
            logger.error('Missing artist or album, cannot place: Artist: %s Album: %s Title: %s Original: %s',
                         songrecord.artist, songrecord.album, songrecord.title, songrecord.original_csv_name)
        for audio_file_path in lost_files:
            logger.error('Audio file is missing artist or album, cannot place. %s', audio_file_path)
        for unmatched_tags in unmatched:
            logger.error('Artist: %s Album: %s Title: %s could not be found in csv files.',
                         unmatched_tags.artist, unmatched_tags.artist, unmatched_tags.title)

        logger.info('Recommend removing all files (or artists/albums) '
                    'raising errors and addressing their migrations / tagging manually.')
        sys.exit(1)

    move_audio_files(
        Path(cmd_args['output_directory']),
        fused_with_tags,
        not cmd_args.get('move_files'),
        cmd_args.get('dry_run'),
    )
