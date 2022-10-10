import re


class Markdown:

    title_ptn = re.compile(r'---\n(.*?)\n---', re.S)
    h_ptn = re.compile(r'(#{1,6}) (.*)?')
    b_ptn1 = re.compile(r'\*\*(.*?)\*\*')
    b_ptn2 = re.compile(r'\_\_(.*?)\_\_')
    i_ptn1 = re.compile(r'\*(.*?)\*')
    i_ptn2 = re.compile(r'\_(.*?)\_')

    del_ptn = re.compile(r'~~(.*?)~~')

    code_ptn = re.compile(r'\`(.*?)\`')

    hr_ptn1 = re.compile(r'\s*\*\s*\*\s*\*\s*')
    hr_ptn2 = re.compile(r'[\s\*]')

    a_ptn = re.compile(r'\[(.*?)\]\((.*?)\)')

    def __init__(self, path):
        with open(path, 'r', encoding='utf8') as f:
            self.data = f.read()
        self.settings = {}

    def title_repl(self, data):
        self.settings.update({
            t.split(':')[0]: t.split(':')[1]
            for t in data.group(1).split('\n')
        })
        return ''

    def pop_settings(self):
        self.data = self.title_ptn.sub(self.title_repl, self.data)
        return self.settings

    def repl_h(self, data):
        h, content = data.groups()
        return f'<h{len(h)}>{content}</h{len(h)}>'

    def repl_b(self, data):
        return f'<b>{data.group(1)}</b>'

    def repl_i(self, data):
        return f'<i>{data.group(1)}</i>'

    def repl_a(self, data):
        return f'<a href="{data.group(2)}">{data.group(1)}</a>'

    def repl_del(self, data):
        return f'<del>{data.group(1)}</del>'

    def repl_code(self, data):
        return f'<code>{data.group(1)}</code>'

    def repl_hr(self, line):
        if self.hr_ptn1.match(line) and not self.hr_ptn2.search(line):
            return '<hr>'
        return line

    def to_html(self):
        content = ''
        for line in self.data.split('\n'):

            line = self.b_ptn1.sub(self.repl_b, line)
            line = self.b_ptn2.sub(self.repl_b, line)
            line = self.i_ptn1.sub(self.repl_i, line)
            line = self.i_ptn2.sub(self.repl_i, line)
            line = self.del_ptn.sub(self.repl_del, line)
            line = self.h_ptn.sub(self.repl_h, line)
            line = self.a_ptn.sub(self.repl_a, line)
            line = self.code_ptn.sub(self.repl_code, line)
            line = self.repl_hr(line)
            if line.endswith('  '):
                line += '<br>'
            if not line:
                line = '<br>'
            line = line.strip()
            content += line
        return content

    def parse(self):
        settings = self.pop_settings()
        content = self.to_html()

        return {
            'settings': settings,
            'content': content
        }
