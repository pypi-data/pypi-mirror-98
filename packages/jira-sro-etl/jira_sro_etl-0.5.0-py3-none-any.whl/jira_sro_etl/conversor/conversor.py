from jiraX import factories as factory
from sro_db.application import factories
from sro_db.model import factories as factories_model
from datetime import datetime
# from ..scrum_development_team import scrum_development_team
# from ..scrum_project_team import scrum_project_team
# from ..scrum_project import scrum_project
# from ..team_member import team_member

class Conversor():

    def __init__(self, organization, data):
        self.organization = organization
        self.data = data
        
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
    
    def project(self, jira_project, 
    ontology_scrum_atomic_project = None,
    ontology_scrum_process = None,
    ontology_product_backlog_definition = None,
    ontology_product_backlog = None):
    
        # Scrum atomic project
        if ontology_scrum_atomic_project is None:
            ontology_scrum_atomic_project = factories_model.ScrumAtomicProjectFactory()
        ontology_scrum_atomic_project.organization = self.organization
        ontology_scrum_atomic_project.name = jira_project.name
        ontology_scrum_atomic_project.index = jira_project.key
        
        # Scrum process
        if ontology_scrum_process is None:
            ontology_scrum_process = factories_model.ScrumProcessFactory()
        ontology_scrum_process.organization = self.organization
        ontology_scrum_process.name = jira_project.name
        ontology_scrum_process.scrum_project_id = ontology_scrum_atomic_project.id

        # Product backlog definition
        if ontology_product_backlog_definition is None:
            ontology_product_backlog_definition = factories_model.ProductBacklogDefinitionFactory()
        ontology_product_backlog_definition.name = jira_project.name
        ontology_product_backlog_definition.scrum_process_id = ontology_scrum_process.id
        
        #Product backlog
        if ontology_product_backlog is None:
           ontology_product_backlog = factories_model.ProductBacklogFactory()
        ontology_product_backlog.name = jira_project.name
        ontology_product_backlog.product_backlog_definition = ontology_product_backlog_definition.id	
        
        return ontology_scrum_atomic_project, ontology_scrum_process, ontology_product_backlog_definition, ontology_product_backlog

    def team_member(self, etl_user, etl_scrum_development_team,
    jira_user, jira_project,
    ontology_team_member = None):

        person_application = factories.PersonFactory()
        scrum_development_team_application = factories.DevelopmentTeamFactory()

        if ontology_team_member is None:
            ontology_team_member = factories_model.DeveloperFactory()
        ontology_team_member.organization = self.organization
        ontology_team_member.name = jira_user.displayName
        ontology_team_member.team_role = 'developer'
        try:
            user_id = jira_user.accountId
            ontology_team_member.person = person_application.retrive_by_external_uuid(user_id)
            if ontology_team_member.person is None:
                raise Exception('Not found')
        except Exception as e:
            user = etl_user()
            user.config(self.data)
            data_to_create = {'content': {'all': {'content': [{'user': {'accountId': user_id}}]}}}
            ontology_team_member.person = user.create(data_to_create)
        try:
            team_id = jira_project.id
            ontology_team_member.team = scrum_development_team_application.retrive_by_external_uuid(team_id)
            if ontology_team_member.team is None:
                raise Exception('Not found')
        except Exception as e:
            scrum_development_team = etl_scrum_development_team()
            scrum_development_team.config(self.data)
            data_to_create = {'content': {'all': {'project': {'id': team_id}}}}
            ontology_team_member.team = scrum_development_team.create(data_to_create)

        return ontology_team_member

    def epic(self, etl_team_member,
    jira_issue, jira_project, 
    ontology_epic = None):

        team_member_application = factories.TeamMemberFactory()

        if ontology_epic is None:
            ontology_epic = factories_model.EpicFactory()
        ontology_epic.name = jira_issue.raw['fields']['customfield_10011']
        try:
            creator_id = jira_issue.raw['fields']['creator']['accountId']
            ontology_epic.created_by = team_member_application.retrive_by_external_id_and_project_name(creator_id, jira_project.name).id
            if ontology_epic.created_by is None:
                raise Exception('Not found')
        except (NameError, TypeError):
            ontology_epic.created_by = None
        except Exception as e:
            team_member = etl_team_member()
            team_member.config(self.data)
            data_to_create = {'accountId': creator_id}
            ontology_epic.created_by = team_member.create(data_to_create, None, jira_project).id
        try:
            reporter_id = jira_issue.raw['fields']['reporter']['accountId']
            ontology_epic.activated_by = team_member_application.retrive_by_external_id_and_project_name(reporter_id, jira_project.name).id
            if ontology_epic.activated_by is None:
                raise Exception('Not found')
        except (NameError, TypeError):
            ontology_epic.activated_by = None
        except Exception as e:
            team_member = etl_team_member()
            team_member.config(self.data)
            data_to_create = {'accountId': reporter_id}
            ontology_epic.activated_by = team_member.create(data_to_create, None, jira_project).id
        try:
            assignee_id = jira_issue.raw['fields']['assignee']['accountId']
            ontology_epic.closed_by = team_member_application.retrive_by_external_id_and_project_name(assignee_id, jira_project['name']).id
            if ontology_epic.closed_by is None:
                raise Exception('Not found')
        except (NameError, TypeError):
            ontology_epic.closed_by = None
        except Exception as e:
            team_member = etl_team_member()
            team_member.config(self.data)
            data_to_create = {'accountId': reporter_id}
            ontology_epic.closed_by = team_member.create(data_to_create, None, jira_project).id
        # ontology_epic.story_points = TODO
        # ontology_epic.created_date = TODO
        ontology_epic.activated_date = self.date_formater(None if type(next(iter(jira_issue.raw['fields'].get('customfield_10018') or []), None)) != dict else jira_issue.raw['fields']['customfield_10018'][0]['startDate'])
        ontology_epic.closed_date = self.date_formater(jira_issue.raw['fields'].get('duedate'))
        ontology_epic.resolved_date = self.date_formater(jira_issue.raw['fields'].get('resolutiondate'))
        
        return ontology_epic

    def sprint(self, etl_scrum_project,
    jira_sprint, jira_project,
    ontology_sprint = None, ontology_sprint_backlog = None):
        
        scrum_process_application = factories.ScrumProcessFactory()

        # Sprint
        if ontology_sprint is None:
            ontology_sprint = factories_model.SprintFactory()
        ontology_sprint.organization = self.organization
        ontology_sprint.startDate = None
        ontology_sprint.endDate = None
        ontology_sprint.name = jira_sprint.name
        try:
            project_id = jira_project.id
            ontology_sprint.scrum_process_id = scrum_process_application.retrive_by_external_uuid(project_id).id
            if ontology_sprint.scrum_process_id is None:
                raise Exception('Not found')
        except NameError:
            ontology_sprint.scrum_process_id = None
        except Exception as e:
            scrum_project = etl_scrum_project()
            scrum_project.config(self.data)
            data_to_create = {'content': {'all': {'project': {'id': project_id}}}}
            _, scrum_process, _, _ = scrum_project.create(data_to_create)
            ontology_sprint.scrum_process_id = scrum_process.id

        # Sprint Backlog
        if ontology_sprint_backlog is None:
            ontology_sprint_backlog = factories_model.SprintBacklogFactory()
        ontology_sprint_backlog.name = ontology_sprint.name
        ontology_sprint_backlog.sprint = ontology_sprint.id

        return ontology_sprint, ontology_sprint_backlog

    def user_story(self, etl_scrum_project, etl_team_member, etl_sprint,
    jira_issue, jira_project, 
    ontology_atomic_user_story = None):

        product_backlog_application = factories.ProductBacklogFactory()
        team_member_application = factories.TeamMemberFactory()
        sprint_backlog_application = factories.SprintBacklogFactory()

        if ontology_atomic_user_story is None:
            ontology_atomic_user_story = factories_model.AtomicUserStoryFactory()
        ontology_atomic_user_story.name = jira_issue.raw['fields']['summary']
        ontology_atomic_user_story.description = jira_issue.raw['fields'].get('description')
        try:
            project_id = jira_project.id
            ontology_atomic_user_story.product_backlog = product_backlog_application.retrive_by_external_uuid(jira_project.id).id
            if ontology_atomic_user_story.product_backlog is None:
                raise Exception('Not found')
        except Exception as e:
            scrum_project = etl_scrum_project()
            scrum_project.config(self.data)
            data_to_create = {'content': {'all': {'project': {'id': project_id}}}}
            _, _, _, product_backlog = scrum_project.create(data_to_create)
            ontology_atomic_user_story.product_backlog = product_backlog.id
        try:
            creator_id = jira_issue.raw['fields']['creator']['accountId']
            ontology_atomic_user_story.created_by = team_member_application.retrive_by_external_id_and_project_name(creator_id, jira_project.name).id
            if ontology_atomic_user_story.created_by is None:
                raise Exception('Not found')
        except (NameError, TypeError):
            ontology_atomic_user_story.created_by = None
        except Exception as e:
            team_member = etl_team_member()
            team_member.config(self.data)
            data_to_create = {'accountId': creator_id}
            ontology_atomic_user_story.created_by = team_member.create(data_to_create, None, jira_project).id
        try:
            reporter_id = jira_issue.raw['fields']['reporter']['accountId']
            ontology_atomic_user_story.activated_by = team_member_application.retrive_by_external_id_and_project_name(reporter_id, jira_project.name).id
            if ontology_atomic_user_story.activated_by is None:
                raise Exception('Not found')
        except (NameError, TypeError):
            ontology_atomic_user_story.activated_by = None
        except Exception as e:
            team_member = etl_team_member()
            team_member.config(self.data)
            data_to_create = {'accountId': reporter_id}
            ontology_atomic_user_story.activated_by = team_member.create(data_to_create, None, jira_project).id
        try:
            assignee_id = jira_issue.raw['fields']['assignee']['accountId']
            ontology_atomic_user_story.closed_by = team_member_application.retrive_by_external_id_and_project_name(assignee_id, jira_project.name).id
            if ontology_atomic_user_story.closed_by is None:
                raise Exception('Not found')
        except (NameError, TypeError):
            ontology_atomic_user_story.closed_by = None
        except Exception as e:
            team_member = etl_team_member()
            team_member.config(self.data)
            data_to_create = {'accountId': assignee_id}
            ontology_atomic_user_story.closed_by = team_member.create(data_to_create, None, jira_project).id
        # ontology_atomic_user_story.story_points = TODO
        # ontology_atomic_user_story.created_date = TODO
        ontology_atomic_user_story.activated_date = self.date_formater(None if type(next(iter(jira_issue.raw['fields'].get('customfield_10018') or []), None)) != dict else self.resolve_start_date(jira_issue.raw['fields']['customfield_10018']))
        ontology_atomic_user_story.closed_date = self.date_formater(jira_issue.raw['fields'].get('duedate'))
        ontology_atomic_user_story.resolved_date = self.date_formater(jira_issue.raw['fields'].get('resolutiondate'))

        #Linkar no sprint
        sprints = jira_issue.raw['fields']['customfield_10020']
        if not sprints: # Check if is None or []
            ontology_atomic_user_story.sprint_backlogs = []
        else:
            backlogs_list = []
            for sprint in sprints:
                sprint_id = sprint['id']
                board_id = sprint['boardId']
                ontology_sprint_backlog = sprint_backlog_application.retrive_by_external_uuid(sprint_id)
                if ontology_sprint_backlog is None:
                    sprint_backlog = etl_sprint()
                    sprint_backlog.config(self.data)
                    data_to_create = {'content': {'all': {'sprint': {'id': sprint_id, 'originBoardId': board_id}}}}
                    _, ontology_sprint_backlog = sprint_backlog.create(data_to_create)
                backlogs_list.append(ontology_sprint_backlog)
            ontology_atomic_user_story.sprint_backlogs = backlogs_list

        return ontology_atomic_user_story
        
    def user(self, jira_user, 
    ontology_user = None):

        if ontology_user is None:
            ontology_user = factories_model.PersonFactory()
        ontology_user.organization = self.organization
        ontology_user.name = jira_user.displayName
        if jira_user.emailAddress != '':
            ontology_user.email = jira_user.emailAddress

        return ontology_user

    def task(self, etl_team_member, etl_user_story, etl_sprint,
    jira_issue, jira_project,
    ontology_scrum_intended_development_task = None, ontology_scrum_performed_development_task = None):

        # Ontology scrum intended development task
        team_member_application = factories.TeamMemberFactory()
        priority_application = factories.PriorityFactory()
        atomic_user_story_application = factories.AtomicUserStoryFactory()
        sprint_application = factories.SprintFactory()
        sprint_backlog_application = factories.SprintBacklogFactory()
        priority_dict = {'1': 'high', '2': 'high', '3': 'medium', '4': 'normal', '5': 'normal'}
        
        if ontology_scrum_intended_development_task is None:
            ontology_scrum_intended_development_task = factories_model.ScrumIntentedDevelopmentTaskFactory()
        ontology_scrum_intended_development_task.name = jira_issue.raw['fields']['summary']
        ontology_scrum_intended_development_task.description = jira_issue.raw['fields'].get('description')
        ontology_scrum_intended_development_task.created_date = self.date_formater(jira_issue.raw['fields']['created'])
        
        # Creator
        creator_id = jira_issue.raw['fields']['creator']['accountId']
        team_member = team_member_application.retrive_by_external_id_and_project_name(creator_id, jira_project.name)
        if team_member is None:
            # Create team_member
            team_member_ = etl_team_member()
            team_member_.config(self.data)
            data_to_create = {'accountId': creator_id}
            team_member = team_member_.create(data_to_create, None, jira_project)
        ontology_scrum_intended_development_task.created_by = team_member.id

        # Assignee
        assignee_id = jira_issue.raw['fields']['assignee']['accountId']
        team_member = team_member_application.retrive_by_external_id_and_project_name(assignee_id, jira_project.name)
        if team_member is None:
            # Create team_member
            team_member_ = etl_team_member()
            team_member_.config(self.data)
            data_to_create = {'accountId': creator_id}
            team_member = team_member_.create(data_to_create, None, jira_project)
        ontology_scrum_intended_development_task.assigned_by = [team_member]

        parent_id = jira_issue.raw['fields']['parent']['id']
        atomic_user_story = atomic_user_story_application.retrive_by_external_uuid(parent_id)
        if atomic_user_story is None:
            # Create atomic_user_story
            atomic_user_story_ = etl_user_story()
            atomic_user_story_.config(self.data)
            data_to_create = {"content": {"all": {"issue": {"id": parent_id } } } }
            atomic_user_story = atomic_user_story_.create(data_to_create, None, jira_project)
        ontology_scrum_intended_development_task.atomic_user_story = atomic_user_story.id
        
        ontology_scrum_intended_development_task.story_points = None
        ontology_scrum_intended_development_task.type_activity = None
        ontology_scrum_intended_development_task.priority = priority_application.retrive_by_name(priority_dict[jira_issue.raw['fields']['priority']['id']]).id
        ontology_scrum_intended_development_task.risk = None

        sprints = jira_issue.raw['fields']['customfield_10020']
        sprints_list = []
        backlogs_list = []
        if not sprints: # Check if is None or []
            ontology_scrum_intended_development_task.sprints = []
            ontology_scrum_intended_development_task.sprint_backlogs = []
        else:
            for sprint in sprints:
                sprint_id = sprint['id']
                board_id = sprint['boardId']
                ontology_sprint = sprint_application.retrive_by_external_uuid(sprint_id)
                ontology_sprint_backlog = sprint_backlog_application.retrive_by_external_uuid(sprint_id)
                if ontology_sprint is None: # Se não existe sprint, tbm não existe sprint_backlog
                    sprint_backlog = etl_sprint()
                    sprint_backlog.config(self.data)
                    data_to_create = {'content': {'all': {'sprint': {'id': sprint_id, 'originBoardId': board_id}}}}
                    ontology_sprint, ontology_sprint_backlog = sprint_backlog.create(data_to_create)
                sprints_list.append(ontology_sprint)
                backlogs_list.append(ontology_sprint_backlog)
            ontology_scrum_intended_development_task.sprints = sprints_list
            ontology_scrum_intended_development_task.sprint_backlogs = backlogs_list

        # Performed
        if (jira_issue.raw['fields']['status']['statusCategory']['id'] == 3 # Itens concluídos
        or jira_issue.raw['fields']['status']['statusCategory']['id'] == 4): # Em andamento
            
            # Ontology scrum performed development task
            if ontology_scrum_performed_development_task is None:
                ontology_scrum_performed_development_task = factories_model.ScrumPerformedDevelopmentTaskFactory()
            ontology_scrum_performed_development_task.name = jira_issue.raw['fields']['summary']
            ontology_scrum_performed_development_task.description = jira_issue.raw['fields'].get('description')
            ontology_scrum_performed_development_task.created_date = self.date_formater(jira_issue.raw['fields']['created'])

            # Creator
            creator_id = jira_issue.raw['fields']['creator']['accountId']
            team_member = team_member_application.retrive_by_external_id_and_project_name(creator_id, jira_project.name)
            if team_member is None:
                # Create team_member
                team_member_ = etl_team_member()
                team_member_.config(self.data)
                data_to_create = {'accountId': creator_id}
                team_member = team_member_.create(data_to_create, None, jira_project) 
            ontology_scrum_performed_development_task.created_by = team_member.id
            
            # Assignee
            assignee_id = jira_issue.raw['fields']['assignee']['accountId']
            team_member = team_member_application.retrive_by_external_id_and_project_name(assignee_id, jira_project.name)
            if team_member is None:
                # Create team_member
                team_member_ = etl_team_member()
                team_member_.config(self.data)
                data_to_create = {'accountId': creator_id}
                team_member = team_member_.create(data_to_create, None, jira_project)
            ontology_scrum_performed_development_task.assigned_by = [team_member]

            # Reporter
            reporter_id = jira_issue.raw['fields']['reporter']['accountId']
            team_member = team_member_application.retrive_by_external_id_and_project_name(reporter_id, jira_project.name)
            if team_member is None:
                # Create team_member
                team_member_ = etl_team_member()
                team_member_.config(self.data)
                data_to_create = {'accountId': creator_id}
                team_member = team_member_.create(data_to_create, None, jira_project)
            ontology_scrum_performed_development_task.activated_by = team_member.id
            
            # Assignee
            assignee_id = jira_issue.raw['fields']['assignee']['accountId']
            team_member = team_member_application.retrive_by_external_id_and_project_name(assignee_id, jira_project.name)
            if team_member is None:
                # Create team_member
                team_member_ = etl_team_member()
                team_member_.config(self.data)
                data_to_create = {'accountId': creator_id}
                team_member = team_member_.create(data_to_create, None, jira_project)
            ontology_scrum_performed_development_task.closed_by = team_member.id

            # Reporter
            reporter_id = jira_issue.raw['fields']['reporter']['accountId']
            team_member = team_member_application.retrive_by_external_id_and_project_name(reporter_id, jira_project.name)
            if team_member is None:
                # Create team_member
                team_member_ = etl_team_member()
                team_member_.config(self.data)
                data_to_create = {'accountId': creator_id}
                team_member = team_member_.create(self, data_to_create, None, jira_project)
            ontology_scrum_performed_development_task.resolved_by = team_member.id
            
            # User Story
            parent_id = jira_issue.raw['fields']['parent']['id']
            atomic_user_story_application = factories.AtomicUserStoryFactory()
            atomic_user_story = atomic_user_story_application.retrive_by_external_uuid(parent_id)
            if atomic_user_story is None:
                # Create atomic_user_story
                atomic_user_story_ = etl_user_story()
                atomic_user_story_.config(self.data)
                data_to_create = {"content": {"all": {"issue": {"id": parent_id } } } }
                atomic_user_story = atomic_user_story_.create(data_to_create, None, jira_project)
            ontology_scrum_performed_development_task.atomic_user_story = atomic_user_story.id
            
            ontology_scrum_performed_development_task.closed_date = self.date_formater(jira_issue.raw['fields'].get('duedate'))
            ontology_scrum_performed_development_task.activated_date = self.date_formater(None if type(next(iter(jira_issue.raw['fields'].get('customfield_10018') or []), None)) != dict else jira_issue.raw['fields']['customfield_10018'][0]['startDate'])
            ontology_scrum_performed_development_task.resolved_date = self.date_formater(jira_issue.raw['fields'].get('resolutiondate'))
            
            ontology_scrum_performed_development_task.sprints = sprints_list
            ontology_scrum_performed_development_task.sprint_backlogs = backlogs_list

            ontology_scrum_performed_development_task.caused_by = ontology_scrum_intended_development_task.id
        return ontology_scrum_intended_development_task, None

    def development_team(self, etl_scrum_project_team,
    jira_project,
    ontology_scrum_development_team = None):

        scrum_team_application = factories.ScrumTeamFactory()

        if ontology_scrum_development_team is None:
            ontology_scrum_development_team = factories_model.DevelopmentTeamFactory()
        ontology_scrum_development_team.organization = self.organization
        ontology_scrum_development_team.name = f"{jira_project.key}_scrum_development_team"
        try:
            project_id = jira_project.id
            ontology_scrum_development_team.scrum_team_id = scrum_team_application.retrive_by_external_uuid(jira_project.id).id
            if ontology_scrum_development_team.scrum_team_id is None:
                raise Exception('Not found')
        except Exception as e:
            scrum_project_team = etl_scrum_project_team()
            scrum_project_team.config(self.data)
            data_to_create = {'content': {'all': {'project': {'id': project_id}}}}
            ontology_scrum_development_team.scrum_team_id = scrum_project_team.create(data_to_create).id

        return ontology_scrum_development_team

    def team(self, etl_scrum_project, 
    jira_project,
    ontology_scrum_team = None):

        scrum_project_application = factories.ScrumAtomicProjectFactory()

        if ontology_scrum_team is None:
            ontology_scrum_team = factories_model.ScrumTeamFactory()
        ontology_scrum_team.name = f"{jira_project.key}_scrum_team"
        ontology_scrum_team.organization = self.organization
        try:
            project_id = jira_project.id
            ontology_scrum_team.scrum_project = scrum_project_application.retrive_by_external_uuid(jira_project.id).id
            if ontology_scrum_team.scrum_project is None:
                raise Exception('Not found')
        except Exception as e:
            scrum_project = etl_scrum_project()
            scrum_project.config(self.data)
            data_to_create = {'content': {'all': {'project': {'id': project_id}}}}
            scrum_project, _, _, _ = scrum_project.create(data_to_create)
            ontology_scrum_team.scrum_project = scrum_project.id

        return ontology_scrum_team