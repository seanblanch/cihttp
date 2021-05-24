# Sean Blanchard
#4/13/2021
#Comp 429

#Project 2 - Simple HTTP server.

import socket, logging, threading
import os
import time
import urllib.parse

# Comment out the line below to not print the INFO messages
logging.basicConfig(level=logging.INFO)

class HttpRequest():
    def __init__(self, requeststr):
        self.rstr = requeststr
        self.rjson = {}
        self.parse_string()


    def parse_string(self):
        #Parse the HTTP Request into a JSON object.,

        string_lines = self.rstr.split('\r\n')
        request_line = string_lines[0].split(' ')

        #Handle the request line parsing
        self.rjson['request-line'] = {
            'method': request_line[0],
            'URI': request_line[1],
            'version': request_line[2]
        }
        #for line_num in range(1, len(string_lines)):
            #print('{:02d}: {:s}'.format(line_num, string_lines[line_num]))

        #Handle the Headers parsing
        blank_index = string_lines.index('')
        self.rjson['headers'] = {}
        header_lines = string_lines[1:blank_index]
        for header_line in header_lines:
            colon_index = header_line.index(':')
            header_key = header_line[0:colon_index]
            header_value = header_line[colon_index+1:].strip()
            self.rjson['headers'][header_key] = header_value

        #Handle the body parsing
        body = '\r\n'.join(string_lines[blank_index+1:])
        self.rjson['body'] = body
        

            #lines = self.rstr.splitlines()
            #blank_line_index = lines.index('')
            #headers = lines[:blank_line_index]


    def display_request(self):
        print(self.rjson)



class ClientThread(threading.Thread):
    def __init__(self, address, socket):
        threading.Thread.__init__(self)
        self.csock = socket
        logging.info('New connection added.')


    def run(self):
        # exchange messages
        request = self.csock.recv(1024)
        req = request.decode('utf-8')
        logging.info('Recieved a request from client: ' + req)

        httpreq = HttpRequest(req)

        httpreq.display_request()

        #A way to grab the method and uri and store those values
        method = httpreq.rjson['request-line']['method']
        uri = httpreq.rjson['request-line']['URI']

        not_found_string = "HTTP/1.1 404 File not found.\r\nContent-length: 0\r\nServer: cihttp\r\nLast-Modified: N/A\r\n\r\n"
        #format the filepath
        file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "www/{:s}".format(uri)))
        if os.path.exists(file_path):
            #Get the last time the file was edited
            time = os.path.getmtime(file_path)

            seconds = time
            seconds_in_day = 60 * 60 * 24
            seconds_in_hour = 60 * 60
            seconds_in_minute = 60

            days = seconds // seconds_in_day
            hours = (seconds - (days * seconds_in_day)) // seconds_in_hour
            minutes = (seconds - (days * seconds_in_day) - (hours * seconds_in_hour)) // seconds_in_minute

            total_days = (days, hours, minutes)
            total_days_response = 'total days: ', days, ' Total hours: ', hours, ' Total minutes: ', minutes

            #get the content-length of file. (File size?)

            file_size = os.path.getsize(file_path)
            #If method returns HEAD
            #The HEAD method asks for a response identical to that of a GET request, but without the response body.
            if method == 'HEAD':
                head_string = "HTTP/1.1 200 OK.\r\nContent-length: {}\r\nServer: cihttp\r\nLast-Modified: {}\r\n\r\n".format(file_size, total_days_response)
                self.csock.send(head_send.encode('utf-8'))

            #If method returns GET OR POST
            #The GET method requests a representation of the specified resource. Requests using GET should only retrieve data.
            if method == 'GET' or method == 'POST':
                with open(file_path, 'r') as file_open:
                    file_string = file_open.read()
                get_string = "HTTP/1.1 200 OK.\r\nContent-length: {}\r\nServer: cihttp\r\nLast-Modified: {}\r\n\r\n{}".format(file_size, total_days_response, file_string)
                self.csock.send(get_string.encode('utf-8'))
        
        #If POST contains a post test
        #decode the body
        elif method == 'POST' and uri == '/post_test':
            #figure out what name and course is using python parse url encoded string
            request_body_form_encoded = httpreq.rjson['body']
            decoded_body = urllib.parse.unquote(request_body_form_encoded)
            print('test here')
            print(decoded_body)
            bad_chars = ['&']
            final_decoded_body = ''.join(i for i in decoded_body if not i in bad_chars)
            print(final_decoded_body)
            response_body = '<!DOCTYPE html><html><body>Sucessful post request.</body></html>'
            content_length = len(bytes(response_body, 'utf-8'))
            post_string = "HTTP/1.1 200 OK.\r\nContent-length: {}\r\nServer: cihttp\r\nLast-Modified: {}\r\n\r\n{}".format(content_length, '', final_decoded_body)
            self.csock.send(post_string.encode('utf-8'))
        # A status code 404 should be sent when a file is not found. Along with some HTML to say "File not found"
        else:
            self.csock.send(not_found_string.encode('utf-8'))

        

        # send a response
        #self.csock.send(b"")

        # disconnect client
        self.csock.close()
        logging.info('Disconnect client.')


def server():
    logging.info('Starting cihttpd...')

    # start serving (listening for clients)
    port = 9001
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost',port))

    while True:
        sock.listen(1)
        logging.info('Server is listening on port ' + str(port))

        # client has connected
        sc,sockname = sock.accept()
        logging.info('Accepted connection.')
        t = ClientThread(sockname, sc)
        t.start()


server()