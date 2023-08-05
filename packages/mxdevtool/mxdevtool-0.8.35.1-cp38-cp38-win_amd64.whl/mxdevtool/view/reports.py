import mxdevtool as mx
import mxdevtool.xenarix as xen
import pandas as pd

import os

def report_scen_html(scen: xen.Scenario, **kwargs):
    # corr
    # timegrid
    # rsg
    # filename

    # show = kwargs.get('show')

    import webbrowser
    from jinja2 import Template

    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ name }}</title>
    </head>
    <body>
        <h1>Scenario Summary</h1>
        <p>models : {{ models_num }} - {{ model_names }}</p>
        <p>calcs : {{ calcs_num }} - {{ calc_names }}</p>
        <p>corr : {{ corr }}</p>
        <p>timegrid : {{ timegrid_items }}</p>
        <p>filename : {{ scen.filename }}</p>
        <p>ismomentmatch : {{ scen.isMomentMatching }}</p>
    </body>
    </html>
    '''

    if kwargs.get('html_template') != None:
        html_template = kwargs.get('html_template')

    model_names = [m.name for m in scen.models]
    calc_names = [c.name for c in scen.calcs]
    corr_df = pd.DataFrame(scen.corr.toList(), index=model_names, columns=model_names)

    tg = scen.timegrid

    data = {
        'name': 'Scenario Summary',
        'scen': scen,
        'models_num': len(scen.models),
        'calcs_num': len(scen.calcs),
        'corr': corr_df.to_html(),
        'model_names': model_names,
        'calc_names': calc_names,
        'timegrid_items': [type(tg).__name__, tg._refDate, len(tg), tg.times()]
    }

    template = Template(html_template)

    filename = 'scen.html'
    f = open(filename, 'w')
    f.write(template.render(data))
    f.close()

    if kwargs.get('browser_isopen') is True:
        webbrowser.open('file://' + os.path.realpath(filename))


def report_scen(scen: xen.Scenario, **kwargs):
    if kwargs.get('typ') == 'html':
        report_scen_html(scen, **kwargs)
    else: # default
        report_scen_html(scen, **kwargs)


