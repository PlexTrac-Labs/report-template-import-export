import api.request_handler as request

#----------Report Template Endpoints----------
def list(base_url, headers, tenant_id):
    name = "List Report Templates"
    root = "/api/v1"
    path = f'/tenant/{tenant_id}/report-templates'
    return request.get(base_url, root, path, name, headers)

def get(base_url, headers, tenant_id, report_template_id):
    name = "Get Report Template"
    root = "/api/v1"
    path = f'/tenant/{tenant_id}/report-template/{report_template_id}'
    return request.get(base_url, root, path, name, headers)

def import_from_json(base_url, headers, tenant_id, payload):
    name = "Import Report Template"
    root = "/api/v1"
    path = f'/tenant/{tenant_id}/report-template'
    return request.put(base_url, root, path, name, headers, payload)

def export_to_json(base_url, headers, tenant_id, payload):
    name = "Export Report Template"
    root = "/api/v1"
    path = f'/tenant/{tenant_id}/report-template'
    return request.post(base_url, root, path, name, headers, payload)
