#!/usr/bin/python

"""
Nerea Del Olmo Sanz - GITT
Ejercicio 9.6
"""


import webapp


class CacheApp (webapp.webApp):

    # Declare the dictionary whose keys are the URL in the resource
    dict_resourceURL = {}

    def parse(self, request):
        """Returns the resource name, NOT including '/' """

        verb = request.split(' ', 2)[0]
        resource = request.split(' ', 2)[1].replace('/', ' ').split(' ', 1)[1]

        return (verb, resource)

    def process(self, parsedRequest):
        """Process the relevant elements of the request.
        Finds the HTML text corresponding to the resource name.
        """

        (verb, resource) = parsedRequest

        if verb == "GET":
            urlList = "<b>URLs dictionary: </b><br>"
            urlList += str(self.dict_resourceURL.keys()) + "<br><br>"

            if resource == "":
                httpCode = "200 OK"
                htmlBody = "<html><body>" + urlList + "</body></html>"
            else:
                if resource in self.dict_resourceURL.keys():
                    URL = self.dict_resourceURL[resource]
                else:
                    URL = "http://" + resource
                    self.dict_resourceURL[resource] = URL

                httpCode = "302 FOUND\nLocation:" + URL
                htmlBody = ""

        else:
            httpCode = "400 BAD REQUEST"
            htmlBody = "<html><body><h3>Verb not available</h3></body></html>"

        return (httpCode, htmlBody)

if __name__ == "__main__":
    practica1 = CacheApp("localhost", 1234)
