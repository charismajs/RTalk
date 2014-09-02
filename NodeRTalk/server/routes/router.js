var Client = require('node-rest-client').Client;
client = new Client();

module.exports = function(express, config) {
  var baseUrl = 'http://' + config.db + ':' + config.db_port;
  var router = express.Router();

  router.route('/write')
    .post(function(req, res) {
      var args = {
        data: { talk: req.body.talk },
        headers: { "Content-Type": "application/json" }
      };

      client.post(baseUrl + '/write', args, function(data, response) {
        res.status(response.statusCode).json(data);
      })
    });

  router.route('/like/:key')
    .get(function(req, res) {
      client.get(baseUrl + '/like/' + req.params.key, function(data, response) {
        console.log('data : ', data);
//        console.log('response : ', response);

        res.status(response.statusCode).send(data);
      })
    });

  router.route('/list/:topn/:listn')
    .get(function(req, res) {
      console.log('topN : ' + req.params.topn +', listN : ' + req.params.listn);

      client.get(baseUrl + '/list/' + req.params.topn + '/' + req.params.listn, function(data, response) {
        console.log('data : ', data);
//        console.log('response : ', response);

        res.status(response.statusCode).send(data);
      })
    });

  // Partial Views
  router.route('/partials/*')
    .get(function (req, res) {
      res.render('../../public/app/' + req.params[0]);
    });

  router.route('/')
    .get(function (req, res) {
      res.render('index');
    });

  return router;
};