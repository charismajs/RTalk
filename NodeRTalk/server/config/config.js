/**
 * Created by LuckyJS on 2014. 8. 28..
 */
var ip = require('ip');
var path = require('path');
var rootPath = path.normalize(__dirname + '/../../');

module.exports = {
  development: {
    server: ip.address(),
    port: process.env.PORT || 5001,
    db: '192.168.245.191',
    db_port: '5001',
    rootPath: rootPath,
    mode: 'development'
  },
  production: {
    server: ip.address(),
    port: process.env.PORT || 80,
    db: '127.0.0.1',
    db_port: '5001',
    rootPath: rootPath,
    mode: 'production'
  }
};