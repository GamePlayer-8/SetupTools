"""
##################################
#  Copyright C 2022 GamePlayer   #
#    AERO Kianit License 1.0     #
##################################
"""

import os
import sys
import datetime

TGT_VERSION = 'DEFAULT'
TGT_DIR = './repo_access/null'
OS_NAME_TYPE = 'Arch'
REPO_INIT = 'GamePlayer-8/github-repo-configure'
GITHUB_TOKEN = '0'
USER_EMAIL = 'gameplayer2019pl@tutamail.com'
PROJECT_NAME = 'SetupTools'

print('\nMade with tea for Github by GamePlayer (@GamePlayer-8).\n')

LOGGING = ''

if '--noclean' not in sys.argv:
    if os.path.exists('./curl_output.txt'):
        os.remove('./curl_output.txt')

    if os.path.exists('./repo_access'):
        os.system('rm -rf ./repo_access')

if '--clean' in sys.argv:
    print('Workspace prepared.')
    sys.exit()

if '--help' in sys.argv or len(sys.argv) == 1:
    print('Missing args.')
    print('\nAvailable args:')
    print('\t--prepare')
    print('\t--os <Arch/other>')
    print('\t--repo user/repo')
    print('\t--token <github token>')
    print('\t--clean')
    print('\t--noclean')
    print('\t--help')
    print('\t--c')
    print('\t--r <asset path>')
    print('\t--b <branch name> <branch dir>')
    print('\t--godot')
    print('\t--godot-server <version>')
    print('\t--godot-headless <version>')
    print('\t--godot-setup <version>')
    print('\t--godot-version')
    print('\t--godot-plugin')
    print('\t--email <email>')
    print('\t--update-dir')
    print('\t--updatec-dir <source>')
    print('\t--auto-version')
    print('\n')
    sys.exit()

if '--token' not in sys.argv:
    print('Missing token.')
    sys.exit()

try:
    GITHUB_TOKEN = sys.argv[sys.argv.index('--token') + 1]
except Exception:
    print('Missing token.')
    sys.exit()

if '--repo' not in sys.argv:
    print('Missing repo.')
    sys.exit()

try:
    REPO_INIT = sys.argv[sys.argv.index('--repo') + 1]
except Exception:
    print('Missing repo.')
    sys.exit()

if len(REPO_INIT.split('/')) != 2:
    print('Repository config is not correct.')
    sys.exit()

if '--os' in sys.argv:
    try:
        OS_NAME_TYPE = sys.argv[sys.argv.index('--os') + 1]
    except Exception:
        print('Invisible OS.')
        sys.exit()

def system_run(command=''):
    """ Execute Shell commands faster """
    global LOGGING

    if GITHUB_TOKEN not in command:
        LOGGING += '\n' + command
    os.system(command)


def get_version(tgt_directory=''):
    """ Get package version """
    version_delta = TGT_VERSION
    if os.path.exists(tgt_directory + '/version'):
        with open(tgt_directory + '/version', newline='', encoding='UTF-8') as version_file_data:
            try:
                version_delta = version_file_data.read().splitlines()[0]
            except Exception:
                print('Failed to version data from ' +
                      tgt_directory + '/version.')

    return version_delta


def update_container(os_type='Arch'):
    """ Update Runtime Container """
    if os_type == 'Arch':
        system_run('  pacman -Sy --noconfirm wget curl file')
        return

    system_run('''  apt update &&
        apt install --yes wget curl file''')

print('\tCOMMANDS LOG:\n')

if OS_NAME_TYPE != 'null':
    update_container(OS_NAME_TYPE)

system_run('mkdir -v ./repo_access')

system_run('cd ./repo_access && git clone --recursive https://github.com/' + REPO_INIT)

for _dir in os.listdir('./repo_access'):
    if os.path.isdir('./repo_access/' + _dir):
        TGT_DIR = './repo_access/' + _dir
        PROJECT_NAME = _dir
        break

TGT_VERSION = get_version(TGT_DIR)
BUILD_ARGS = sys.argv

if os.path.exists(TGT_DIR + '/SetupTools'):
    with open(TGT_DIR + '/SetupTools', newline='', encoding='UTF-8') as setup_config:
        setup_config_data = setup_config.read().splitlines()
        for line in setup_config_data:
            BUILD_ARGS += line.split(' ')

