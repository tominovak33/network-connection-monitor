import templates


# merge 2 dictionaries into one
def merge(a, b):
    a.update(b)
    return a


# wrapper around merge to allow for more than two dictionaries
def merge_many(*arguments):
    res = {}
    for argument in arguments:
        res = merge(res, argument)

    return res


def throw404(self):
    self.error(404)
    templates.render_page("errors/404", {}, self)
