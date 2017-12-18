#!/usr/bin/env python
'''
    Take input as a single word and find all anagrams in the
    pre-populated AWS DynamoDB.

'''
import boto3
import itertools
import logging
import os

class AnagramHandler(object):

    def __init__(self, event, context):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('anagram_words')

        self.anagrams = self.anagrams_handler(event, context)

    def anagrams_handler(self, event, context=False):
        '''Find anagrams of a word'''

        self.logger.info('event details: %s', event)
        self.logger.info('context details: %s', context)
        
        orig_word = event['word']
        word = (''.join(sorted(event['word']))).strip()
        
        if word[0] not in [chr(a) for a in range(ord('a'), ord('z')+1)]:
            self.logger.info('invalid lookup character: %s', word[0])
            return {'fail': 'invalid lookup character: {}'.format(word[0])}

        self.logger.info('sorted word: %s', word)

        cache_value = self.cache_lookup(word)

        if not cache_value:

            self.logger.info('could not find anagrams: %s', event['word'])
            found_anagrams = orig_word

        else:
            found_anagrams = cache_value
            self.logger.info('cached anagrams: %s', found_anagrams)

        return {'anagrams': found_anagrams}

    def cache_lookup(self, word):
        '''Lookup a word in the cache'''

        word_lookup = self.table.get_item(
            Key={'alpha': word}
            )
        
        self.logger.info('retrieved data for "%s": %s', word, word_lookup)
        
        if 'Item' in word_lookup and len(word_lookup['Item']) == 2:
            word_lookup = {
                'anagram': word_lookup['Item']['words']
            }
        
        self.logger.info('retrieved anagrams for "%s": %s', word, word_lookup)
        
        return word_lookup['anagram'] if (word_lookup and 'anagram' in word_lookup) else False

def anagrams_handler(event, context=False):

    anagrams = AnagramHandler(event, context)
    return anagrams.anagrams
