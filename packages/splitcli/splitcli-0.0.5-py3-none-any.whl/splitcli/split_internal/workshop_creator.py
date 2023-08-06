import sys
import time
import traceback

from splitcli.split_internal import org_internal
from splitcli.ux import menu

def print_users():
    orgs = org_internal.list_demo_orgs()
    menu.info_message("\nActive Demo Organizations")
    for org in orgs:
        menu.info_message(org['userEmail'] + " : " + org['userPassword'])

def create_orgs(org_creator):
    count = int(menu.text_input("# Organizations Needed"))
    # org_internal.delete_all_demo_orgs()
    menu.info_message("Creating Organizations")

    existing_orgs = org_internal.list_demo_orgs()
    total_orgs = len(existing_orgs)

    created_orgs = 0
    while created_orgs < count:
        try:
            org_creator()
            created_orgs += 1
        except KeyboardInterrupt as interrupt:
            menu.warn_message(f"Execution stopped by user, completed: {created_orgs} / {count}")
            cleanup_orgs(total_orgs + created_orgs)
            count = created_orgs
            break
        except Exception as exception:
            # Cleanup after failures
            menu.error_message("Error creating organization: " + str(exception))
            traceback.print_exc()
            cleanup_orgs(total_orgs + created_orgs)

    menu.info_message("\nOrganizations Created")
    # Output newly created orgs
    new_orgs = org_internal.list_demo_orgs()
    for i in range(total_orgs, len(new_orgs)):
        org = new_orgs[i]
        menu.info_message(org['userEmail'] + " : " + org['userPassword'])

def cleanup_orgs(expected_orgs):
    new_orgs = org_internal.list_demo_orgs()
    while len(new_orgs) > expected_orgs:
        latest_org_id = new_orgs[-1]['organizationId']
        org_internal.delete_demo_org(latest_org_id)
        menu.warn_message("Deleted failed org: " + latest_org_id)
        new_orgs = org_internal.list_demo_orgs()
    # Add buffer time in case of throttling
    time.sleep(.1)

def create_exp_orgs():
    create_orgs(lambda: org_internal.create_org_workshop_exp())

def create_imp_orgs():
    create_orgs(lambda: org_internal.create_org_workshop_imp())

def main_menu():
    admin_password = org_internal.admin_password()
    while True:
        menu.info_message("\nWelcome to the Split Workshop Tool!")
        if admin_password == None:
            admin_password = menu.password_input("Provide password for workshop@split.io")
        else:
            options = [
                {"option_name":"Setup Exp Workshop Organizations", "operation": lambda: create_exp_orgs()},
                {"option_name":"Setup Imp Workshop Organizations", "operation": lambda: create_imp_orgs()},
                {"option_name":"List Demo Organization Logins", "operation": lambda: print_users()},
                {"option_name":"Delete Demo Organizations", "operation": lambda: org_internal.delete_all_demo_orgs()},
                {"option_name":"Exit", "operation": lambda: sys.exit()}
            ]
            title = "Please select your option:"
            menu.select_operation(title, options)

main_menu()