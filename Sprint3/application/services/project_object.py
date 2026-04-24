class ProjectNode:
    def __init__(self, project_id, title, due_date, manager_id, description):
        self.project_id = project_id
        self.title = title  #project title
        self.date = due_date  # datetime.date
        self.manager_id = manager_id    #project manager id
        self.description = description  #project description
