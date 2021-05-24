# cihttp

cihttp is an extremely deficient HTTP server. It is also likely very insecure, consider not running it in production. Yet at the same time, its kind of awesome. Imagine you navigate to a website in your browser, a real browser like Firefox, and then a web page shows up; a web page that was served from your very own cihttp. Amazing. Stoke meter off the charts.

Overview
The Tic Tac Toe protocol was a simplistic protocol (a few commands) and stateful protocol (pregame, game, postgame). HTTP/1.0 is a browser friendly protocol that serves media-rich webpages. cihttp is a python implementation of this protocol.

A request message from a client to a server includes, within the first line of that message, the method to be applied to the resource, the identifier of the resource, and the protocol version in use.
Request       = Request-Line
                        *(( general-header
                         | request-header
                         | entity-header ) CRLF)
                        CRLF
                        [ message-body ]
                       


Example Request
Note: CRLF will be shown as \r\n

GET / HTTP/1.1\r\n
Host: localhost:9001\r\n
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:69.0) Gecko/20100101 Firefox/69.0\r\n
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n
Accept-Language: en-US,en;q=0.5\r\n
Accept-Encoding: gzip, deflate\r\n
Connection: keep-alive\r\n
Upgrade-Insecure-Requests: 1\r\n
Cache-Control: max-age=0\r\n
\r\n
