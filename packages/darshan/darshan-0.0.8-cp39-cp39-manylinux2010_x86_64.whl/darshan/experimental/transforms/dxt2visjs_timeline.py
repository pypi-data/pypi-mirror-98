##!/usr/bin/env python3
## -*- coding: utf-8 -*-
#
#import os
#import sys
#import re
#import json
#import argparse
#
#import pprint
#import bisect
#import datetime
#
#from operator import itemgetter
#
#import darshan_dxt_timeline.dxt_parser as dxt_parser
#import darshan_dxt_timeline.dxt_visualize as dxt_visualize
#
#
#def generate_groups_and_items(data, files, ranks, images=False, path="./", modes=None):
#    #print(files)
#
#    groups = []
#    items = []
#
#    for fileid in files:
#        cur = files[fileid]
#        #pprint.pprint(cur, depth=3)
#        #print()
#
#        nested_groups = []
#      
#        summary_item = {
#                'id': str(fileid),
#                'group': str(fileid),
#                #'content': str(fileid),
#                'content': '',
#
#                'start': float('inf'),
#                'end':   float('-inf'),
#                }
#
#
#
#        for rankid in cur['ranks']:
#            #print(rankid)
#            rank = cur['ranks'][rankid]
#            rgid = str(fileid) + ':' + rankid
#
#
#            trace = rank['trace']
#            splitlist = lambda A, n=5: [A[i:i+n] for i in range(0, len(A), n)]
#            trace = splitlist(trace)
#            trace = sorted(trace, key=itemgetter(3))
#            flatten = lambda l: [item for sublist in l for item in sublist]
#            trace = flatten(trace)
#			
#
#            nested_groups.append(rgid)
#            rankgroup = {
#                'id': rgid,
#                'content': rankid,
#                }
#            groups.append(rankgroup)
#
#            # add item
#            start = data['start_time'] + datetime.timedelta(seconds=float(rank['start']))
#            end = data['start_time'] + datetime.timedelta(seconds=float(rank['end']))
#
#            if summary_item['start'] > rank['start']:
#                summary_item['start'] = rank['start']
#
#            if summary_item['end'] < rank['end']:
#                summary_item['end'] = rank['end']
#
#            item = {
#                'id': rgid,
#                'group': rgid,
#                #'content': rgid,
#
#                'start': start.isoformat(),
#                'end':   end.isoformat(),
#                'data': {
#                    'duration': (end-start).total_seconds(),
#                    'start': float(rank['start']),
#                    'size': cur['minsize'],
#                    #'trace': rank['trace'],
#                    'trace': trace
#                    },
#                }
#            items.append(item)
#
#            #if fileid == "15202353719065296799":
#            #   # TODO: remove again (generates images)
#            if images:
#                dxt_visualize.visualize({'rankid': cur['ranks'][rankid]['rankid'], 'minsize': cur['minsize'], 'cur': cur}, modes=modes, path=path)
#          
#
#        filegroup = {
#            'id': str(fileid),
#            'content': '%s [%dR %dMiB]' % (cur['filename'][-42:], len(cur['ranks'].keys()), cur['minsize']/1024/1024),
#            #'order': '%s [%dR %dMiB]' % (cur['filename'], len(cur['ranks'].keys()), cur['minsize']/1024/1024),
#            'order': float(rank['start']),
#            'showNested': False,
#            'nestedGroups': nested_groups,
#            }
#        groups.append(filegroup)
#
#
#        # add summary item
#        summary_item['data'] = item['data'] # TODO: switch for more sensitive default then simply last
#
#        summary_item['start'] = data['start_time'] + datetime.timedelta(seconds=float(summary_item['start']))
#        summary_item['end'] = data['start_time'] + datetime.timedelta(seconds=float(summary_item['end']))
#
#        summary_item['start'] = summary_item['start'].isoformat()
#        summary_item['end'] = summary_item['end'].isoformat()
#        items.append(summary_item)
#
#
#    return groups, items
#
#
#
#
#
#
#
#
#
#def generate_groups_and_items2(report, images=False, path="./", modes=None):
#    #print(files)
#
#    groups = []
#    items = []
#
#    for fileid in files:
#        cur = files[fileid]
#        #pprint.pprint(cur, depth=3)
#        #print()
#
#        nested_groups = []
#      
#        summary_item = {
#                'id': str(fileid),
#                'group': str(fileid),
#                #'content': str(fileid),
#                'content': '',
#
#                'start': float('inf'),
#                'end':   float('-inf'),
#                }
#
#
#
#        for rankid in cur['ranks']:
#            #print(rankid)
#            rank = cur['ranks'][rankid]
#            rgid = str(fileid) + ':' + rankid
#
#
#            trace = rank['trace']
#            splitlist = lambda A, n=5: [A[i:i+n] for i in range(0, len(A), n)]
#            trace = splitlist(trace)
#            trace = sorted(trace, key=itemgetter(3))
#            flatten = lambda l: [item for sublist in l for item in sublist]
#            trace = flatten(trace)
#			
#
#            nested_groups.append(rgid)
#            rankgroup = {
#                'id': rgid,
#                'content': rankid,
#                }
#            groups.append(rankgroup)
#
#            # add item
#            start = data['start_time'] + datetime.timedelta(seconds=float(rank['start']))
#            end = data['start_time'] + datetime.timedelta(seconds=float(rank['end']))
#
#            if summary_item['start'] > rank['start']:
#                summary_item['start'] = rank['start']
#
#            if summary_item['end'] < rank['end']:
#                summary_item['end'] = rank['end']
#
#            item = {
#                'id': rgid,
#                'group': rgid,
#                #'content': rgid,
#
#                'start': start.isoformat(),
#                'end':   end.isoformat(),
#                'data': {
#                    'duration': (end-start).total_seconds(),
#                    'start': float(rank['start']),
#                    'size': cur['minsize'],
#                    #'trace': rank['trace'],
#                    'trace': trace
#                    },
#                }
#            items.append(item)
#
#            #if fileid == "15202353719065296799":
#            #   # TODO: remove again (generates images)
#            if images:
#                dxt_visualize.visualize({'rankid': cur['ranks'][rankid]['rankid'], 'minsize': cur['minsize'], 'cur': cur}, modes=modes, path=path)
#          
#
#        filegroup = {
#            'id': str(fileid),
#            'content': '%s [%dR %dMiB]' % (cur['filename'][-42:], len(cur['ranks'].keys()), cur['minsize']/1024/1024),
#            #'order': '%s [%dR %dMiB]' % (cur['filename'], len(cur['ranks'].keys()), cur['minsize']/1024/1024),
#            'order': float(rank['start']),
#            'showNested': False,
#            'nestedGroups': nested_groups,
#            }
#        groups.append(filegroup)
#
#
#        # add summary item
#        summary_item['data'] = item['data'] # TODO: switch for more sensitive default then simply last
#
#        summary_item['start'] = data['start_time'] + datetime.timedelta(seconds=float(summary_item['start']))
#        summary_item['end'] = data['start_time'] + datetime.timedelta(seconds=float(summary_item['end']))
#
#        summary_item['start'] = summary_item['start'].isoformat()
#        summary_item['end'] = summary_item['end'].isoformat()
#        items.append(summary_item)
#
#
#    return groups, items
#
#
#
#
#
#
#
#
#
#
#def main():
#    parser = argparse.ArgumentParser(description='')
#
#    #parser.add_argument('arg1', help='a mendatory argument', nargs='?')
#    parser.add_argument('input', help='inputfile', nargs='?', default='example.darshan')
#    parser.add_argument('--output', help='outfile?', nargs='?', default='example.output')
#    parser.add_argument('--input-format', help='', choices=["darshan", "ascii"], default="darshan")
#    parser.add_argument('--verbose', help='', action='store_true')
#    parser.add_argument('--option', help='', choices=["json", "js", "xml"], default="json")
#
#    parser.add_argument('--output-js', nargs='?', default='output-dxt-timeline-groups.js')
#    parser.add_argument('--output-json', nargs='?', default='output-dxt-timeline-groups.js')
#
#    parser.add_argument('--export-json', help='', action='store_true')
#    parser.add_argument('--export-js', help='', action='store_true')
#    
#
#    parser.add_argument('--export-png', help='', action='store_true', default=False)
#    parser.add_argument('--export-png-path', nargs='?', default='./generated-png/')
#
#    parser.add_argument('--add-mode', action='append')
#
#
#
#    args = parser.parse_args()
#    print(args)
#
#    
#    if args.add_mode is None:
#        args.add_mode = ['wallclock', 'segment'] 
#
#	
#    raw = dxt_parser.load_dxt(args.input)
#
#    # ensure output directory exists
#    directory = args.export_png_path
#    if not os.path.exists(directory):
#        os.makedirs(directory)
#
#    # parse and process input
#    data, files, ranks = dxt_parser.parse(raw)
#    groups, items = generate_groups_and_items(data, files, ranks, images=args.export_png, path=args.export_png_path, modes=args.add_mode)
#
#
#    print("Files: ", len(files))
#
#    print("Ranks:")
#    print(list(ranks))
#
#    print("\nMetadata:")
#    pprint.pprint(data)
#    timeline = {'groups': groups, 'items': items}
#
#
#
#    if args.export_js:
#        outfile = args.output_js
#        out = open(outfile, "w")
#        out.write("timelines.push(%s);" % (json.dumps(timeline, indent=1)))
#
#    if args.export_json:
#        outfile = args.output_json
#        out = open(outfile, "w")
#        out.write("%s" % (json.dumps(timeline, indent=1)))
#
#
#    
#
#
#
#
#if __name__ == '__main__':
#    main()
#
## vim: set filetype=python:
