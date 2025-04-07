import pysbd
seg_en = pysbd.Segmenter(language="en", clean=False)

from transformers import pipeline
fugu_translator = pipeline('translation', model='staka/fugumt-en-ja')
txt = 'This is a cat. It is very cute.'
print(fugu_translator(seg_en.segment(txt)))