from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

import copy
import re

class MdxSpannerExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        if 'table' in md.parser.blockprocessors:
            md.treeprocessors.add(
                'mdx_spanner',
                MdxSpannerTreeProcessor(self),
                '<inline'
            )

class MdxSpannerTreeProcessor(Treeprocessor):

    ROWSPAN_MARKER_PATTERN = re.compile(r'^_[_^= ]*_$')
    COLSPAN_MARKER_PATTERN = re.compile(r'\s*~~\s*$')
    EMPTY_PATTERN = re.compile(r'^\s*$')

    def __init__(self, extension_obj):
        super(MdxSpannerTreeProcessor, self).__init__()

    def run(self, root):
        tables = root.findall('.//table')
        for table in tables:
            tbody = table.find('tbody')

            for row in tbody:
                self._merge_row_cells(row)

            for col in zip(*tbody):
                self._merge_col_cells(col)

            for tr in tbody:
                for td in copy.copy(tr):
                    if td.get('remove'):
                        tr.remove(td)

    def _merge_row_cells(self, row):
        span_count = 1
        for cell in row[::-1]:
            if self.COLSPAN_MARKER_PATTERN.search(cell.text):
                span_count += 1
                cell.set('remove', 'true')
            elif span_count > 1:
                cell.set('colspan', str(span_count))
                span_count = 1

    def _merge_col_cells(self, col):
        span_count = 1
        for cell in col[::-1]:
            if self.ROWSPAN_MARKER_PATTERN.search(cell.text):
                # pdb.set_trace()
                span_count = 2
                cell.set('remove', 'true')
            elif self.EMPTY_PATTERN.search(cell.text) and span_count > 1:
                span_count += 1
                cell.set('remove', 'true')
            elif span_count > 1:
                cell.set('rowspan', str(span_count))
                # td.set('style', 'vertical-align: middle;text-align:center;')
                span_count = 1

def makeExtension(*args, **kwargs):
    return MdxSpannerExtension(*args, **kwargs)
