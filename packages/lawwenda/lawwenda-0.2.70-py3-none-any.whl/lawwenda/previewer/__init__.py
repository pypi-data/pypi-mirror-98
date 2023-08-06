# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import abc
import dataclasses
import io
import typing as t

import PIL.Image

if t.TYPE_CHECKING:
    import lawwenda.fs


@dataclasses.dataclass
class IsAbleRequest:
    name: str
    mimetype: str


class Previewer(abc.ABC):

    thumbsize = thumbwidth, thumbheight = 300, 300

    @abc.abstractmethod
    def is_thumbnailable(self, iar: IsAbleRequest) -> bool:
        pass

    @abc.abstractmethod
    def thumbnail(self, node: 'lawwenda.fs.Filesystem.Node') -> bytes:
        pass

    @abc.abstractmethod
    def is_previewable(self, iar: IsAbleRequest) -> bool:
        pass

    @abc.abstractmethod
    def preview_html(self, node: 'lawwenda.fs.Filesystem.Node') -> str:
        pass

    def _image_scale_to_thumbnail_size(self, imgdata: t.BinaryIO) -> io.BytesIO:
        img = PIL.Image.open(imgdata)
        img.thumbnail(self.thumbsize, PIL.Image.ANTIALIAS)
        resultimg = PIL.Image.new("RGBA", self.thumbsize, (0, 0, 0, 0))
        resultimg.paste(img, (int((self.thumbwidth - img.width) / 2), int((self.thumbheight - img.height) / 2)))
        bimg = io.BytesIO()
        resultimg.save(bimg, format="png")
        return bimg
