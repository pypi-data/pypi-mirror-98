import logging
logging.basicConfig(level=logging.INFO)

from jiraX import factories as factory
from pprint import pprint
from .base_entity import BaseEntity

from sro_db.application import factories
from sro_db.model import factories as factories_model

""" User """
class user(BaseEntity):
	"""
	Class responsible for retrieve users from jira and sabe them on database
	"""

	def create(self, data, jira_user = None):
		try:
			logging.info("Creating User")

			if jira_user is None:
				user_id = data['content']['all']['content'][0]['user']['accountId']
				user_apl = factory.UserFactory(user=self.user,apikey=self.key,server=self.url)
				jira_user = user_apl.find_by_id(user_id)
			person = self.conversor.user(jira_user)

			person_application = factories.PersonFactory()
			person_application.create(person)
			self.create_application_reference('user', person, jira_user.accountId, jira_user.self)

			logging.info("User created")

			return person

		except Exception as e:
			pprint(e)
			logging.error("Failed to create User")

	def update(self, data):
		try:
			logging.info("Updating User")
			user_id = data['content']['all']['user']['accountId']
			user_apl = factory.UserFactory(user=self.user,apikey=self.key,server=self.url)
			jira_user = user_apl.find_by_id(user_id)

			person_application = factories.PersonFactory()
			ontology_user = person_application.retrive_by_external_uuid(jira_user.accountId)
			person = self.conversor.user(jira_user, ontology_user)
			person_application.update(person)

			logging.info("User updated")

			return person

		except Exception as e:
			pprint(e)
			logging.error("Failed to update User")

	def delete(self, data):
		pass

	def do(self,data):
		"""Retrieve all users from all projects and save on database

		Args:
			data (dict): With user, key, server, organization_id and 
						 configuration_id to configure object
		"""
		try:
			logging.info("User")
			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			user_apl = factory.UserFactory(user=self.user,apikey=self.key,server=self.url)
			members = list({str(member.accountId): member 
				for project in project_apl.find_all() 
				for member in user_apl.find_by_project(project.key)}.values())

			person_application = factories.PersonFactory()
			for member in members:
				if person_application.retrive_by_external_uuid(member.accountId):
					continue
				self.create(None, member)
			
			logging.info("Successfully done User")

		except Exception as e:
			pprint(e)
			logging.error("Failed to do User")




	


		
