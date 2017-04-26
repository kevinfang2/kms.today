var express = require('express');
var fs = require('fs');
var request = require('request');
var cheerio = require('cheerio');
var app     = express();

// app.get('/scrape', function(req, res){
  //All the web scraping magic will happen here
// })

// app.listen('8081')
url = 'http://reddit.com/r/anime_irl';

    // The structure of our request call
    // The first parameter is our URL
    // The callback function takes 3 parameters, an error, response status code and the html

    request(url, function(error, response, html){

        // First we'll check to make sure no errors occurred when making the request

        if(!error){
            // Next, we'll utilize the cheerio library on the returned html which will essentially give us jQuery functionality

            var $ = cheerio.load(html);

            // Finally, we'll define the variables we're going to capture

            var title, release, rating;
            var count = 0;
            $('.title').filter(function(){
              if(count < 10){
                var data = $(this);
                title = data.children().first().text();
                console.log(title)
                count += 1;
              }
            })
        }
    })

console.log('Magic happens on port 8081');

// exports = module.exports = app;
