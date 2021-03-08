import jinja2
import os
from quart import Quart, redirect, request, url_for
from util.stat import process_all

template_folder = os.path.join(os.path.dirname(__file__), 'template')
env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_folder), enable_async=True)

pic_path = {}

async def render_template(template,**kwargs):
    t = env.get_template(template)
    return await t.render_async(**kwargs)

app = Quart(__name__, static_folder = './data')

@app.route('/',methods=['GET','POST'])
async def input():
    if request.method == 'GET':
        return await render_template('input.html')
    else:
        form = await request.form
        song_list_id = int(form['song_list_id'])
        pic_list = process_all(int(song_list_id))
        if isinstance(pic_list, int):
            return await render_template('error.html', code = pic_list)
        else:
            pic_path[song_list_id] = pic_list
            return redirect(url_for('show_result', id = song_list_id))

@app.route('/result/?<int:id>')
async def show_result(id):
    fpath = pic_path[id]
    rel = [url_for('static', filename = fname) for fname in fpath]
    return await render_template('result.html', id = id, filepath = rel)

app.run(host = '0.0.0.0')