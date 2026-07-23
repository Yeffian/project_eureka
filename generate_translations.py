import polib
import argparse
from deep_translator import GoogleTranslator

parser = argparse.ArgumentParser(
    prog='make_translations',
    description='Produces translations for .po files'
)

parser.add_argument('filename', type=str, help="The path of the .po file to update")
parser.add_argument('lang', type=str, help='A short code of the language for which to produce translations')
# parser.add_

args = parser.parse_args()
translator = GoogleTranslator(source='auto', target=args.lang)

pofile = polib.pofile(args.filename)
for entry in pofile:
    translated = translator.translate(entry.msgid)
    print(entry.msgid, "=>", translated)
    entry.msgstr = translated

pofile.save()