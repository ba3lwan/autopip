#!/usr/bin/python3
# -*- encoding: utf-8 -*-

##################################################
#  autopip :
#    - auto install & update pip
#    - collect required modules
#    - auto install required modules
#
#  08-03-25
#
#  ali elainous
#  ali.elainous130@gmail.com
#
#################################################

__version__ = '5'

import os
import re
import sys
import time
import datetime
import shutil
import tarfile
import zipfile

from http.client import HTTPConnection, HTTPSConnection


lib_standard = (
    '__future__',
    '__main__',
    '_thread',
    '_tkinter',
    'abc',
    'aifc',
    'argparse',
    'array',
    'ast',
    'asynchat',
    'asyncio',
    'asyncore',
    'atexit',
    'audioop',
    'base64',
    'bdb',
    'binascii',
    'bisect',
    'builtins',
    'bz2',
    'calendar',
    'cgi',
    'cgitb',
    'chunk',
    'cmath',
    'cmd',
    'code',
    'codecs',
    'codeop',
    'collections',
    'colorsys',
    'compileall',
    'concurrent',
    'configparser',
    'contextlib',
    'contextvars',
    'copy',
    'copyreg',
    'cProfile',
    'crypt',
    'csv',
    'ctypes',
    'curses',
    'dataclasses',
    'datetime',
    'dbm',
    'decimal',
    'difflib',
    'dis',
    'distutils',
    'doctest',
    'email',
    'encodings',
    'ensurepip',
    'enum',
    'errno',
    'faulthandler',
    'fcntl',
    'filecmp',
    'fileinput',
    'fnmatch',
    'fractions',
    'ftplib',
    'functools',
    'gc',
    'getopt',
    'getpass',
    'gettext',
    'glob',
    'graphlib',
    'grp',
    'gzip',
    'hashlib',
    'heapq',
    'hmac',
    'html',
    'http',
    'idlelib',
    'imaplib',
    'imghdr',
    'imp',
    'importlib',
    'inspect',
    'io',
    'ipaddress',
    'itertools',
    'json',
    'keyword',
    'linecache',
    'locale',
    'logging',
    'lzma',
    'mailbox',
    'mailcap',
    'marshal',
    'math',
    'mimetypes',
    'mmap',
    'modulefinder',
    'msilib',
    'msvcrt',
    'multiprocessing',
    'netrc',
    'nis',
    'nntplib',
    'numbers',
    'operator',
    'optparse',
    'os',
    'ossaudiodev',
    'pathlib',
    'pdb',
    'pickle',
    'pickletools',
    'pipes',
    'pkgutil',
    'platform',
    'plistlib',
    'poplib',
    'posix',
    'pprint',
    'profile',
    'pstats',
    'pty',
    'pwd',
    'py_compile',
    'pyclbr',
    'pydoc',
    'queue',
    'quopri',
    'random',
    're',
    'readline',
    'reprlib',
    'resource',
    'rlcompleter',
    'runpy',
    'sched',
    'secrets',
    'select',
    'selectors',
    'shelve',
    'shlex',
    'shutil',
    'signal',
    'site',
    'sitecustomize',
    'smtpd',
    'smtplib',
    'sndhdr',
    'socket',
    'socketserver',
    'spwd',
    'sqlite3',
    'ssl',
    'stat',
    'statistics',
    'string',
    'stringprep',
    'struct',
    'subprocess',
    'sunau',
    'symtable',
    'sys',
    'sysconfig',
    'syslog',
    'tabnanny',
    'tarfile',
    'telnetlib',
    'tempfile',
    'termios',
    'test',
    'textwrap',
    'threading',
    'time',
    'timeit',
    'tkinter',
    'token',
    'tokenize',
    'tomllib',
    'trace',
    'traceback',
    'tracemalloc',
    'tty',
    'turtle',
    'turtledemo',
    'types',
    'typing',
    'unicodedata',
    'unittest',
    'urllib',
    'usercustomize',
    'uu',
    'uuid',
    'venv',
    'warnings',
    'wave',
    'weakref',
    'webbrowser',
    'winreg',
    'winsound',
    'wsgiref',
    'xdrlib',
    'xml',
    'xmlrpc',
    'zipapp',
    'zipfile',
    'zipimport',
    'zlib',
    'zoneinfo')


