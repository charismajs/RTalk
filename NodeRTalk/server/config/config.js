/**
 * Created by LuckyJS on 2014. 8. 28..
 */
var path = require('path');
var rootPath = path.normalize(__dirname + '/../../');

module.exports = {
  development: {
    server: '192.168.246.11',
    rootPath: rootPath,
    port: process.env.PORT || 5001,
    mode: 'development'
  },
  ambari: {
    db: '192.168.245.191',
    rootPath: rootPath,
    port: process.env.PORT || 5001,
    mode: 'ambari'
  }
};