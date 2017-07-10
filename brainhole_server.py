# coding:utf8

import web
from web import form
import os
import sys
from datetime import datetime

urls = (
    '/', 'index',
    '/publish', 'publish',
)

BRAINHOLE_DOT_FUN_ROOT = os.path.join(os.path.dirname(
    os.path.dirname(os.curdir)), 'brainhole.fun')

POSTS_ROOT = os.path.join(BRAINHOLE_DOT_RUN_ROOT, '_posts')

post = form.Form(
  form.Textbox('file_name'),
  form.Textbox('title'),
  form.Textbox('author'),
  form.Textarea('content')
)

render = web.template.render('./templates')

def create_post(file_name, title, author, content):
  now = datetime.now()
  file_name = '{}-{}.md'.format(now.strftime('%Y-%m-%d'), file_name)
  file_path = os.path.join(POSTS_ROOT, file_name)

  header_title = title
  header_
  header_date = now.strftime('%Y-%m-%d %X +0800')

  with open(file_path, 'wt') as f:




class index:
  def GET(self):
    return 'hello world'

class publish:
  def GET(self):
    post_form = post()
    return render.post(post_form)
  def POST(self):
    posted_form = post()
    # if posted_form.validates():
      # pass
    print posted_form.d
    return 'hello world'

if __name__ == '__main__':
  app = web.application(urls, globals())
  app.run()
