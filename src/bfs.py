# iterate each pre-filtered company and test if they are alone
# TODO: compute distance matix to save time for other tests.
def filter_on_similarity(_df, _model, thres=0.5, cluster_size=20):
    # construct graph using adj. list represented by dict
    graph = {}
    df_idx = _df.index.values.tolist()
    for i in df_idx:
        for j in df_idx:
            if i == j:
                continue
            dist = _model.sv.similarity(i, j)
            if dist >= thres:
                if i in graph:
                    graph[i].add(j)
                else:
                    graph[i] = {j}
                    
    # Spit out groups from the largest group without duplication
    # Greedy BFS (Bredth First Search)
    print('BFSing ...')
    helper = []
    for k, v in graph.items():
        helper.append((k, len(v)))
    helper = sorted(helper, key=lambda x: x[1], reverse=True)
    
    result = []
    for entry in helper:
        idx = entry[0]
        if idx not in graph:
            continue
        tmp = {idx}
        for org in graph[idx]:
            if org in graph:
                tmp.add(org)
                del graph[org]
        del graph[idx]
        if len(tmp) > cluster_size:
            result.append(tmp)
    
    return result