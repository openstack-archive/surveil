from pecan import make_app
# from pecanrest import model


def setup_app(config):

    # model.init_model()
    app_conf = dict(config.app)

    return make_app(
        app_conf.pop('root'),
        logging=getattr(config, 'logging', {}),
        **app_conf
    )
