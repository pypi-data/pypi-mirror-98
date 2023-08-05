from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from wagtail_cblocks.blocks import (
    ButtonBlock,
    ColumnsBlock,
    HeadingBlock,
    ImageBlock,
    ParagraphBlock,
)


class BaseBlock(StreamBlock):
    title_block = HeadingBlock()
    paragraph_block = ParagraphBlock()
    button_block = ButtonBlock()
    image_block = ImageBlock()


class BodyBlock(BaseBlock):
    columns_block = ColumnsBlock(BaseBlock())


class StandardPage(Page):
    body = StreamField(BodyBlock())

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
