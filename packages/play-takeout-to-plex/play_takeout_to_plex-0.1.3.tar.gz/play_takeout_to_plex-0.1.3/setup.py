# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['play_takeout_to_plex']

package_data = \
{'': ['*']}

install_requires = \
['eyed3>=0.9.6,<0.10.0']

entry_points = \
{'console_scripts': ['play2plex = play_takeout_to_plex:main']}

setup_kwargs = {
    'name': 'play-takeout-to-plex',
    'version': '0.1.3',
    'description': 'Re-name and re-structure google play music takeout to be plex friendly.',
    'long_description': "=================================\nGoogle Play Music Takeout to Plex\n=================================\n\nA tool for restructuring Google Play Music Takeout to a plex (and human)-friendly format.\n\nThis tool comes with zero garuntees. I recommend testing on a small subset of audio files before attempting it on a full takeout library.\n\nThe first step of the tool scrapes all of the google play CSV files and turns them in to one main csv. This will be output even during dry run, and can be used on its own in this way.\n\n=================================\nUsage\n=================================\n\n``python takeout_converter.py --takeout-tracks-directory 'google_extract/Takeout/Google Play Music/Tracks/'``\n\n=================================\nOptions\n=================================\n\n.. list-table:: Options\n   :header-rows: 1\n\n   * - name\n     - type\n     - required\n     - description\n   * - -i/--takeout-tracks-directory\n     - string\n     - yes\n     - the directory containing extracted takeout files (audio files and csv files\n   * - dry-run\n     - any value\n     - no\n     - skip actually operating on files if anything is passed. Will still output the main-csv file.\n   * - move-files\n     - any value\n     - no\n     - moves files instead of copying them. Useful if you have limited space.\n   * - main-csv\n     - string\n     - no\n     - filepath to a csv that combines all play takeout files. Mostly for debugging. CSV that can be used here is output by the program.\n   * - output-directory\n     - string\n     - no\n     - Directory to which to move or copy the audio files. defaults to 'out'\n\n=================================\nOutput\n=================================\n\nThe tool scrapes the google play music CSVs and the audio files' metadata.\n\nActual metadata is prioritized, but if metadata is missing but is present in the CSV (artist, album, track name), it will be added to the audio file.\n\nFiles are then moved to directories underneath ``out``, or the supplied ``takeout-tracks-directory`` location.\n\n\n\nThe directory structure follows `Plex music directory and file naming <https://support.plex.tv/articles/200265296-adding-music-media-from-folders>`_.\n\nBased on play csvs and file metadata, they will be structured to be: ``ArtistName/AlbumName/TrackNumber - TrackName.ext``\n",
    'author': 'checkroth',
    'author_email': 'checkroth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Checkroth/play-takeout-to-plex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