if '--email' in BUILD_ARGS:
    try:
        USER_EMAIL = BUILD_ARGS[BUILD_ARGS.index('--email') + 1]
    except Exception:
        print('Invisible mail.')
        sys.exit()

system_run('git config --global user.name "' + REPO_INIT.split('/')[0] + '"')

system_run('git config --global user.email "' + USER_EMAIL + '"')

def publish_release(target_version='', target_branch='', release_name='', assets_path=''):
    """ Publish release to Github """
    create_release = [
        'curl -s ',
        '-H "Authorization: token ',
        GITHUB_TOKEN,
        '" -d \'{"tag_name": "',
        target_version,
        '","generate_release_notes":false,"branch":"',
        target_branch,
        '","name":"',
        release_name,
        '","body":"# ',
        release_name + '\\n[Github Page](',
        'https://github.com/' + REPO_INIT + ').',
        '\\n[Webpage](https://' + REPO_INIT.split('/')[0],
        '.github.io/' + REPO_INIT.split('/')[1] + '/).',
        '"}\'',
        ' "https://api.github.com/repos/',
        REPO_INIT,
        '/releases"',
    ]

    system_run(''.join(create_release) + ' >> curl_output.txt')

    if assets_path == 'null':
        return

    url = ''

    with open('./curl_output.txt', newline='', encoding='UTF-8') as curl_file:
        url = curl_file.read().splitlines()
        for _line in url:
            if 'upload_url' in _line:
                url = _line
                break

        system_run('cat curl_output.txt')

        url = url.split('"')[len(url.split('"')) - 2]
        url = url.split('{')[0] + '?name='
    if os.path.isdir(TGT_DIR + '/' + assets_path):
        for _file in os.listdir(TGT_DIR + '/' + assets_path):
            if not os.path.isdir(TGT_DIR + '/' + assets_path + '/' + _file):
                upload_artifact = [
                    'cd ',
                    TGT_DIR + '/' + assets_path,
                    ' && ',
                    'curl -H "Authorization: token ',
                    GITHUB_TOKEN,
                    '" -H "Accept: application/vnd.github.manifold-preview"',
                    ' -H "Content-Type: $(file -b --mime-type ',
                    _file + ')',
                    '" --data-binary @',
                    _file,
                    ' "',
                    url,
                    _file,
                    '"'
                ]

                system_run(''.join(upload_artifact))
    else:
        upload_artifact = [
            'curl -H "Authorization: token ',
            GITHUB_TOKEN,
            '" -H "Accept: application/vnd.github.manifold-preview"',
            ' -H "Content-Type: $(file -b --mime-type ',
            TGT_DIR + '/',
            assets_path + ')',
            '" --data-binary @',
            TGT_DIR + '/',
            assets_path,
            ' "',
            url,
            assets_path.split('/')[len(assets_path.split('/')) - 1],
            '"'
        ]

        system_run(''.join(upload_artifact))

def deconstruct_big_files(target_dir = ''):
    """ Deconstruct files bigger than 99 MB """
    for _obj in os.listdir(target_dir):
        if os.path.isdir(target_dir + '/' + _obj):
            deconstruct_big_files(target_dir + '/' + _obj)
        else:
            if os.path.getsize(target_dir + '/' + _obj) > 103809024:
                system_run('cd ' + target_dir +
                    ' && mkdir -v ' + _obj + '_tgt' +
                    ' && mv ' + _obj + ' ' + _obj + '_tgt/' +
                    ' && cd ' + _obj + '_tgt/' +
                    ' && split -b 50M ' + _obj +
                    ' && rm -f ' + _obj +
                    ' && cd ..' +
                    ' && cat cd\\ ' + _obj + '_tgt/' +
                    '\\ncat\\ *\\ >\\ ' + _obj +
                    '\\nmv\\ ' + _obj + '\\ .. >> ' + _obj +
                    '_build.sh'
                )

