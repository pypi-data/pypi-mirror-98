from tabulate import tabulate

from omg.common.helper import age


# Simple out put with just name and age
def ev_out(t, ns, res, output, show_type):
    output_res=[[]]
    # header
    if ns == '_all':
        output_res[0].append('NAMESPACE')
    output_res[0].extend(['LAST SEEN','TYPE','REASON','OBJECT','MESSAGE'])
    # resources
    for r in res:
        ev = r['res']
        row = []
        # namespace (for --all-namespaces)
        if ns == '_all':
            row.append(ev['metadata']['namespace'])

        # last
        last_ts = str(ev['lastTimestamp'])
        gen_ts = r['gen_ts']
        row.append(age(last_ts,gen_ts))
        # type
        if 'type' in ev:
            row.append(ev['type'])
        else:
            row.append('')
        # reason
        if 'reason' in ev:
            row.append(ev['reason'])
        else:
            row.append('')
        # object
        if ( 'involvedObject' in ev
        and 'kind' in ev['involvedObject']
        and 'name' in ev['involvedObject'] ):
            inv_obj = ev['involvedObject']
            row.append(
                inv_obj['kind'].lower() + '/' + inv_obj['name']
            )
        else:
            row.append('<none>')
        # message
        row.append(ev['message'])

        output_res.append(row)

    print(tabulate(output_res,tablefmt="plain"))
