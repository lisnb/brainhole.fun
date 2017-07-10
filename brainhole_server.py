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
  os.path.dirname((os.path.abspath(__file__)))), 'brainhole.fun')

POSTS_ROOT = os.path.join(BRAINHOLE_DOT_FUN_ROOT, '_posts')
print POSTS_ROOT

post = form.Form(
  form.Textbox('file_name', form.Validator('Must be more than 5', lambda x:' ' not in x and '"' not in x)),
  form.Textbox('title'),
  form.Textbox('author'),
  form.Textarea('content')
)

render = web.template.render('./templates')

def create_post(file_name, title, author, content):
  try:
    now = datetime.now()
    file_name = '{}-{}.md'.format(now.strftime('%Y-%m-%d'), '-'.join(file_name.split()))
    file_path = os.path.join(POSTS_ROOT, file_name)
    
    header = {
      'title': 'title: "%s"' % title.replace('"', '#'),
      'author': 'author: %s' % author,
      'via': 'via: %s' % u'网页版',
      'date': 'date: %s ' % now.strftime('%Y-%m-%d %X +0800'),
      'layout': 'layout: %s' % 'post',
    }
    print file_path
    with open(file_path, 'wt') as f:
      lines = [
        '---',
        '\n'.join(header.values()),
        '---',
        '\n',
        '\n\n'.join(content.splitlines())
      ]
      print lines
      f.write(('\n'.join(lines).encode('utf8')))
    return 0, None
  except Exception as ex:
    return -1, 'create post failed'

def commit_post(file_name, title, author, content):
  code, err = create_post(file_name, title, author, content)
  if err:
    return code, err
  commands = [
    ('cd', BRAINHOLE_DOT_FUN_ROOT),
    ('git', 'add', '.'),
    ('git', 'commit', '-m', '"add %s.md"'%file_name),
    ('git', 'push', 'origin', 'gh-pages:gh-pages')
  ]
  command_line = ';'.join(' '.join(command) for command in commands)
  print command_line
  return_code = os.system(command_line)
  if return_code != 0 :
    return return_code, 'git failed'
  return 0, 'success'


class index:
  def GET(self):
    return 'hello world'

class publish:
  def GET(self):
    post_form = post()
    return render.post(post_form)
  def POST(self):
    posted_form = post()
    if posted_form.validates():
      code, err = commit_post(**posted_form.d)
      if code != 0:
        return 'failed: %s %s' % (code, err)
    # print posted_form.d
      return 'success'
    return 'not validated'

if __name__ == '__main__':
  app = web.application(urls, globals())
  app.run()
