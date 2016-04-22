from payu import PayU as PayUBase

class PayU(PayUBase):

    def __init__(self, app, **config):
        super(PayU, self).__init__(**config)
        self.app = app
        if app is not None:
            self.init_app(app)


    def init_app(self, app):
        for key, value in self.app.config.items():
            if not key.startswith('PAYU_'):
                continue
            k = key.split('PAYU_')[-1]
            self.config[k] = value
