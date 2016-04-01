TOP = "<div class='top'>Middleware TOP</div>"
BOTTOM = "<div class='botton'>Middleware BOTTOM</div>"

def app(environ, start_response): 
    start_response('200 OK', [('Content-Type', 'text/html')])
    path = environ['PATH_INFO'] # считываем путь 
	# анализируем путь и корректируем его
    pathResult = '/' + path 
    if pathResult == '/':
            pathResult ='/index.html' 
    file = open(pathResult, 'r')
    return [file.read()]

class WSGIMiddleware(app): # Прослойка middleware
    def __init__(self, app): 
        self.app = app
    def __call__(self, environ, start_response):
		# получаем html страницу, которую будем изменять
        resultHTML = self.app(environ, start_response)[0] 
		# если страница иммет body, то мы  лишь добавляем в него TOP и BOTTOM
		# сначала всталяя TOP полсле <body>
		# послее вставляя BOTTOM перед </body>
		# с помощью оразделителя split
        if (resultHTML.find('<body>') >= 0):	 
        	# делим html страницу на три части - до <body>, содержимое самого тела и после </body>
            beginHTML, bodyHTML	= 	resultHTML.split('<body>')
            bodyHTML, endHTML 	= 	bodyHTML.split('<body>')
            resultHTML = beginHTML + '\n<body>\n' + TOP + '\n' + bodyHTML + '\n' + BOTTOM + '\n</body>\n' + endHTML # add TOP, BOTTOM
		# если страница не иммет body, то мы сначала добавляем перед </html> само тело 
		# и лишь потом в body добавляем TOP и BOTTOM
		# с помощью оразделителя split		
		else:
			beginHTML, endHTML = resultHTML.split('</html>')
			resultHTML = beginHTML + '\n<body>\n' + TOP + '\n' + BOTTOM + '\n</body>'+ '\n</html>'
		# возвращаем полученный результат - страница html со вставленныйми в него TOP и BOTTOM
        return resultHTML

app = WSGIMiddleware(app) # Прослойка middleware

if __name__ == '__main__':
    from paste.httpserver import serve

    serve(app, host='localhost', port=8000)
