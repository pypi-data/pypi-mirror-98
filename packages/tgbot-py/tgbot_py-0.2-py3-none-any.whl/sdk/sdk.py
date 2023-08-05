from datetime import datetime
import json

from opentracing.propagation import Format
from opentracing_instrumentation import request_context
from jaeger_client import tracer
import requests


class SDK:
    """
    SDK to telegram bot service instance.
    """

    def __init__(self, base_url: str, tr: tracer):
        """
        :param base_url: url of telegram bot service.
        :param tr: jaeger open tracer.
        """

        self._base_url = base_url
        self._tracer = tr

    def send(self, time: datetime, lvl: str, msg: str) -> requests.Response:
        """
        Sending event via telegram bot.
        :param time: time creation event.
        :param lvl: level event.
        :param msg: payload of event message.
        :return: response of the query.
        """

        headers = {
            'Content-Type': 'application/json'
        }

        request = {
            'time': time.isoformat() + 'Z',
            'level': lvl,
            'message': msg,
        }

        with self._before_http_request(current_span_extractor=request_context.get_current_span, operation_name='tgbot',
                                       headers=headers):
            response = requests.post("http://" + self._base_url + '/notify', data=json.dumps(request), headers=headers)

            return response

    def _before_http_request(self, current_span_extractor, operation_name: str, headers: dict):
        parent_span = current_span_extractor()
        outbound_span = self._tracer.start_span(
            operation_name=operation_name,
            child_of=parent_span
        )

        http_header_carrier = {}
        self._tracer.inject(
            span_context=outbound_span,
            format=Format.HTTP_HEADERS,
            carrier=http_header_carrier)

        for key, value in http_header_carrier.items():
            headers[key] = value

        return outbound_span