def upload_branch(branch_dir = '', branch_name = ''):
    """ Upload a branch from path """

    system_run('mkdir -v ./repo_access/' + branch_name)

    copy_object(TGT_DIR + '/' + branch_dir, './repo_access/' + branch_name)

    system_run('cd ' + TGT_DIR + ' && git checkout --orphan ' + branch_name)

    remove_object(TGT_DIR, True, [TGT_DIR + '/.git', TGT_DIR + '/.', TGT_DIR + '/..'], False)

    system_run('cd ' + TGT_DIR + ' && git rm *')

    deconstruct_big_files('./repo_access/' + branch_name)

    copy_object('./repo_access/' + branch_name, TGT_DIR)

    system_run('cd ' + TGT_DIR + ' && ' +
        'git add -A && git commit -m "Sync"'
    )

    system_run('cd ' + TGT_DIR + ' && git push --force https://' + REPO_INIT.split('/')[0] +
        ':' + GITHUB_TOKEN + '@github.com/' + REPO_INIT + '.git ' + branch_name
    )

def remove_object(dest_object = '', recursive = True, exclude = ['.', '..'], remove_dest = True):
    """ Remove directory or object """

    if not os.path.isdir(dest_object):
        os.remove(dest_object)
        return

    for _obj in os.listdir(dest_object):
        if not dest_object + '/' + _obj in exclude:
            if os.path.isdir(dest_object + '/' + _obj) and recursive:
                remove_object(dest_object + '/' + _obj, recursive, exclude, True)
            else:
                os.remove(dest_object + '/' + _obj)

    if remove_dest:
        os.rmdir(dest_object)

def copy_object(from_path = '', dest_path = '', recursive = True, exclude = ['.', '..']):
    """ Copy directory or object """

    if os.path.isdir(from_path):
        for _obj in os.listdir(from_path):
            if not from_path + '/' + _obj in exclude:
                if os.path.isdir(from_path + '/' + _obj) and recursive:
                    os.mkdir(dest_path + '/' + _obj)
                    copy_object(from_path + '/' + _obj, dest_path + '/' + _obj, recursive, exclude)
                else:
                    system_run('cp -v ' + from_path + '/' + _obj + ' ' + dest_path)

def get_datetime():
    """ Get OS Datetime """
    return datetime.datetime.now().strftime("%Y") + '-' + \
        datetime.datetime.now().strftime("%m") + '-' + \
        datetime.datetime.now().strftime("%d") + '-' + \
        datetime.datetime.now().strftime("%H") + '-' + \
        datetime.datetime.now().strftime("%M") + '-' + \
        datetime.datetime.now().strftime("%S")

def count_up(array):
    """ Versioning style """

    counter = True

    delta_array = array
    delta_array.reverse()

    output_array = []

    for _i in delta_array:
        if not _i.isnumeric():
            return array

        if counter:
            if int(_i) <= 8:
                output_array += [str(int(_i) + 1)]
                counter = False
            else:
                output_array += ['0']
                counter = True
        else:
            output_array += [_i]

    output_array.reverse()

    return output_array



if '--auto-version' in BUILD_ARGS:
    if os.path.exists(TGT_DIR + '/version'):
        CALC = TGT_VERSION.split('.')
        CALC = '.'.join(count_up(CALC))
        os.remove(TGT_DIR + '/version')

        with open(TGT_DIR + '/version', 'w', newline='', encoding='UTF-8') as version_file:
            version_file.write(CALC)
            TGT_VERSION = CALC
    else:
        with open(TGT_DIR + '/version', 'w', newline='', encoding='UTF-8') as version_file:
            version_file.write('0.0.1')
            TGT_VERSION = '0.0.1'

if '--update-dir' in BUILD_ARGS or REPO_INIT.split('/')[0] == 'GamePlayer-8':
    system_run('cp -v ./LICENSE.txt ' + TGT_DIR)
    system_run('cp -v ./CODE_OF_CONDUCT.md ' + TGT_DIR)
    system_run('cp -rv ./.github ' + TGT_DIR)
    system_run('cp -v ./.gitignore ' + TGT_DIR)
    system_run('cp -rv ./licensing ' + TGT_DIR)
    system_run('rm -rf ' + TGT_DIR + '/LICENSE ')

