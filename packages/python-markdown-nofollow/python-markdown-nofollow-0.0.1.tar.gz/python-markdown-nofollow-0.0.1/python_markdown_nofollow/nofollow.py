
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class NofollowLink(Treeprocessor):
    def run(self, root):
        for element in root.iter("a"):
            element.set("rel", "external nofollow")
            element.set("target", "_blank")


class NofollowExtension(Extension):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        md.treeprocessors.register(NofollowLink(md), 'nofollowlink', 15)


def makeExtension(**kwargs):
    return NofollowExtension(**kwargs)
