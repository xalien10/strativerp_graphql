from reporting.models import ReportedHour
from project.models import ProjectEmployee


def run():
    try:
        pr_em = ProjectEmployee.objects.filter(project__project_type='internal')
        for pr_em_obj in pr_em:
            rh = ReportedHour.objects.filter(project_employee=pr_em_obj)
            for rh_obj in rh:
                rh_obj.is_billable = False
                rh_obj.save()
    except Exception as e:
        print(str(e))
        return "Successfully converted billable hours into non-billable in the internal projects" + str(e)
    return "Successfully converted billable hours into non-billable in the internal projects"
