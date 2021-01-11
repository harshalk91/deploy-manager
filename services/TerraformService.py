# This service is to execute Terraform hardware stack using python library.
from python_terraform import *

class TerraformService:
    def __init__(self):
        self.terraform_obj = Terraform()

    def process_terraform_vars(self):
        pass

    def terraform_init(self, terraform_root_path=None):
        print("Running Terraform init please wait....")
        return_code, stdout, stderr = self.terraform_obj.init(dir_or_plan=terraform_root_path)

        return return_code, stdout, stderr

    def terraform_plan(self, state_file=None, terraform_vars=None):
        plan_kwargs = dict()
        plan_kwargs["state"] = state_file,
        plan_kwargs["var"] = terraform_vars
        print("Running Terraform plan please wait....")
        return_code, stdout, stderr = self.terraform_obj.plan(no_color=IsFlagged,
                                                              refresh=False,
                                                              capture_output=True,
                                                              **plan_kwargs)
        return return_code, stdout, stderr

    def terraform_apply(self):
        pass

    def terraform_destroy(self):
        pass