"""Client library for Direqt Ads API."""
import json
import logging
import uuid
import hashlib
import requests
import re

from util import detect_gae
from . import rbm

logger = logging.getLogger(__name__)

_DEFAULT_ENDPOINT = 'https://ads.direqt.io'
_DEFAULT_USER_AGENT = 'unknown'

_AD_FORMAT_RBM10 = 'RBMV1.0'
_AD_FORMAT_SMS = 'SMS'
_DEFAULT_AD_FORMAT = _AD_FORMAT_RBM10
_VALID_AD_FORMATS = [_AD_FORMAT_RBM10, _AD_FORMAT_SMS]

_DEFAULT_RBM_ENDPOINT = 'https://rcsbusinessmessaging.googleapis.com'


class DireqtClient(object):
    """Client for the Direqt ad server."""

    def __init__(self, api_key, ad_format=_DEFAULT_AD_FORMAT, user_agent=_DEFAULT_USER_AGENT, **kwargs):
        """Initializes a DireqtClient.

        Args:
            api_key: A string containing your Direqt API key.
            format: One of 'RBMV1.0' or 'SMS'
            user_agent: An arbitrary string containing only ASCII characters
                that will be used to identify your application. If not set,
                defaults to "unknown".
            **kwargs: Optional keyword arguments.

        Keyword Arguments:
            None defined.
        """
        super(DireqtClient, self).__init__()

        if ad_format not in _VALID_AD_FORMATS:
            raise NotImplementedError(
                'The provided ad format "%s" is invalid. Accepted formats are: %s'
                % (format, _VALID_AD_FORMATS))

        if detect_gae():
            import requests_toolbelt.adapters.appengine
            requests_toolbelt.adapters.appengine.monkeypatch()

        self.api_key = api_key
        self.fmt = ad_format
        self.user_agent = user_agent
        self.endpoint = kwargs.get('endpoint', _DEFAULT_ENDPOINT)               # private
        self.http = kwargs.get('http', requests)                                # private
        self.rbm_endpoint = kwargs.get('rbm_endpoint', _DEFAULT_RBM_ENDPOINT)   # private
        self.rbm_http = kwargs.get('rbm_http', rbm.http)

    def fetch(self, ad_unit, msisdn=None, subscriber_id=None,
              targeting=None, url_shortener=None, fetch_only=False):
        """Fetch an ad from the Direqt Ads API.

        If no ad is available, this method returns False.

        If the ad_format is "SMS", or `fetch_only` is True, this method will
        return an object containing the 'message_id' and 'payload' of the
        message that should be sent to the subscriber using the application's
        messaging platform.

        If the ad_format specified in the constructor was "RBMV1.0" this method
        will handle the sending of any messages necessary to deliver the
        advertisement (though see `fetch_only` parameter).

        Args:
            ad_unit: An ad unit code configured in your project.
            subscriber_id: A string identifying the current user. This identifier
                is used to track interactions with a given user, but is not
                otherwise interpreted.
            msisdn: The MSISDN of the user. This argument is only required when
                using RBM, and is ignored for the case of SMS.
            targeting: An array of tuples specifying name/value pairs for targeting
            url_shortener: A custom function to use for shortening marketing urls
                before embedding in messages. If specified, the default Direqt
                url shortener will not be used, and Direqt will not automatically
                truncate SMS messages to 160 characters.
            fetch_only: Specifies that this method should return the message
                payload to the caller rather than automatically send it to the
                subscriber. Note that any media files in the payload will still be
                uploaded automatically, and the corresponding URLs in the message
                payload fixed up as appropriate. This flag has no effect unless
                ad_format is "RBMv1.0".
        """
        targeting = targeting or {}

        if not msisdn and self.fmt != _AD_FORMAT_SMS:
            return self._process_error_result(self.ErrorCode.MISSING_REQUIRED_PARAMETER, "MSISDN is required for RBM message operations.")

        if not subscriber_id and msisdn:
            subscriber_id = hashlib.md5(self.api_key + msisdn).hexdigest()

        if not subscriber_id and not msisdn:
            return self._process_error_result(self.ErrorCode.MISSING_REQUIRED_PARAMETER, "Must specify at least one of (subscriber_id, msisdn).")

        params = {
            'key': self.api_key,
            'format': self.fmt,
            'adUnit': ad_unit,
            'subscriber': subscriber_id,
            'targeting': json.dumps(targeting)
        }

        if url_shortener:
            params['longUrl'] = 'true'

        url = self.endpoint + "/v1/fetch"
        response = self.http.post(url, params=params, data={})
        if response.status_code == 200:
            body = response.json()
            return self._process_fetch_result(msisdn, body, url_shortener, fetch_only)
        else:
            try:
                error_response = response.json()
                error_message = "Direqt fetch error: {0}".format(json.dumps(error_response))
                error = self._process_error_result(error_response['reasonCode'], error_response['description'])
            except:
                error_message = "Direqt fetch error: status_code={0} reason={1}".format(response.status_code, response.reason)
                status_code = self.ErrorCode.NO_AD_RETURNED

                if 500 <= response.status_code <= 599:
                    status_code = self.ErrorCode.RETRIABLE_ERROR

                error = self._process_error_result(status_code, response.reason)

            logger.debug(error_message)
            return error

    def notify_suggested_reply(self, msisdn, postback_data):
        """Notify of a suggested reply from a user.

        This method should be called whenever your agent is notified that a user
        has responded to a suggestion from an earlier message.

        Suggested replies are only relevant for ad_format "RBMV1.0".

        If the suggested reply was handled by Direqt, this method will return True.
        Otherwise, returns False.
        :type postback_data: str
        """
        if not postback_data or not postback_data.startswith('@direqt'):
            return False

        params = {
            'key': self.api_key,
            'format': self.fmt,
            'postbackData': postback_data
        }

        url = self.endpoint + "/v1/interact"
        response = self.http.post(url, params=params, data={})
        if response.status_code == 200:
            body = response.json()
            self._process_fetch_result(msisdn, body)    # return code ignored

        return True

    def track_custom_event(self, message_id, event_name, event_data):
        """Notify that a custom event has occurred.

        This method can be used to record custom events associated with the
        delivery of or interaction with a message that was received by fetch.
        For example, delivery and conversion notifications can be recorded with
        this method, allowing them to be visible in reports generated by the
        Direqt console.
        """
        params = {
            'key': self.api_key
        }
        data = {
            'messageId': message_id,
            'eventName': event_name,
            'eventData': event_data,
        }
        url = self.endpoint + "/v1/event"
        response = self.http.post(url, params=params, json=data)
        if response.status_code == 200:
            body = response.json()
        else:
            body = None

        return body

    def offline_conversion(self, message_id, event_data):
        """Notify that an offline conversion has occurred.

        This method can be used to record an offline conversion event
        associated with a message that was received by fetch.
        For example, conversion notifications can be recorded with
        this method when a tracking pixel is not an option, allowing
        them to be visible in reports generated by the Direqt console.

        If the conversion was handled by Direqt, this method will return True.
        Otherwise, returns False.
        """
        params = {
            'key': self.api_key
        }
        data = {
            'messageId': message_id,
            'eventName': "Conversion",
            'eventData': event_data,
        }
        url = self.endpoint + "/v1/event/offlineConversion"
        response = self.http.post(url, params=params, json=data)
        if response.status_code != 200:
            return False

        return True

    def _process_error_result(self, status, text):
        logger.debug('status={0} {1}'.format(status, text))
        error = {
            'error': {
                'status': status,
                'description': text
            }
        }
        return error

    def _process_fetch_result(self, msisdn, body, url_shortener=None, fetch_only=False):
        if self.fmt == _AD_FORMAT_SMS:
            payload = body['payload'] if 'payload' in body else None
            message_id = body['messageId'] if 'messageId' in body else None
            properties = body['properties'] if 'properties' in body else {}
            is_test = body['isTest'] if 'isTest' in body else False
            if not payload or not message_id:
                return self._process_error_result(self.ErrorCode.NO_AD_RETURNED, 'No ad returned')

            if url_shortener:
                match = re.search("(?P<url>https?://[^\s]+)", payload)
                url = match.group("url") if match else None
                if url:
                    new_url = url_shortener(url)
                    payload = payload.replace(url, new_url)

            response = {
                'payload': payload,
                'message_id': message_id,
                'properties': properties,
                'is_test': is_test
            }

            return response

        media = body['media'] if 'media' in body else []
        payload = body['payload'] if 'payload' in body else None
        message_id = body['messageId'] if 'messageId' in body else None
        properties = body['properties'] if 'properties' in body else {}
        is_test = body['isTest'] if 'isTest' in body else False

        if not media and not payload:
            return self._process_error_result(self.ErrorCode.OTHER, "Unexpected response from Direqt fetch.")

        logger.info("Received payload: " + (payload or '<none>'))

        for m in media:
            uri = self._upload_media(m['file_url'],
                                     thumbnail_url=m['thumbnail_url'],
                                     content_description=m['content_description'])
            if not uri:
                logger.error('Failed to upload media file.')
                return self._process_error_result(self.ErrorCode.UPLOAD_FAILED, 'Failed to upload media file.')

            if payload:
                payload = payload.replace(m['file_url'], uri)

        if is_test:
            return True

        if fetch_only:
            response = {
                'payload': payload,
                'message_id': message_id,
                'properties': properties,
                'is_test': is_test
            }
            return response

        return self._deliver_payload(msisdn, uuid.uuid4(), payload)

    def _deliver_payload(self, msisdn, message_id, payload):
        url = self.rbm_endpoint + "/v1/phones/{0}/agentMessages?messageId={1}".format(msisdn, message_id)

        logger.info("Posting agent message {0} for {1}".format(message_id, msisdn))
        logger.info("  url = " + url)
        logger.info("  payload = " + payload)

        response = self.rbm_http.post(url, data=payload, headers={'Content-Type': 'application/json'})

        logger.info("Received response from " + url)
        logger.info("  status_code: " + str(response.status_code))
        logger.info("  response: " + json.dumps(response.json()))

        success = response.status_code == 200
        if not success:
            logger.error("Post of agent message failed!")

        return success

    def _upload_media(self, file_url, thumbnail_url=None, content_description=None):
        url = self.rbm_endpoint + "/v1/files"
        request = {'fileUrl': file_url}
        if thumbnail_url is not None:
            request['thumbnailUrl'] = thumbnail_url
        if content_description is not None:
            request['contentDescription'] = content_description

        logger.info("Uploading media file")
        logger.info("  url = " + url)
        logger.info("  fileUrl = " + file_url)
        logger.info("  thumbnailUrl = " + thumbnail_url)
        logger.info("  contentDescription = " + content_description)

        response = self.rbm_http.post(url, json=request)

        logger.info("Received response from " + url)
        logger.info("  status_code: " + str(response.status_code))
        logger.info("  response: " + json.dumps(response.json()))

        success = response.status_code == 200
        if not success:
            logger.error("Post of file upload failed!")
            return None

        response_json = response.json()
        if not response_json or 'name' not in response_json:
            logger.error("Unexpected response from file upload.")
            return None

        return response_json['name']

    class ErrorCode(object):
        UNSUPPORTED_FORMAT = 1000
        MISSING_REQUIRED_PARAMETER = 1002
        UNKNOWN_ADUNIT = 1004
        NO_LINEITEMS_CONFIGURED = 1006
        ADUNIT_LIMIT_EXCEEDED = 1008
        TARGETING_PREVENTED_FILL = 1010
        LINEITEM_LIMIT_EXCEEDED = 1012
        CREATIVE_LIMIT_EXCEEDED = 1014
        UPLOAD_FAILED = 1100
        OTHER = 1120
        NO_AD_RETURNED = 1122
        RETRIABLE_ERROR = 1124
