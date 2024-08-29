import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import malayalam_morpheme_splitter as mms

def test_morph_analysis_empty_string():
    assert mms.morph_analysis('') == []

def test_morph_analysis_single_word():
    assert mms.morph_analysis('ആന') == [['ആന']]

def test_morph_analysis_sentence():
    assert mms.morph_analysis('ആനയുടെ വൃക്ഷമായ') == [['ആന', 'ഉടെ'], ['വൃക്ഷം', 'ആയ']]

def test_morph_analysis_multiple_split():
    assert mms.morph_analysis('മനുഷ്യന്മാരിലൂടെ') == [['മനുഷ്യൻ', 'മാർ', 'ഇൽ', 'ഊടെ']]

def test_db_entry_add_new_entry():
    new_entry = {'ചിരിയിൽ': ['ചിരി', 'ഇൽ']}
    mms.db_entry(new_entry)
    assert mms.morph_analysis('ചിരിയിൽ') == [['ചിരി', 'ഇൽ']]

def test_db_entry_redundancy():
    with pytest.raises(ValueError):
        mms.db_entry({'ആനയെ': ['ആന', 'എ']})

def test_root_word_entry_redundancy():
    with pytest.raises(ValueError):
        mms.root_word_entry('ആന')

def test_db_entry_size():
    len1 = len(mms.read_all_examples())
    mms.db_entry({'മലയോടെ' : ['മല', 'ഓടെ'], 'മലയുടെ' : ['മല', 'ഉടെ']})
    len2 = len(mms.read_all_examples())
    assert len2 - len1 == 2

def test_read_all_examples_consistency():
    mms.db_entry({'പുസ്തകത്തിൻ്റെ': ['പുസ്തകം', 'ഇൻ്റെ']})
    examples = mms.read_all_examples()
    assert 'പുസ്തകത്തിൻ്റെ' in examples, "Expected 'പുസ്തകത്തിൻ്റെ' to be present in examples after db_entry"

def test_db_entry_update_existing_entry():
    mms.db_entry({'മടി': ['മടി', '-']})
    mms.db_entry({'മടി': ['മടി']})
    assert mms.morph_analysis('മടി') == [['മടി']]


