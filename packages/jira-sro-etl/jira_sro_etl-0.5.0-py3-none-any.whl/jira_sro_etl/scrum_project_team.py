import logging
logging.basicConfig(level=logging.INFO)
from .base_entity import BaseEntity
from jiraX import factories as factory
from pprint import pprint

from sro_db.application import factories
from sro_db.model import factories as factories_model

from .scrum_project import scrum_project as etl_scrum_project

""" Scrum development team """
class scrum_project_team(BaseEntity):
	"""
	Class responsible for retrieve teams from jira
	"""

	def create(self, data, jira_project = None):
		"""Create a team and save it on database.

		Args:
			data (dict): With content from Jira_RealTime
		"""
		try:
			logging.info("Creating Scrum Project Team")

			if jira_project is None:
				project_id = data['content']['all']['project']['id']
				project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
				jira_project = project_apl.find_by_id(project_id)
			scrum_team = self.conversor.team(
				etl_scrum_project,
				jira_project)

			scrum_team_application = factories.ScrumTeamFactory()
			scrum_team_application.create(scrum_team)
			self.create_application_reference('project', scrum_team, jira_project.id)
			
			logging.info("Scrum Project Team created")

			return scrum_team

		except Exception as e:
			pprint(e)
			logging.error("Failed to create Scrum Project Team")

	def update(self, data):
		pass

	def delete(self, data):
		try:
			logging.info("Creating Scrum Project Team")

			scrum_team_application = factories.ScrumTeamFactory()

			content = data['content']
			project = content['all']['project']

			scrum_team = scrum_team_application.retrive_by_external_uuid(project['id'])
			scrum_team_application.delete(scrum_team)

			logging.info("Scrum project Team deleted")

		except Exception as e:
			pprint(e)
			logging.error("Failed to delete Scrum Project Team")

	def do (self,data):
		"""Retrieve all teams

		Args:
			data (dict): With user, key and server to connect with jira

		Returns:
			list: List of all develpoment teams
		"""
		try:
			logging.info("Scrum Project Team")

			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			projects = project_apl.find_all() 
			scrum_teams = {str(project.id): f"{project.key}_scrum_team" for project in projects}

			scrum_project_application = factories.ScrumAtomicProjectFactory()
			scrum_team_application = factories.ScrumTeamFactory()

			for project_id,scrum_team_name in scrum_teams.items():
				if scrum_team_application.retrive_by_external_uuid(project_id):
					continue
				scrum_team = factories_model.ScrumTeamFactory()
				scrum_team.name = scrum_team_name
				scrum_team.organization = self.organization
				scrum_project = scrum_project_application.retrive_by_external_uuid(project_id)
				try: #Temporary
					scrum_team.scrum_project = scrum_project.id
				except Exception as e:
					pass
				scrum_team_application.create(scrum_team)
				self.create_application_reference('project', scrum_team, project_id)
			
			logging.info("successfuly done (Scrum Project Team)")
			return scrum_teams

		except Exception as e:
			pass
