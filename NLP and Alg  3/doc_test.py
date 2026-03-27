from docx import Document

data = {'the': 0.0945945945945946, 'day': 0.02702702702702703, 'was': 0.02702702702702703, 'grey': 0.02702702702702703, 'and': 0.05405405405405406, 'bitter': 0.02702702702702703, 'cold': 0.02702702702702703, 'dogs': 0.02702702702702703, 'would': 0.02702702702702703, 'not': 0.02702702702702703, 'take': 0.02702702702702703, 'scent': 0.02702702702702703, 'big': 0.02702702702702703, 'black': 0.02702702702702703, 'hound': 0.02702702702702703, 'had': 0.02702702702702703, 'taken': 0.02702702702702703, 'one': 0.02702702702702703, 'sniff': 0.02702702702702703, 'at': 0.02702702702702703, 'bear': 0.02702702702702703, 'tracks': 0.02702702702702703, 'backed': 0.02702702702702703, 'off': 0.02702702702702703, 'skulked': 0.02702702702702703, 'back': 0.02702702702702703, 'to': 0.02702702702702703, 'pack': 0.02702702702702703, 'with': 0.02702702702702703, 'her': 0.04054054054054054, 'tail': 0.02702702702702703, 'between': 0.02702702702702703, 'legs': 0.02702702702702703}

doc = Document()
doc.add_heading('Unigram Counts', level=1)

# rows = words + header
table = doc.add_table(rows=len(data)+1, cols=2)

# header
table.rows[0].cells[0].text = "Word"
table.rows[0].cells[1].text = "Probablity"

# fill rows
for i, (word, count) in enumerate(sorted(data.items()), start=1):
    table.rows[i].cells[0].text = word
    table.rows[i].cells[1].text = str(count)

doc.save("unigrams.docx")
print("Saved unigrams.docx")