# 09.10.24 | 15.02.25
class AutoPip:
    def __init__(self, *modules):
        self.requires = {}
        self.modules  = list(modules)
        
        modules and type(modules) in (tuple, list) and self.__call__(*modules)

    def __call__(self, *modules):
        '''
        # import_lib , install_lib, version
        # ---------------------------------
        "pip"             => "pip" , "pip" , "last"

        "requests==3.14"  => "requests" , "requests" , "3.14"

        "tk,tkinter==4.2" => "tk" , "tkinter" , "4.2"
        
        "telegram,python-telegram-bot" => "telegram" , "python-telegram-bot" , "last"
        '''

        self.modules = list(modules)

        if  not self.modules:
            print('Nothing to do.')
            return

        if  sys.argv[0].endswith('.exe'):
            print("\nYou don't need autopip because you are using executable program.")
            time.sleep(2)
            return

        major = sys.version_info.major
        minor = sys.version_info.minor

        if  not (major >= 3 and minor >= 7):
            print(f'\nWarning: This version of python:{major}.{minor} is not suported.')
            time.sleep(3)

        self.version_info = f'{major}.{minor}'

        pip_install, pip_uninstall = self.import_pip()
        
        pip_install or sys.exit(f'Error in pip_install "{pip_install}"')
        
        while self.modules:
            modules_copy = self.modules.copy()

            for module in modules_copy:
                if  module not in self.modules:
                    continue
                
                print(f'\nChecking "{module}"')

                Import, Install, Version = self.get_name_version(module)
                _version, module_path = self.import_module(Import, Install)
                
                if  _version == -1: # other module required but not installed
                    lst = self.requires.get(module_path, [])
                    if  module not in lst:
                        self.requires[module_path] = lst + [module]
                    continue

                if  Import in lib_standard:
                    print(' Done 0')
                    
                elif _version and not module_path:
                    print(' Done 1')
                    
                elif _version and not Version:
                    print(' Done 2')
                    
                elif _version == Version:
                    print(' Done 3')
                    
                elif not self.get_module_info(Install, Version):
                    print(f' Warning: module "{Install}" is not found in PYPI.')

                else:
                    Version = f'=={Version}' if Version else ''

                    print(f'Installing {Install}{Version}')
                    pip_uninstall(['-y', Install])
                    pip_install([f'{Install}{Version}'])

                self.modules.remove(module)
                
                if  module in self.requires:
                    for require in self.requires.get(module, []):
                        if  require in self.modules:
                            self.modules.remove(require)
                    del self.requires[module]

            if  self.modules == modules_copy:
                print(f'Cannot install modules: {modules_copy}')
                break

    def start(self, *modules):
        self.__call__(*modules)

    def get_name_version(self, module):
        'return : import_name, install_name, version'

        import_name, *install_version = module.replace(' ', '').split(',')

        install_name = (install_version or [import_name])[0]

        if  '==' in module:
            import_name , *version1 = import_name.split('==')
            install_name, *version2 = install_name.split('==')
            version = (version1 or version2 or [''])[0]
        else:
            version = ''

        return import_name, install_name, version

    def import_module(self, import_name, install_name=''):
        '''
        return version, path
        
        version :   False   : Not found
                    True    : Found
                    Version : Found + Version
        
        path    :   ''      : Not found
                    True    : Found
                    path    : Found + dsit-info
        '''
        
        version     = False
        module_path = ''
        
        install_name = (install_name or import_name).replace('-', '_')

        try:
            exec(f'import {import_name}')
        except Exception as err:
            if  "from '" in str(err):
                x, module = str(err).split("from '", 1)
                module, x = module.split("'", 1)
            else:
                x, module = str(err).split("'", 1)
                module = module[:-1]

            if  module == import_name:
                return version, module_path

            if  module not in self.modules:
                self.modules = [module] + self.modules

            return -1, module
        
        for verattr in ('__version__', '_version', 'version', 'Version', 'VERSION', 'ver', '_ver'):
            try:
                version = re.findall(r'\d+\.\d+\.*\d*', str(eval(f'{import_name}.{verattr}')))[0]
                break
            except:
                pass
        else:
            version = True

        try:
            assert import_name != 'pip'
            module_path = eval(f'{import_name}.__path__')
            
            assert module_path

            if  type(module_path) == list:
                module_path = module_path[0]

            if  module_path.endswith('.py'):
                module_path = True

            else:
                base_path, module = module_path.rsplit(os.sep, 1)
                for file in os.listdir(base_path):
                    if  file.startswith(f'{install_name}-') and file.endswith('-info'):
                        break
                else:
                    module_path = True
        except Exception as err:
            pass

        try:
            exec(f'del {import_name}')
        except:
            pass

        return version, module_path

    def compare_version(self, ver1, ver2):
        '''
        None  '==' : ver1 == ver2
        False '<'  : ver1 <  ver2
        True  '>'  : ver1 >  ver2
        '''
        def ver_to_int(ver):
            ver = str(ver or '0').lower() + '.0.0.0'
            
            for i, j in enumerate('abcdefghijklmnopqrstuvwxyz'):
                ver = ver.replace(j, f'.{i}.')
            
            x, y, z, w = map(int, ver.split('.')[:4])

            return 1000*x + 100*y + 10*z + w

        assert ver1 not in (None, True, False)
        assert ver2 not in (None, True, False)

        test = ver_to_int(ver1) - ver_to_int(ver2)

        if  not test:
            return
        return test > 0
    
    def get_module_info(self, install_name, target_version=None, sign='==', target_ext='tar.gz'):
        install_name1 = install_name.replace('-', '_')
        target_ext    = '.' + target_ext.lower().lstrip('.')
        base_url      = 'https://files.pythonhosted.org/packages'
        
        if  target_version:
            assert sign in ('>', '<', '>=', '<=', '!=', '==')

        try:
            req = Request(f'https://pypi.org/simple/{install_name}', timeout=5)
            req.close()
            assert req.ok
            urls = re.findall(fr'href="{base_url}/(.+)/(.+?)#(.+?=.+?)"', req.text)
            assert urls
        except AssertionError:
            return
        except Exception as err:
            return print(f'err: {err}')

        for url, name_version_ext, hash in urls[::-1]:
            algo, hash = hash.split('=')

            name = install_name if name_version_ext.startswith(install_name) else install_name1
            version_ext = name_version_ext[len(name)+1:]

            ext0 = ''
            if  version_ext.endswith('.tar.gz'):
                ext = '.tar.gz'

            elif version_ext.endswith(('.egg', '.whl')):
                if  '-py3' not in version_ext:
                    continue

                if  version_ext.endswith('.whl'):
                    ext = '.whl'
                else:
                    ext = '.egg'
                    ver = re.findall(r'-py(3.\d+)', version_ext)
                    
                    if  not ver or self.compare_version(ver[0], self.version_info) == False:
                        continue

                index = version_ext.find('-py')
                ext0  = version_ext[index:-4]

            elif version_ext.endswith('.zip'):
                ext = '.zip'

            else:
                sys.exit(f'\n\tPlease fix this !! (version_ext: {version_ext})')

            version = version_ext[:-len(ext0+ext)]

            if  target_ext and target_ext != ext:
                continue

            info = dct2obj({
                'url'     : f'{base_url}/{url}/{name}-{version}{ext0+ext}',
                'hash'    : hash,
                'algo'    : algo,
                'version' : version,
                'ext'     : ext,
                'name'    : name,
                })

            if  not target_version:
                del req, urls
                return info

            r = self.compare_version(version, target_version)

            if  r and sign in ('>', '>=', '!='):
                del req, urls
                return info

            elif r == False and sign in ('<', '<=', '!='):
                del req, urls
                return info

            elif r == None and sign in ('==', '>=', '<='):
                del req, urls
                return info
        
        del req, urls

    def import_pip(self):
        '''
        return: pip_install, pip_uninstall
        pip_install(['-U', 'requests'])
        pip_uninstall(['-y', 'requests'])
        '''

        update = False
        pack   = '<bound method Command.main of <pip._internal.commands.install.InstallCommand'
        
        try:
            version, pip_path = self.import_module('pip')
            print(f'\nChecking pip:{version} | path: {pip_path}')
            assert str(self.pip_install).startswith(pack)
            print(' Imported.')
            return self.pip_install, self.pip_uninstall
        except Exception as err:
            pass

        try:
            assert version in (False, True, None)
            info = self.get_module_info('pip')
            
            print(f'Downloading pip={info.version}')
            req = Request(info.url)
            
            src = req.save('pip')
            dst = req.extract(src)
            
            os.path.isdir('pip') and shutil.rmtree('pip')
            os.path.isfile('pip') and os.remove('pip')
            
            shutil.copytree(f'{dst}{os.sep}src{os.sep}pip', 'pip')
            os.remove(src)
            shutil.rmtree(dst)
            update = True
        except AssertionError:
            pass
        except Exception as err:
            print(f' Error when download pip:', err)
        
        if  update or os.path.isdir('pip'):
            print('Updating pip...')
            
            filename = '__update__pip__.py'
            C = "from pip._internal.commands import create_command as cc\ncc('install').main(['-U', 'pip'])"

            with open(filename, 'w', encoding='utf-8') as file:
                file.write(C)

            cmd = f'{sys.executable} {filename}'

            os.system(cmd)
            os.path.isdir('pip') and shutil.rmtree('pip')
            os.remove(filename)

        try:
            from pip._internal.commands import create_command
            self.pip_install =  create_command('install').main
            self.pip_uninstall = create_command('uninstall').main
        except Exception as err:
            print(' Error when import pip :', err)
            return None, None

        print(' Done')
        return self.pip_install, self.pip_uninstall

    def collect_modules_info(self, path='.', as_str=True, freeze=None, all_pack=None):
        def parse_text_info(file_path):
            with open(file_path, encoding='utf-8') as fo:
                text = fo.read()
                        
            name      = re.findall(f'\nName: (.+)\n', text)[0]
            version   = re.findall(f'\nVersion: (.+)\n', text)[0]
            top_level = name.replace('-', '_')
            del text
            return name, version, [top_level]
        
        modules = set()

        if  os.path.isfile(path) and path.endswith('.py'):
            lst = self.parse_module(path)
            for item in lst.copy():
                if  os.path.isdir(item) or os.path.isfile(f'{item}.py'):
                    lst.remove(item)
            modules.update(lst)
        
        else:
            for pwd, dirs, files in os.walk(path or '.'):
                for file in files:
                    if  not file.endswith('.py'):
                        continue
                    
                    _path = f'{pwd}{os.sep}{file}'
                    lst = self.parse_module(_path)
                    
                    for item in lst.copy():
                        _path = f'{pwd}{os.sep}{item}'
                        if  os.path.isdir(_path) or os.path.isfile(f'{_path}.py'):
                            lst.remove(item)
                    modules.update(lst)
        
        if  freeze:
            return modules

        if  not modules and not all_pack:
            print()
            return modules

        modules_info = {}
        
        for path in sys.path:    
            if  not modules and not all_pack:
                break

            if  not os.path.isdir(path):
                continue
            
            for file in os.listdir(path):
                target_path = f'{path}{os.sep}{file}'

                if  not file.endswith(('.dist-info', '.egg-info')):
                    continue

                top_file = target_path + os.sep + 'top_level.txt'

                if  os.path.isfile(target_path):
                    target_file = target_path

                elif os.path.isdir(target_path):
                    for metadata in ('METADATA', 'PKG-INFO'):
                        target_file = target_path + os.sep + metadata

                        if  os.path.isfile(target_file):
                            break
                    else:
                        continue

                name, version, top_level_lst = parse_text_info(target_file)

                if  os.path.isfile(top_file):
                    with open(top_file, encoding='utf-8') as fo:
                        top_level_lst = fo.read().split()

                    for top in top_level_lst.copy():
                        if  not top or '-' in top:
                            top_level_lst.remove(top)

                if  modules:
                    for top_level in top_level_lst:
                        if  top_level in modules:
                            modules_info[name] = (top_level_lst, version)
                            modules.remove(top_level)
                
                elif all_pack:
                    modules_info[name] = (top_level_lst, version)

                else:
                    break

        for module in modules.copy():
            if  module in lib_standard:
                modules.remove(module)
                continue

            version, path = self.import_module(module)
            if  version == -1:
                modules.add(path)

            else:
                modules_info[module] = ([module], version)
            
            modules.remove(module)

        if  as_str:
            rslt = '    autopip(\n'
            for lib_install, info in modules_info.items():
                libs, version = info
                for lib_import in libs:
                    version = '' if version in (True, False, None) else f'=={version}'
                    rslt += f"\t'{lib_import},{lib_install}{version}',\n"
            
            for module in modules:
                rslt += f"\t'{module}',\n"
            
            print(rslt + '        )')
            return rslt

        return modules_info, modules

    def parse_module(self, path):
        with open(path, encoding='utf-8') as fo:
            text =  '\n' + fo.read()
        
        modules = set()

        lst = re.findall(r'exec\((.+?)\)', text)
        for item in lst:
            item = item[1:-1]
            exp1 = re.findall(r'from ([a-zA-Z\d_]+?) import ', item)
            exp2 = re.findall(r'^import ([a-zA-Z\d_, ]+)', item)
            modules.update(exp1 + exp2)

        text = re.sub(pattern=r'#.*?\n', repl=' E0\n', string=text)
        text = re.sub(pattern=r'\\\n', repl='E1\n', string=text)        
        text = re.sub(pattern=r"'''[\w\W]*?'''", repl='E2\n', string=text)
        text = re.sub(pattern=r'"""[\w\W]*?"""', repl='E3\n', string=text)
        text = re.sub(pattern=r'\\"', repl='E4\n', string=text)
        text = re.sub(pattern=r"\\'", repl='E5\n', string=text)
        text = re.sub(pattern=r'"[\w\W]*?"', repl='E6\n', string=text)
        text = re.sub(pattern=r"'[\w\W]*?'", repl='E7\n', string=text)
        
        text = text.replace(';', '\n')
        text = text.replace('\n', '\n\n')
        
        modules_exp = re.findall(r'from ([a-zA-Z\d_]+?) import ', text)
        modules_exp += re.findall(r'\n *import ([a-zA-Z\d_, ]+?)\n', text)
        
        for module_exp in modules_exp:
            for module in module_exp.split(','):
                module = module.strip()
                if  ' as ' in module:
                    module = module.split(' as ')[0].strip()
                    
                if  module.startswith(('_', '.')):
                    continue
                
                if  '.' in module:
                    module = module.split('.')[0]

                modules.add(module.split(' ')[0].strip())
        return modules