if '--godot-plugin' in BUILD_ARGS:
    EXPORT_DELTA = ''
    if os.path.exists(TGT_DIR + '/plugin.template'):
        with open(TGT_DIR + '/plugin.template', newline = '', encoding = 'UTF-8') as export_file:
            EXPORT_DELTA = export_file.read().replace('%VERSIONPATCH%', TGT_VERSION)

        if os.path.exists(TGT_DIR + '/plugin.cfg'):
            os.remove(TGT_DIR + '/plugin.cfg')

        with open(TGT_DIR + '/plugin.cfg', 'w', newline='', encoding='UTF-8') as export_file:
            export_file.write(EXPORT_DELTA)

if '--updatec-dir' in BUILD_ARGS:
    SOURCE_PATH = ''

    try:
        SOURCE_PATH = sys.argv[sys.argv.index('--updatec-dir') + 1]
    except Exception:
        print('Missing source path for update dir.')
        sys.exit()

    if 'https://' in SOURCE_PATH:
        system_run('mkdir -v ./source')
        system_run('cd ./source && git clone --recursive ' + SOURCE_PATH)
        TARGET_DIR = ''
        for _obj in os.listdir('./source'):
            TARGET_DIR = './source' + _obj
            break

        system_run('cp -rv ' + TARGET_DIR + ' ' + TGT_DIR)
    else:
        system_run('cp -rv ' + TGT_DIR + '/' + SOURCE_PATH + ' ' + TGT_DIR)


if '--auto-version' in BUILD_ARGS or \
    '--update-dir' in BUILD_ARGS or \
    '--updatec-dir' in BUILD_ARGS or \
    '--godot-plugin' in BUILD_ARGS or REPO_INIT.split('/')[0] == 'GamePlayer-8':
    system_run('cd ' + TGT_DIR + ' && git add -A && git commit -m "Update via script"')
    system_run('cd ' + TGT_DIR + ' && git push https://' + REPO_INIT.split('/')[0] +
        ':' + GITHUB_TOKEN + '@github.com/' + REPO_INIT + '.git'
    )


if '--prepare' in BUILD_ARGS:
    if os.path.exists(TGT_DIR + '/prepare.sh'):
        system_run('cd ' + TGT_DIR + ' && sh ./prepare.sh')

if '--godot-setup' in BUILD_ARGS:
    GODOT_VERSION = '3.4.4'

    try:
        GODOT_VERSION = sys.argv[sys.argv.index('--godot-setup') + 1]
    except Exception:
        GODOT_VERSION = '3.4.4'

    system_run('mkdir -v ./runner')
    system_run('cd ./runner && wget https://downloads.tuxfamily.org/godotengine/' +
        GODOT_VERSION + '/Godot_v' + GODOT_VERSION + '-stable_linux_headless.64.zip -O runner.zip')

    system_run('cd ./runner && unzip runner.zip && rm -f runner.zip')

    GODOT_FILE = ''
    for _i in os.listdir('./runner'):
        GODOT_FILE = _i
        break

    system_run('cd ./runner && mv ' + GODOT_FILE + ' ../godot')

    system_run('chmod +rwx ./godot')

    system_run('mkdir -v ./template')
    system_run('cd ./template && wget https://downloads.tuxfamily.org/godotengine/' +
        GODOT_VERSION + '/Godot_v' + GODOT_VERSION + '-stable_export_templates.tpz -O template.zip'
    )

    system_run('cd ./template && unzip template.zip && rm -f template.zip')

    system_run('mkdir -v -p ~/.local/share/godot/templates/' + GODOT_VERSION + '.stable')

    system_run('cp -rv ./template/templates/* ~/.local/share/godot/templates/' +
        GODOT_VERSION + '.stable/'
    )

if '--godot-version' in BUILD_ARGS:
    EXPORT_DELTA = ''
    if os.path.exists(TGT_DIR + '/export_presets.cfg'):
        with open(TGT_DIR + '/export_presets.cfg', newline = '', encoding = 'UTF-8') as export_file:
            EXPORT_DELTA = export_file.read().replace('%VERSIONPATCH%', TGT_VERSION)

        os.remove(TGT_DIR + '/export_presets.cfg')

        with open(TGT_DIR + '/export_presets.cfg', 'w', newline='', encoding='UTF-8') as \
            export_file:
            export_file.write(EXPORT_DELTA)

