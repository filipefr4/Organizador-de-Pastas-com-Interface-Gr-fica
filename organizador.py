import customtkinter as ctk 
from tkinter import filedialog,messagebox
from pathlib import Path

TIPOS = {
    "Imagens": [".jpg",".jpeg",".png",".gif"],
    "Documentos": [".pdf",".docx",".txt"],
    "Vídeos": [".mp4",".mkv"],
    "Áudios": [".mp3",".wav"],
    "Compactados": [".zip",".rar"]
}

def executar_organizacao(caminho_pasta):
    pasta_alvo = Path(caminho_pasta)

    if not pasta_alvo.exists():
        raise FileNotFoundError("Pasta não encontrada")
    
    contagem = 0 
    for arquivo in pasta_alvo.iterdir():
        if arquivo.is_file():
            extensao = arquivo.suffix.lower()
            movido = False

            for pasta,extensoes in TIPOS.items():
                if extensao in extensoes:
                    destino = pasta_alvo / pasta
                    destino.mkdir(exist_ok=True)
                    arquivo.rename(destino/arquivo.name)
                    movido = True
                    contagem += 1
                    break

            
            if not movido:
                outros = pasta_alvo / "Outros"
                outros.mkdir(exist_ok=True)
                arquivo.rename(outros/arquivo.name)
                contagem += 1

    return contagem 

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Organizador de arquivos')
        self.geometry('500x300')
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')

        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self,text='Selecione uma pasta para organizar', font=("Roboto",20))
        self.label.pack(pady=20)

        self.botao_selecionar = ctk.CTkButton(self,text='Escolha a pasta',command=self.selecionar_pasta)
        self.botao_selecionar.pack(pady=10)

        self.caminho_label = ctk.CTkLabel(self, text='Nenhuma pasta foi selecionada', text_color='gray')
        self.caminho_label.pack(pady=5)

        self.botao_organizar = ctk.CTkButton(self, text='Organizar agora!',
                                             command=self.iniciar_organizacao,
                                             fg_color='green', hover_color='darkgreen')
        
        self.botao_organizar.pack(pady=20)

        self.pasta_selecionada = ""

    def selecionar_pasta(self):
        self.pasta_selecionada = filedialog.askdirectory()
        if self.pasta_selecionada:
            self.caminho_label.configure(text=f"Pasta: {self.pasta_selecionada}", text_color='white')
    
    def iniciar_organizacao(self):
        if not self.pasta_selecionada:
            messagebox.showwarning("Aviso!", "Selecione uma pasta primeiro")
            return 
        
        try:
            total = executar_organizacao(self.pasta_selecionada)
            messagebox.showinfo("Sucesso!", f"Concluído! {total} arquivos foram organizados")
        except Exception as erro:
            messagebox.showerror("Erro", f"Falha ao organizar os arquivos - {erro}")

if __name__ == "__main__":
    app = App()
    app.mainloop()

