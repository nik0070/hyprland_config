
def build_line(msg):

    def add_tag(msg):
        print(f'<{tag}>{msg}</{tag}>')

    return add_tag

tag1 = build_line("h2")
print(tag1)
out = tag1("good one")
print(out)