if '--godot' in BUILD_ARGS:
    system_run('mkdir -v -p ' + TGT_DIR + '/builds')

    system_run('mkdir -v -p ' + TGT_DIR + '/builds/windows')
    system_run('mkdir -v -p ' + TGT_DIR + '/builds/linux')
    system_run('mkdir -v -p ' + TGT_DIR + '/builds/mac')
    system_run('mkdir -v -p ' + TGT_DIR + '/builds/web')
    system_run('mkdir -v -p ' + TGT_DIR + '/builds/android')

    system_run('rm -rf ' + TGT_DIR + '/.import')

    EXPORT_OPTIONS = ''

    with open(TGT_DIR + '/export_presets.cfg', newline='', encoding='UTF-8') as export_file:
        EXPORT_OPTIONS = export_file.read()

    os.mkdir(TGT_DIR + '/packs')

    if 'Windows Desktop' in EXPORT_OPTIONS:
        system_run('cd ' + TGT_DIR +
            ' && ../../godot -v --export "Windows Desktop" builds/windows/' +
            PROJECT_NAME + '.exe project.godot'
        )
        system_run('cd ' + TGT_DIR + '/builds/windows && zip ' + PROJECT_NAME + '-windows.zip *')
        system_run('mv ' + TGT_DIR + '/builds/windows/' + PROJECT_NAME + '-windows.zip ' +
            TGT_DIR + '/packs/'
        )

    if 'Linux/X11' in EXPORT_OPTIONS:
        system_run('cd ' + TGT_DIR +
            ' && ../../godot -v --export "Linux/X11" builds/linux/' +
            PROJECT_NAME + '.x86_64 project.godot'
        )
        system_run('cd ' + TGT_DIR + ' && chmod +rwx builds/linux/' + PROJECT_NAME + '.x86_64')
        system_run('cd ' + TGT_DIR + '/builds/linux && zip ' + PROJECT_NAME + '-linux.zip *')
        system_run('mv ' + TGT_DIR + '/builds/linux/' + PROJECT_NAME + '-linux.zip ' +
            TGT_DIR + '/packs/'
        )

    if 'Mac OSX' in EXPORT_OPTIONS:
        system_run('cd ' + TGT_DIR +
            ' && ../../godot -v --export "Mac OSX" builds/mac/' +
            PROJECT_NAME + '.zip project.godot'
        )
        system_run('mv ' + TGT_DIR + '/builds/mac/' + PROJECT_NAME + '.zip ' + TGT_DIR + '/packs/' +
            PROJECT_NAME + '-mac.zip'
        )

    if 'HTML5' in EXPORT_OPTIONS:
        system_run('cd ' + TGT_DIR +
            ' && ../../godot -v --export "HTML5" builds/web/' +
            PROJECT_NAME + '.html project.godot'
        )
        system_run('cd ' + TGT_DIR +
            ' && cp builds/web/' + PROJECT_NAME +
            '.html builds/web/index.html'
        )
        system_run('cd ' + TGT_DIR + '/builds/web && zip ' + PROJECT_NAME + '-html5.zip *')
        system_run('mv ' + TGT_DIR + '/builds/web/' + PROJECT_NAME + '-html5.zip ' +
            TGT_DIR + '/packs/'
        )

    if 'Android' in EXPORT_OPTIONS:
        system_run('cd ' + TGT_DIR +
            ' && ../../godot -v --export "Android" builds/android/' +
            PROJECT_NAME + '.apk project.godot'
        )
        system_run('cd ' + TGT_DIR + '/builds/android && zip ' + PROJECT_NAME + '-android.zip *')
        system_run('mv ' + TGT_DIR + '/builds/android/' + PROJECT_NAME + '-android.zip ' +
            TGT_DIR + '/packs/'
        )

