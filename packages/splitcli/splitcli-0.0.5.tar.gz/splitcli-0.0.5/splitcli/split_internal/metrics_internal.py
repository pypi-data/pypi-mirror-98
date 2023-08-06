def list_metrics(session, org_id):
    url = f"https://app.split.io/internal/api/organization/{org_id}/metrics"
    response = session.get(url, headers={'Split-CSRF': session.cookies['split-csrf']})
    return response.json()

def delete_metric(session, org_id, metric_id):
    url = f"https://app.split.io/internal/api/organization/{org_id}/metrics/{metric_id}"
    session.delete(url, headers={'Split-CSRF': session.cookies['split-csrf']})

def delete_metrics(session, org_id):
    metrics = list_metrics(session, org_id)
    for metric in metrics['data']:
        delete_metric(session, org_id, metric['id'])
