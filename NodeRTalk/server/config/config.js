/**
 * Created by LuckyJS on 2014. 8. 28..
 */
var ip = require('ip');
var path = require('path');
var rootPath = path.normalize(__dirname + '/../../');

module.exports = {
  development: {
    server: ip.address(),
    port: process.env.PORT || 3030,
    db: '191.168.245.191',
    db_port: '5001',
    rootPath: rootPath
  }
};