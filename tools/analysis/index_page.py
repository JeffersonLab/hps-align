import sys
import os


class htmlWriter:
    """! Write html file with images"""

    index_html = ""
    img_folder = ""
    img_type = "png"

    def __init__(self, fld, update_only=False, html_name="index.html"):
        if not update_only:
            self.index_html = open(fld+"/"+html_name, "w")
            self.img_folder = fld

            self.wline("<html>")
            self.wline("<head>")
            self.wline("</head>")
        else:
            self.index_html = open(fld+"/"+html_name, 'r+')

    def wline(self, line):
        self.index_html.write(line+"\n")

    def close_html(self):
        self.wline("</body>")
        self.wline("</html>")
        self.index_html.close()

    def add_images(self, folder=""):

        print("searching for " + self.img_type)
        import glob
        list_images = glob.glob(folder + "/*"+self.img_type)
        for img in list_images:
            # print img
            if (self.img_type == "png"):
                self.wline('<img src="'+img.split("/")[-1]+'" width="900" height="700" >')
            elif (self.img_type == "pdf"):
                # print "Found pdf"
                self.wline('<embed src="'+img.split("/")[-1]+'" width="700px" height="500px" />')

    def add_folder_links(self):
        list_folders = next(os.walk('.'))[1]

        list_of_links = []
        for line in self.index_html.readlines():
            if "href" in line:
                list_of_links.append(line.strip())
        self.index_html.seek(0)

    #    for line in self.indexHtml.readlines():
    #        if "Available Plots" in line:

    #            for folder in list_folders:
    #    entry = '<a href="'+folder+'">'+folder+"</a> </br>"
    #        print entry


def main():

    for arg in sys.argv[1:]:
        print(arg)
        pass

    folder = sys.argv[1]
    hw = htmlWriter(sys.argv[1])
    hw.add_images(folder)
    hw.close_html()


if __name__ == "__main__":
    main()
