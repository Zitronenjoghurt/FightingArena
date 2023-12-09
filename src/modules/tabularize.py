def create_table(headers, rows):
    column_widths = [len(header) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            column_widths[i] = max(column_widths[i], len(str(cell)))

    row_format = "| " + " | ".join("{:<" + str(width) + "}" for width in column_widths) + " |"

    def create_row_string(row):
        return row_format.format(*row)

    def create_separator():
        return "-" * (len(row_format.format(*[""] * len(headers))) - 2)

    table_str = create_separator() + "\n"
    table_str += create_row_string(headers) + "\n"
    table_str += create_separator() + "\n"

    for row in rows:
        table_str += create_row_string(row) + "\n"
        table_str += create_separator() + "\n"

    return table_str