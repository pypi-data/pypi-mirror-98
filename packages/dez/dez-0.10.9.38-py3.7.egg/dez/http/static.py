from dez.logging import default_get_logger
from dez.http.server import HTTPResponse, HTTPVariableResponse
from dez.http.cache import NaiveCache, INotifyCache
from dez import io
import os, event
try:
    from urllib import parse # py3
except:
    import urllib as parse # py2.7

class StaticHandler(object):
    id = 0
    def __init__(self, server_name, get_logger=default_get_logger, timestamp=False, dir_404=False):
        StaticHandler.id += 1
        self.id = StaticHandler.id
        self.log = get_logger("StaticHandler(%s)"%(self.id,))
        self.log.debug("__init__")
        self.server_name = server_name
        self.timestamp = timestamp
        self.dir_404 = dir_404
        try:
            self.cache = INotifyCache(get_logger=get_logger)
        except:
            self.cache = NaiveCache(get_logger=get_logger)

    def __isi(self, req):
        ua = req.headers.get("user-agent")
        if ua:
            for iflag in ["iPad", "iPod", "iPhone"]:
                if iflag in ua:
                    return True
        return False

    def __respond(self, req, path=None, ctype=False, headers={}, data=[], stream=False):
        chunked = stream and not self.__isi(req)
        if chunked: # i devices choke on chunked media sometimes...
            response = HTTPVariableResponse(req)
        else:
            response = HTTPResponse(req)
        response.headers['Server'] = self.server_name
        response.headers["Accept-Range"] = "bytes"
        if self.timestamp and path:
            response.headers['Last-Modified'] = self.cache.get_mtime(path, True)
        if ctype:
            response.headers['Content-Type'] = self.cache.get_type(path)
        for header in headers:
            response.headers[header] = headers[header]
        if not path:
            response.status = "404 Not Found"
        for d in data:
            response.write(d)
        if stream:
            openfile = open(path, "rb")
            limit = os.stat(path).st_size
            if "range" in req.headers:
                rs, re = self.__range(req, response.headers, limit)
                rs and openfile.seek(rs)
                if re:
                    limit = re - rs
                response.status = "206 Partial Content"
            response.headers["Content-Length"] = str(limit)
            if chunked:
                self.__write_file(response, openfile, path, limit)
            else:
                response.write(openfile.read(limit))
                openfile.close()
                response.dispatch()
        else:
            response.dispatch()

    def __call__(self, req, prefix, directory):
        req.url = req.url.split("?")[0] # remove qs (sometimes used to get around caching)
        url = parse.unquote(req.url)
        if "*" in prefix: # regex
            path = directory + url
        else:
            path = os.path.join(directory, url[len(prefix):])
        self.log.debug("__call__", path)
        if ".." in path:
            return self.__404(req)
        try:
            isdir = os.path.isdir(path)
        except:
            return self.__404(req)
        if isdir:
            if not self._try_index(req, path):
                if self.dir_404:
                    return self.__404(req)
                if url.endswith('/'):
                    url = url[:-1]
                return self.__respond(req, data=[
                    '<b>%s</b><br><br>'%(url,),
                    "<a href=%s>..</a><br>"%(os.path.split(url)[0],)
                ] + ["<a href=%s>%s</a><br>"%(parse.quote("%s/%s"%(url,
                    child)),child) for child in os.listdir(path)])
        else:
            self.cache.get(req, path, self.__write, self.__stream, self.__404)

    def _try_index(self, req, path):
        indexp = os.path.join(path, "index.html")
        if os.path.isfile(indexp):
            req.url += "index.html"
            self.cache.get(req, indexp, self.__write, self.__stream, self.__404)
            return True
        return False

    def __range(self, req, headers, size):
        rs, re = req.headers["range"][6:].split("-")
        headers["Content-Range"] = "bytes %s-%s/%s"%(rs, re or (size - 1), size)
        return int(rs), re and int(re) or None

    def __write(self, req, path):
        data = self.cache.get_content(path)
        headers = {}
        if "range" in req.headers:
            rs, re = self.__range(req, headers, len(data))
            data = data[rs:re]
        self.__respond(req, path, True, headers, [data])

    def __stream(self, req, path):
        self.__respond(req, path, True, stream=True)

    def __404(self, req):
        self.__respond(req, data=[
            "<b>404</b><br>Requested resource \"<i>%s</i>\" not found" % (req.url,)
        ])

    def __write_file(self, response, openfile, path, limit):
        data = openfile.read(min(limit, io.BUFFER_SIZE))
        limit -= len(data)
        if not data:
            openfile.close()
            return response.end_or_close()
#        self.cache.add_content(path, data)
        event.timeout(0, response.write, data, self.__write_file, [response, openfile, path, limit])