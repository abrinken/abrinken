from datetime import datetime as dt
from dateutil import tz
import os
import markdown
import rssgen
import rssgen.feed
import xml.dom.minidom
from operator import attrgetter

class Post:
    def __init__(self):
        self.title: str = ""
        self.published: dt = dt.fromtimestamp(0)
        self.content: str = ""
        self.filename:str = ""
    
    def parse(self, content: list[str], filename: str):
        self.filename = filename
        for line in content:
            if line.startswith("title: "): self.title = line[len("title: "):None]
            elif line.startswith("published: "): self.published = dt.fromisoformat(line[len("published: "):None]).astimezone(tz.tzutc())
            else: self.content += line + "\n"

        return self
    
    def getHtml(self):
        return markdown.markdown(self.content)

    def createRssPost(self, fg: rssgen.feed.RssGenerator):
        post: rssgen.feed.FeedEntry = fg.add_entry()
        post.title("Abrinken - " + self.title)
        post.published(self.published)
        post.description(self.getHtml())


if __name__ == "__main__":

    # Set up feed 
    feed = rssgen.feed.RssGenerator()
    feed.id('https://abrinken.org')
    feed.title('Ⓐbrinken Updates & News')
    feed.description('Update feed for the Abrinken collective')
    feed.author( {'name':'A group of volunteers for the Ⓐbrinken collective','email':'abrinken8000@proton.me'} )
    feed.link( href='https://abrinken.org', rel='alternate' )
    feed.logo('https://abrinken.org/assets/anarchy.png')
    feed.link( href='https://abrinken.org/rss.xml', rel='self' )
    feed.language('en')

    posts: list[Post] = []

    srcDir = "news_source"
    compDir = "news"
    for filename in os.listdir(srcDir):
        if filename.endswith(".md"):
            filepath: str = srcDir + "/" + filename
            with open(filepath, "r") as file:
                content: list[str] = [line.strip() for line in file.readlines()]
                newPost: Post = Post().parse(content, filename)
                posts.append(newPost)
    
    posts = sorted(posts, key=attrgetter("published"))

    for post in posts:
        html: str = newPost.getHtml()
        with open(compDir + "/" + filename.replace(".md", ".html"), "w+") as file:
            file.write(html)
        post.createRssPost(feed)

    with open("rss.xml", "w+") as file:
        rss: str = feed.rss_str()
        rssPretty = dom = xml.dom.minidom.parseString(rss)
        file.writelines(rssPretty.toprettyxml())

    with open("index.html", "r") as file:
        lines: list[str] = file.readlines()
        lines_stripped = [line for line in lines if not line.strip().startswith("<tr id=\"feed_entry\">")]
        feed_start = [line.strip() for line in lines].index("<!--start feed data-->") + 1
        for i, post in enumerate(reversed(posts)):
            lines_stripped.insert(feed_start + i, f"<tr id=\"feed_entry\"><td>{post.published.strftime("%Y-%m-%d")}</td><td><a href=\"/news/{post.filename.replace(".md", ".html")}\">{post.title}</a></td></tr>\n")
    with open("index.html", "w+") as newfile:
        newfile.writelines(lines_stripped)