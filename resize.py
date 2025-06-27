import argparse
import contextlib
import logging
import pathlib
from argparse import ArgumentParser
from pathlib import Path

from PIL import Image, UnidentifiedImageError

RES_DIR_NAME = "compressed_with_koeff_%s"

LOG = logging.getLogger()
logging.basicConfig(
    format="%(levelname)s:%(message)s", encoding="utf-8", level=logging.INFO,
)

@contextlib.contextmanager
def wrap_error(err_msg: str) -> None:
    try:
        yield
    except Exception:
        LOG.exception(err_msg)
        return


def get_files_in_directory(path: str, regex: str) -> iter:
    current_dir = Path(path)
    if not current_dir.is_dir():
        err_msg = f"Path '{path}' should end by directory with images"
        raise ValueError(err_msg)
    return (i for i in current_dir.glob(regex) if not i.is_dir())


def resize(dir_name: str, file_name: Path, koeff: float) -> None | str:
    try:
        im = Image.open(file_name)
    except UnidentifiedImageError:
        LOG.warning("File %s can not be opened by Pillow, so skip it.", file_name)
        return None

    with wrap_error(f"Failed to resize {file_name}"):
        new_size = tuple(int(v * koeff) for v in im.size)
        new_im = im.resize(new_size)

    with wrap_error(f"Failed to store resized {file_name}"):
        new_image_name = f"{dir_name}/{file_name.name}"
        new_im.save(new_image_name, resolution=100.0)
    return new_image_name


def convert_to_pdf(dir_name: str, pdf_name: str, files: list[str]) -> None:
    if not pdf_name:
        return
    target_name = f"{dir_name}/{pdf_name}.pdf"
    images = [Image.open(i) for i in files]
    images = [i.convert("RGB") for i in images]
    images[0].save(target_name, save_all=True, append_images=images[1:])


def init_parser() -> ArgumentParser:
    parser = argparse.ArgumentParser(
        "resize",
        description="Script for resizing image files by using Pillow library",
    )
    parser.add_argument(
        "path", help="Path to directory with image files for compression",
    )
    parser.add_argument(
        "koeff", help="Koeff for modification original images size. "
        "Image with X,Y size will be converted to X * koeff, Y * koeff.",
    )
    parser.add_argument(
        "--regex", help="Regular expression for file compression. F.e: *.jpg",
        default="*",
    )
    parser.add_argument(
        "--pdf", help="Name of PDF file for storing all compresed files",
    )
    return parser


def main() -> None:
    parser = init_parser()
    arguments = parser.parse_args()
    koeff = float(arguments.koeff)
    if koeff == 0:
        err_msg = "The koeff could not be equal 0"
        raise ValueError(err_msg)
    files = get_files_in_directory(arguments.path, arguments.regex)

    # add directory for results
    dir_name = f"{arguments.path}/{RES_DIR_NAME % koeff}"
    pathlib.Path(dir_name).mkdir(parents=True, exist_ok=True)
    new_file_names = []
    for file in files:
        new_f_name = resize(dir_name, file, koeff)
        if new_f_name:
            new_file_names.append(new_f_name)
    LOG.info("Compressed files:\n\n%s", "\n".join(new_file_names))
    convert_to_pdf(dir_name, arguments.pdf, new_file_names)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        LOG.exception("Script failed due to:")
