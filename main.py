import os
import sys
import shutil


CATEGORIES = dict(IMAGE=['jpeg', 'png', 'jpg', 'svg'],
                  VIDEO=['avi', 'mp4', 'mov', 'mkv'],
                  DOCS=['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
                  MUSIC=['mp3', 'ogg', 'wav', 'amr'],
                  ARCHIVE=['zip', 'gz', 'tar'],
                  OTHER=[])


translate_dict = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
                  'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
                  'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
                  'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
                  'ю': 'u', 'я': 'ya', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO',
                  'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
                  'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
                  'Ц': 'C', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SCH', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'E',
                  'Ю': 'U', 'Я': 'YA', 'ґ': '', 'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i',
                  'Є': 'e', '1': '1', '2': '2', '3': '3'}

sorted_path = sys.argv[1]


def transliterate(word):
    for key in translate_dict:
        word = word.replace(key, translate_dict[key])
    return word


def normalize():
    for el in os.listdir(sorted_path):
        tel = transliterate(el)
        os.rename(os.path.join(sorted_path, el),
                  os.path.join(sorted_path, tel))


def create_ext_set():
    ext_set = set()
    for el in os.listdir(sorted_path):
        ext = el.split('.')[-1]
        if os.path.isfile(os.path.join(sorted_path, el)) and ext in str(CATEGORIES.values()):
            ext_set.add(ext)
    return ext_set


def create_un_ext_set():
    ext_set = set()
    for el in os.listdir(sorted_path):
        ext = el.split('.')[-1]
        if os.path.isfile(os.path.join(sorted_path, el)) and ext not in str(CATEGORIES.values()):
            ext_set.add(ext)
    return ext_set


def del_empty_dirs(adress):
    for dirs in os.listdir(adress):
        dir = os.path.join(adress, dirs)
        if os.path.isdir(dir):
            del_empty_dirs(dir)
            if not os.listdir(dir):
                shutil.rmtree(dir)


def deep_folders(root_folder):
    for subdir, dirs, files in os.walk(root_folder):
        for file in files:
            src = os.path.join(subdir, file)
            dst = os.path.join(root_folder, file)
            shutil.move(src, dst)
        del_empty_dirs(root_folder)


def create_sort_folders(sorted_path):
    for category in CATEGORIES:
        if category not in os.listdir():
            os.mkdir(os.path.join(sorted_path, category))


def get_category(ext):
    for category, extinsions in CATEGORIES.items():
        if ext in extinsions:
            return category
    return "OTHER"


def sort(sorted_path):
    for el in os.listdir(sorted_path):
        if os.path.isfile(os.path.join(sorted_path, el)):
            ext = el.split('.')[-1]
            category = get_category(ext)
            target_folder = os.path.join(sorted_path, category)
            if category == "ARCHIVE":
                shutil.unpack_archive(os.path.join(
                    sorted_path, el), target_folder)
                os.remove(os.path.join(sorted_path, el))
                continue
            shutil.move(os.path.join(sorted_path, el), target_folder)


def main():
    deep_folders(sorted_path)
    with_ext = create_ext_set()
    without_ext = create_un_ext_set()
    normalize()
    create_sort_folders(sorted_path)
    sort(sorted_path)


if __name__ == "__main__":
    main()