if '--godot-headless' in BUILD_ARGS:
    GODOT_VERSION = '3.4.4'

    try:
        GODOT_VERSION = sys.argv[sys.argv.index('--godot-headless') + 1]
    except Exception:
        GODOT_VERSION = '3.4.4'

    system_run('mkdir -v -p ' + TGT_DIR + '/packs')

    system_run('mkdir -v -p ./headless')

    system_run('cd ./headless && wget https://downloads.tuxfamily.org/godotengine/' +
        GODOT_VERSION + '/Godot_v' + GODOT_VERSION + '-stable_linux_headless.64.zip -O headless.zip'
    )

    system_run('cd ./headless && unzip headless.zip && rm -rf headless.zip')

    system_run('cd ./headless && mv Godot_v' + \
        GODOT_VERSION + \
        '-stable_linux_headless.64 headless.64')

    system_run('mkdir -v -p ' + TGT_DIR + '/builds/headless')

    system_run('cd ' + TGT_DIR +
        ' && ../../godot -v --export "Headless" builds/headless/' +
        PROJECT_NAME + '.x86_64 project.godot'
    )

    system_run('cd ' + TGT_DIR + '/builds/headless && zip ' + PROJECT_NAME + '-headless.zip *')

    system_run('mv ' + TGT_DIR + '/builds/headless/' + PROJECT_NAME + '-headless.zip ' +
        TGT_DIR + '/packs/'
    )

if '--godot-server' in BUILD_ARGS:
    GODOT_VERSION = '3.4.4'

    try:
        GODOT_VERSION = sys.argv[sys.argv.index('--godot-server') + 1]
    except Exception:
        GODOT_VERSION = '3.4.4'

    system_run('mkdir -v -p ' + TGT_DIR + '/packs')

    system_run('mkdir -v -p ./server')

    system_run('cd ./server && wget https://downloads.tuxfamily.org/godotengine/' +
        GODOT_VERSION + '/Godot_v' + GODOT_VERSION + '-stable_linux_server.64.zip -O server.zip'
    )

    system_run('cd ./server && unzip server.zip && rm -rf server.zip')

    system_run('cd ./server && mv Godot_v' + GODOT_VERSION + '-stable_linux_server.64 server.64')

    system_run('mkdir -v -p ' + TGT_DIR + '/builds/server')

    system_run('cd ' + TGT_DIR +
        ' && ../../godot -v --export "Server" builds/server/' +
        PROJECT_NAME + '.x86_64 project.godot'
    )

    system_run('cd ' + TGT_DIR + '/builds/server && zip ' + PROJECT_NAME + '-server.zip *')

    system_run('mv ' + TGT_DIR + '/builds/server/' + PROJECT_NAME + '-server.zip ' +
        TGT_DIR + '/packs/'
    )



if '--c' in BUILD_ARGS:
    if os.path.exists(TGT_DIR + '/configure.sh'):
        system_run('cd ' + TGT_DIR + ' && sh configure.sh')

    if os.path.exists(TGT_DIR + '/Makefile'):
        system_run('cd ' + TGT_DIR + ' && make &&   make install')

    if os.path.exists(TGT_DIR + '/build.sh'):
        system_run('cd ' + TGT_DIR + ' && sh build.sh')

    if os.path.exists(TGT_DIR + '/compile.sh'):
        system_run('cd ' + TGT_DIR + ' && sh compile.sh')

    print('\nCompilations succed.')

if '--r' in BUILD_ARGS:
    ASSETS_DIRECTORY = 'null'

    try:
        ASSETS_DIRECTORY = BUILD_ARGS[BUILD_ARGS.index('--r') + 1]
    except Exception:
        ASSETS_DIRECTORY = 'null'

    publish_release(get_datetime(), 'master', TGT_VERSION +
                    ' Release', ASSETS_DIRECTORY)
    print('\nRelease published.')

if '--b' in BUILD_ARGS:
    BRANCH_DIRECTORY = ''
    BRANCH_TGT_NAME = ''

    try:
        BRANCH_TGT_NAME = BUILD_ARGS[BUILD_ARGS.index('--b') + 1]
        BRANCH_DIRECTORY = BUILD_ARGS[BUILD_ARGS.index('--b') + 2]
    except Exception:
        print('Missing args for upload branch.')
        sys.exit()

    upload_branch(BRANCH_DIRECTORY, BRANCH_TGT_NAME)

print(LOGGING)

print('\n\n\tEND OF LOG.\n')

BUILD_ARGS.remove(GITHUB_TOKEN)

CMD_OUTPUT = '\n\t - '.join(BUILD_ARGS)

print('\nBuild args (token unavailable): ' + CMD_OUTPUT)

print('\nMade with tea for Github by GamePlayer (@GamePlayer-8).')
