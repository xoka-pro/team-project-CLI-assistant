from os import listdir
from pathlib import Path
import shutil
import re

IMAGES_SUFFIX = ('JPEG', 'PNG', 'JPG', 'SVG')
DOCUMENTS_SUFFIX = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'PPT')
AUDIO_SUFFIX = ('MP3', 'OGG', 'WAV', 'AMR')
VIDEO_SUFFIX = ('AVI', 'MP4', 'MOV', 'MKV')
ARCHIVES_SUFFIX = ('ZIP', 'GZ', 'TAR')


def normalize(in_string: str) -> str:
    """Replace cyrillic symbols on latin and change other to _ (except digit)

    Args:
        in_string (string):  need re module and use string translate
    """
    latin = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
              "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    trans = {}
    for c, l in zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ", latin):
        trans[ord(c)] = l
        trans[ord(c.upper())] = l.upper()

    return re.sub(r'[^0-9a-zA-Z]', '_', in_string.translate(trans))


def sorter(*args):
    """Main sort function"""
    if len(args) < 1:
        return f'Directory to sort not specified'
    else:
        path = Path(args[0])
        if path.exists() and path.is_dir():
            print(f"Start working with {path.resolve()}")
            if len(args) > 1 and args[1] != None:
                path_out = Path(args[1])
            else:
                path_out = path
            print(f"Prepare directory {path_out.resolve()}")
            Path(str(path_out.parent.resolve())+'/'+normalize(path_out.name)).mkdir(
                exist_ok=True, parents=True)
            # prepared, now we can sorting
            result = sort_dir(path, Path(path_out))
            if not len(result['result_list']):
                print("|----------|----------...\n")
                print("|{:^10}|{:^100}\n".format("Type", "file"))
                print("|----------|----------...\n")
            for key in result['result_list'].keys():
                for fil in result['result_list'][key]:
                    print("|{:^10}| {:<100}".format(key, fil))
            if len(result['to_do_suffix']):
                print(f"Processed known extensions: {result['to_do_suffix']}")
            if len(result['unknown_suffix']):
                print(f"Found unknown extensions: {result['unknown_suffix']}")
            if len(result['trobles_list']):
                print(f"Errors: {result['trobles_list']}")
        else:
            return f"Incorrect directory specified"
    return f'Directory {args[0]} sorted!'


def sort_archives(file_path: Path, out_dir: Path) -> str:
    """unpak archive to sub cat archives in directory like filename 

    Args:
        file_path (Path): archive filename
        out_dir (Path): destination directory

    Returns:
        str: directory name of ?err 
    """
    new_dir = str(out_dir.resolve()) + '/archives/' + \
        normalize(file_path.stem)
    try:
        Path(str(out_dir.resolve()) +
             '/archives').mkdir(exist_ok=True, parents=True)
        Path(new_dir).mkdir(exist_ok=True, parents=True)
    except OSError:
        new_dir = "?errOS"

    try:
        shutil.unpack_archive(file_path.resolve(), new_dir)
    except shutil.ReadError:
        new_dir = "?errAR"

    try:
        file_path.resolve().unlink()
    except FileNotFoundError:
        new_dir = "?errDF"

    return new_dir


def move_file(file_path: Path, out_dir: Path, destany: str) -> str:
    """move file to sub directory in sub directory destany 

    Args:
        file_path (Path): archive filename
        out_dir (Path): destination directory

    Returns:
        str: normalized new file name of ?err 
    """
    new_f = str(out_dir.resolve()) + '/' + destany + '/' + \
        normalize(file_path.stem) + file_path.suffix
    try:
        Path(str(out_dir.resolve()) + '/' +
             destany).mkdir(exist_ok=True, parents=True)
        shutil.move(str(file_path.resolve()), new_f)
    except OSError:
        new_f = "?errOS"
    finally:
        return new_f


def sort_dir(path: Path, out_dir: Path) -> dict:
    """sorting dir and file to sub directory 

    Args:
        path (Path): soure directory
        out_dir (Path): destination directory

    Returns:
        dict: 
            result_list = {'images': [], 'documents': [],
                   'audio': [], 'video': [], 'archives': []}
            to_do_suffix = set()
            unknown_suffix = set()
            trobles_list = []
    """

    result_list = {'images': [], 'documents': [],
                   'audio': [], 'video': [], 'archives': []}
    to_do_suffix = set()
    unknown_suffix = set()
    trobles_list = []

    for p in path.iterdir():
        if p.is_dir():
            if not str(p.name) in result_list.keys():
                # магія
                dir_res = sort_dir(p, out_dir)
                # доповнення результатів теки
                for key in result_list.keys():
                    result_list[key].extend(dir_res['result_list'][key])
                to_do_suffix = to_do_suffix | dir_res['to_do_suffix']
                unknown_suffix = unknown_suffix | dir_res['unknown_suffix']
                trobles_list.extend(dir_res['trobles_list'])

                # перевірка на пусту теку
                if not listdir(p):
                    # видалення теки
                    try:
                        p.rmdir()
                    except OSError:
                        trobles_list.append(
                            f'empty dir {p.resolve} dont want to die')

        else:
            if p.suffix.removeprefix('.').upper() in IMAGES_SUFFIX:
                to_do_suffix.add(p.suffix.removeprefix('.'))
                res = move_file(p, out_dir, 'images')
                if res[0] != '?':
                    result_list['images'].append(res)
                else:
                    trobles_list.append(
                        f'in file {p.resolve()} code error {res[1:]}')
            elif p.suffix.removeprefix('.').upper() in DOCUMENTS_SUFFIX:
                to_do_suffix.add(p.suffix.removeprefix('.'))
                res = move_file(p, out_dir, 'documents')
                if res[0] != '?':
                    result_list['documents'].append(res)
                else:
                    trobles_list.append(
                        f'in file {p.resolve()} code error {res[1:]}')
            elif p.suffix.removeprefix('.').upper() in AUDIO_SUFFIX:
                to_do_suffix.add(p.suffix.removeprefix('.'))
                res = move_file(p, out_dir, 'audio')
                if res[0] != '?':
                    result_list['audio'].append(res)
                else:
                    trobles_list.append(
                        f'in file {p.resolve()} code error {res[1:]}')
            elif p.suffix.removeprefix('.').upper() in VIDEO_SUFFIX:
                to_do_suffix.add(p.suffix.removeprefix('.'))
                res = move_file(p, out_dir, 'video')
                if res[0] != '?':
                    result_list['video'].append(res)
                else:
                    trobles_list.append(
                        f'in file {p.resolve()} code error {res[1:]}')
            elif p.suffix.removeprefix('.').upper() in ARCHIVES_SUFFIX:
                to_do_suffix.add(p.suffix.removeprefix('.'))
                res = sort_archives(p, out_dir)
                if res[0] != '?':
                    result_list['archives'].append(res)
                else:
                    trobles_list.append(
                        f'in file {p.resolve()} code error {res[1:]}')
            else:
                unknown_suffix.add(p.suffix)

    return {'result_list': result_list, 'to_do_suffix': to_do_suffix, 'unknown_suffix': unknown_suffix, 'trobles_list': trobles_list}
