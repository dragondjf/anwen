#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import yaml
import sys
import os
import re
sys.path.append('..')
from db import User, Share, Ande, Comment, Hit, Talk, Tag, Feedback, Room, VideoMsg  # todo
from bson import ObjectId


doc_list = ['User', 'Share', 'Comment', 'Ande', 'Hit', 'Talk', 'Tag', 'Feedback', 'Room', 'VideoMsg']


def make_doc():
    if os.path.isfile('Share.yaml'):
        docs = yaml.load(file('Share.yaml', 'r').read())
        for i in docs:
            filename = '../docs/shares/%s_%s.md' % (i['id'], i['slug'])
            title = i['title']
            markdown = i['markdown']
            filebody = '%s\n========\n\n\n%s' % (
                title, re.sub(r'\r\n', r'\n', markdown))
            with open(filename, 'w') as share:
                share.write(filebody)
        print 'shares are markdownd'


def run_import(name):
    if name == 'all':
        for doc in doc_list:
            doc_import(doc)
    elif name in doc_list:
        doc_import(name)


def doc_import(doc):
    d = eval(doc)
    if d.find().count() == 0:
        if doc == 'User' and not os.path.isfile(doc + '.yaml'):
            doc = '%sSafe' % doc
            print 'load usersafe'
        docs = yaml.load(file(doc + '.yaml', 'r').read())
        for i in docs:
            i['_id'] = ObjectId(i['_id'])
            if doc == 'UserSafe':
                i['user_email'] = ''
                i['user_pass'] = ''
            d.new(i)
        print '%s done' % doc


def run_export(name):
    if name == 'all':
        for doc in doc_list:
            doc_export(doc)
    elif name in doc_list:
        doc_export(name)
    if os.path.isfile('User.yaml'):
        input_file = open('User.yaml')
        output_file = open('UserSafe.yaml', 'w')
        a = re.sub(r'  user_pass: \S*\n', '', input_file.read())
        b = re.sub(r'  user_email: \S*\n', '', a)
        output_file.write(b)
        output_file.close()
        print 'users are safe'
    make_doc()


def doc_export(doc):
    d = eval(doc)
    obj = d.find()
    if obj.count() == 0:
        return
    res = []
    for i in obj:
        i['_id'] = str(i['_id'])
        i = convert(i)
        res.append(i)
    document = open(doc + '.yaml', 'w')
    yaml.dump(
        res, document,
        default_style=None, default_flow_style=False,
        canonical=False, indent=False, width=None,
        allow_unicode=True, line_break=None,
        encoding='utf-8', explicit_start=None, explicit_end=None,
        version=None, tags=None)


def convert(input):
    if isinstance(input, dict):
        return dict((convert(k), convert(v)) for k, v in input.iteritems())
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

parser = argparse.ArgumentParser(
    description='Anwen DB in or out')

parser.add_argument(
    '-i', '--in',
    dest='run_import',
    action='store_const',
    const=True,
    default=False,
    help='run import'
)

parser.add_argument(
    '-o', '--out',
    dest='run_export',
    action='store_const',
    const=True,
    default=False,
    help='run export'
)

parser.add_argument(
    '-d', '--doc',
    dest='make_doc',
    action='store_const',
    const=True,
    default=False,
    help='make doc'
)

parser.add_argument(
    '-n', '--name',
    dest='name',
    action='store',
    type=str,
    default='all',
    help='document name'
)

if __name__ == '__main__':
    args = parser.parse_args()
    if args.run_import:
        run_import(args.name)
    elif args.run_export:
        run_export(args.name)
    elif args.make_doc:
        make_doc()
