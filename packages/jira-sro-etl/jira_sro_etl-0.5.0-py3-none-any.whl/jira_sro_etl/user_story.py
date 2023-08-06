import logging
logging.basicConfig(level=logging.INFO)

from jiraX import factories as factory
from pprint import pprint
from .base_entity import BaseEntity

from sro_db.application import factories
from sro_db.model import factories as factories_model

from .scrum_project import scrum_project as etl_scrum_project
from .team_member import team_member as etl_team_member
from .sprint import sprint as etl_sprint

""" User story """
class user_story(BaseEntity):
	"""
	Class responsible for retrieve user storys from jira
	"""

	def resolve_start_date(self, arr):
		if arr == None:
			return None
		for d in arr:
			if 'startDate' in d:
				return d['startDate']
		return None

	def create(self, data, jira_issue = None, jira_project = None):
		try:
			logging.info("Creating Atomic User Story")

			if jira_issue is None:
				issue_id = data['content']['all']['issue']['id']
				issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)
				jira_issue = issue_apl.find_by_id(issue_id)
			
			if jira_project is None:
				project_id = data['content']['all']['issue']['fields']['project']['id']
				project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
				jira_project = project_apl.find_by_id(project_id)
			
			atomic_user_story = self.conversor.user_story(
				etl_scrum_project, etl_team_member, etl_sprint,
				jira_issue, jira_project)

			atomic_user_story_application = factories.AtomicUserStoryFactory()
			atomic_user_story_application.create(atomic_user_story)
			self.create_application_reference('issue', atomic_user_story, jira_issue.id, jira_issue.self)

			logging.info("Atomic User Story created")

			return atomic_user_story

		except Exception as e:
			pprint(e)
			logging.error("Failed to create Atomic User Story")

	def update(self, data):
		try:
			logging.info("Updating Atomic User Story")

			issue_id = data['content']['all']['issue']['id']
			issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)
			jira_issue = issue_apl.find_by_id(issue_id)
			
			project_id = data['content']['all']['issue']['fields']['project']['id']
			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			jira_project = project_apl.find_by_id(project_id)
			
			atomic_user_story_application = factories.AtomicUserStoryFactory()
			ontology_user_story = atomic_user_story_application.retrive_by_external_uuid(jira_issue.id)
			atomic_user_story = self.conversor.user_story(
				etl_scrum_project, etl_team_member, etl_sprint,
				jira_issue, jira_project, 
				ontology_user_story)
			atomic_user_story_application.update(atomic_user_story)
			
			logging.info("Atomic User Story updated")

		except Exception as e:
			pprint(e)
			logging.error("Failed to update Atomic User Story")

	def delete(self, data):
		pass

	def do(self,data):
		"""Retrieve user stories from all projects

		Args:
			data (dict): With user, key and server to connect with jira

		Returns:
			dict: Key is the project's key and value is a list with all user stories of this project
		"""
		try:
			logging.info("User Story")
			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)

			atomic_user_story_application = factories.AtomicUserStoryFactory()

			projects = project_apl.find_all()
			for project in projects:
				stories = issue_apl.find_story_by_project(project.key)
				for story in stories:
					if atomic_user_story_application.retrive_by_external_uuid(story.id): 
						continue
					self.create(None, story, project)

			logging.info("Successfully done Atomic User Story")

		except Exception as e:
			pprint(e)
			logging.error("Failed to do Atomic User Story")

	def update_by_time(self, data, time):
		try:
			logging.info("Update User Story by time")
			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)
			atomic_user_story_application = factories.AtomicUserStoryFactory()

			projects = project_apl.find_all()
			for project in projects:
				stories = issue_apl.find_story_by_project(project.key, time)
				for jira_story in stories:
					ontology_user_story = atomic_user_story_application.retrive_by_external_uuid(jira_story.id)
					if ontology_user_story is not None:
						atomic_user_story = self.conversor.user_story(
							etl_scrum_project, etl_team_member, etl_sprint,
							jira_story, project,
							ontology_user_story)
						atomic_user_story_application.update(atomic_user_story)
					else:
						self.create(None, jira_story, project)

			logging.info("Successfully updated User Story by time")

		except Exception as e:
			pprint(e)
			logging.error("Failed to update User Story by time")
