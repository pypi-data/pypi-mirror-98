import logging
logging.basicConfig(level=logging.INFO)

from jiraX import factories as factory
from pprint import pprint
from .base_entity import BaseEntity

from sro_db.application import factories
from sro_db.model import factories as factories_model

from .user import user as etl_user
from .scrum_development_team import scrum_development_team as etl_scrum_development_team

""" Team member of a project """
class team_member(BaseEntity):
	"""
	Class responsible for retrieve team members from jira and save on database
	"""
	def create(self, data, jira_user = None, jira_project = None):
		"""Create all team_members and save it on database.

		Args:
			data (dict): With content from Jira_RealTime
		"""
		try:
			logging.info("Creating Team Member")

			if jira_project is None:
				project_id = data['project_id']
				project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
				jira_project = project_apl.find_by_id(project_id)

			if jira_user is None:
				user_accountId = data['accountId']
				user_apl = factory.UserFactory(user=self.user,apikey=self.key,server=self.url)
				jira_user = user_apl.find_by_project_key_and_accountId(jira_project.key, user_accountId)

			team_member = self.conversor.team_member(
				etl_user, etl_scrum_development_team, 
				jira_user, jira_project)
			developer_application = factories.DeveloperFactory()
			developer_application.create(team_member)
			#Essa classe não tem application reference

			logging.info("Team Member created")

			return team_member

		except Exception as e:
			pprint(e)
			logging.error("Failed to create Team Member")

	def update(self, data):
		"""Create all team_members and save it on database.

		Args:
			data (dict): With content from Jira_RealTime
		"""
		try:
			logging.info("Updating Team Member")

			user_accountId = data['accountId']
			project_id = data['project_id']

			developer_application = factories.DeveloperFactory()
			team_member_application = factories.TeamMemberFactory()

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			user_apl = factory.UserFactory(user=self.user,apikey=self.key,server=self.url)
			project = project_apl.find_by_id(project_id)
			user = user_apl.find_by_project_key_and_accountId(project.key, user_accountId)

			team_member = self.conversor.user(
				user,
				project,
				team_member_application.retrive_by_external_id_and_project_name(user.accountId, project.name)
			)
			developer_application.update(team_member)

			logging.info("Team Member updated")

			return team_member

		except Exception as e:
			pprint(e)
			logging.error("Failed to update Team Member")

	def delete(self, data):
		pass

	def do(self, data):
		"""Retrieve members from all projects and save on database

		Args:
			data (dict): With user, key, server, organization_id and 
						 configuration_id to configure object
		"""
		try:
			logging.info("Team Member")

			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			user_apl = factory.UserFactory(user=self.user,apikey=self.key,server=self.url)
			issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)

			team_member_application = factories.TeamMemberFactory()

			projects = project_apl.find_all()
			for project in projects:
				issues = issue_apl.find_by_project(project.key)
				accountIds = [
					issues.raw['fields']['assignee']['accountId'],
					issues.raw['fields']['creator']['accountId'],
					issues.raw['fields']['reporter']['accountId']
				]
				for user_accountId in accountIds:
					if team_member_application.retrive_by_external_id_and_project_name(user_accountId, project.name): 
						continue
					user = user_apl.find_by_project_key_and_accountId(project.key, user_accountId)
					self.create(None, user, project)

			logging.info("Successfully done Team Member")

		except Exception as e:
			pprint(e)
			logging.error("Failed to do Team Member")


