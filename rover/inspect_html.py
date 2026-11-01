# -*- coding: utf-8 -*-
with open('D:/Graphic hackathon/rover/dashboard/v1_backup.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print('Total lines in v1_backup.html:', len(lines))
for i, line in enumerate(lines):
    if 'id="tabBar"' in line:
        print('tabBar start:', i)
    if 'id="page0"' in line:
        print('page0 start:', i)
    if 'id="page1"' in line:
        print('page1 start:', i)
    if 'id="page2"' in line:
        print('page2 start:', i)
    if 'id="page3"' in line:
        print('page3 start:', i)
    if 'id="page4"' in line:
        print('page4 start:', i)
    if 'id="page5"' in line:
        print('page5 start:', i)
    if 'id="page6"' in line:
        print('page6 start:', i)
    if '<script' in line:
        print('script tag:', i)
