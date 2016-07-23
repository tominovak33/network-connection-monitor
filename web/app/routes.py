import handlers

ROUTES = [
    ('/', handlers.HomeHandler),
    ('/status', handlers.StatusHandler),
    ('/(.*)', handlers.NotFoundHandler),
]
