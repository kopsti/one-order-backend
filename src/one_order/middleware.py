import logging
import socket
import time

logger = logging.getLogger('requests')


class RequestLogMiddleware(object):

    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):

        if request.method == 'GET':
            log_data = {
                'user': request.user.pk,
                'remote_address': request.META['REMOTE_ADDR'],
                'server_hostname': socket.gethostname(),
                'request_method': request.method,
                'request_path': request.get_full_path(),
                'request_body': request.body,
                'response_status': response.status_code,
                'response_body': response.content,
                'run_time': time.time() - request.start_time,
            }
        else:
            log_data = {
                'user': request.user.pk,
                'remote_address': request.META['REMOTE_ADDR'],
                'server_hostname': socket.gethostname(),
                'request_method': request.method,
                'request_path': request.get_full_path(),
                'response_status': response.status_code,
                'response_body': response.content,
                'run_time': time.time() - request.start_time,
            }

        logger.info(log_data)
        return response
