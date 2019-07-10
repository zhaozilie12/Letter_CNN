#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-


print('Content-Type: application/json')
print()
import cgi, os
import cgitb;

from letter_predict import letter_predict

cgitb.enable()
form = cgi.FieldStorage()
fileitem = form['rec_img']

letter = ''
precent = ''

if fileitem.filename:
    stream = fileitem.file.read()
    f = open("test.png", "wb")
    f.write(stream)
    f.close()
    pred = letter_predict("test.png")
    letter = chr(65 + pred.argmax())
    precent = str('%.2f' % pred[0][pred.argmax()])

print("""\
{
 "letter":"%s",
 "precent":"%s"
}
""" % (letter, precent))
