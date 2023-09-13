from pathlib import Path
import sys
import string
import os
import shutil
CATEGORIES = {'images': ['.jpeg', '.png', '.jpg', '.svg'],
              'video': ['.avi', '.mp4', '.mov', '.mkv'],
              'documents': ['.doc', '.docx','.txt', '.pdf', '.xlsx', '.pptx'],
              'audio': ['.mp3', '.ogg', '.wav', '.amr'],
              'archives': ['.zip', '.gz', '.tar']}
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}
result_know = []
result_dont_know = []
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()
punct = string.punctuation + ' '
def normalize(name:str):
    ext = name[name.rfind('.'):]
    n = name[:name.rfind('.')]
    name_out = ''
    for i in name:
        if i in punct:
            n = n.replace(i, '_')
    name_out = n + ext
    return name_out.translate(TRANS)
def delete_dir(path:Path):
    for root, dirs, _ in os.walk(path, topdown=False):
        for d in dirs:
            p = os.path.join(root, d)
            if not os.listdir(p):
                os.rmdir(p)
def get_categories(file:Path):
    ext = file.suffix.lower()
    for cat, exst in CATEGORIES.items():
        if ext in exst:
            result_know.append(ext)
            print(cat, file)
            return cat
    result_dont_know.append(ext)
    print('Other', file)
    return 'Other'
def move_file(file:Path, category, root_dir:Path):
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    file.replace(target_dir.joinpath(normalize(file.name)))
def sort_folder(path:Path):
    for element in path.glob('**/*'):
        if element.is_file():
            category = get_categories(element)
            move_file(element, category, path)
def archives_unpack(sort_folder:Path):
    try:
        for elem in sort_folder.glob('*archives*'):
            new_folder = elem.parent.joinpath(elem.stem)
            shutil.unpack_archive(elem, new_folder)
    except shutil.ReadError:
        return None
def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return 'Not param for folder'
    if not path.exists():
        return 'Folder is not exists'
    sort_folder(path)
    delete_dir(path)
    archives_unpack(path)
if __name__ == '__main__':
    print(main())
print(f'Not idintifield {set(result_know)}')
print(f'Idintifield {set(result_dont_know)}')