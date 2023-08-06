import logging
logging.basicConfig(level=logging.INFO)

from jiraX import factories as factory
from pprint import pprint
from .base_entity import BaseEntity

from sro_db.application import factories
from sro_db.model import factories as factories_model

from .team_member import team_member as etl_team_member
from .user_story import user_story as etl_user_story
from .sprint import sprint as etl_sprint

""" Scrum performed development task """
class scrum_development_task(BaseEntity):
	"""
	Class responsible for retrieve tasks from jira and save them on database
	"""

	def create(self, data, jira_issue = None, jira_project = None):
		try:
			logging.info("Creating Scrum Development Task")
			if jira_issue is None:
				issue_id = data['content']['all']['issue']['id']
				issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)
				jira_issue = issue_apl.find_by_id(issue_id)
			
			if jira_project is None:
				project_id = data['content']['all']['issue']['fields']['project']['id']
				project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
				jira_project = project_apl.find_by_id(project_id)

			scrum_intended_development_task, scrum_performed_development_task = self.conversor.task(
				etl_team_member, etl_user_story, etl_sprint,
				jira_issue, jira_project,
			)

			intended_task_application = factories.ScrumIntentedDevelopmentTaskFactory()
			intended_task_application.create(scrum_intended_development_task)
			self.create_application_reference('issue', scrum_intended_development_task, jira_issue.id, jira_issue.self)

			if(scrum_performed_development_task is not None):
				performed_task_application = factories.ScrumPerformedDevelopmentTaskFactory()
				performed_task_application.create(scrum_performed_development_task)
				self.create_application_reference('issue', scrum_performed_development_task, jira_issue.id, jira_issue.self)

			logging.info("Scrum Development Task created")

		except Exception as e:
			pprint(e)
			logging.error("Failed to create Scrum Development Task")

	def update(self, data):
		try:
			logging.info("Updating Scrum Development Task")

			issue_id = data['content']['all']['issue']['id']
			issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)
			jira_issue = issue_apl.find_by_id(issue_id)
			
			project_id = data['content']['all']['issue']['fields']['project']['id']
			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			jira_project = project_apl.find_by_id(project_id)
			
			intended_task_application = factories.ScrumIntentedDevelopmentTaskFactory()
			performed_task_application = factories.ScrumPerformedDevelopmentTaskFactory()
			ontology_scrum_intended_development_task = intended_task_application.retrive_by_external_uuid(jira_issue.id)
			ontology_scrum_performed_development_task = performed_task_application.retrive_by_external_uuid(jira_issue.id)

			scrum_intended_development_task, scrum_performed_development_task = self.conversor.task(
				etl_team_member, etl_user_story, etl_sprint,
				jira_issue, jira_project, 
				ontology_scrum_intended_development_task, ontology_scrum_performed_development_task
			)

			intended_task_application.update(scrum_intended_development_task)

			if scrum_performed_development_task is not None:
				if ontology_scrum_performed_development_task is None:
					performed_task_application.create(scrum_performed_development_task)
					self.create_application_reference('issue', scrum_performed_development_task, jira_issue.id, jira_issue.self)
				else:
					performed_task_application.update(scrum_performed_development_task)
			
			logging.info("Scrum Development Task updated")

		except Exception as e:
			pprint(e)
			logging.error("Failed to update Scrum Development Task")

	def delete(self, data):
		pass

	def do(self,data):
		"""Retrieve all tasks from the projects and save them on db as 
		Scrum performed development task

		Args:
			data (dict): With user, key and server to connect with jira
		"""
		try:
			logging.info("Scrum Development Task")

			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)
			
			intended_task_application = factories.ScrumIntentedDevelopmentTaskFactory()

			projects = project_apl.find_all()
			for project in projects:
				tasks = issue_apl.find_sub_task_by_project(project.key)
				for task in tasks:
					if intended_task_application.retrive_by_external_uuid(task.id):
						pass
					self.create(None, task, project)

			logging.info("Successfully done Scrum Development Task")
		
		except Exception as e:
			pprint(e)
			logging.error("Failed to do Scrum Development Task")

	def update_by_time(self, data, time):
		try:
			logging.info("Update Scrum Development Task by time")
			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)
			intended_task_application = factories.ScrumIntentedDevelopmentTaskFactory()
			performed_task_application = factories.ScrumPerformedDevelopmentTaskFactory()

			projects = project_apl.find_all()
			for project in projects:
				tasks = issue_apl.find_sub_task_by_project(project.key, time)
				for jira_task in tasks:
					ontology_scrum_intended_development_task = intended_task_application.retrive_by_external_uuid(jira_task.id)
					if ontology_scrum_intended_development_task is not None:
						ontology_scrum_performed_development_task = performed_task_application.retrive_by_external_uuid(jira_task.id)
						scrum_intended_development_task, scrum_performed_development_task = self.conversor.task(
							etl_team_member, etl_user_story, etl_sprint,
							jira_task, project, 
							ontology_scrum_intended_development_task, ontology_scrum_performed_development_task
						)
						intended_task_application.update(scrum_intended_development_task)
						if scrum_performed_development_task is not None:
							if ontology_scrum_performed_development_task is None:
								performed_task_application.create(scrum_performed_development_task)
								self.create_application_reference('issue', scrum_performed_development_task, jira_task.id, jira_task.self)
							else:
								performed_task_application.update(scrum_performed_development_task)
					else:
						self.create(None, jira_task, project)

			logging.info("Successfully updated Scrum Development Task by time")

		except Exception as e:
			pprint(e)
			logging.error("Failed to update Scrum Development Task by time")
