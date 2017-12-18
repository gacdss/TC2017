#!/usr/bin/env python
'''Populate DynamoDB for anagram search'''

import boto3
import os

class AnagramDynamoDBPopulate(object):

    def __init__(self):
        self.conn = boto3.client('dynamodb')

    def dynamodb_populate(self):

        anagrams = {}

        if os.path.isfile('words.txt'):
            wordlist = open('words.txt', 'rb').read().lower()
            for word in set([a.strip() for a in wordlist.split("\n")]):
                if "'" in word:
                    continue
                word_sorted = (''.join(sorted(word))).strip()
                if word_sorted not in anagrams:
                    anagrams[word_sorted] = []
                anagrams[word_sorted].append(word)

            item_count = len(anagrams)
            ctr = 0
            
            for cache_result in anagrams:
                ctr += 1
                if len(anagrams[cache_result]) < 2:
                    continue

                anagram_attribute = ', '.join(anagrams[cache_result])
                if anagram_attribute == '':
                    continue
                
                self.conn.put_item(
                    TableName='anagram_words',
                    Item={'alpha':{'S':cache_result},'words':{'S':anagram_attribute}}
                    )
                print " {} / {}       \r".format(ctr, item_count),
            print " {} / {}       \r".format(ctr, item_count)
            

if __name__ == '__main__':
    sdb = AnagramDynamoDBPopulate()
    sdb.dynamodb_populate()
