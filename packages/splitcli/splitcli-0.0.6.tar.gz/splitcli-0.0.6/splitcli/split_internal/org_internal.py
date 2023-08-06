from splitcli.accounts import user
from splitcli.split_internal import login_internal, metrics_internal, traffictypes_internal, workshop_experiment, eventtypes_internal
from splitcli.split_apis import splits_api, workspaces_api, segments_api, traffic_types_api
from splitcli.ux import menu
from splitcli.splitio_selectors import split_selectors, definition_selectors

def admin_user():
    return 'workshop@split.io'

def admin_password():
    return 'Workshop_12345' # input('Provide Workshop Account Password: ')

_admin_session = None
def admin_session():
    global _admin_session
    if _admin_session == None:
        _admin_session = login_internal.login(admin_user(), admin_password())
    return _admin_session

def demo_base_url():
    return 'https://app.split.io/internal/api/splitAdmin/organization'

def demo_email_url():
    email = admin_user()
    base_url = demo_base_url()
    return f'{base_url}?email={email}'

def demo_org_url(org_id):
    base_url = demo_base_url()
    return f'{base_url}/{org_id}'

def create_org_workshop_imp():
    menu.success_message("Creating Implementation Workshop Organization")
    session = admin_session()
    response = session.post(demo_email_url(), headers={'Split-CSRF': session.cookies['split-csrf']})
    
    result = response.json()
    org_id = result['organizationId']

    menu.success_message("Logging in as User")
    user_session = login_internal.login(result['userEmail'],result['userPassword'])

    # Internal Actions
    menu.success_message("Deleting Metrics & Event Types")
    metrics_internal.delete_metrics(user_session, org_id)
    eventtypes_internal.delete_all_event_types(user_session, org_id)
    menu.success_message("Creating Admin Token")
    admin_token = login_internal.create_admin_token(user_session, org_id)

    # Shift Scope for External API actions
    base_user = user.get_user()
    org_user = user.User(admin_token, "", "", "", "", "")
    user.set_user(org_user)

    # External Actions
    workspaces = workspaces_api.list_workspaces()
    for workspace in workspaces:
        menu.success_message("Clearing Workspace: " + workspace["name"])
        splits_api.delete_all_splits(workspace["id"])
        segments_api.delete_all_segments(workspace["id"])

        traffic_types = traffic_types_api.list_traffic_types(workspace["id"])
        # Internal again
        for traffic_type in traffic_types:
            if traffic_type['name'] != 'user':
                traffictypes_internal.delete_traffic_type(user_session, traffic_type['id'])
    
    # Return scope to base_user
    user.set_user(base_user)

    menu.success_message("Organization created")

    return result

def create_org_workshop_exp():
    menu.success_message("Creating Experimentation Workshop Organization")
    session = admin_session()
    response = session.post(f'https://app.split.io/internal/api/splitAdmin/organization?email={admin_user()}', headers={'Split-CSRF': session.cookies['split-csrf']})

    result = response.json()
    org_id = result['organizationId']

    menu.success_message("Logging in as User")
    user_session = login_internal.login(result['userEmail'],result['userPassword'])

    # Internal Actions
    menu.success_message("Modifying Settings")
    enable_recalculations(org_id)
    disable_mcc(user_session, org_id)
    menu.success_message("Deleting Metrics & Event Types")
    metrics_internal.delete_metrics(user_session, org_id)
    eventtypes_internal.delete_all_event_types(user_session, org_id)
    menu.success_message("Creating Admin Token")
    admin_token = login_internal.create_admin_token(user_session, org_id)

    # Shift Scope for External API actions
    base_user = user.get_user()
    org_user = user.User(admin_token, "", "", "", "", "")
    user.set_user(org_user)

    # External Actions
    workspaces = workspaces_api.list_workspaces()
    for workspace in workspaces:
        menu.success_message("Clearing Workspace: " + workspace["name"])
        splits_api.delete_all_splits(workspace["id"])
        segments_api.delete_all_segments(workspace["id"])

        traffic_types = traffic_types_api.list_traffic_types(workspace["id"])
        # Internal again
        for traffic_type in traffic_types:
            if traffic_type['name'] != 'user':
                traffictypes_internal.delete_traffic_type(user_session, traffic_type['id'])
    
    # Create and ramp onboarding_v2
    split_name = "onboarding_v2"
    workspace_id = workspaces_api.get_workspace("Default")["id"]
    split_selectors.create_split_operator(workspace_id, "user", split_name)
    definition_selectors.ramp_split_operator(workspace_id, "Prod-Default", split_name, ramp_percent=50)
    
    # Run Experiment
    sdk_token = login_internal.sdk_token(user_session, org_id)
    workshop_experiment.run_experiment(sdk_token, split_name)
    
    # Return scope to base_user
    user.set_user(base_user)

    menu.success_message("Organization created")

    return result

def list_demo_orgs():
    session = admin_session()
    response = session.get(demo_email_url(), headers={'Split-CSRF': session.cookies['split-csrf']})
    try:
        return response.json()
    except:
        return []

def delete_demo_org(org_id):
    session = admin_session()
    session.delete(demo_org_url(org_id), headers={'Split-CSRF': session.cookies['split-csrf']})

def delete_all_demo_orgs():
    orgs = list_demo_orgs()
    for org in orgs:
        delete_demo_org(org['organizationId'])

def enable_recalculations(org_id):
	session = admin_session()
	url = f"https://app.split.io/internal/api/plans/organization/{org_id}/limits"
	data = [
	  {
	    "orgId": org_id,
	    "limitValue": 1,
	    "limitKey": "metricsCalculation",
	    "type": "SERVICE",
	    "hidden": True
	  },
	  {
	    "orgId": org_id,
	    "limitValue": 100,
	    "limitKey": "metrics",
	    "type": "SERVICE",
	    "hidden": False
	  }
	]
	session.put(url, json=data, headers={'Split-CSRF': session.cookies['split-csrf']})

def disable_mcc(session, org_id):
	data = {
	  "organizationId": org_id,
	  "typeOneThreshold": 0.05,
	  "typeTwoThreshold": 0.2,
	  "reviewPeriod": 86400000, # Set review period to 1 day
	  "monitoringWindow": 86400000,
	  "multipleComparisonCorrection": "NONE", # Disable MCC
	  "monitorSignificanceThreshold": 0.05,
	  "minimumSampleSize": 355
	}
	session.post(f'https://app.split.io/internal/api/organization/{org_id}/results/settings', json=data, headers={'Split-CSRF': session.cookies['split-csrf']})
