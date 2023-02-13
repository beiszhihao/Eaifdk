var http=require("http");
var fs=require("fs");
var url=require("url");

var IP='xxx.xxx.xxx.xxx';
var PORT=0000;

var server=http.createServer(function(req,res){
	var pathname=url.parse(req.url).pathname;
	if(pathname.search('css') != -1){
		var css = fs.readFileSync(__dirname + '/' + req.url);
		res.writeHead(200,{"Content-Type": "text/css"});
		res.write(css);
		res.end();
		return;
	}
	if(pathname.search('jpg') != -1){
    		var jpg = fs.readFileSync(__dirname + '/' + req.url);
		res.writeHead(200,{"Content-Type": "image/jpeg"});
		res.write(jpg);
		res.end();
		return;
  	}
	
	var html = fs.readFileSync(__dirname + '/' + 'index.html');
	res.writeHead(200,{"Content-Type": "text/html"});
	res.write(html);
	res.end();

}).listen(PORT, IP);

console.log('Server running at http://'+ IP + ':' + PORT + '/');
