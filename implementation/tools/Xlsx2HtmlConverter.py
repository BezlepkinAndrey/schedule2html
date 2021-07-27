import xlsx2html.core as core
from openpyxl import worksheet
import implementation.tools.RangeGenerator as RangeGenerator
import re
import io
from openpyxl.drawing.image import Image

COEFFICIENT_PX_TO_REM = 1. / 16.

originWorksheetToData = core.worksheet_to_data
originGetStylesFromCell = core.get_styles_from_cell
originImageToData = core.image_to_data
originRenderTable = core.render_table

def worksheetToDataOverride(ws, locale=None, fs=None, default_cell_border="none"):
    data = originWorksheetToData(ws=ws, locale=locale, fs=fs, default_cell_border=default_cell_border)
    data['cols'] = getColumnDimensions(ws)
    return data


def getColumnDimensions(workbookSheet: worksheet):
    leftColumnLetter, rightColumnLetter = re.sub(r'\d+', r'', workbookSheet.dimensions).strip().split(':')
    columnLettersRange = RangeGenerator.strange(leftColumnLetter, rightColumnLetter)

    columnsStiles = []
    for letter in columnLettersRange:
        columnDimension = workbookSheet.column_dimensions[letter]

        width = 0.89
        if columnDimension.customWidth:
            width = round(columnDimension.width / 10., 2)
        pxColumnWidth = 96 * width
        columnsStiles.append({
            'index': columnDimension.index,
            'hidden': columnDimension.hidden,
            'style': {
                "width": "{}rem".format(pxColumnWidth * COEFFICIENT_PX_TO_REM),
                "min-width": "{}rem".format(pxColumnWidth * COEFFICIENT_PX_TO_REM),
                "max-width": "{}rem".format(pxColumnWidth * COEFFICIENT_PX_TO_REM),
            }
        })
    return columnsStiles


def imageToDataOverride(image: Image) -> dict:
    data = originImageToData(image)
    offsetX = data['offset']['x']
    offsetY = data['offset']['y']

    data['style']['margin-left'] = f'{offsetX * COEFFICIENT_PX_TO_REM}rem'
    data['style']['margin-top'] = f'{offsetY * COEFFICIENT_PX_TO_REM}rem'

    return data


def getStylesFromCellOverride(cell, merged_cell_map=None, default_cell_border="none"):
    styleData = originGetStylesFromCell(cell, merged_cell_map, default_cell_border)
    if cell.font:
        styleData['font-size'] = "%srem" % (cell.font.sz * COEFFICIENT_PX_TO_REM)
    return styleData


def convert(inputThread: io.BytesIO, sheet: str) -> io.StringIO:
    return core.xlsx2html(filepath=inputThread, locale='ru', sheet=sheet)

def renderTableOverride(data, append_headers, append_lineno):
    html = [
        '<table  '
        'style="border-collapse: collapse; table-layout:auto" '
        'border="0" '
        'cellspacing="0" '
        'cellpadding="0">'
    ]

    hidden_columns = set()
    for col in data['cols']:
        if col['hidden']:
            hidden_columns.add(col['index'])

    html.append('<tr>')
    for col in data['cols']:
        html.append('<td {attrs} style="{styles}">'.format(
            attrs=core.render_attrs(col.get('attrs')),
            styles=core.render_inline_styles(col.get('style')),
        ))
    html.append('</tr>')

    append_headers(data, html)

    for i, row in enumerate(data['rows']):
        trow = ['<tr>']
        append_lineno(trow, i)
        for cell in row:
            if cell['column'] in hidden_columns:
                continue
            images = data['images'].get((cell['column'], cell['row'])) or []
            formatted_images = []
            for img in images:
                styles = core.render_inline_styles(img['style'])
                img_tag = (
                    '<img width="{width}" height="{height}"'
                    'style="{styles_str}"'
                    'src="{src}"'
                    '/>'
                ).format(
                    styles_str=styles, **img)
                formatted_images.append(img_tag)
            trow.append((
                '<td {attrs_str} style="{styles_str}">'
                '{formatted_images}'
                '{formatted_value}'
                '</td>'
            ).format(
                attrs_str=core.render_attrs(cell['attrs']),
                styles_str=core.render_inline_styles(cell['style']),
                formatted_images='\n'.join(formatted_images),
                **cell))

        trow.append('</tr>')
        html.append('\n'.join(trow))
    html.append('</table>')
    return '\n'.join(html)

core.worksheet_to_data = worksheetToDataOverride
core.image_to_data = imageToDataOverride
core.get_styles_from_cell = getStylesFromCellOverride
core.render_table = renderTableOverride
