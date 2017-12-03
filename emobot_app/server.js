
const express = require('express');
const bodyParser = require('body-parser');
const request = require('request');
const app = express()

const apiKey = '*****************';

const img_dict = {
  'joy': 'JOY',
  'anger': 'ANGER',
  'disgust': 'DISGUST',
  'fear': 'FEAR',
  'sadness': 'SADNESS',
  'confident': 'SURE',
  'tentative': 'TENTATIVE',
  'neutral': 'CALM',
  'analytical': 'ANALYTICAL'
};

app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'ejs')

app.get('/', function (req, res) {
  res.render('index', {emotion: null, img_name: null});
})

app.post('/', function (req, res) {
  let text = req.body.wantedText;
  console.log(text);
  //res.render('index', {emotion: "sad", img_name: "SAD"});

  let url = `http://localhost:5000/${text}`
  request(url, function (err, response, body) {
    let emotion = JSON.parse(body);
    //console.log(Object.keys(emotion[0]));
    emotion_dict = emotion[0];

    for (var key in emotion_dict) {
      console.log(key + '->' + emotion_dict[key]);
    };

    var items = Object.keys(emotion_dict).map(function(key) {
      return [key, emotion_dict[key]];
    });

    items.sort(function(first, second) {
      return second[1] - first[1];
    });

    console.log(items);
    best_emotion_name = items[0][0];
    
    //let emotion_name = Object.keys(emotion[0]);
    //console.log(emotion_name)
    //res.render('index', {emotion: emotion_name[0], img_name: 'SAD'});
    res.render('index', {emotion: best_emotion_name, img_name: img_dict[best_emotion_name]});
  });
})

app.listen(3000, function () {
  console.log('Example app listening on port 3000!')
})
