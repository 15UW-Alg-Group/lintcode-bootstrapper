import os, sys, re, getopt, subprocess

from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self):
        # cannot using super() here because HTMLParser is an `old-style` class
        # http://stackoverflow.com/questions/9698614/super-raises-typeerror-must-be-type-not-classobj-for-new-style-class
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
    # root directory (15UW-Alg-group)
    ROOT = os.path.dirname(os.path.dirname(__file__))
    GIT_USER = '15UW-Alg-Group'
    LINTCODE_REPO = "15UW-lintcode"

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hu:",["gituser=",])
    except getopt.GetoptError:
        print 'usage: python simleCraw.py -u|--gituser <github username>'
        sys.exit()

    for opt, arg in opts:
        if opt == 'h':
            print 'usage: python simleCraw.py -u|--gituser <github username>'
            sys.exit()
        elif opt in ("-u", "--gituser"):
            GIT_USER = arg
    print "gituser is: ", GIT_USER

    os.chdir(ROOT)
    if not os.path.isdir(LINTCODE_REPO):
        try:
            # best practice of passing cmd to subprocess:
            # http://stackoverflow.com/questions/4348524/subprocess-variables
            lintcode_repo_url = "https://github.com/"+GIT_USER+"/15UW-lintcode.git"
            git_cmd = "git clone {0}".format(lintcode_repo_url)
            subprocess.check_output(git_cmd.split(), shell=False)
        except subprocess.CalledProcessError:
            print "Error when calling git clone, is the repo url does not right?"
            sys.exit(1)

    # print "success clone your lintcode repo!"
    # Change working directory so relative paths works
    os.chdir(os.path.dirname(__file__))

    f = open('lintcode_main.html', 'r')
    parser = MyHTMLParser()
    parser.feed(f.read())
    f.close()

    # initialize lintcode repo and eclipse config
    os.chdir(os.path.join(ROOT,LINTCODE_REPO))
    if not os.path.isdir("src"):
        os.mkdir("src")
    # config eclipse project
    if not os.path.isfile(".classpath"):
        f = open('.classpath', 'w')
        f.write(ECLIPSE_CLASSPATH)
        f.close()
    if not os.path.isfile(".project"):
        f = open('.project', 'w')
        f.write(ECLIPSE_PROJECT)
        f.close()

    os.chdir(os.path.join(ROOT,LINTCODE_REPO, "src"))

    for question in parser.QUESTION_LIST:
        if not os.path.isdir(question):
            os.mkdir(question)
