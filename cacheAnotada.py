#!/usr/bin/python

"""
Nerea Del Olmo Sanz - GITT
Ejercicio 9.7: Cache de contenidos anotado
"""


import webapp
import urllib2


class CacheApp (webapp.webApp):

    # Declare the dictionary whose keys are the HTML saved in cache memmory
    dict_cache = {}
    lastHTTP = ""

    def parse(self, request):
        """ Returns the resource (URL and additional resource) name,
            NOT including '/'
        """
        request = request.split(' ', 2)
        verb = request[0]
        resources = request[1].split('/')[1:]
        if len(resources) == 1:
            url = resources[0]
            optionalResource = ""
        elif len(resources) > 1:
            url = resources[0]
            optionalResource = resources[1]
        headerBrow = request[2]

        return (verb, url, optionalResource, headerBrow)

    def process(self, parsedRequest):
        """ Process the relevant elements of the request.
            Finds the HTML text corresponding to the resource name.
        """
        (verb, url, optionalResource, headerBrow) = parsedRequest

        if verb == "GET":
            if url == "":
                httpCode = "200 OK"
                htmlBody = "<html><body><h1>Type "
                htmlBody += '"localhost:12340/url/optionalResource"</h1><br>'
                htmlBody += "<p>Optional resources: "
                htmlBody += "/reload /server-side /client-side </p>"
                htmlBody += "</body></html>"
                self.lastHTTP = httpCode

            elif optionalResource == "":
                try:
                    request = urllib2.urlopen("http://" + url)
                    html = request.read()
                    self.headerServ = request.info()
                    self.dict_cache[url] = html

                    # Looking for tag "<body>"
                    body_tag = html.find('<body')
                    html = html[body_tag:]
                    body_tag = html.find('>')

                    httpCode = "200 OK"
                    htmlBody = html[:body_tag+1]
                    htmlBody += "<h1>Resource options</h1>"
                    htmlBody += '<HR align="left" size="2" width="300"'
                    htmlBody += 'color="black" noshade>'
                    htmlBody += "<ul type=square>"
                    htmlBody += '<li><a href="http://' + url + '" targer="_blank"'
                    htmlBody += ">Original webpage</a></li>"
                    htmlBody += "<li><a href=http://localhost:12340/" + url
                    htmlBody += "/reload>Reload</a></li>"
                    htmlBody += "<li><a href=http://localhost:12340/" + url
                    htmlBody += "/server-side>Server-side</a></li>"
                    htmlBody += "<li><a href=http://localhost:12340/" + url
                    htmlBody += "/client-side>Client-side</a></li>"
                    htmlBody += "</ul>" + html
                    self.lastHTTP = httpCode

                except:
                        httpCode = "400 BAD REQUEST"
                        htmlBody = "<html><body><h1>EXCEPTION!<br>Type "
                        htmlBody += '"localhost:12340/url/optionalResource"'
                        htmlBody += "</h1><br>'<p>Optional resources: "
                        htmlBody += "/reload /cache /header</p>"
                        htmlBody += "</body></html>"
                        self.lastHTTP = httpCode

            elif optionalResource == "reload":
                httpCode = "200 OK"
                htmlBody = urllib2.urlopen("http://" + url).read()
                self.lastHTTP = httpCode


            elif optionalResource == "server-side":
                try:
                    httpCode = "200 OK"
                    htmlBody = "<html><body><h3>Browser headers:</h3>"
                    htmlBody += "<p>" + headerBrow + "</p><br>"
                    htmlBody += "<h3>Server headers:</h3><p>"
                    htmlBody += str(self.headerServ) + "</p></body></html>"
                    self.lastHTTP = httpCode
                except AttributeError:
                    httpCode = "404 NOT FOUND"
                    htmlBody = "<html><body><h1>No HTTP iterations yet."
                    htmlBody += "</h1></body></html>"
                    self.lastHTTP = httpCode

            elif optionalResource == "client-side":
                if url in self.dict_cache:
                    try:
                        request = urllib2.urlopen("http://" + url)
                        html = request.read()
                        self.headerServ = request.info()
                        self.dict_cache[url] = html

                        httpCode = "200 OK"
                        htmlBody = "<html><body><h1>CACHE</h1>"
                        htmlBody += "<h3>Browser headers: </h3>"
                        htmlBody += "<p>" + headerBrow + "</p><br>"
                        htmlBody += "<h3>Client HTTP (app):</h3><p>"
                        htmlBody += self.lastHTTP + "</p></body></html>"
                        self.lastHTTP = httpCode

                    except AttributeError:
                        httpCode = "404 NOT FOUND"
                        htmlBody = "<html><body><h1>No HTTP iterations yet."
                        htmlBody += "</h1></body></html>"
                        self.lastHTTP = httpCode
                else:
                    httpCode = "404 NOT FOUND"
                    htmlBody = "<html><body><h1>No contents in cache for "
                    htmlBody += str(url) + ".</h1></body></html>"
                    self.lastHTTP = httpCode

            else:
                httpCode = "404 NOT FOUND"
                htmlBody = "<html><body><h1>"
                htmlBody += "Resource not available</h1></body></html>"
                self.lastHTTP = httpCode

        else:
            httpCode = "400 BAD REQUEST"
            htmlBody = "<html><body><h1>Verb not available</h1></body></html>"
            self.lastHTTP = httpCode

        return (httpCode, htmlBody)

if __name__ == "__main__":
    practica1 = CacheApp("localhost", 12340)
