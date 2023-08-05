import os, json, logging, re
from termcolor import cprint
from pathlib import Path
_FOLDER = os.path.dirname(os.path.realpath(__file__))
_CONFIGFILE = os.path.join(_FOLDER,'vyconfig.json')
_FIELDS = ['contexts','items','secrets','jobs','menu','ssh']
SEARCHED_REPO_PATHS = {}
ITEMS = {}
KEYMATCH = re.compile("^[A-Za-z_0-9]+$")


def check_folder(field,values):
  success = True
  for v in values:
    if not os.path.isdir(v):
      logging.error('The path "{v}" is not a directory. Create this directory before setting it as your "{f}" directory'.format(v=v,f=field))
      success = False
  return success

class __CONFIG:
  def __init__(self):
    # // 'BITBUCKET_SSH':'/home/nate/.ssh/bitbucketnopassphrase'
    self._data = {}
    self._secrets = {'secret':{},'ssh':{}}
    try:
      self._data = json.loads(Path(_CONFIGFILE).read_text().strip())
      self.__get_secrets_ssh()
    except:
      pass
  
  def __write(self):
    with open(_CONFIGFILE,'w') as w:
      w.write(json.dumps(self._data))

  def __get_secrets_ssh(self):
    self._secrets = {'secret':{},'ssh':{}}
    if self._data.get('secrets'):
      if type(self._data['secrets']) == str: # backward compatibility
        self._data['secrets'] = [self._data['secrets']]
      for folder in self._data['secrets']:
        for root, dirs, files in os.walk(folder):
          for sname in files:
            if KEYMATCH.search(sname):
              self._secrets['secret'][sname] = os.path.join(folder, sname)
    if self._data.get('ssh'):
      self._secrets['ssh'] = {k:v for k,v in self._data.get('ssh',{}).items() if KEYMATCH.search(k)}

  def set(self,field,value):
    if field in _FIELDS:
      if field in ['secrets','contexts']:
        if check_folder(field, value):
          self._data[field] = [str(Path(v).resolve()) for v in value]
      elif field in ['jobs']:
        if check_folder(field, [value]):
          self._data[field] = str(Path(value).resolve())
          ign = os.path.join(self._data[field],'.vyignore')
          if not os.path.exists(ign):
            with open(ign,'w'): pass
      else:
        self._data[field] = value
      self.__write()
    if field in ['secrets','ssh']:
      self.__get_secrets_ssh()

  def get(self,field):
    return self._data[field] if self._data and field in self._data else None

  def secrets_cmd(self, secret_list, ssh_list):
    cmd = []
    ok = True
    lists = {'secret':secret_list, 'ssh':ssh_list}
    for typ,lst in lists.items():
      for secret in lst:
        if typ == 'secret' and secret in self._secrets['secret']:
          cmd += ['--secret','id='+secret+',src='+self._secrets['secret'][secret]]
        elif typ == 'ssh' and secret in self._secrets['ssh']:
          cmd += ['--ssh',secret+'='+self._secrets['ssh'][secret]]
        else:
          if typ == 'secret':
            secrets_path = self.get('secrets')
            msg = '\n'
            if not secrets_path:
              msg += '  Secrets used by vytools must exist in a "secrets" folder.\n'
              msg += '  Secrets folder(s) can be added via the command line\n'
              msg += '    (e.g. "vytools --secrets path/to/folder/containing/secrets1,path/to/secrets2")\n'
            msg += '  A file named "{s}" containing the secret does not exist in the secrets folders\n'.format(s=secret)
            if secrets_path:
              msg += '    ({f}).'.format(f=','.join(secrets_path))
            logging.error(msg)
          else:
            logging.error('This ssh path for {s} has not been stored in vy, please specify path with vytools (e.g. "vytools --ssh {s}=/path/to/key")'.format(s=secret))
          ok = False
    return (ok, cmd)

  def info(self):
    cprint('VyTools Configuration & Summary:', attrs=['bold'])
    print('  Configuration saved at: '+_CONFIGFILE)
    print('  Contexts = {s}'.format(s=self.get('contexts')))
    print('  Secrets at {s}'.format(s=self.get('secrets')))
    jobpath = self.get('jobs')
    if jobpath:
      print('  Jobs at {s}'.format(s=jobpath))
    else:
      cprint('  Jobs path not specified, specify path with vytools --jobs , (e.g. "vytools --jobs path/to/folder/for/jobs" info)', attrs=['bold'])
    print('  Items found:')
    items = self.get('items')
    typs = {}
    if items:
      for i in items:
        typ = i.split(':')[0]
        if typ not in typs: typs[typ] = 0
        typs[typ] += 1
    for typ in typs:
      print('    - {n} {t} items'.format(t=typ,n=typs[typ]))

  def job_path(self):
    jp = self.get('jobs')
    if not jp:
      logging.error('No jobs path specified ("vytools info")')
      return None
    return jp

CONFIG = __CONFIG()

