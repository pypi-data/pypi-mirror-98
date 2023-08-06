from weboa.project import *
from weboa.utils import *
from weboa import json, prepare, os
from weboa import __VERSION__

class PHP(General):
    def __init__(self, langs=("en","ru"), path = "../", BUILDFOLDER = ""):
        super().__init__(langs=langs,path=path, BUILDFOLDER = BUILDFOLDER)
        Printer.log("Start PHP Project")
        Printer.info(f"Your system is {self.os}")
        Printer.info(f"Weboa version is {__VERSION__}")

    def FS(self):
        # Creating folders for php project
        folders = ("","/css","/js","/img","/php","/php/api","/php/configs","/php/controller","/php/lib","/php/modules")
        for f in folders:
            self.Folder_Create(f)
        #self.File_Create("/.weboa", json.dumps(Processing.Processing.Weboa_Init()))

    def index(self):
        self.copy(prepare.Package.stream + 'phpfs/_index.php',"/index.php")

    def language(self):
        # Language system
        self.copy(prepare.Package.stream + 'phpfs/language',"/php/controller/language.php")
        for l in self.langs:
            self.copy(prepare.Package.stream + 'phpfs/l', f"/php/configs/{l}.php")

    def controller(self):
        files = ("controller","index","router","auth")
        for f in files:
            self.copy(prepare.Package.stream + 'phpfs/'+f,"/php/controller/"+f+".php")

        # .htaccess
        self.copy(prepare.Package.stream + 'phpfs/.htaccess',"/.htaccess")

    def project(self):
        self.copy(prepare.Package.stream + 'phpfs/autoload.php', "/php/lib/autoload.php")       # Autoload
        self.copy(prepare.Package.stream + 'phpfs/db',"/php/db.php")                            # DATABASE
        self.copy(prepare.Package.stream + 'phpfs/test',"/php/api/test.php")                    # API
        self.copy(prepare.Package.stream + 'phpfs/consts',"/php/configs/consts.php")            # CONSTS
        self.copy(prepare.Package.stream + 'phpfs/header', "/php/modules/header.phtml")         # META
        self.copy(prepare.Package.stream + 'phpfs/footer', "/php/modules/footer.phtml")         # SCRIPTS
        self.copy(prepare.Package.stream + 'phpfs/mainphtml', "/php/modules/mainphtml.phtml")   # TEST PAGE