from kama_sdk.core.core import prom_api_client
from kama_sdk.model.supplier.ext.prometheus.prometheus_supplier import PrometheusSupplier


class PrometheusScalarSupplier(PrometheusSupplier):

  def _compute(self):
    raw = prom_api_client.compute_instant(self.query_expr, self.tn)
    result = self.extract_datapoints(raw)
    if result:
      return float(result[0]['value'][1])
    else:
      return None
