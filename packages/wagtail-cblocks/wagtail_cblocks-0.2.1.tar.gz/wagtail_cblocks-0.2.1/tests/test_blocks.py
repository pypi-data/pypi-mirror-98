import pytest
from bs4 import BeautifulSoup
from pytest_django.asserts import assertHTMLEqual
from wagtail_factories import DocumentFactory, ImageFactory, PageFactory

from wagtail_cblocks import blocks

from .models import BaseBlock


class BlockTest:
    def render(self, data, block=None):
        if block is None:
            block = self.block
        return block.render(block.to_python(data))

    def render_html(self, *args, **kwargs):
        return BeautifulSoup(self.render(*args, **kwargs), 'html.parser')


class TestHeadingBlock(BlockTest):
    block = blocks.HeadingBlock()

    def test_render(self):
        assertHTMLEqual(
            self.render({'text': "Un titre !", 'level': 2}),
            '<h2 id="un-titre">Un titre !</h2>',
        )


class TestParagraphBlock(BlockTest):
    block = blocks.ParagraphBlock()

    def test_features(self):
        assert self.block.features == blocks.ParagraphBlock.features

        block = blocks.ParagraphBlock(features=['bold', 'italic'])
        assert block.features == ['bold', 'italic']

    def test_render(self):
        data = '<p><i>Un</i> paragraphe !</p>'
        assertHTMLEqual(self.render(data), data)


@pytest.mark.django_db
class TestLinkBlock:
    block = blocks.LinkBlock()

    def get_value(self, target):
        return self.block.to_python({'target': target})

    def test_local_blocks(self):
        block = blocks.LinkBlock([('text', blocks.ParagraphBlock())])
        assert 'target' not in block.child_blocks
        assert 'target' in self.block.child_blocks

    def test_required(self):
        block = blocks.LinkBlock(required=False)
        assert block.required is False
        assert block.child_blocks['target'].required is False

        assert self.block.required is True
        assert self.block.child_blocks['target'].required is True

    def test_href_value_page(self, root_page):
        page = PageFactory(parent=root_page, title="About", slug='about')
        value = self.get_value([{'type': 'page', 'value': page.id}])
        assert value.href == '/about/'

    def test_href_value_page_invalid(self):
        value = self.get_value([{'type': 'page', 'value': 1000}])
        assert value.href is None

    def test_href_value_document(self):
        document = DocumentFactory()
        value = self.get_value([{'type': 'document', 'value': document.id}])
        assert value.href == document.file.url

    def test_href_value_document_invalid(self):
        value = self.get_value([{'type': 'document', 'value': 1000}])
        assert value.href is None

    def test_href_value_image(self):
        image = ImageFactory()
        value = self.get_value([{'type': 'image', 'value': image.id}])
        assert value.href == image.file.url

    def test_href_value_image_invalid(self):
        value = self.get_value([{'type': 'image', 'value': 1000}])
        assert value.href is None

    def test_href_value_external_url(self):
        url = 'http://example.org/truc/'
        value = self.get_value([{'type': 'url', 'value': url}])
        assert value.href == url

    def test_href_value_anchor(self):
        anchor = '#truc'
        value = self.get_value([{'type': 'anchor', 'value': anchor}])
        assert value.href == anchor

    def test_href_value_empty(self):
        value = self.get_value([])
        assert value.href is None

    def test_href_value_no_target(self):
        block = blocks.LinkBlock([('text', blocks.ParagraphBlock())])
        value = block.to_python({'text': "some text"})
        assert value.href is None


class TestButtonBlock(BlockTest):
    block = blocks.ButtonBlock()

    def test_render_link(self):
        url = 'http://example.org/truc/'
        assertHTMLEqual(
            self.render(
                {
                    'text': "Lien",
                    'link': {'target': [{'type': 'url', 'value': url}]},
                }
            ),
            '<a class="btn btn-primary mb-3" href="{}">Lien</a>'.format(url),
        )


@pytest.mark.django_db
class TestImageBlock(BlockTest):
    block = blocks.ImageBlock()

    def test_render(self):
        html = self.render_html(
            {
                'image': ImageFactory().id,
                'caption': '',
                'link': {'target': []},
            }
        )
        assert len(html.select('img.figure-img.img-fluid.mb-0')) == 1
        assert not html.select('figcaption')
        assert not html.select('a')

    def test_render_with_caption(self):
        html = self.render_html(
            {
                'image': ImageFactory().id,
                'caption': "Une légende en dessous.",
                'link': {'target': []},
            }
        )
        assert html.select_one('figcaption').text == "Une légende en dessous."
        assert not html.select('a')

    def test_render_with_link(self):
        url = 'http://example.org/truc/'
        html = self.render_html(
            {
                'image': ImageFactory().id,
                'caption': '',
                'link': {'target': [{'type': 'url', 'value': url}]},
            }
        )
        assert html.select_one('a').attrs['href'] == url
        assert not html.select('figcaption')


class TestColumnsBlock(BlockTest):
    block = blocks.ColumnsBlock(BaseBlock())

    def test_render(self):
        url = 'http://example.org/truc/'
        data = {
            'horizontal_align': 'center',
            'columns': [
                [
                    {
                        'type': 'button_block',
                        'value': {
                            'text': "Lien",
                            'link': {
                                'target': [{'type': 'url', 'value': url}],
                            },
                        },
                    },
                    {
                        'type': 'paragraph_block',
                        'value': "<p>A first paragraph.</p>",
                    },
                ],
                [
                    {
                        'type': 'paragraph_block',
                        'value': "<p>Another paragraph.</p>",
                    },
                ],
            ],
        }
        assertHTMLEqual(
            self.render(data),
            (
                '<div class="row text-center">'
                '<div class="col-sm">{}{}</div>'
                '<div class="col-sm">{}</div>'
                '</div>'
            ).format(
                '<a class="btn btn-primary mb-3" href="{}">Lien</a>'.format(
                    url
                ),
                '<p>A first paragraph.</p>',
                '<p>Another paragraph.</p>',
            ),
        )