class Request:
    def __new__(self, url, method='GET', **kwargs):
        methods = ('GET', 'POST', 'DELETE', 'PUT', 'OPTIONS', 'HEAD', 'PATCH')
        method  = method.upper()
        
        if  method not in methods:
            raise Exception(f'method "{method}" must be in {methods}')

        self   = super().__new__(self)

        headers = self.parse_headers(kwargs.get('headers', {}))
        kwargs.update({'headers' : headers})

        while 1:
            url, proto, host, port, url_path = self.parse_url(url)
            _path, filename = url_path.rsplit('/', 1)
            filename        = filename or 'index.html'
            
            res = self._request(method, proto, host, port, url_path, **kwargs)
            
            if  not res:
                return

            if  res.code in (301, 302): # Moved & Found
                res.close()
                location = res.headers.get('Location')
                if  location.startswith('http'):
                    url = location

                else:
                    sep = '' if location.startswith('/') else '/'
                    url = f'{proto}://{host}:{port}{sep}{location}'
                time.sleep(0.2)
                continue        
            break
        
        res.ok        = res.code == 200
        res.url       = url
        res.proto     = proto
        res.host      = host
        res.port      = port
        res.url_path  = url_path
        res.filename  = filename
        res.content   = self.content = res.read()
        res.text      = self.text    = ''
        res.extract   = self.extract
        res.save      = self.save
        res.date_time = self.date_time
        
        for mode in ('latin', 'utf8'):
            try:
                res.text = self.text = res.content.decode(mode)
                break
            except:
                pass
        else:
            print(f'Warning: response does not support utf8 & latin decodes.')
        return res
    
    def _request(self, method, proto, host, port, url_path, timeout=None, **kwargs):
        headers    = kwargs.get('headers', {})

        Connection = HTTPConnection if proto == 'http' else HTTPSConnection
        
        while 1:
            try:
                conn = Connection(host, port, timeout=timeout)
                conn.request(method, url_path, headers=headers)
                return conn.getresponse()
            except KeyboardInterrupt:
                break
            except Exception as err:
                if  'timed out' in str(err):
                    print(f'Trying to connect "{proto}://{host}:{port}" ...')
                else:
                    print(err)
                time.sleep(1)

    def parse_url(self, url):
        proto, port, from_id = 'http', 80, 7

        if  url.startswith('https://'):
            proto   += 's'
            port     = 443
            from_id += 1    

        elif not url.startswith('http://'):
            raise Exception(f'url: "{url}" incorrect.')

        url, *path = url[from_id:].split('/', 1)
        path       = '/' + (path or [''])[0]
        host, port = url.split(':') if ':' in url else (url, port)
        proto      = 'https' if port == '443' else proto
        return f'{proto}://{host}:{port}{path}', proto, host, int(port), path

    def parse_headers(self, headers):
        headers['Accept-Encoding'] = headers.get('Accept-Encoding', 'utf-8')
        headers['Accept']     = headers.get('Accept', 'text/plain,text/html')
        headers['Connection'] = headers.get('Connection', 'keep-alive')
        headers['User-Agent'] = headers.get('User-Agent', 'python-irequest/1.0')
        return headers

    def date_time(self, ext='', exist=None):
        while 1:
            dt  = str(datetime.datetime.now()).split('.')[0]
            dt  = dt.replace(':', '_').replace('-', '_').replace(' ', '_')
            dt += ext
            if  exist and os.path.exists(dt):
                continue
            return dt

    def extract(self, src, dst=None):
        def rm(_path):
            os.path.isdir(_path) and shutil.rmtree(_path)
            os.path.isfile(_path) and os.remove(_path)

        def mv(_src, _dst):
            _src != _dst and rm(_dst)
            shutil.move(_src, _dst)
        
        src = os.path.abspath(src)
        assert os.path.exists(src)

        ftype = fext(src)

        if  ftype == '.zip':
            decompress = zipfile.ZipFile

        elif ftype == '.tar.gz':
            decompress = tarfile.open

        else:
            return print('\nWarning: support only *.zip & *.tar.gz')
            
        
        while 1:
            src1 = tmp = os.path.abspath(str(time.time()))
            if  not os.path.exists(tmp):
                break

        if  dst:
            dst = os.path.abspath(dst)

        data = decompress(src)
        data.extractall(tmp)
        data.close()

        dirs = os.listdir(tmp)
        
        if  len(dirs) == 1:
            src2 = os.path.join(tmp, dirs[0])
            if  os.path.isdir(src2):
                src1 = src2
                dst  = dst or os.path.abspath(dirs[0])

        dst = dst or src.split('.', 1)[0]

        mv(src1, dst)
        rm(tmp)
        mode = int('775' if os.path.isdir(dst) else '664', 8)
        os.chmod(dst, mode)
        return dst

    def save(self, filename, content=''):
        content = content or self.content
        if  not content:
            return
        
        isbin     = type(content[0]) == int
        mode      = 'wb' if isbin else 'w'
        x, *ftype = filename.rsplit('.', 2)
        ftype     = ('.' + '.'.join(ftype)) if ftype else fext(data=content[:10])
        filename  = f'{x}{ftype}'
        
        with open(filename, mode) as file:
            file.write(content)
        return os.path.abspath(filename)


