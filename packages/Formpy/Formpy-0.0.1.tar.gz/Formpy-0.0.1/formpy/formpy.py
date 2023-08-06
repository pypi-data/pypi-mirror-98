
import os


path = os.getcwd()

class Form():

    forForm = ""
    formName = ""
    f = ""
    formId = ""
    formMethod= ""
    formAction = ""
    formStyle = ""
    onlyForm = ""
    endHtml = ""
    

    def __init__(self, formName, formId = "" ,onlyForm = False, styleLink = "", action = "", method = ""):
        self.formName = formName
        self.formMethod = method
        self.formAction = action
        self.formStyle = styleLink
        self.formId = formId
        self.onlyForm = onlyForm
        if onlyForm == False:         
            self.f = """
        <!DOCTYPE html>
        <html>

        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="%s">
            <title> formpy 0.0.1 </title>
        </head> 

        <body>

            <form action='%s' method='%s' id='%s'>
            """ % (styleLink, self.formAction, method, self.formId)
        else:
            self.f = """
            <form action='%s' method='%s' id='%s'>
            """ % (action, method, self.formId)

            


    def input(self, dic = None, p = None, text = ""):
        if dic and p == None and "type" in dic:
            inp = ""
            for v, k in dic.items():
                inp += " %s='%s'" % (v,k)
            self.f += """
                <input%s > %s
                """ % (inp, text)
            return self

        elif dic and p and "type" in dic:
            inp = ""
            for v, k in dic.items():
                inp += " %s='%s'" % (v,k)
            self.f += """
                <p> %s <input%s > %s </p>
                """ % (p, inp, text)
            return self
        
        elif dic and p == None and "type" not in dic:
            inp = ""
            for v, k in dic.items():
                inp += " %s='%s'" % (v,k)
            self.f += """
                <input type='text'%s> %s
                """ % (inp, text)
            return self

        elif dic and p and "type" not in dic:
            inp = ""
            for v, k in dic.items():
                inp += " %s='%s'" % (v,k)
            self.f += """
                <p> %s <input type='text'%s > %s </p>
                """ % (p, inp, text)
            return self

        else:
            self.f += """
                <input>
                """
            return self

    def openSection(self, label, text = ""):
        if label == "!-":
            self.f += """
            <%s- %s
            """ % (label, text)
            return self
        else:
            self.f += """
            <%s>%s
            """ % (label, text)
            return self
    
    def closeSection(self, label, text = ""):
        if label == "-!":
            self.f += """
            --> %s
            """ % (text)
            return self
        else:
            self.f += """
            </%s>%s
            """ % (label, text)
            return self
    
    def setId(self, idF):
        self.formId = idF
        if self.onlyForm == False:
            self.f = """
        <!DOCTYPE html>
        <html>

        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="%s">
            <title> formpy 1.0 </title>
        </head> 

        <body>

            <form action='%s' method='%s' id='%s'>
                """ % (self.formStyle, self.formAction, self.formMethod, self.formId)
            f = open(path + "/forms/" + self.formName +".html", 'w')
            mensaje = self.f
            f.write(mensaje)
            f.close()
        else:
            self.f = """
            <form action='%s' method='%s' id='%s'>
            """ % (self.formAction, self.formMethod, self.formId)

    
    def setAction(self, action):
        self.formAction = action
        self.f = """
        <!DOCTYPE html>
        <html>

        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="%s">
            <title> formpy 1.0 </title>
        </head> 

        <body>

            <form action='%s' method='%s' id='%s'>
            """ % (self.formStyle, self.formAction, self.formMethod, self.formId)
        f = open(path + "/forms/" + self.formName +".html", 'w')
        mensaje = self.f
        f.write(mensaje)
        f.close()
        
    def setMethod(self, method):
        self.formMethod = method
        self.f = """
        <!DOCTYPE html>
        <html>

        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="%s">
            <title> formpy 1.0 </title>
        </head> 

        <body>

            <form action='%s' method='%s' id='%s'>
            """ % (self.formStyle, self.formAction, self.formMethod, self.formId)
        f = open(path + "/forms/" + self.formName +".html", 'w')
        mensaje = self.f
        f.write(mensaje)
        f.close()

    def setStyleLink(self, dic):
        styleLink = ""
        if type(dic) == list:
            for i in dic:
                print(i)
                styleLink += """
            <link rel="stylesheet" href="%s">
                """ % (i)

                
        self.f = """
        <!DOCTYPE html>
        <html>

        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            %s
            <title> formpy 1.0 </title>
        </head> 

        <body>

            <form action='%s' method='%s' id='%s'>
            """ % (styleLink, self.formAction, self.formMethod, self.formId)
        f = open(path + "/forms/" + self.formName +".html", 'w')
        mensaje = self.f
        f.write(mensaje)
        f.close()
                


    def button(self, dic = None, text = None):
        if dic and text:
            inp = ""
            for v, k in dic.items():
                inp += " %s='%s'" % (v,k)
                self.f += """
                <button%s> %s </button>
                    """ % (inp, text)
            return self
        elif dic and text == None:
            inp = ""
            for v, k in dic.items():
                inp += " %s='%s'" % (v,k)
                self.f += """
                <button%s>  </button>
                    """ % (inp)
            return self
        else:
            self.f += """
                <button>  </button>
                """
            return self

    def img(self, dic):
        if dic:
            inp = ""
            for v, k in dic.items():
                inp += " %s='%s'" % (v,k)
                self.f += """
                <img%s>
                    """ % (inp)
            return self
    
    def textarea(self, dic = None, text = None):
        if dic and text == None:
            inp = ""
            for v, k in dic.items():
                inp += " %s='%s'" % (v,k)
                self.f += """
                <textarea%s> </textarea
                    """ % (inp)
            return self
        elif dic and text:
            inp = ""
            for v, k in dic.items():
                inp += " %s='%s'" % (v,k)
                self.f += """
                <textarea%s> %s </textarea>
                    """ % (inp, text)
            return self
        else:
            self.f += """
                <textarea>  </textarea>
                """
            return self
    
    def openSelect(self, dic):
        inp = ""
        for v, k in dic.items():
            inp += " %s='%s'" % (v,k)
            self.f += """
                <select%s> 
                """ % (inp)
        return self
    
    def withOption(self, dic, text = ""):
        inp = ""
        for v, k in dic.items():
            inp += " %s='%s'" % (v,k)
            self.f += """
                    <option%s> %s </option>
                """ % (inp, text)
        return self
    
    def closeSelect(self):
        self.f += """
                </select> 
            """ 
        return self
    
    def br(self):
        self.f += """<br>
            """ 
        return self

    '''def exception(self, formId, isMerge = False):
        
        if self.onlyForm == False and self.formId != formId:         
            self.f = """
        <!DOCTYPE html>
        <html>

        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="%s">
            <title> formpy 1.0 </title>
        </head> 

        <body>

            <form action='%s' method='%s' id='%s' style="visibility:hidden;">
            """ % (self.formStyle, self.formAction, self.formMethod, self.formId)
        elif self.formId == formId and isMerge == True:
            self.f += """
            <form action='%s' method='%s' id='%s' style="visibility:hidden;">
            """ % (self.formAction, self.formMethod, self.formId)
            f = open(path + "/forms/" + self.forForm +".html", 'w')
            mensaje = self.f
            f.write(mensaje)
            f.close()
            return self'''



    def toMerge(self, forForm):
        self.forForm = forForm
        print(path)
        self.f += """

            </form>
        """ 
        f = open(path + "/forms/" + self.forForm +".html", 'a')
        mensaje = self.f
        f.write(mensaje)
        f.close()
        return self

    def toHTML(self, withEndHTML = False):
        if withEndHTML == True:
            self.f += """

            </form>

        </body>

        </html>
            """ 
            f = open(path + "/forms/" + self.formName +".html", 'w')
            mensaje = self.f
            f.write(mensaje)
            f.close()
        else:
            self.f += """

            </form>
            """ 
            f = open(path + "/forms/" + self.formName +".html", 'w')
            mensaje = self.f
            f.write(mensaje)
            f.close()
    
    def withEndHTML(self, opc):
        if opc == True:
            self.endHtml += """
        </body>

        </html>
            """ 
            f = open(path + "/forms/" + self.forForm +".html", 'a')
            mensaje = self.endHtml
            f.write(mensaje)
            f.close()
        else:
            print("This function need the parameter in True")

            
       
        

    


