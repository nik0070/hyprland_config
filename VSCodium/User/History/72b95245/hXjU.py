
def build_line(msg):

    def add_tag(tag, msg):
        print(f'<{tag}>{msg}</{tag}>')

    return add_tag

tag1 = build_line("h1")
