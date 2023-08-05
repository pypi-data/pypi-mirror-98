from tabulate import tabulate

from omg.common.helper import age


def bc_out(t, ns, res, output, show_type):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    output_res[0].extend(['NAME','TYPE','FROM','LATEST'])
    # resources
    for r in res:
        bc = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(bc['metadata']['namespace'])
        # name
        if show_type:
            row.append(t + '/' + bc['metadata']['name'])
        else:
            row.append(bc['metadata']['name'])
        # type
        try:
            row.append(bc['spec']['strategy']['type'])
        except:
            row.append('??')
        # from
        try:
            row.append(bc['spec']['source']['type'])
        except:
            row.append('??')
        # latest
        try:
            row.append(bc['status']['lastVersion'])
        except:
            row.append('??')
        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
