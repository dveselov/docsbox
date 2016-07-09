import os

from wand.image import Image


def make_thumbnails(image, tmp_dir, size):
    thumbnails_folder = os.path.join(tmp_dir, "thumbnails/")
    os.mkdir(thumbnails_folder)
    (width, height) = size
    for index, page in enumerate(image.sequence):
        with Image(page) as page:
            filename = os.path.join(thumbnails_folder, "{0}.png".format(index))
            page.resize(width, height)
            page.save(filename=filename)
    else:
        image.close()
    return index
