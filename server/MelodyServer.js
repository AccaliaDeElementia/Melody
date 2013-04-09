/*jslint node: true, regexp: true */
'use strict';

function handler(req, res) {
    res.writehead(400);
    res.end('Expect Websocket Connection Only');
}

var app = require('http').createServer(handler),
    net = require('net'),
    io = require('socket.io').listen(app, {'log level': 0});

app.listen(4446);

function parseLine(line) {
    function createLine(code, name, message) {
        return {
            code: parseInt(code, 10),
            name: name,
            message: message
        };
    }
    var matches = [[/^(\d+)\s+([^:]+)$/, 1, 2, 2],
            [/^(\d+)\s+([\d:\/\-]+)\s+(\S+)$/, 1, 3, 2],
            [/^(\d+)\s+([^:]+):\s+([\w\W]+)$/, 1, 2, 3]],
        value;
    if (!line) { return; }
    matches.forEach(function (cfg) {
        var match = line.match(cfg[0]);
        if (match) {
            value = createLine(match[cfg[1]], match[cfg[2]], match[cfg[3]]);
        }
    });
    if (!matches) {
        value = createLine(400, 'BAD DATA', line);
    }
    return value;
}

function parseLines(data) {
    return data.toString().split('\n').map(parseLine).filter(function(item) {
        return item && item.code !== 132;
    });
}

function createResponse(message, extra, nonce) {
    if (!extra) { extra = {}; }
    if (!nonce) { nonce = (new Date()).getTime(); }
    return {code: message.code, message: message, extra: extra, nonce: nonce};
}

function parseError(lines, nonce) {
    var reason = lines.filter(function(item) {
            return item.code >= 300;
        }).map(function(item) { return item.message; }).join('\n'),
        extra = {};
    lines.filter(function(item) { return item.code < 200; }).
        forEach(function(item) { extra[item.name] = item.message; });

    return createResponse({code: 400, name: 'Error',  message: reason},
        extra, nonce);
}

function parseSimple(lines, nonce) {
    var result, extra = {};
    lines.forEach(function(item) {
        if (item.code < 200) {
            extra[item.name] = item.message;
        } else if (item.code >= 200 && item.code < 300) {
            result = item;
        }
    });
    return createResponse(result, extra, nonce);
}

function parseData(lines, nonce) {
    var started, stopped, message = {code: 200}, extra = {};
    lines.forEach(function(item) {
        if ((!started || stopped) && item.code < 200) {
            extra[item.name] = item.message;
        } else if (item.code === 203) {
            started = true;
        } else if (item.code === 204) {
            stopped = true;
        } else if (started && !stopped && item.code < 200) {
            if (!message[item.name]) {
                message[item.name] = [];
            }
            message[item.name].push(item.message);
        }
    });
    return createResponse(message, extra, nonce);
}

function parseComplexData(lines, nonce) {
    var started, stopped, message = [], extra = {}, i = {};
    lines.forEach(function(item) {
        if ((!started || stopped) && item.code < 200) {
            extra[item.name] = item.message;
        } else if (item.code === 203) {
            if (started) {
                message.push(i);
            }
            i = {};
            started = true;
        } else if (item.code === 204) {
            message.push(i);
            i = {};
            stopped = true;
        } else if (started && !stopped && item.code < 200) {
            i[item.name] = item.message;
        }
    });
    return createResponse({code: 200, message: message}, extra, nonce);
}

function parseResponse(lines, nonce) {
    var isError, isData, isComplex, preamble, prior, dataEnd, result;
    lines = parseLines(lines).filter(function(line) {
        if (line.code === 117) { preamble = true; }
        var result = (preamble && prior) || line.code >= 300;
        if (line.code === 117) { prior = true; }
        return result;
    });
    prior = undefined;
    lines.forEach(function(line) {
        if (line.code >= 300) { isError = true; }
        if (line.code === 203) { isData = true; }
        if (line.code === 204) { dataEnd = true; }
        if (isData && !dataEnd && prior && prior !== line.code) {
            isComplex = true;
        }
        if (isData && line.code < 200) { prior = line.code; }
    });

    if (isError) {
        result = parseError(lines, nonce);
    } else if (isComplex) {
        result = parseComplexData(lines, nonce);
    } else if (isData) {
        result = parseData(lines, nonce);
    } else {
        result = parseSimple(lines, nonce);
    }
    return result;
}

io.on('connection', function(socket) {
    net.connect({port: 4445}, function() {
    }).on('data', function(data) {
        parseLines(data).forEach(function(item) {
            socket.emit('stream', createResponse(item));
        });
    }).on('error', function(err) {
        console.error(err);
    });

    socket.on('command', function(cmd) {
        var lines = '', piano;
        piano = net.connect({port: 4445}, function() {
            piano.end(cmd.text + '\n');
        }).on('data', function(data) {
            lines += data;
        }).on('end', function() {
            socket.emit('response', parseResponse(lines, cmd.nonce));
        });
    });
});
