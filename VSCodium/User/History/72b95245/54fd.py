
def build_line(tag):

    def add_tag(msg):
        print(f'<{tag}>{msg}</{tag}>')

    return add_tag

tag1 = build_line("h2")
print(tag1)
tag1('onely')
tag1('killerone')