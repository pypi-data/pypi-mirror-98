import logging
import datetime
logging.basicConfig(level=logging.INFO)

from jiraX import factories as factory
from pprint import pprint
from .base_entity import BaseEntity

from sro_db.application import factories
from sro_db.model import factories as factories_model

from .scrum_project import scrum_project as etl_scrum_project

""" Sprint (Time box) """
class sprint(BaseEntity):
	"""
	Class responsible for retrieve sprints from jira
	"""
	def create(self, data, jira_sprint = None, jira_project = None):
		try:
			logging.info("Creating Sprint")

			if jira_sprint is None:
				sprint_id = data['content']['all']['sprint']['id']
				sprint_apl = factory.SprintFactory(user=self.user,apikey=self.key,server=self.url)
				jira_sprint = sprint_apl.find_by_id(sprint_id)

			if jira_project is None:
				board_id = data['content']['all']['sprint']['originBoardId']
				project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
				jira_project = project_apl.find_by_board_id(board_id)

			sprint, sprint_backlog = self.conversor.sprint(
				etl_scrum_project,
				jira_sprint, jira_project)
			sprint_application = factories.SprintFactory()
			sprint_application.create(sprint)
			self.create_application_reference('sprint', sprint, jira_sprint.id, jira_sprint.self)
			sprint_backlog_application = factories.SprintBacklogFactory()
			sprint_backlog_application.create(sprint_backlog)
			self.create_application_reference('sprint', sprint_backlog, jira_sprint.id, jira_sprint.self)

			logging.info("Sprint created")

			return sprint, sprint_backlog
			
		except Exception as e:
			pprint(e)
			logging.error("Failed to create Sprint")

	def update (self, data):
		try:
			logging.info("Updating Sprint")

			sprint_application = factories.SprintFactory()
			sprint_backlog_application = factories.SprintBacklogFactory()

			sprint_id = data['content']['all']['sprint']['id']
			sprint_apl = factory.SprintFactory(user=self.user,apikey=self.key,server=self.url)
			jira_sprint = sprint_apl.find_by_id(sprint_id)

			board_id = data['content']['all']['sprint']['originBoardId']
			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			jira_project = project_apl.find_by_board_id(board_id)

			#Update
			ontology_sprint = sprint_application.retrive_by_external_uuid(jira_sprint.id)
			ontology_sprint_backlog = sprint_backlog_application.retrive_by_external_uuid(jira_sprint.id)
			sprint, sprint_backlog = self.conversor.sprint(
				etl_scrum_project,
				jira_sprint, jira_project, 
				ontology_sprint, ontology_sprint_backlog)
			sprint_application.update(sprint)
			self.create_application_reference('sprint', sprint, jira_sprint.id, jira_sprint.self)
			sprint_backlog_application.update(sprint_backlog)
			self.create_application_reference('sprint', sprint_backlog, jira_sprint.id, jira_sprint.self)

			logging.info("Sprint updated")
			
			return sprint, sprint_backlog

		except Exception as e:
			pprint(e)
			logging.error("Failed to update Sprint")

	def delete (self, data):
		pass

	def do(self,data):
		"""Retrive all sprints from all projects

		Args:
			data (dict): With user, key and server to connect with jira

		Returns:
			dict: Key is the project's key and value is a list with all sprints of this project
		"""
		try:
			logging.info("Sprint")
			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			board_apl = factory.BoardFactory(user=self.user,apikey=self.key,server=self.url)
			sprint_apl = factory.SprintFactory(user=self.user,apikey=self.key,server=self.url)
		
			sprint_application = factories.SprintFactory()

			projects = project_apl.find_all()
			for project in projects:
				boards = board_apl.find_by_project(project.key)
				if(boards != None):
					for board in boards:
						try:
							sprints = sprint_apl.find_by_board(board.id)
							for sprint in sprints:
								if sprint_application.retrive_by_external_uuid(sprint.id):
									continue
								self.create(None, sprint, project)
							
						except Exception as e:
							pprint("O quadro não aceita sprints")

			logging.info("Successfully done Sprint")
			return sprints
			
		except Exception as e:
			pprint(e)
			logging.error("Failed to do Sprint")
			pass
