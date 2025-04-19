def split_list(lst, num_cols):
    avg_len = (len(lst) + num_cols - 1) // num_cols 
    return [lst[i * avg_len:(i + 1) * avg_len] for i in range(num_cols)]

def create_md_table(lst, num_cols=4):
    columns = split_list(lst, num_cols)
    max_rows = max(len(col) for col in columns)

    for col in columns:
        while len(col) < max_rows:
            col.append("")

    header = "| " + " | ".join(f"Col {i+1}" for i in range(num_cols)) + " |"
    separator = "| " + " | ".join("---" for _ in range(num_cols)) + " |"
    rows = []

    for i in range(max_rows):
        row = "| " + " | ".join(columns[j][i] for j in range(num_cols)) + " |"
        rows.append(row)

    table = "\n".join([header, separator] + rows)
    return table


def main() -> None:
    the_list = []
    line = input().strip()
    while line not in ['stop', 'end', 'quit', 'q']:
        the_list.append(line)
        line = input().strip()
    markdown_table = create_md_table(the_list)
    print(markdown_table)


if __name__=='__main__':
    main()