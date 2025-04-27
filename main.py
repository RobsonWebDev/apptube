import flet as ft
from pytubefix import YouTube
import os

def main(page: ft.Page):
    # Configurações da página
    page.title = "AppTube Downloader"
    page.adaptive = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # Variáveis de estado
    download_in_progress = False
    progress_bar = ft.ProgressBar(width=400, visible=False, color=ft.colors.LIGHT_BLUE_400)
    status_text = ft.Text("", text_align="center")

    # Funções de tema
    def temaLight(e):
        page.theme_mode = ft.ThemeMode.LIGHT
        page.update()

    def temaDark(e):
        page.theme_mode = ft.ThemeMode.DARK
        page.update()

    def limpaPesquisa(e):
        if not download_in_progress:
            reset_ui()
        else:
            show_error("Aguarde o download atual ser concluído")

    def reset_ui():
        """Reseta a interface para o estado inicial"""
        page.controls.clear()
        page.add(container_main)
        page.update()

    def show_error(message):
        """Mostra uma mensagem de erro"""
        error_msg = ft.Container(
            ft.Text(message, color=ft.colors.WHITE),
            margin=ft.margin.only(top=20),
            bgcolor=ft.colors.RED_400,
            border_radius=10,
            padding=15,
        )
        
        page.controls.clear()
        page.add(container_main, error_msg)
        page.update()

    def show_success(message):
        """Mostra uma mensagem de sucesso"""
        success_msg = ft.Container(
            ft.Text(message, color=ft.colors.WHITE),
            margin=ft.margin.only(top=20),
            bgcolor=ft.colors.GREEN_400,
            border_radius=10,
            padding=15,
        )
        
        page.controls.clear()
        page.add(container_main, success_msg)
        page.update()

    def on_download_progress(stream, chunk, bytes_remaining):
        """Callback para atualizar a barra de progresso"""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        progress = bytes_downloaded / total_size
        
        progress_bar.value = progress
        status_text.value = f"Baixando: {int(progress * 100)}%"
        page.update()

    def buscar(e):
        """Busca informações do vídeo"""
        url = barra_de_busca.value.strip()
        
        if not url:
            show_error("Por favor, insira uma URL válida")
            return
            
        try:
            yt = YouTube(url, on_progress_callback=on_download_progress)
            
            titulo_video = ft.Text(f'{yt.title}', size=18, text_align='center')
            thumber = ft.Container(
                ft.Image(src=f"{yt.thumbnail_url}"), 
                width=200, 
                on_click=lambda e: checkMp4(e, yt)
            )
            
            page.controls.clear()
            page.add(
                container_main,
                titulo_video,
                thumber,
                ft.Row([check_mp4, formato_video], alignment="center"),
                progress_bar,
                status_text,
                download_button
            )
            page.update()
            
        except Exception as e:
            show_error(f"Erro ao buscar vídeo: {str(e)}")

    def checkMp4(e, yt=None):
        """Alterna entre opções de download"""
        if check_mp4.value == False:
            check_mp4.value = True
            formato_video.visible = True
            download_button.visible = True
        else:
            check_mp4.value = False
            formato_video.visible = False
            download_button.visible = False
            
        page.update()

    def escolherFormato(e):
        """Realiza o download no formato selecionado"""
        nonlocal download_in_progress
        url = barra_de_busca.value.strip()
        
        if not url:
            show_error("Por favor, insira uma URL válida")
            return
            
        try:
            download_in_progress = True
            progress_bar.visible = True
            status_text.value = "Preparando download..."
            page.update()
            
            yt = YouTube(url, on_progress_callback=on_download_progress)
            
            # Cria diretórios se não existirem
            os.makedirs('./apptube/video', exist_ok=True)
            os.makedirs('./apptube/music', exist_ok=True)
            
            if formato_video.value == '.mp4':
                ys = yt.streams.get_highest_resolution()
                output_path = './apptube/video'
            else:
                ys = yt.streams.get_audio_only()
                output_path = './apptube/music'
            
            # Concluído com sucesso
            status_text.value = "Download concluído!"
            progress_bar.value = 1.0
            page.update()
            
            # Mostra mensagem de sucesso
            show_success(f"Download concluído!")
            
        except Exception as e:
            show_error(f"Erro durante o download: {str(e)}")
        finally:
            download_in_progress = False
            progress_bar.visible = False

    # Componentes da UI
    barra_de_busca = ft.TextField(
        label='Digite a URL do YouTube',
        width=400,
        border_color=ft.colors.LIGHT_BLUE_400,
        focused_border_color=ft.colors.LIGHT_BLUE_700
    )

    pesquisar = ft.IconButton(
        icon=ft.icons.SEARCH,
        icon_color=ft.colors.LIGHT_BLUE_400,
        on_click=buscar
    )

    check_mp4 = ft.Checkbox(
        label="Baixar vídeo?",
        value=False,
        visible=False,
        on_change=checkMp4
    )

    formato_video = ft.Dropdown(
        width=150,
        visible=False,
        options=[
            ft.dropdown.Option('.mp4', "Vídeo (MP4)"),
            ft.dropdown.Option('.mp3', "Áudio (MP3)"),
        ],
        value='.mp4'
    )

    download_button = ft.ElevatedButton(
        "Iniciar Download",
        icon=ft.icons.DOWNLOAD,
        on_click=escolherFormato,
        visible=False,
        color=ft.colors.WHITE,
        bgcolor=ft.colors.LIGHT_BLUE_400
    )

    container_main = ft.Column(
        [
            ft.Row(
                [barra_de_busca, pesquisar],
                alignment='center',
            )
        ],
        alignment='center',
    )

    # AppBar e BottomAppBar
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.icons.CLEAR_ALL_OUTLINED, on_click=limpaPesquisa),
        title=ft.Text('AppTube Downloader'),
        center_title=True,
        bgcolor=ft.colors.LIGHT_BLUE_400,
        actions=[
            ft.IconButton(ft.icons.LIGHT_MODE, on_click=temaLight),
            ft.IconButton(ft.icons.DARK_MODE, on_click=temaDark),            
        ]
    )

    page.bottom_appbar = ft.BottomAppBar(
        content=ft.Container(
            ft.Text('by Robson Cerqueira', size=16),
            alignment=ft.alignment.center
        ),
        bgcolor=ft.colors.LIGHT_BLUE_400,
        height=50
    )

    # Inicializa a UI
    reset_ui()

ft.app(target=main)