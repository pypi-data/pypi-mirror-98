import os
import rclone
import sqlite3
import shutil
import subprocess
import json

class ZoteroSync:
  """
  A class used to sync zotero storage with a rclone remote
  """
  def __init__(self, zotero_path, zoterosync_path):
    """
    Parameters
    ----------
    zotero_path: str
      Path to zotero
    zoterosync_path: str
      Path to zoterosync
    """
    self.zoterosync_path = zoterosync_path
    self.config_file = self.zoterosync_path+'/zoterosync.conf.json'
    self.zotero_path = zotero_path
    self.rclone_config = None
    self.config = self.load_config()

  def rclone_configuration(self):
    result = None
    with subprocess.Popen(['rclone', 'config', 'file'],
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE) as proc:
        (out,err) = proc.communicate()
        result = out.split()[-1].decode('UTF-8')
    return result

  def load_config(self):
    if shutil.which('rclone') is None:
        print('Error: could not find rclone, please install it')
        return False
    else:
        self.rclone_config = self.rclone_configuration()
    
    if os.path.isfile(self.config_file) is False:
        print('Config file not found, creating one with default values: ')

        os.makedirs(self.zoterosync_path, exist_ok=True)
        data = {}
        data['rclone_cfg_path'] = self.rclone_config
        data['zoterosync_dirs'] = self.zoterosync_path+"/sync_dirs"
        data['zoterosync_path'] = self.zoterosync_path
        data['zotero_path'] = self.zotero_path
        data['default_remote_path'] = "zotero-storage"
        data['app_name'] = "zoterosync"

        with open(self.config_file, 'x') as f:
          json.dump(data,f, indent=1)
          f.close()
        print('configuration file created: '+self.config_file)
    with open(self.config_file) as json_file:
      return json.load(json_file)
  
  def save_config(self):
    with open(self.config_file, 'w') as file:
      json.dump(self.config, file)
      file.close()

  def mkdir(self, remote, remote_path):
    rrp = remote+':'+remote_path
    print('creating remote path '+rrp)    
    with open(self.config['rclone_cfg_path']) as f:
        cfg = f.read()
        result = rclone.with_config(cfg).run_cmd(command='mkdir',
                                                  extra_args=[rrp])
    if result['code'] == 0:
        return True
    else:
        return False

  def setremote(self, group_name, remote):
    print('configuring "'+remote+'" as remote of "'+group_name+'"')
    if group_name not in self.config['groups']:
      self.config['groups'][group_name] = {}
    self.config['groups'][group_name]['remote'] = remote
    self.save_config()
    self.mkdir(remote, self.config['default_remote_path'])
    return True

  def remote_dir(self, group_name):
    return self.config['groups'][group_name]['remote']+':'+self.config['default_remote_path']

  def local_storage(self):
    return self.config['zotero_path']+'/storage'

  def list_remotes(self):
      remotes = None
      with open(self.config['rclone_cfg_path']) as f:
          cfg = f.read()
          result = rclone.with_config(cfg).run_cmd('listremotes')
          remotes = result['out'].decode('UTF-8').replace(':','')
      return remotes

  def get_files_from_sqlite(self, group_name):
      filenames=[]
      conn = sqlite3.connect('file:'+self.config['zotero_path']+'/zotero.sqlite?mode=ro', uri=True)
      c = conn.cursor()
      sql="""
          select l.lastSync, i.key, i.itemID, ia.path
          from groups as g, libraries as l, items as i, itemAttachments as ia
          where
              g.libraryID = l.libraryID
              AND i.itemID = ia.itemID
              AND l.libraryID = i.libraryID
              AND g.name='{group_name}'
      """
      sqlf=sql.format(group_name=group_name)
      rows = c.execute(sqlf)
      for row in rows:
          hash_dir=row[1]
          if row[3] is not None:
              filename=row[3].replace('storage:','')
              file=self.config['zotero_path']+'/storage/'+hash_dir+'/'+filename 
              filenames.append(file)
      return filenames

  def list_groups_from_sqlite(self):
      groups=[]
      conn = sqlite3.connect('file:'+self.config['zotero_path']+'/zotero.sqlite?mode=ro', uri=True)
      c = conn.cursor()
      sql="""
          select name
          from groups
      """
      rows = c.execute(sql)
      for row in rows:
          groups.append(row[0])
      return groups

  def list_groups_with_remote(self):
    groups = dict()
    for group in self.config['groups'].keys():
      groups[group] = self.config['groups'][group]['remote']
    return groups

  # create links to files to be synced
  def link_files(self, group_name):
      filenames = self.get_files_from_sqlite(group_name)
      sync_dir = self.config['zoterosync_dirs']+'/'+group_name.replace(' ','_')
      for file in filenames:
          hash_dir = file.split('/')[-2]
          fname = file.split('/')[-1]
          dest_dir = sync_dir+'/'+hash_dir
          dest_link = dest_dir+'/'+fname
          try:
              if os.path.isfile(file):
                  os.makedirs(dest_dir, exist_ok=True)
                  if not os.path.isfile(dest_link):
                      # links save disk space
                      # hard links works on same device
                      os.link(file,dest_link)
                      # symbolic links are not working
                      # os.symlink(file,dest_link)
              else:
                  print('file not exists: '+file)
          except Exception as e:
              print(e)
              return False
      return sync_dir

  def copy_files(self, source, dest):
      result = None
      with open(self.config['rclone_cfg_path']) as f:
          cfg = f.read()
          result = rclone.with_config(cfg).copy(source,dest,flags=['-v'])
      return result