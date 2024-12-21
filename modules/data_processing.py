

def format_number_text(column):
    return column.apply(
        lambda x: (
            f"{x / 1e6:.1f}M" if x >= 1e6 else
            f"{x / 1e3:.1f}K" if x >= 1e3 else
            str(x)
        )
    )

# Format numerical values in a DataFrame column to 'K', 'M', or plain string.


def format_number_text_2(data, column):
    data[f"{column} (formatted)"] = data[column].apply(
        lambda x: (
            f"{x / 1e6:.1f}M" if x >= 1e6 else
            f"{x / 1e3:.1f}K" if x >= 1e3 else
            str(x)
        )
    )
    return data
