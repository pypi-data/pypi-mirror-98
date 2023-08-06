# https://integration.arcopole.fr/Orion/orion/admin/tree/object/BUSINESS/Cadastre

import json
from .BusinessResource import BusinessResource


# TODO : factorize with Resource !
class StorageResource(BusinessResource):
    def __init__(self, resource_description):
        """

        :param resource_id: Param _id returned by the REST API
        :param definition: Definition of the cadastre resource
        """
        super().__init__(resource_description)

    @property
    def filter_id(self):
        """
        :return: Associated filter's id
        """
        # TODO get the full filter instead ! (How ?)
        return self._description.get('dimensionId')

    @property
    def service_url(self):
        """
        :return: Stats service url
        """
        service_url = None
        if self._description.get('service'):
            service_url = self._description.get('service').get('url')

        return service_url

    # ----- Activate a filter -----

    def update_filter(self, filter_id):
        """Associate a filter to this resource

        :param filter_id: filter to associate
        """
        if filter_id and self.filter_id == filter_id:
            print("The filter is already used for this stats storage")
        else:
            config_url = self._url_builder.stats_configuration_url(self.id)

            self._description['dimensionId'] = filter_id
            self._request_mgr.post(config_url, data = {'value': json.dumps(self._description)})

            print('Filter {} successfully updated in Stats resource'.format(filter_id))

    def disassociate_filter(self, filter_id=None):
        """ disassociate the (given) associated filter.
        :param filter_id: Optional. If want to be sure to disassociate only a specific filter.
        """
        if filter_id is not None and self.filter_id != filter_id:
            print('This filter is not associated with our resource, nothing happens')
        else:
            self.update_filter("")

    # ------ Manage stats handler ------
    def get_status(self):
        """Get capabilities on resource
        """
        status = self._request_mgr.get_in_python(self._url_builder.stats_status_url())

        print('Stats detail capabilities: ', status)
        return status

    def create_new_session(self, info):
        """Create new session
        """
        session = self._request_mgr.post_in_python(self._url_builder.stats_newSession_url(), data = {'info': json.dumps(info)})
        print('Stats detail session: ', session)
        return session['sessionId']

    def heart_beat(self, info):
        """Call heart_beat method
        """
        result = self._request_mgr.post_in_python(self._url_builder.stats_heartBeat_url(), data = {'info': json.dumps(info)})
        print('Stats heart beat: ', result)
        if not result['success']: 
            raise Exception('Issue during heartBeat process')
        return result['success']

    def push(self):
        """Force to push stats data
        """
        result = self._request_mgr.get_in_python(self._url_builder.stats_push_url())
        print('Stats heart beat: ', result)
        if not result['success']: 
            raise Exception('Issue during push process')
        return result.get('result')

    def synthesis(self):
        """Force to synthesis stats data
        """
        result = self._request_mgr.get_in_python(self._url_builder.stats_synthesis_url())
        print('Stats synthesis: ', result)
        return result

    def clean(self):
        """Force to clean stats data
        """
        result = self._request_mgr.get_in_python(self._url_builder.stats_clean_url())
        print('Stats clean: ', result)
        return result
    
    
    def __str__(self):
        """Provides a string representation of a cadastre resource"""
        resource_str = 'Resource id : {}, ' \
                       'Filtre associé : {}'.format(self.id,
                                                    self.filter_id)
        return resource_str
