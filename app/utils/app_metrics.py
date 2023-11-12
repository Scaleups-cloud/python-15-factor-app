from prometheus_flask_exporter import PrometheusMetrics

def setup_metrics(app):
    """
    Sets up Prometheus metrics for a Flask application.
    """
    metrics = PrometheusMetrics(app, group_by='endpoint')

    @app.route('/metrics')
    def metrics_route():
        return metrics

    return metrics