"""boostnote_to_wordpress - """
from mistune_contrib.mdrenderer import MdRenderer
from urlpath import URL

__version__ = "0.1.0"
__author__ = "fx-kirin <fx.kirin@gmail.com>"
__all__: list = []


class CustomMdRenderer(MdRenderer):
    def __init__(self, modifier=None):
        super(CustomMdRenderer, self).__init__()
        self.image_links = []
        self.modifier = modifier

    def image(self, src, title, text):
        if src[0:8] == ":storage":
            image_dict = {}
            image_dict["src"] = src
            image_dict["title"] = title
            image_dict["text"] = text
            self.image_links.append(image_dict)

            if self.modifier is not None:
                if src in self.modifier:
                    src = self.modifier[src]
        return self.link(src, title, text, image=True)

    def header(self, text, level, raw=None):
        if not hasattr(self, "title"):
            if level == 1:
                self.title = text
        return "#" * (level) + " " + text + "\n\n"


def upload_image_link(wp, boost_note_root, image_link):
    actual_src = image_link["src"].replace(
        ":storage", str(boost_note_root / "attachments")
    )
    result = wp.upload_image(actual_src, name=image_link["text"])
    result = result.json()
    url = URL(result["guid"]["rendered"])
    url.path
    return url.path
