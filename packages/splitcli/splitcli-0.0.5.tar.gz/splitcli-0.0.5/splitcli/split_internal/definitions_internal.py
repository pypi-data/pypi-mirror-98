from splitcli.split_apis import splits_api

def force_calculation(session, org_id, definition):
	definition_id = definition['id']
	version = definition['lastUpdateTime']
	url = f"https://app.split.io/internal/api/organization/{org_id}/metrics/results/tests/{definition_id}/version/{version}/force"
	session.get(url, headers={'Split-CSRF': session.cookies['split-csrf']})