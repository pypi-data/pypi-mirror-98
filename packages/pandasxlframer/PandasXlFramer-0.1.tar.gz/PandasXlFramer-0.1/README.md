# pandasxlframer
This is a simple wrapper of openpyxl to enable additional Excel formatting for Pandas' dataframe. The intented use is to add formatting function when saving a dataframe to Excel: font size, text alignment, coloring/merging cells, and adding header. The goal is to use method chaining to provide a quick syntax to accomplish such task.

For example the default Pandas' to_excel output a file like this:
<img src="data/image/default_output.png">
A task that we often encounter is to add a header to this Excel file, merge some column cells, formatting cells, and to change background color. This can be accomplish by the following codes:<br>
```\python
int_map = {"全量": "int", "S+": "int", "S": "int", "A": "int", "B": "int", "无级别": "int"}
path = "../data/output/test.xlsx"
(
    df.excel_format.add_header(title_text="兴趣点为空统计总览")
    .set_columns_format(int_map)
    .column_color("频道", green, skip_row=2)
    .merge_column_cell("频道")
    .row_color(2, orange, skip_col=1)
    .save(path)
)
```

It will now output a file that looks like this:
<img src="data/image/format_output.png">

Because I currently use this formatter primary for Chinese audience, the default font style is "微软雅黑". However, if you need a different font style, you can do some by changing the default_font_style in the framer.py file.

The current supported functionalities are:
- add header;
- set column width;
- set column format (integer, float, percentage);
- set row alignment;
- merge cells in a column;
- change column/row color;

### To Do
- add more cell coloring options;
- add more alignment options;
- add examples of how to write multiple dataframe and multiple sheets.