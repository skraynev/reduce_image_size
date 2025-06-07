from pathlib import Path
from PIL import Image

def get_files_in_directory(path: str, regexp: str):
    current_dir = Path(path)
    return (
        item
        for item in current_dir.iterdir()
        if item.is_file()  # and filter_by_regexp(item, regexp)
    )


if __name__ == '__main__':
    print(list(get_files_in_directory('.', '')))


    dev = int(input())

    im = Image.open('orig.jpg')
    new_size = tuple((x // dev for x in im.size))
    new_im = im.resize(new_size)

    new_im.save(f'compressed_{dev}.jpg', resolution=100.0)