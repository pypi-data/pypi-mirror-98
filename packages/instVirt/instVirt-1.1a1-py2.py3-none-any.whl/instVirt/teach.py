'''  instVirt, este projeto constroi um instrutor virtual para auxílio em
#    sala de aula, ele acompanha textos de estudos dirigidos para a área
#    de ciência da computação.
#    Copyright (C) 2018, 2020–2021  Leonardo de Araújo Lima <leonardo@asl-sl.com.br>
#    Copyright (C) 1983, 1994–1995, 1997, 2005, 2007, 2015  Leonardo de Araújo Lima
#                                             <mailto:leonardo@asl-sl.com.br>
#                                               <xmpp:linux77@suchat.org>
#                               <https://linux77.asl-sl.com.br>
# 
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
# 
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of 
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
#    GNU General Public License for more details.
# 
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.  
    This program comes with ABSOLUTELY NO WARRANTY
    This is free software, and you are welcome to redistribute it '''
#!/usr/bin/env python3
from tkinter import *
import os
class vteach(Tk):
    def __init__(self):
        os.system('echo "asl-lab (Academia do Software Livre)." &')
        super().__init__()
        super().geometry("280x390")
        super().title("Instrutor virtual")
        self.filename = ""
        self.e = StringVar()
        self.d = StringVar()
        self.lTitle = Label(self, text='Etapas do curso')
        self.lDisc = Label(self, text='Disciplinas do curso')
        self.sbtn = Button(self, text=" Ler", command=self.mtext)
        self.bbtn = Button(self, text=" Narrar", command=self.bvindo)
        self.le = Listbox(self, background="white", height=10, listvariable=self.e)
        self.ld = Listbox(self, background="white", height=4, width=22, listvariable=self.d)
        etapas = [ "primeira","segunda","terceira","quarta","quinta","sexta","sétima","oitava","nona","décima" ]
        idx = 0
        for etap in etapas:
            self.le.insert(idx, etap)
            idx+= 1
        disc_items = [  "Matemática", "Eletricidade", "Tecnologia-da-Informação", "Sistemas-Operacionais" ]
        idx= 0
        for item in disc_items:
            self.ld.insert(idx, item)
            idx+= 1

        self.lTitle.place(x=52, y=0)
        self.le.place(x=52, y=20)
        self.lDisc.place(x=52, y=205)
        self.ld.place(x=52, y=225)
        self.sbtn.place(x=52, y=305)
        self.bbtn.place(x=52, y=338)
        pass    
    
    def slivre(self):
        self.filename="/home/asl-teach/ASL-SL/software_livre.txt"
        os.system("clear")
        talkStr = "cat " + self.filename + " | tsurya "
        texto = ""
        f = open(self.filename, "r")
        texto += f.read()
        print(texto)
        os.system(talkStr)
        pass
    
    def bvindo(self):
        d = StringVar()
        e = StringVar()
        fname = StringVar()
        disc = self.ld.get(ACTIVE)
        d.set(disc)
        etapa = self.le.get(ACTIVE)
        e.set(etapa)
        fname = d.get() + "/" + e.get()
        strCmd = "nohup espeak -a 120 -b 1 -s 128 -v brazil-mbrola-1 -f " + fname + " 2>/dev/null"
        print (strCmd)
        os.system(strCmd)
        pass
    
    def mtext(self):
        d = StringVar()
        e = StringVar()
        disc = self.ld.get(ACTIVE)
        d.set(disc)
        etapa = self.le.get(ACTIVE)
        e.set(etapa)
        strCmd = "nohup xterm -T Instrutor -e less " + d.get() + "/" + e.get() + "> /dev/null 2>&1"
        os.system(strCmd)

if __name__ == "__main__":
    app = vteach()
    app.mainloop()
