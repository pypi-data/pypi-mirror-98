from pprint import pprint
from jiraX import factories as factory
import logging
logging.basicConfig(level=logging.INFO)

from sro_db.application import factories
from sro_db.model import factories as factories_model

from datetime import datetime
from .conversor.conversor import Conversor

class BaseEntity():
    """ 
    Class responsible to connect with jira and make default tasks with database
    """   
    def config (self, data):
        """Responsible to configure connection parameters

        Args:
            data (dict): Dictionary with user, key, url, organization_id and 
                         configuration_id to connect with jira plus get 
                         organization and configuration from database
        """
        self.data = data

        self.user = self.data['user']
        self.key = self.data['key']
        self.url = self.data['url']

        uuid = data['organization_id']
        organization_application = factories.OrganizationFactory()
        self.organization = organization_application.get_by_uuid(uuid)
        
        uuid_configuration = data['configuration_id']
        configuration_application = factories.ConfigurationFactory()
        self.configuration = configuration_application.get_by_uuid(uuid_configuration)

        self.conversor = Conversor(self.organization, self.data)

    def create_application_reference(self, external_type_entity, internal_entity, external_id, external_url=None ):
        """Responsible to save application reference on database

        Args:
            external_type_entity (str): Entity name on jira 
            internal_entity (obj): Object created by a sro_db's factory
            external_id (str): Unique identifier of object on jira
            external_url (str, optional): Url from jira object
        """
        application_reference_application = factories.ApplicationReferenceFactory()
        application_reference = factories_model.ApplicationReferenceFactory()
        application_reference.external_id = external_id
        application_reference.external_url = external_url
        application_reference.configuration = self.configuration.id
        application_reference.external_type_entity = external_type_entity
        application_reference.internal_uuid = internal_entity.uuid
        application_reference.entity_name = internal_entity.__tablename__
        application_reference_application.create(application_reference)
        
    def date_formater(self,date_string):
        """Receive date in YYYY-MM-DD and return datetime

        Can receive date with more details like hour, minute and second, but all info
        after day is ignored

		Args:
			date_string (str/NoneType): string YYYY-MM-DD or None

		Returns:
			datetime/NoneType: Formated date or None if param was None
		"""
        if date_string:
            return datetime.strptime(date_string[:10], "%Y-%m-%d")
        return None
        
    
    