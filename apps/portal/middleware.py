"""
Security and indexing middleware for idesignweb member portal.
Enforces strict noindex and noarchive headers on all authenticated portal routes.
"""

class PortalSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Enforce noindex and non-cacheable directives on private/administrative routes
        private_prefixes = ('/portal/', '/login/', '/admin/')
        if any(request.path.startswith(prefix) for prefix in private_prefixes):
            response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
            response['Cache-Control'] = 'private, no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            
        return response
