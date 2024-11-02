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
                formato_video.visible = True
                page.add(check_mp4, formato_video, your_down)
                page.update()

            else:
                check_mp4.value = False
                formato_video.visible = False
                your_down.visible = False
                page.add(check_mp4, formato_video, your_down)
                page.update()

        def escolherFormato(e):
            url = barra_de_busca.value

            if formato_video.value == '.mp4':
                yt = YouTube(url)
                ys = yt.streams.get_highest_resolution()
                ys.download(output_path='./apptube/mp4')
                page.update()

            else:
                your_down.visible = True
                yt = YouTube(url)
                ys = yt.streams.get_audio_only()
                ys.download(output_path='./apptube/mp3', mp3=True)
                page.update()

        def mostrarDown(e):
            if formato_video.value == '.mp4':
                your_down.visible = True
                page.controls.append(your_down)
                page.update()
            else:
                your_down.visible = True
                page.controls.append(your_down)
                page.update()

        yt = YouTube(barra_de_busca.value)

        thumber = ft.Container(ft.Image(src=f"{yt.thumbnail_url}"), width=200, on_click=checkMp4)
        formato_video = ft.Dropdown(
            width=100,
            visible=False,
            options = [
                ft.dropdown.Option('.mp4'),
                ft.dropdown.Option('.mp3'),
            ],
            on_click=mostrarDown
        )
        your_down = ft.IconButton(icon=ft.icons.DOWNLOAD, on_click=escolherFormato, visible=False)



        check_mp4 = ft.Checkbox(value=False, visible=False)

        page.add(thumber, check_mp4, formato_video, your_down)
        page.update()
        
   
    barra_de_busca = ft.TextField(label='Digite a Url')

    pesquisar = ft.IconButton(icon=ft.icons.SEND, on_click=buscar)

    page.add(
        ft.Row(
            [
                barra_de_busca,
                pesquisar
            ]
        )
    )


ft.app(target = main)
