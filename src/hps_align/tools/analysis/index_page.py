import sys


class htmlWriter:
    """! Class to write html file with output plots"""

    def __init__(self, dir, img_type="png", update_only=False, html_name="index.html", img_folder=""):
        ## png or pdf
        self.img_type = img_type
        ## folder where the images are stored
        self.img_folder = img_folder

        if not update_only:
            self.index_html = open(dir + "/" + html_name, "w")  # html file to be written
            self.img_folder = dir

            self.wline("<html>")
            self.wline("<head>")
            self.wline("</head>")
        else:
            self.index_html = open(dir + "/" + html_name, 'r+')

    def wline(self, line):
        """!
        Write line to html file

        @param line  line to be written
        """
        self.index_html.write(line + "\n")

    def close_html(self):
        """! Close html file"""
        self.wline("</body>")
        self.wline("</html>")
        self.index_html.close()

    def add_images(self, folder=""):
        """!
        Add images to html file

        @param folder  folder where the images are stored
        """
        print("searching for " + self.img_type)
        import glob
        list_images = glob.glob(folder + "/*" + self.img_type)
        for img in list_images:
            # print img
            if (self.img_type == "png"):
                self.wline('<img src="' + img.split("/")[-1]+'" width="900" height="700" >')
            elif (self.img_type == "pdf"):
                # print "Found pdf"
                self.wline('<embed src="' + img.split("/")[-1] + '" width="700px" height="500px" />')

    def add_folder_links(self):
        """! Add links to subfolders to html file"""
        list_of_links = []
        for line in self.index_html.readlines():
            if "href" in line:
                list_of_links.append(line.strip())
        self.index_html.seek(0)


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
