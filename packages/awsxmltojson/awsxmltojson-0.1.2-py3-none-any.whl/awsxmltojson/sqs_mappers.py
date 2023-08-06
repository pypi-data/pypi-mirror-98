class SQSMappers:
    def ListQueuesResponse(xmldict):
        queue_urls = list(xmldict["ListQueuesResponse"]["ListQueuesResult"].values())
        return {"ListQueuesResponse": {"ListQueuesResult": {"queueUrls": queue_urls}}}