class dct2obj:
    def __new__(self, dct):
        self = super().__new__(self)
        for i, j in dct.items():
            i = str(i)
            if  i[0].isnumeric():
                i = f'_{i}'
            setattr(self, i, j)
        self.as_dct = dct
        return self


def fext(fpath=None, data=None):
    '''
    0x1f8b08          .tar.gz
    0x504b03  PK      .zip
    0x526172  Rar     .rar
    '''
    if  fpath:
        try:
            fo = open(fpath, encoding='latin')
            data = fo.read(10)
            fo.close()
            assert data
        except Exception as err:
            raise
    
    elif not data:
        raise Exception('err: data is empty.')

    elif type(data) != str:
        for mod in ('latin', 'utf-8'):
            try:
                data = data.decode(mod)
                break
            except:
                pass
        else:
            raise Exception('err: cannot decode data')
    
    data = data.lstrip('\r\n ')

    if  data.startswith('\x1f\x8b\x08'):
        ftype = '.tar.gz'

    elif data.startswith('PK\x03'):
        ftype = '.zip'

    elif data.startswith('Rar'):
        ftype = '.rar'

    elif data.startswith(('<html', '<!DOCTYP')):
        ftype = '.html'

    elif data.startswith('<?xml'):
        ftype = '.xml'

    elif data.startswith('<?php'):
        ftype = '.php'

    else:
        ftype = '.txt'
        print(f'{data[:6].encode("latin")} signature not found.')
    return ftype


