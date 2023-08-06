import json
import os
import argparse
import pya0
from .mindex_info import list_indexes
from .eval import run_topics
from .msearch import msearch


def abort_on_network_index(index):
    if isinstance(index, str):
        print('Abort on network index')
        exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Conduct math-aware search using Approach0 search engine')

    parser.add_argument('--query', type=str, required=False, nargs='+',
        help="Mixed type of keywords, math keywords are written in TeX and wrapped up in dollars")
    parser.add_argument('--docid', type=int, required=False,
        help="Lookup a raw document from index")
    parser.add_argument('--index', type=str, required=False,
        help="Open index at specified path, a prebuilt index name, or a searchd Web API" +
             " (e.g., http://localhost:8921/search)")
    parser.add_argument('--topk', type=int, required=False,
        help="Keep at most top-K hits in results")
    parser.add_argument('--trec-output', type=str, required=False,
        help="Output TREC-format results")
    parser.add_argument('--verbose', required=False, action='store_true',
        help="Verbose output (showing query structures and merge times)")
    parser.add_argument('--use-fallback-parser', required=False, action='store_true',
        help="Use fallback LaTeXML parser for parsing TeX")
    parser.add_argument('--print-index-stats', required=False,
        action='store_true', help="Print index statistics and abort")
    parser.add_argument('--list-prebuilt-indexes', required=False,
        action='store_true', help="List available prebuilt math indexes and abort")
    parser.add_argument('--run-topics', type=str, required=False,
        help="Generate TREC output using specified collection qrels/topics")
    parser.add_argument('--eval-args', type=str, required=False,
        help="Passing extra command line arguments to trec_eval. E.g., '-q -m map -m P.30'")

    args = parser.parse_args()

    # list prebuilt indexes?
    if (args.list_prebuilt_indexes):
        list_indexes()
        exit(0)

    # open index from specified index path or prebuilt index
    if args.index is None:
        print('no index specified, abort.')
        exit(0)

    elif isinstance(args.index, str) and args.index.startswith('http'):
        index = args.index
        pass

    elif not os.path.exists(args.index):
        index_path = pya0.from_prebuilt_index(args.index)
        if index_path is None: # if index name is not registered
            exit(1)
        index = pya0.index_open(index_path, option="r")
    else:
        index_path = args.index
        index = pya0.index_open(index_path, option="r")

    if index is None:
        print(f'index open failed: {index_path}')
        exit(1)

    # enable fallback parser?
    if args.use_fallback_parser:
        print('use fallback parser.')
        pya0.use_fallback_parser(True)

    # print index stats if requested
    if args.print_index_stats:
        abort_on_network_index(index)
        print(f' --- index stats ({args.index}) ---')
        pya0.index_print_summary(index)
        exit(0)

    # overwrite default arguments for running searcher
    verbose = args.verbose if args.verbose else False
    topk = args.topk if args.topk else 20
    trec_output = args.trec_output if args.trec_output else '/dev/null'

    if args.query:
        # parser query by different types
        query = []
        for kw in args.query:
            kw_type = 'term'
            if kw.startswith('$'):
                kw = kw.strip('$')
                kw_type = 'tex'
            query.append({
                'keyword': kw,
                'type': kw_type
            })
        if verbose:
            print('[query] ', query)

        # actually run query
        results = msearch(index, query,
            verbose=verbose,
            topk=topk
        )

        # handle results
        if results['ret_code'] == 0: # successful
            hits = results['hits']
        else:
            print(results['ret_str'])
            exit(1)

        for hit in hits:
            print(hit)

    elif args.docid:
        abort_on_network_index(index)
        url, contents = pya0.index_lookup_doc(index, args.docid)
        print(url, end="\n\n")
        print(contents)

    elif args.run_topics:
        if args.trec_output is None:
            print('Error: Must specify a TREC output file to run topics')
            exit(1)

        run_topics(index, args.run_topics,
            output=trec_output,
            topk=topk,
            verbose=verbose,
            trec_eval_args=args.eval_args
        )

    else:
        print('no docid, query or evaluating collection specifed, abort.')
        exit(0)
