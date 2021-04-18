from subprocess import Popen

def load_jupyter_server_extension(nbapp):
    """serve the epl_discipline_app directory with bokeh server"""
    Popen(["bokeh", "serve", "epl_discipline_app", "--allow-websocket-origin=*"])