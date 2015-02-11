var express = require('express');
var path = require('path');
var favicon = require('static-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

var app = express();
//var env = process.env.NODE_ENV = process.env.NODE_ENV || 'development';
var env = process.env.RTALK_MODE = process.env.RTALK_MODE || 'development';

app.use(favicon('./../public/favicon.ico'));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded());
app.use(cookieParser());

var config = require('./config/config')[env];
require('./config/express')(app, config);


var router = require('./routes/router')(express, config);
app.use('/', router);

/// catch 404 and forward to error handler
app.use(function(req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

/// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function(err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});

var startServer = function() {
  app.listen(config.port, function() {
    console.log('\n========== Server is running ==========');
    console.log("Server's Info : " + config.server + ":" + config.port);
    console.log("DB Server's Info : " + config.db + ":" + config.db_port);
    console.log('=======================================\n');
  });
};


module.exports = app;
module.exports.startServer = startServer;
