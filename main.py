import flet as ft
from pytubefix import YouTube


def main(page: ft.Page):

    page.adaptive=True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    def temaLight(e):
        page.theme_mode = ft.ThemeMode.LIGHT
        page.update()

    def temaDark(e):
        page.theme_mode = ft.ThemeMode.DARK
        page.update()

    def limpaPesquisa(e):
        page.controls.clear()
        page.add(container_main)
        page.update()

    def buscar(e):
        
        def checkMp4(e):
            if check_mp4.value == False:
                check_mp4.value = True
                formato_video.visible = True
                page.add(container_main, check_mp4, formato_video, your_down)
                page.update()

            else:
                check_mp4.value = False
                formato_video.visible = False
                your_down.visible = False
                page.add(container_main, check_mp4, formato_video, your_down)
                page.update()

        def escolherFormato(e):
            url = barra_de_busca.value

            if formato_video.value == '.mp4':
                yt = YouTube(url)
                ys = yt.streams.get_highest_resolution()
                ys.download(output_path='./apptube/video')
                page.update()

            else:
                your_down.visible = True
                yt = YouTube(url)
                ys = yt.streams.get_audio_only()
                ys.download(output_path='./apptube/music', mp3=True)
                page.update()
                
        def mostrarDown(e):
            if formato_video.value == '.mp4':
                your_down.visible = True
                page.add(your_down)
                page.update()
            else:
                your_down.visible = True
                page.add(your_down)
                page.update()

        try:
            yt = YouTube(barra_de_busca.value)

            titulo_video = ft.Text(f'{yt.title}', size=18, text_align='center')

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
            check_mp4 = ft.Checkbox(value=False, visible=False)
            your_down = ft.IconButton(icon=ft.icons.DOWNLOAD, on_click=escolherFormato, visible=False)
            
            page.controls.clear()
            page.add(container_main, titulo_video, thumber, check_mp4, formato_video, your_down)
            page.update()
        except:
            txt_error = ft.Container(
                    ft.Text('Video não encontrado, verifique sua url.', color=ft.colors.WHITE ),
                    margin=ft.margin.only(top=20),
                    bgcolor=ft.colors.RED_400,
                    border_radius=10,
                    padding=15,
            )
            page.controls.clear()
            page.add(container_main, txt_error)
            page.update()

    page.appbar = ft.AppBar(
        ft.IconButton(ft.icons.CLEAR_ALL_OUTLINED, on_click=limpaPesquisa),
        title= ft.Text('Apptube'),
        center_title=True,
        bgcolor= ft.colors.LIGHT_BLUE_400,
        actions=[
            ft.IconButton(ft.icons.LIGHT_MODE, on_click=temaLight),
            ft.IconButton(ft.icons.DARK_MODE, on_click=temaDark),            
        ]
        
    )

    page.bottom_appbar = ft.BottomAppBar(
        content= ft.Container(
            ft.Text('by Robson Cerqueira', size=16),
            alignment=ft.alignment.center
        ),
        bgcolor=ft.colors.LIGHT_BLUE_400,
        height=50
    )


    barra_de_busca = ft.TextField(label='Digite a Url')

    pesquisar = ft.IconButton(icon=ft.icons.SEND, on_click=buscar)

    container_main = ft.Row(
            [
                barra_de_busca,
                pesquisar
            ],
            alignment= 'center',
            
        )
   
    page.controls.clear()
    page.add(
        container_main
    )
    page.update()


ft.app(target = main)
