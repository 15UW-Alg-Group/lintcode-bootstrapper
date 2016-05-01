import os
from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        #Tricky globa1 variable
        self.flag = False
        self.QUESTION_LIST = []

    def handle_starttag(self, tag, attrs):
        if tag != "span":
            return
        for attr in attrs:
            if attr[0] == "class" and attr[1] == "m-l-sm title":
                self.flag = True

    def handle_endtag(self, tag):
        if tag != "span":
            return
        self.flag = False
    def handle_data(self, data):
        if not self.flag:
            return
        question_title = data.strip().replace(" ", "_")
        # print "Encountered a question title :", question_title

        #zero-fill for keeping order in question No. when using string cmp
        if question_title[1] == '.':
            question_title = "00" + question_title
        if question_title[2] == '.':
            question_title = "0" + question_title
        #assume maximum quetions No. in lintcode < 1000
        if question_title[3] != ".":
            return
        self.QUESTION_LIST.append(question_title)



if __name__ == '__main__':
    f = open('lintcode_main.html', 'r')
    parser = MyHTMLParser()
    parser.feed(f.read())
    if not os.path.isdir("../lintcode"):
        os.mkdir("../lintcode")
    os.chdir("../lintcode")
    question_list = parser.QUESTION_LIST
    for question in question_list:
        if not os.path.isdir("./"+question):
            os.mkdir("./"+question)