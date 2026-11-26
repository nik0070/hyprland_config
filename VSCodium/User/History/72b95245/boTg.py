
def build_line(tag):

    def add_tag(msg):
        
        def add_more(non):
            print(f'<{tag}>{msg}</{tag}> |||| {non}')

        return add_more
    return add_tag

tag1 = build_line("h2")
print(tag1)
tag1('onely')
tag1('killerone')
build_line("h1")("testing")("non_test")