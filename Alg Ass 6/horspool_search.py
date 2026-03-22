pattern = "TCCTATTCTT"
text =    "TTATAGATCTCGTATTCTTTTATAGATCTCCTATTCTT"

def build_table(pattern):
    c_table = {}

    for c in pattern:
        if c not in c_table.keys():
            c_table.update({c : len(pattern)})
    
    for c in range(len(pattern) - 1):
        if pattern[c] in c_table:
            c_table.update({pattern[c]: len(pattern) - c - 1})

    print(c_table)

    return c_table
    

def search_text(text, pattern):
    table = build_table(pattern)
    c = len(pattern) - 1

    while c < len(text):
        if pattern == text[c - len(pattern) + 1:c+1]:
            return (c - len(pattern) + 1, c)
        
        elif text[c] in table.keys():
            c += table[text[c]]
        
        else:
            c += len(pattern)
    
    return -1

print(search_text(text, pattern))
