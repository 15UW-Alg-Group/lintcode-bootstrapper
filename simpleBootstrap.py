import os, sys, re, getopt, subprocess
from os.path import dirname, abspath, join, isfile, isdir
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

def usage():
    print 'usage: python simleCraw.py -u|--gituser <github username>'

def clone_lintcode_repo(ROOT, GIT_USER, LINTCODE_REPO):
    os.chdir(ROOT)
    if not isdir(LINTCODE_REPO):
        try:
            # best practice of passing cmd to subprocess:
            # http://stackoverflow.com/questions/4348524/subprocess-variables
            lintcode_repo_url = "https://github.com/"+GIT_USER+"/15UW-lintcode.git"
            git_cmd = "git clone {0}".format(lintcode_repo_url)
            subprocess.check_output(git_cmd.split(), shell=False)
        except subprocess.CalledProcessError:
            print "Error when calling git clone, is the repo url does not right?"
            sys.exit(1)

def bootstrap_lintcode_repo(ROOT, LINTCODE_REPO):
    # Change working directory so relative paths works
    os.chdir(join(ROOT,LINTCODE_REPO))

    f = open('../lintcode-bootstrapper/lintcode_main.html', 'r')
    parser = MyHTMLParser()
    parser.feed(f.read())
    f.close()

    # initialize lintcode repo and eclipse config
    if not isdir("src"):
        os.mkdir("src")

    os.chdir(join(ROOT,LINTCODE_REPO, "src"))

    for question in parser.QUESTION_LIST:
        if not isdir(question):
            os.mkdir(question)

if __name__ == '__main__':
    # http://stackoverflow.com/questions/7783308/os-path-dirname-file-returns-empty
    SCRIPT_DIR = dirname(abspath(__file__))
    # root directory (15UW-Alg-group)
    ROOT = dirname(SCRIPT_DIR)
    GIT_USER = None
    LINTCODE_REPO = "15UW-lintcode"

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hu:",["gituser=",])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == 'h':
            print 'usage: python simleCraw.py -u|--gituser <github username>'
            sys.exit()
        elif opt in ("-u", "--gituser"):
            GIT_USER = arg
        else:
            assert False, "Found unhandled option"

    if GIT_USER is None:
        print "Hey, I need your github username to clone your lintcode repo."
        usage()
        sys.exit(2)

    clone_lintcode_repo(ROOT, GIT_USER, LINTCODE_REPO)

    bootstrap_lintcode_repo(ROOT, LINTCODE_REPO)
