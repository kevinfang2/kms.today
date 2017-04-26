import re, praw, requests, os, glob, sys
from bs4 import BeautifulSoup
from bottle import route, run, template, static_file, get, post, request
from PIL import Image
import urllib


targetSubreddit = "anime_irl"

imgurUrlPattern = re.compile(r'(http://i.imgur.com/(.*))(\?.*)?')

f = open('database.txt', 'w')
count = 0;

def downloadImage(imageUrl):
	global count
	# url = urllib2.urlopen(imageUrl).read()
	#
	# with open(str(count) + '.jpg', 'wb') as f:
	# 	f.write(url.read())

	# img = Image.open('temp.jpg')
	# img.show()
	urllib.urlretrieve(imageUrl, str(count) + ".jpg")

	count = count + 1;

	# f.write(imageUrl + '\n')

# Connect to reddit and download the subreddit front page
r = praw.Reddit('bot1')
submissions = r.subreddit(targetSubreddit).top('day')

# Process all the submissions from the front page
for submission in submissions:
    # Check for all the cases where we will skip a submission:
    if "imgur.com/" not in submission.url:
        continue # skip non-imgur submissions
    if len(glob.glob('reddit_%s_%s_*' % (targetSubreddit, submission.id))) > 0:
        continue # we've already downloaded files for this reddit submission

	print "\n" + submission.url

    if 'http://imgur.com/a/' in submission.url:
		print "album"
		albumId = submission.url[len('http://imgur.com/a/'):]
		htmlSource = requests.get(submission.url).text

		soup = BeautifulSoup(htmlSource)
		matches = soup.select('.album-view-image-link a')
		for match in matches:
			imageUrl = match['href']
			if '?' in imageUrl:
				imageFile = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('?')]
			else:
				imageFile = imageUrl[imageUrl.rfind('/') + 1:]
			downloadImage('http:' + match['href'])

    elif 'http://i.imgur.com/' in submission.url:
		print "direct link"
		mo = imgurUrlPattern.search(submission.url) # using regex here instead of BeautifulSoup because we are pasing a url, not html

		imgurFilename = mo.group(2)
		if '?' in imgurFilename:
            # The regex doesn't catch a "?" at the end of the filename, so we remove it here.
			imgurFilename = imgurFilename[:imgurFilename.find('?')]

		localFileName = 'reddit_%s_%s_album_None_imgur_%s' % (targetSubreddit, submission.id, imgurFilename)
		downloadImage(submission.url)

    elif 'http://imgur.com/' in submission.url:
		pass
