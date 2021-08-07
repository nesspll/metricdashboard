import logging

from flask import Flask, render_template, request, jsonify, Blueprint
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask_prometheus_metrics import register_metrics
from jaeger_client import Config
from flask_opentracing import FlaskTracing


CONFIG = {"version": "v0.1.2", "config": "staging"}
MAIN = Blueprint("main", __name__)


@MAIN.route('/')
def homepage():
    return render_template("main.html")
    homepages = []
    res = requests.get('https://jobs.github.com/positions.json?description=python')
    for result in res.json():
        try:
            homepages.append(requests.get(result['company_url']))
        except:
            return "Unable to get site for %s" % result['company']
        


    return jsonify(homepages)

def register_blueprints(app):
    """
    Register blueprints to the app
    """
    app.register_blueprint(MAIN)


def create_app(config):
    """
    Application factory
    """
    app = Flask(__name__)
    register_blueprints(app)
    register_metrics(app, app_version=config["version"], app_config=config["config"])

    config = Config(
        config={
            'sampler':
                {'type': 'const',
                 'param': 1},
            'logging': True,
            'reporter_batch_size': 1, },
        service_name="service-trial")
    jaeger_tracer = config.initialize_tracer()
    tracing = FlaskTracing(jaeger_tracer, True, app)

    return app


#
# Dispatcher
#


def create_dispatcher() -> DispatcherMiddleware:
    """
    App factory for dispatcher middleware managing multiple WSGI apps
    """
    main_app = create_app(config=CONFIG)
    return DispatcherMiddleware(main_app.wsgi_app, {"/metrics": make_wsgi_app()})


#
# Run
#

if __name__ == "__main__":
    app = run_simple(
        hostname="0.0.0.0",
        port=5000,
        application=create_dispatcher(),
        use_reloader=True,
        use_debugger=True,
        use_evalex=True,
        threaded=True,
    )