def find_arg(keys, val=None, sep='', typ=str, default=None):
    if  not hasattr(sys, 'argv_copy'):
        sys.argv_copy = sys.argv.copy()

    if  not keys:
        return sys.argv_copy[1:]

    for i, arg in enumerate(sys.argv_copy[1:], 1):
        if  type(keys) == str:
            keys = [keys]

        assert type(keys) in (tuple, list)
        assert type(sep) == str

        for key in keys:
            if  key == arg:
                try:
                    assert val
                    v = sys.argv_copy.pop(i+1)
                    sys.argv_copy.remove(arg)
                    return typ(v)
                except AssertionError:
                    sys.argv_copy.remove(arg)
                    return default if default else True
                except:
                    raise Exception(f'error in param "{arg}"')

            if  arg.startswith(key):
                if  sep:
                    pass

                elif '=' in arg:
                    sep = '='

                elif ':' in arg:
                    sep = ':'
                
                try:
                    k, v = arg.split(sep)
                    if  key == k:
                        sys.argv_copy.remove(arg)
                        return typ(v)
                except:
                    pass

    return default


def main():
    autopip = AutoPip()
    
    if  __name__ == '__main__':
        find_arg(['-h', '--help', 'help']) and sys.exit(f'''
        \r autopip [options] pathname
        \r
        \roptions:
        \r      -c --collect collect    # collect required modules
        \r      -a --all                # collect all packages installed
        \r      -h --help               # show this help
        \r
        \rUsage:
        \r      autopip collect         # pathname = '.'
        \r      autopip collect all     # all packages names
        \r      autopip                 # install & update pip
        \r                              # install modules
        
        ''')

        all_pack = find_arg(['-a', '--all', 'all'])

        if  find_arg(['-c', '--collect', 'collect']):
            module_path = (find_arg('') + ['.'])[0]

            print(f'Collect {"all" if all_pack else ""} "{module_path}" modules\n')
        
            if  not os.path.exists(module_path):
                sys.exit(f'err: path "{from_path}" is not exist.')

            lst = autopip.collect_modules_info(module_path, all_pack=all_pack)
        
        return

    autopip(
      'requests',
      'selenium,selenium',
      'telegram,python-telegram-bot',
      'kivy==1.0.0',
      'psutil,psutil==5.9.0',
    )
    

__name__ == '__main__' and main()
