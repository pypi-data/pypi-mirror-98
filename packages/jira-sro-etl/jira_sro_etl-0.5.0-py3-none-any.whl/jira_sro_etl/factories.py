import factory
from .product_backlog import product_backlog
from .scrum_development_task import scrum_development_task
from .scrum_project import scrum_project
from .scrum_project_team import scrum_project_team
from .scrum_development_team import scrum_development_team
from .sprint import sprint
from .team_member import team_member
from .user_story import user_story
from .epic import epic
from .user import user
from .sprint_backlog import sprint_backlog

from sro_db.model.activity.models import *
from sro_db.model.artifact.models import *
from sro_db.model.core.models import *
from sro_db.model.organization.models import *
from sro_db.model.process.models import *
from sro_db.model.stakeholder.models import *
from sro_db.model.stakeholder_participation.models import *

class product_backlogFactory(factory.Factory):
	class Meta:
		model = product_backlog
		  
class scrum_development_taskFactory(factory.Factory):
	class Meta:
		model = scrum_development_task

class ScrumIntentedDevelopmentTaskFactory(factory.Factory):
    class Meta:
        model = ScrumIntentedDevelopmentTask

class ScrumPerformedDevelopmentTaskFactory(factory.Factory):
    class Meta:
        model = ScrumPerformedDevelopmentTask
		  
class scrum_projectFactory(factory.Factory):
	class Meta:
		model = scrum_project
		  
class scrum_project_teamFactory(factory.Factory):
	class Meta:
		model = scrum_project_team
		  
class scrum_development_teamFactory(factory.Factory):
	class Meta:
		model = scrum_development_team
		  
class sprintFactory(factory.Factory):
	class Meta:
		model = sprint
		  
class team_memberFactory(factory.Factory):
	class Meta:
		model = team_member
		  
class user_storyFactory(factory.Factory):
	class Meta:
		model = user_story
		  
class epicFactory(factory.Factory):
	class Meta:
		model = epic
		  
class userFactory(factory.Factory):
	class Meta:
		model = user
		  
class sprint_backlogFactory(factory.Factory):
	class Meta:
		model = sprint_backlog

		  

