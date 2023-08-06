from flask import request

def webevidence(request):

    """!
    Get evidence from a web request (gets headers, cookies and query parameters)
    
    @type request: Request 
    @param request: A Request object
    @rtype dict
    @return A dictionary of web evidence that can be using in flowdata.evidence.add_from_dict()

    """

    webevidence = {}

    for header in request.headers:
        webevidence["header." + header[0].lower()] = header[1]

    for cookieKey, cookieValue in request.cookies.items():
        webevidence["cookie." + cookieKey] = cookieValue

    for query,value in request.args.items():

        webevidence["query." + query] = value
    
    webevidence["server.client-ip"] =  request.remote_addr

    webevidence["server.host-ip"] =  request.host

    if (request.is_secure):
        webevidence["header.protocol"] = "https"
    else:
        webevidence["header.protocol"] = "http"

    return webevidence
