import re


class Markdown:

    title_pattern = re.compile(r'---\n(.*?)\n---', re.S)

    def __init__(self, path):
        with open(path, 'r') as f:
            self.data = f.read()
        self.settings = {}

    def title_repl(self, data):
        self.settings.update({
            t.split(':')[0]: t.split(':')[1]
            for t in data.group(1).split('\n')
        })
        return ''

    def pop_settings(self):
        self.data = self.title_pattern.sub(self.title_repl, self.data)
        return self.settings

    def repl_h1(self, data):

        return '<h1>' + data.group(1) + '</h1>'

    def to_html(self):
        content = ''
        for line in self.data.split('\n'):
            line = re.sub('# (.*)?', self.repl_h1, line)
            content += line
        return content

    def parse(self):
        settings = self.pop_settings()
        content = self.to_html()

        return {
            'settings': settings,
            'content': content
        }
