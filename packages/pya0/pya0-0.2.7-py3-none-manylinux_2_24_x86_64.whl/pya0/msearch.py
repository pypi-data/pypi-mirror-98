import pya0
import json
import requests

def send_json(url, obj, verbose=False):
    headers = {'content-type': 'application/json'}
    try:
        if verbose:
            print(f'[post] {obj} {url}')
        r = requests.post(url, json=obj, headers=headers)
        j = json.loads(r.content.decode('utf-8'))
        return j

    except Exception as e:
        print(e)
        exit(1)


def msearch(index, query, verbose=False, topk=1000):
    if isinstance(index, str):
        results = send_json(index, {
            "page": -1, # return results without paging
            "kw": [{"type": kw['type'], "str": kw['keyword']} for kw in query]
        }, verbose=verbose)

        ret_code = results['ret_code']
        ret_msg = results['ret_str']
        if ret_code == 0:
            hits = results['hits']
            results['hits'] = hits[:topk] # truncate results in cluster case
            if verbose: print(f'cluster returns {len(hits)} results in total')
        else:
            if verbose: print(f'cluster returns error: #{ret_code} ({ret_msg})')
    else:
        result_JSON = pya0.search(index, query,
            verbose=verbose,
            topk=topk)
        results = json.loads(result_JSON)
    return results
