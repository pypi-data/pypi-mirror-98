
def delete_traffic_type(session, traffic_type_id):
    url = f"https://app.split.io/internal/api/trafficTypes/{traffic_type_id}"
    session.delete(url, headers={'Split-CSRF': session.cookies['split-csrf']})