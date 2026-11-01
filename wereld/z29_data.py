# Ronde Z29 sfeerdetails per hoofdstuk (volledige lezing h01-h33). Bron: z29/notes_a.py
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'z29'))
from notes_a import N
SKIP={2,35,37,43,65}  # volledig al in canon (alle toetswoorden aanwezig)
D=[(h,f'{o} ({cat})',f,j) for i,(h,cat,o,f,j,k) in enumerate(N) if i not in SKIP]
