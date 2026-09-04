## Updating the RSS feed:

The RSS feed and news table on the home page is generated from the `news_source` folder.
The python script `main.py` takes the markdown files in that directory, converts them html files, generates the RSS feed file, and updates the news table `index.html`.

### Adding a new post:
To create a new post, simply create a new file in the `news_source` folder.
Ensure that it has the `title` and `published` tags (check another post for example).
Then, run `python main.py` and check that everything was updated correctly.

Finally, just commit and push your changes