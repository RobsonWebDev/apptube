import flet as ft
from pytubefix import YouTube




def main(page: ft.Page):

    page.adaptive=True
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.padding = 80


    def buscar(e):
        def checkMp4(e):
            if check_mp4.value == False:
                check_mp4.value = True
                page.add(check_mp4)
                page.update()

            else:
                check_mp4.value = False
                page.add(check_mp4)
                page.update()


        yt = YouTube(barra_de_busca.value)

        thumber = ft.Container(ft.Image(src=f"{yt.thumbnail_url}"), width=200, on_click=checkMp4)
        check_mp4 = ft.Checkbox(value=False, visible=False)

        page.add(thumber, check_mp4)
        page.update()
        
   
    barra_de_busca = ft.TextField(label='Digite a Url')

    pesquisar = ft.IconButton(icon=ft.icons.SEND, on_click=buscar)

    page.add(
        barra_de_busca,
        pesquisar
    )


ft.app(target = main)
