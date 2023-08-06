import logging
logging.basicConfig(level=logging.INFO)

from jiraX import factories as factory
from pprint import pprint
from .base_entity import BaseEntity

from sro_db.application import factories
from sro_db.model import factories as factories_model

""" Scrum project """
class scrum_project(BaseEntity):
	"""
	Class responsible for retrieve projects from jira and save them on database
	"""

	def create(self, data, jira_project = None):
		"""Create a project and save it on database. And save
		a scrum process for the project

		Args:
			data (dict): With content from Jira_RealTime
		"""
		try:
			logging.info("Creating Scrum Project")

			scrum_project_application = factories.ScrumAtomicProjectFactory()
			scrum_process_application = factories.ScrumProcessFactory()
			product_backlog_definition_application = factories.ProductBacklogDefinitionFactory()
			product_backlog_application = factories.ProductBacklogFactory()

			if jira_project is None:
				project_id = data['content']['all']['project']['id']
				project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
				jira_project = project_apl.find_by_id(project_id)

			scrum_project, scrum_process, product_backlog_definition, product_backlog = self.conversor.project(jira_project)
			scrum_project_application.create(scrum_project)
			self.create_application_reference('project', scrum_project, jira_project.id, jira_project.self)
			scrum_process_application.create(scrum_process)
			self.create_application_reference('project', scrum_process, jira_project.id, jira_project.self)
			product_backlog_definition_application.create(product_backlog_definition)
			self.create_application_reference('project', product_backlog_definition, jira_project.id, jira_project.self)
			product_backlog_application.create(product_backlog)
			self.create_application_reference('project', product_backlog, jira_project.id, jira_project.self)

			logging.info("Scrum Project created")

			return scrum_project, scrum_process, product_backlog_definition, product_backlog

		except Exception as e:
			pprint(e)
			logging.error("Failed to create Scrum Project")

	def update(self, data):
		"""Update a project and save it on database. And save
		a scrum process for the project

		Args:
			data (dict): With content from Jira_RealTime
		"""
		try:
			logging.info("Updating Scrum Project")

			scrum_project_application = factories.ScrumAtomicProjectFactory()
			scrum_process_application = factories.ScrumProcessFactory()
			product_backlog_definition_application = factories.ProductBacklogDefinitionFactory()
			product_backlog_application = factories.ProductBacklogFactory()

			content = data['content']
			project = content['all']['project']
			project_id = project['id']
			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			jira_project = project_apl.find_by_id(project_id)

			scrum_project, scrum_process, product_backlog_definition, product_backlog = self.conversor.project(
				jira_project,
				scrum_project_application.retrive_by_external_uuid(jira_project.id),
				scrum_process_application.retrive_by_external_uuid(jira_project.id),
				product_backlog_definition_application.retrive_by_external_uuid(jira_project.id),
				product_backlog_application.retrive_by_external_uuid(jira_project.id)
			)

			scrum_project_application.update(scrum_project)
			scrum_process_application.update(scrum_process)
			product_backlog_definition_application.update(product_backlog_definition)
			product_backlog_application.update(product_backlog)

			logging.info("Scrum Project updated")

			return scrum_project, scrum_process, product_backlog_definition, product_backlog

		except Exception as e:
			pprint(e)
			logging.error("Failed to update Scrum Project")

	def delete(self, data):
		pass

	def do(self, data):
		"""Retrieve all projects and save them on database. And save
		a scrum process for each project

		Args:
			data (dict): With user, key, server, organization_id and 
						 configuration_id to configure object
		"""
		try:
			logging.info("Scrum Project")
			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			projects = project_apl.find_all()

			scrum_project_application = factories.ScrumAtomicProjectFactory()
			for project in projects:
				if scrum_project_application.retrive_by_external_uuid(project.id):
					continue
				self.create(None, project)

			logging.info("Successfully done Scrum Project")

		except Exception as e:
			pprint(e)
			logging.error("Failed to do Scrum Project")

