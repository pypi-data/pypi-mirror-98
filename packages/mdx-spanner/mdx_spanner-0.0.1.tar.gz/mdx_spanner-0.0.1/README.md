# mdx_spanner

This package enables `rowspan` and `colspan` in markdown tables when using [MkDocs](https://www.mkdocs.org/).

## Syntax

You can activate `colspan` by putting only `~~` in a cell. This will merge the cell with the cell in the previous column.

You can activate `rowspan` by putting `__` in a cell. This will merge the cell with the cell in the previous row. If the cell in previous row is empty it will continue to merge until it finds a non-empty cell.

Sample:

```md
| Header 1 | Header 2 | Header 3 |
| ---------| -------- | -------- |
| Value 1  |    ~~    | Value 2  |
|          |    ~~    | Value 3  |
|_        _|    ~~    | Value 5  |
| Value 6  | Value 7  | Value 8  |
```

This should result in the following table:
```md
+----------+----------+----------+
| Header 1 | Header 2 | Header 3 |
+----------+----------+----------+
| Value 1             | Value 2  |
|                     +----------+
|                     | Value 3  |
|                     +----------+
|                     | Value 5  |
+----------+----------+----------+
| Value 6  | Value 7  | Value 8  |
+----------+----------+----------+
```

## Install
