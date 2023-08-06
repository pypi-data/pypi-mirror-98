import logging
logging.basicConfig(level=logging.INFO)

from jiraX import factories as factory
from .base_entity import BaseEntity
from pprint import pprint

from sro_db.application import factories
from sro_db.model import factories as factories_model

from .scrum_project_team import scrum_project_team as etl_scrum_project_team

""" Scrum development team """
class scrum_development_team(BaseEntity):
	"""
	Class responsible for retrieve teams from jira
	"""
	
	def create (self, data, jira_project = None):
		"""Create a development team and save it on database.

		Args:
			data (dict): With content from Jira_RealTime
		"""
		try:
			logging.info("Creating Scrum Development Team")

			if jira_project is None:
				project_id = data['content']['all']['project']['id']
				project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
				jira_project = project_apl.find_by_id(project_id)
			scrum_development_team = self.conversor.development_team(
				etl_scrum_project_team,
				jira_project)

			scrum_development_team_application = factories.DevelopmentTeamFactory()
			scrum_development_team_application.create(scrum_development_team)
			self.create_application_reference('project', scrum_development_team, jira_project.id)

			logging.info("Scrum Development Team created")

			return scrum_development_team
 
		except Exception as e:
			pprint(e)
			logging.error("Failed to create Scrum Development Team")

	def update(self, data):
		pass

	def delete(self, data):
		try:
			logging.info("Deleting Scrum Development Team")

			scrum_development_team_application = factories.DevelopmentTeamFactory()

			content = data['content']
			project = content['all']['project']

			scrum_development_team = scrum_development_team_application.retrive_by_external_uuid(project['id'])
			scrum_development_team_application.delete(scrum_development_team)

			logging.info("Scrum Development Team deleted")

		except Exception as e:
			pprint(e)
			logging.error("Failed to delete Scrum Development Team")

	def do (self,data):
		"""Retrieve all teams

		Args:
			data (dict): With user, key and server to connect with jira

		Returns:
			list: List of all develpoment teams
		"""
		try:
			logging.info("Scrum Development Team")

			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			projects = project_apl.find_all() 
			scrum_development_teams = {str(project.id): f"{project.key}_scrum_development_team" for project in projects}

			scrum_team_application = factories.ScrumTeamFactory()
			scrum_development_team_application = factories.DevelopmentTeamFactory()

			for project_id, scrum_development_team_name in scrum_development_teams.items():
				if scrum_development_team_application.retrive_by_external_uuid(project_id):
					continue
				scrum_development_team = factories_model.DevelopmentTeamFactory()
				scrum_development_team.organization = self.organization
				scrum_development_team.name = scrum_development_team_name
				scrum_team = scrum_team_application.retrive_by_external_uuid(project_id) 
				scrum_development_team.scrum_team_id = scrum_team.id
				scrum_development_team_application.create(scrum_development_team)
				self.create_application_reference('project', scrum_development_team, project_id)
			
			logging.info("successfuly done (Scrum Development Team)")
			return scrum_development_teams

		except e:
			pass
