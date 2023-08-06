import logging
logging.basicConfig(level=logging.INFO)

from jiraX import factories as factory
from pprint import pprint
from .base_entity import BaseEntity

from sro_db.application import factories
from sro_db.model import factories as factories_model
from datetime import datetime

from .team_member import team_member as etl_team_member

""" An epic """
class epic(BaseEntity):
	"""
	Class responsible for retrieve epics from jira lala
	"""
	def create(self, data, jira_issue = None, jira_project = None):
		try:
			logging.info("Creating Epic")

			if jira_issue is None:
				issue_id = data['content']['all']['issue']['id']
				issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)
				jira_issue = issue_apl.find_by_id(issue_id)

			if jira_project is None:
				project_id = data['content']['all']['issue']['fields']['project']['id']
				project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
				jira_project = project_apl.find_by_id(project_id)

			epic = self.conversor.epic(
				etl_team_member, 
				jira_issue, jira_project)
			epic_application = factories.EpicFactory()
			epic_application.create(epic)
			self.create_application_reference('issue', epic, jira_issue.id, jira_issue.self)

			logging.info("Epic created")

			return epic

		except Exception as e:
			pprint(e)
			logging.error("Failed to create Epic")

	def update(self, data):
		try:
			logging.info("Updating Epic")
			
			issue_id = data['content']['all']['issue']['id']
			issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)
			jira_issue = issue_apl.find_by_id(issue_id)

			project_id = data['content']['all']['issue']['fields']['project']['id']
			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			jira_project = project_apl.find_by_id(project_id)

			epic_application = factories.EpicFactory()
			epic = self.conversor.epic(
				etl_team_member,
				jira_issue, jira_project,
				epic_application.retrive_by_external_uuid(issue_id))
			
			epic_application.update(epic)

			logging.info("Epic updated")

			return epic

		except Exception as e:
			pprint(e)
			logging.error("Failed to update Epic")	

	def delete(self, data):
		pass

	def do(self, data):
		"""Retrieve all epics from jira

		Args:
			data (dict): With user, key and server to connect with jira

		"""
		try:
			logging.info("Epic")
			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)

			epic_application = factories.EpicFactory()

			projects = project_apl.find_all()
			for project in projects:
				epics = issue_apl.find_epic_by_project(project.key)
				for epic in epics:
					if epic_application.retrive_by_external_uuid(epic.id):
						continue
					self.create(None, epic, project)

			logging.info("Successfully done (Epic)")

		except Exception as e:
			pprint(e)
			logging.error("Failed to do Epic")

	def update_by_time(self, data, time):
		try:
			logging.info("Update Epic by time")
			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)
			epic_application = factories.EpicFactory()

			projects = project_apl.find_all()
			for project in projects:
				epics = issue_apl.find_epic_by_project(project.key, time)
				for jira_epic in epics:
					ontology_epic = epic_application.retrive_by_external_uuid(jira_epic.id)
					if ontology_epic is not None:
						epic = self.conversor.epic(
							etl_team_member,
							jira_epic, project,
							ontology_epic)
						epic_application.update(epic)
					else:
						self.create(None, jira_epic, project)

			logging.info("Successfully updated Epic by time")

		except Exception as e:
			pprint(e)
			logging.error("Failed to update Epic by time")