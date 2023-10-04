---
title: Batch edit .docx files 
---

## Background
There are times where you kept documents as seperate files, however you received notification that the Date format for all the document were to be changed from `dd-mm-yyyy` to `yyyy-mm-dd`. Or something like that, check out the guide below on how I used python to help solve this issue


## Setup
1. Install the package `!pip install python-docx` 
2. Use glob to read the files
3. Open said document
4. Loop thru all the `paragraph` and replace as neccessary
5. Save document


## Code
```python
from glob import glob
from docx import Document

fl = glob('{YOUR_DIRECTORY}/*.docx')
for f in fl:
    doc = Document(f)
    for p in doc.paragraphs:
        # Here you add your logic, 
        # for example I replace the G123 keyword to G234
        if 'G123' in p.text:
            p.text = p.text.replace('G123','G234')
    doc.save(f)
```