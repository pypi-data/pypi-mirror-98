# wagtail-cblocks

A collection of StreamField blocks to use in Wagtail CMS.

**Warning!** This project is still early on in its development lifecycle. It is possible for breaking changes to occur between versions until reaching a stable 1.0. Feedback and pull requests are welcome.

## Requirements

wagtail-cblocks requires the following:
- Python (3.7, 3.8, 3.9)
- Django (2.11, 3.0, 3.1)
- Wagtail (2.11, 2.12)

Older versions of Wagtail could work too but they are not tested. The efforts are focused in LTS and recent versions.

## Installation

Install using ``pip``:

```shell
pip install wagtail-cblocks
```

Add ``wagtail_cblocks`` to your ``INSTALLED_APPS`` setting:

```python
INSTALLED_APPS = [
    # ...
    'wagtail_cblocks',
    # ...
]
```

## Usage

Each block comes with a template made for Bootstrap 5 which is not shipped by this plugin. If you plan to use them as is, you must have at least the Bootstrap stylesheet loaded in your base template - refer as needed to the [Bootstrap documentation](https://getbootstrap.com/).

In waiting for the documentation, here is a sample usage:

```python
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
```

Factories are also provided for some of the blocks to ease tests - see
[`wagtail_cblocks/factories.py`](wagtail_cblocks/factories.py). To make use of
them, install the extra *factories* requirements:

```shell
pip install wagtail-cblocks[factories]
```

## Development
### Quick start

To set up a development environment, ensure that ``virtualenv`` is installed on your system. Then:

1. Clone this repository
2. Create a virtual environment and activate it:
   ```shell
   virtualenv -p python3 venv
   source venv/bin/activate
   ```
3. Install this package in develop mode with extra requirements:
   ```shell
   pip install -e .[test]
   ```

Finally, if you want to run the test application to preview the blocks, you will have to create the database before running a development server:
```shell
./tests/manage.py migrate
DEBUG=1 ./tests/manage.py runserver
```

Note that ``DEBUG=1`` is required since tests are run without the debug mode. All the media will be stored in ``tests/var``.

### Contributing

The Python code is formatted and linted thanks to flake8, isort and black. To ease the use of this tools, the following commands are available:
- ``make lint``: check the Python code syntax and imports order
- ``make format``: fix the Python code syntax and imports order

The tests are written with pytest and code coverage is measured with coverage.py. You can use the following commands for that:
- ``make test``: run the tests and output a quick report of code coverage
- ``make coverage``: run the tests and produce an HTML report of code coverage

When submitting a pull-request, please ensure that the code is well formatted and covered, and that all the other tests pass.
