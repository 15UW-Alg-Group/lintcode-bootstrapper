import os
import re
from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        # Tricky globa1 variable
        self.flag = False
        self.QUESTION_LIST = []
        # rx4qt: RegeX for Cleaning Question Title
        self.rx4cqt = re.compile('\W+')

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
        # http://stackoverflow.com/questions/3621296/python-cleaning-up-a-string
        question_title = self.rx4cqt.sub(" ", data).strip().replace(" ", "_")

        # zero-fill for keeping order in question No. when using string cmp
        if question_title[1] == '_':
            question_title = "00" + question_title
        if question_title[2] == '_':
            question_title = "0" + question_title
        # assume maximum quetions No. in lintcode < 1000
        if question_title[3] != "_":
            return

        # print "Encountered a question title :", question_title

        # Add `Q` for following the eclipse package naming convention 
        # (should begin with letter)
        self.QUESTION_LIST.append("Q" + question_title)

# don't use `os.linesep`: http://stackoverflow.com/questions/11497376/new-line-python
ECLIPSE_CLASSPATH = '<?xml version="1.0" encoding="UTF-8"?>\n\
<classpath>\n\
        <classpathentry kind="src" path="src"/>\n\
        <classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.8"/>\n\
        <classpathentry kind="output" path="bin"/>\n\
</classpath>\n'

ECLIPSE_PROJECT = '<?xml version="1.0" encoding="UTF-8"?>\n\
<projectDescription>\n\
        <name>15UW-lintcode</name>\n\
        <comment></comment>\n\
        <projects>\n\
        </projects>\n\
        <buildSpec>\n\
                <buildCommand>\n\
                        <name>org.eclipse.jdt.core.javabuilder</name>\n\
                        <arguments>\n\
                        </arguments>\n\
                </buildCommand>\n\
        </buildSpec>\n\
        <natures>\n\
                <nature>org.eclipse.jdt.core.javanature</nature>\n\
        </natures>\n\
</projectDescription>\n'

if __name__ == '__main__':
    f = open('lintcode_main.html', 'r')
    parser = MyHTMLParser()
    parser.feed(f.read())
    f.close()

    lintcode_relative_path = "../"
    lintcode_repo_name = "15UW-lintcode"
    lintcode_dir = lintcode_relative_path + lintcode_repo_name

    # initialize lintcode repo and eclipse config
    if not os.path.isdir(lintcode_dir):
        os.mkdir(lintcode_dir)
        os.mkdir(lintcode_dir+"/src")
        # config eclipse project
        os.chdir(lintcode_dir)
        f = open('.classpath', 'w')
        f.write(ECLIPSE_CLASSPATH)
        f.close()
        f = open('.project', 'w')
        f.write(ECLIPSE_PROJECT)
        f.close()

    os.chdir(lintcode_dir+"/src")

    for question in parser.QUESTION_LIST:
        if not os.path.isdir("./"+question):
            os.mkdir("./"+question)
