import sys
import os


class htmlWriter:
    indexHtml = ""
    img_folder = ""
    img_type = "png"

    def __init__(self, fld, updateOnly=False, htmlname="index.html"):
        if not updateOnly:
            self.indexHtml = open(fld+"/"+htmlname, "w")
            self.img_folder = fld

            self.wline("<html>")
            self.wline("<head>")
            self.wline("</head>")
        else:
            self.indexHtml = open(fld+"/"+htmlname, 'r+')

    def wline(self, line):
        self.indexHtml.write(line+"\n")

    def closeHtml(self):
        self.wline("</body>")
        self.wline("</html>")
        self.indexHtml.close()

    def AddImages(self, folder=""):

        print("searching for " + self.img_type)
        import glob
        listImages = glob.glob(folder + "/*"+self.img_type)
        for img in listImages:
            # print img
            if (self.img_type == "png"):
                self.wline('<img src="'+img.split("/")[-1]+'" width="900" height="700" >')
            elif (self.img_type == "pdf"):
                # print "Found pdf"
                self.wline('<embed src="'+img.split("/")[-1]+'" width="700px" height="500px" />')

    def AddFolderLinks(self):
        listFolders = next(os.walk('.'))[1]

        listOfLinks = []
        for line in self.indexHtml.readlines():
            if "href" in line:
                listOfLinks.append(line.strip())
        self.indexHtml.seek(0)

    #    for line in self.indexHtml.readlines():
    #        if "Available Plots" in line:
        

    #            for folder in listFolders:
    #    entry = '<a href="'+folder+'">'+folder+"</a> </br>"
    #        print entry


def main():

    for arg in sys.argv[1:]:
        print(arg)
        pass

    folder = sys.argv[1]
    hw = htmlWriter(sys.argv[1])
    hw.AddImages(folder)
    hw.closeHtml()


if __name__ == "__main__":
    main()
