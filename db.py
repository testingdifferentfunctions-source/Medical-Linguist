from peewee import *

db = SqliteDatabase("database.db")


class LatinWords(Model):
    latin_original = CharField()
    latin_translated = CharField()

    class Meta:
        database = db


class GreekWords(Model):
    greek_original = CharField()
    greek_translated = CharField()

    class Meta:
        database = db


class EnglishWords(Model):
    english_original = CharField()
    english_translated = CharField()

    class Meta:
        database = db


db.connect()
db.create_tables([LatinWords, GreekWords, EnglishWords], safe=True)

if LatinWords.select().count() == 0:
    for latin_word, latin_translation in latin_dict.items():
        latin_row = LatinWords(latin_original=latin_word, latin_translated=latin_translation)
        latin_row.save()

elif GreekWords.select().count() == 0:
    for greek_word, greek_translation in greek_dict.items():
        greek_row = GreekWords(greek_original=greek_word, greek_translated=greek_translation)
        greek_row.save()

elif EnglishWords.select().count() == 0:
    for english_word, english_translation in english_dict.items():
        english_row = EnglishWords(english_original=english_word, english_translated=english_translation)
        english_row.save()

print("Created!")

random_latin_word = LatinWords.select().order_by(fn.Random()).get()
word_variant_one = LatinWords.select().order_by(fn.Random()).get()
word_variant_two = LatinWords.select().order_by(fn.Random()).get()

print("Random latin word: ", random_latin_word.latin_original)
print("Random latin translation: ", random_latin_word.latin_translated)

db.close()