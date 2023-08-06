# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
from typing import Dict
from zipfile import ZipFile
from logging import Logger

def backup_qbittorrent(config_dir: str, destzip_path: str,
                       last_backupzip_path: str=None, logger: Logger=None):

    '''
    - `config_dir` - the qbittorrent config dir, which should contains a `BT_backup` dir.
    - `destzip_path` - the dest zip file path to save the backup files.
    - `last_backupzip_path` - the last backuped zip file to compare if provided.
    '''

    def find_BT_backup():
        BT_backup_dirs = [
            os.path.join(config_dir, 'qBittorrent', 'BT_backup'), # for new version
            os.path.join(config_dir, 'data', 'qBittorrent', 'BT_backup'), # for old version
        ]
        for backup_dir in BT_backup_dirs:
            if os.path.isdir(backup_dir):
                return backup_dir
        logger.error(f'none of {BT_backup_dirs!r} is a dir.')

    BT_backup = os.path.join(config_dir, 'qBittorrent', 'BT_backup')

    BT_backup = find_BT_backup()
    if BT_backup is None:
        return

    files_to_backup: Dict[str, str] = {}

    filenames = set(os.listdir(BT_backup))
    for name in filenames:
        prefix, ext = os.path.splitext(name)
        arc_name = None

        if ext == '.torrent':
            arc_name = 'torrents/' + name
        elif ext == '.fastresume':
            if (prefix + '.torrent') not in filenames:
                # this is a magnet link file
                arc_name = 'magnets/' + name

        if arc_name:
            files_to_backup[arc_name] = os.path.join(BT_backup, name)

    # load exists backups
    if last_backupzip_path:
        with ZipFile(last_backupzip_path, 'r') as last_backup_zip:
            last_backup_torrents = set(last_backup_zip.namelist())
    else:
        last_backup_torrents = set()

    if last_backup_torrents == set(files_to_backup):
        logger.info('nothing changed after last backup.')
        return

    zipsafe = False
    try:
        with ZipFile(destzip_path, 'w') as backup_file:
            for arc_name in sorted(files_to_backup):
                try:
                    backup_file.write(files_to_backup[arc_name], arc_name)
                except:
                    logger.error('error when backuping {}'.format(arc_name), exc_info=True)
                    raise
        zipsafe = True
    finally:
        if not zipsafe and os.path.isfile(destzip_path):
            try:
                os.unlink(destzip_path)
            except:
                pass
