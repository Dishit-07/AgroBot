# -*- coding: utf-8 -*-
with open('D:/Graphic hackathon/rover/app/app_new/app_new.ino', 'r', encoding='utf-8') as f:
    text = f.read()

# Check brace balance
open_braces = text.count('{')
close_braces = text.count('}')
open_parens = text.count('(')
close_parens = text.count(')')

print(f"Braces: {open_braces} open, {close_braces} close. Balance: {open_braces - close_braces}")
print(f"Parens: {open_parens} open, {close_parens} close. Balance: {open_parens - close_parens}")

lines = text.splitlines()
print(f"Total lines: {len(lines)}")
for i, l in enumerate(lines):
    if "probeCommandedAngle" in l or "gpsValid" in l:
        print(f"L{i+1}: {l}")
