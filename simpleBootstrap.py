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
        self.no_flag = False
        self.QUESTION_URL_LIST = []
        self.QUESTION_TITLE_LIST = []

    def handle_starttag(self, tag, attrs):
        if tag == "span":
            for attr in attrs:
                if attr[0] == "class" and attr[1] == "m-l-sm title":
                    self.no_flag = True
        if tag == "a":
            is_problem_url = False
            href = None
            for attr in attrs:
                if attr[0] == "href":
                    href = attr[1]
                    continue
                if attr[0] == "class" and attr[1] == "problem-panel list-group-item":
                    is_problem_url = True
            if is_problem_url:
                self.QUESTION_URL_LIST.append(href)

    def handle_endtag(self, tag):
        if tag == "span":
            self.no_flag = False

    def handle_data(self, data):
        if not self.no_flag:
            return
        question_title = data.strip()

        # # http://stackoverflow.com/questions/3621296/python-cleaning-up-a-string
        # question_title = self.rx4cqt.sub(" ", data).strip().replace(" ", "_")

        # zero-fill for keeping order in question No. when using string cmp
        if question_title[1] == '.':
            question_title = "00" + question_title
        if question_title[2] == '.':
            question_title = "0" + question_title
        # assume maximum quetions No. in lintcode < 1000
        if question_title[3] != ".":
            return

        self.QUESTION_TITLE_LIST.append(question_title)

def usage():
    print 'usage: python simleCraw.py -u|--gituser <github username>'

# def clone_lintcode_repo(ROOT, GIT_USER, LINTCODE_REPO):
#     os.chdir(ROOT)
#     if not isdir(LINTCODE_REPO):
#         try:
#             # best practice of passing cmd to subprocess:
#             # http://stackoverflow.com/questions/4348524/subprocess-variables
#             lintcode_repo_url = "https://github.com/"+GIT_USER+"/15UW-lintcode.git"
#             git_cmd = "git clone {0}".format(lintcode_repo_url)
#             subprocess.check_output(git_cmd.split(), shell=False)
#         except subprocess.CalledProcessError:
#             print "Error when calling git clone, is the repo url does not right?"
#             sys.exit(1)

# tricky global, add this prefix to the lintcode url
LINTCODE_PREFIX='http://www.lintcode.com'
def get_problem_md_file_content(question_title, question_url, **kw):
    prev_link = None
    next_link = None
    if kw.get('prev_problem') is None:
        prev_link = '- prev: none\n'
    else:
        prev_problem = kw.get('prev_problem')
        prev_link = '- [prev: ' + prev_problem['title'] + ']('+ prev_problem['md_file']+')\n'
    if kw.get('next_problem') is None:
        next_link = '- next: none\n'
    else:
        next_problem = kw.get('next_problem')
        next_link = '- [next: ' + next_problem['title'] + '](' + next_problem['md_file'] + ')\n'

    return ('[' + question_title + '](' + question_url + ')\n\n' +
            prev_link +
            next_link + '\n'
            "---\n\n" +
            "put your own notes and solutions here.\n" +
            "you can add any reference link such as [title](reference url) here.\n\n" +
            "---\n\n" +
            prev_link +
            next_link)

def bootstrap_lintcode_repo(REPO_DIR, QUESTION_TITLE_LIST, QUESTION_URL_LIST):
    if not isdir(REPO_DIR):
        os.mkdir(REPO_DIR)
    # Change working directory so relative paths works
    os.chdir(REPO_DIR)

    # initialize lintcode repo java folder
    if not isdir("java"):
        os.mkdir("java")

    os.chdir(join(REPO_DIR, "java"))

    question_md_file_list = []

    for idx, question_title in enumerate(QUESTION_TITLE_LIST):
        question_url = QUESTION_URL_LIST[idx]
        question_md_file = question_title.split('.')[0] + "-" + question_url.split('/')[2] + ".md"
        question_md_file_list.append(question_md_file)

    for idx, question_md_file in enumerate(question_md_file_list):
        content = None
        if idx == 0:
            prev_problem = None
        else:
            prev_problem = {'title': QUESTION_TITLE_LIST[idx - 1], 'md_file': question_md_file_list[idx - 1]}
        if idx == len(question_md_file_list) - 1:
            next_problem = None
        else:
            next_problem = {'title': QUESTION_TITLE_LIST[idx + 1], 'md_file': question_md_file_list[idx + 1]}
        content = get_problem_md_file_content(QUESTION_TITLE_LIST[idx], LINTCODE_PREFIX + QUESTION_URL_LIST[idx],
                prev_problem=prev_problem, next_problem=next_problem)
        # print content
        if not isfile(question_md_file):
            f = open(question_md_file, 'w')
            f.write(content)
            f.close()

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

    # if GIT_USER is None:
    #     print "Hey, I need your github username to clone your lintcode repo."
    #     usage()
    #     sys.exit(2)

    f = open('lintcode_main.html', 'r')
    parser = MyHTMLParser()
    parser.feed(f.read())
    f.close()

    assert len(parser.QUESTION_TITLE_LIST) == len(parser.QUESTION_URL_LIST), "nums of question title and question url should be the same"

    bootstrap_lintcode_repo(join(ROOT, LINTCODE_REPO), parser.QUESTION_TITLE_LIST, parser.QUESTION_URL_LIST)
