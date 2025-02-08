import flet as ft
import mysql.connector


def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="******", 
            database="industria"
        )
        return conexao
    except mysql.connector.Error as erro:
        print(f"Erro ao conectar ao banco de dados: {erro}")
        return None

def verificar_login(matricula, senha):
    conexao = conectar_banco()
    if conexao:
        cursor = conexao.cursor()
        sql = "SELECT id, nome, cargo FROM funcionarios WHERE matricula = %s AND senha = %s"
        valores = (matricula, senha)
        cursor.execute(sql, valores)
        resultado = cursor.fetchone()
        cursor.close()
        conexao.close()
        return resultado
    return None


def obter_centros_acesso(funcionario_id):
    conexao = conectar_banco()
    if conexao:
        cursor = conexao.cursor()
        sql = """
        SELECT ca.nome 
        FROM centros_acesso ca
        JOIN funcionarios_centros fc ON ca.id = fc.centro_id
        WHERE fc.funcionario_id = %s
        """
        valores = (funcionario_id,)
        cursor.execute(sql, valores)
        resultados = cursor.fetchall()
        cursor.close()
        conexao.close()
        return [centro[0] for centro in resultados]
    return []


def obter_patrimonio():
    conexao = conectar_banco()
    if conexao:
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM equipamentos")
        equipamentos = cursor.fetchall()

        cursor.execute("SELECT * FROM veiculos")
        veiculos = cursor.fetchall()

        cursor.execute("SELECT * FROM dispositivos_de_seguranca")
        dispositivos = cursor.fetchall()

        cursor.close()
        conexao.close()

        return {
            "equipamentos": equipamentos,
            "veiculos": veiculos,
            "dispositivos": dispositivos,
        }
    return None


def adicionar_patrimonio(tabela, dados):
    conexao = conectar_banco()
    if conexao:
        cursor = conexao.cursor()
        colunas = ", ".join(dados.keys())
        valores = ", ".join(["%s"] * len(dados))
        sql = f"INSERT INTO {tabela} ({colunas}) VALUES ({valores})"
        cursor.execute(sql, tuple(dados.values()))
        conexao.commit()
        cursor.close()
        conexao.close()
        return True
    return False


def atualizar_patrimonio(tabela, id, dados):
    conexao = conectar_banco()
    if conexao:
        cursor = conexao.cursor()
        sets = ", ".join([f"{chave} = %s" for chave in dados.keys()])
        sql = f"UPDATE {tabela} SET {sets} WHERE id = %s"
        cursor.execute(sql, tuple(dados.values()) + (id,))
        conexao.commit()
        cursor.close()
        conexao.close()
        return True
    return False


def remover_patrimonio(tabela, id):
    conexao = conectar_banco()
    if conexao:
        cursor = conexao.cursor()
        sql = f"DELETE FROM {tabela} WHERE id = %s"
        cursor.execute(sql, (id,))
        conexao.commit()
        cursor.close()
        conexao.close()
        return True
    return False


def main(page: ft.Page):
    page.title = "Sistema de Gestão Industrial WAYNE"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    usuario_logado = None
    centros_acesso = []

    def login(e):
        nonlocal usuario_logado, centros_acesso
        resultado = verificar_login(campo_matricula.value, campo_senha.value)
        if resultado:
            usuario_logado = resultado
            centros_acesso = obter_centros_acesso(usuario_logado[0])
            page.session.set("usuario_logado", usuario_logado)
            page.clean()
            exibir_pagina_principal()
        else:
            campo_matricula.error_text = "Matrícula ou senha inválida"
            campo_senha.error_text = "Matrícula ou senha inválida"
            page.update()

    def exibir_pagina_principal():
        nome, cargo = usuario_logado[1], usuario_logado[2]
        page.add(
            ft.Column(
                [
                    ft.Text(f"Bem-vindo, {nome} ({cargo})", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Text("Centros de Acesso Permitidos:", size=18, weight=ft.FontWeight.BOLD),
                    *[ft.Text(centro) for centro in centros_acesso],
                ],
                spacing=20,
            )
        )

        if cargo == "Administrador de Segurança":
            exibir_crud_patrimonio()

    def exibir_crud_patrimonio():
        page.add(
            ft.Column(
                [
                    ft.Text("Gerenciar Patrimônio", size=18, weight=ft.FontWeight.BOLD),
                    ft.ElevatedButton(text="Ver Patrimônio", on_click=ver_patrimonio),
                    ft.ElevatedButton(text="Adicionar Item", on_click=adicionar_item_ui),
                    ft.ElevatedButton(text="Atualizar Item", on_click=atualizar_item_ui),
                    ft.ElevatedButton(text="Remover Item", on_click=remover_item_ui),
                ],
                spacing=10,
            )
        )

    def ver_patrimonio(e):
        page.clean()
        exibir_pagina_principal()
        patrimonio = obter_patrimonio()
        if patrimonio:
            page.add(ft.Text("Equipamentos:", size=16, weight=ft.FontWeight.BOLD))
            for item in patrimonio["equipamentos"]:
                page.add(
                    ft.ListTile(
                        title=ft.Text(item[1]),
                        subtitle=ft.Text(f"Marca: {item[2]}, Quantidade: {item[3]}, Localização: {item[4]}"),
                    )
                )

            page.add(ft.Text("Veículos:", size=16, weight=ft.FontWeight.BOLD))
            for item in patrimonio["veiculos"]:
                page.add(
                    ft.ListTile(
                        title=ft.Text(f"{item[1]} {item[2]}"),
                        subtitle=ft.Text(f"Ano: {item[3]}, Cor: {item[4]}"),
                    )
                )

            page.add(ft.Text("Dispositivos de Segurança:", size=16, weight=ft.FontWeight.BOLD))
            for item in patrimonio["dispositivos"]:
                page.add(
                    ft.ListTile(
                        title=ft.Text(item[1]),
                        subtitle=ft.Text(f"Marca: {item[2]}, Quantidade: {item[3]}, Localização: {item[4]}"),
                    )
                )
        else:
            page.add(ft.Text("Nenhum item de patrimônio encontrado."))

   

    def adicionar_item_ui(e):
        page.clean()

        menu_tabela = ft.Dropdown(
            label="Tabela",
            options=[
                ft.dropdown.Option("equipamentos"),
                ft.dropdown.Option("veiculos"),
                ft.dropdown.Option("dispositivos_de_seguranca"),
            ],
            width=300,
            value="equipamentos"
        )

        
        campo_nome = ft.TextField(label="Nome", width=300)
        campo_marca = ft.TextField(label="Marca", width=300)
        campo_quantidade = ft.TextField(label="Quantidade", width=300)
        campo_localizacao = ft.TextField(label="Localização", width=300)

        campo_modelo = ft.TextField(label="Modelo", width=300)
        campo_ano = ft.TextField(label="Ano", width=300)
        campo_cor = ft.TextField(label="Cor", width=300)

        
        campos_container = ft.Column()

        def atualizar_campos(e):
            
            campos_container.controls.clear()

            if menu_tabela.value == "equipamentos":
                campos_container.controls.extend([
                    ft.Text("Adicionar Equipamento", size=18, weight=ft.FontWeight.BOLD),
                    campo_nome,
                    campo_marca,
                    campo_quantidade,
                    campo_localizacao
                ])
            elif menu_tabela.value == "veiculos":
                campos_container.controls.extend([
                    ft.Text("Adicionar Veículo", size=18, weight=ft.FontWeight.BOLD),
                    campo_modelo,
                    campo_marca,
                    campo_ano,
                    campo_cor
                ])
            elif menu_tabela.value == "dispositivos_de_seguranca":
                campos_container.controls.extend([
                    ft.Text("Adicionar Dispositivo de Segurança", size=18, weight=ft.FontWeight.BOLD),
                    campo_nome,
                    campo_marca,
                    campo_quantidade,
                    campo_localizacao
                ])

            page.update()  

        
        menu_tabela.on_change = atualizar_campos
        atualizar_campos(None)  

        def salvar_item(e):
            dados = {}

            if menu_tabela.value == "equipamentos":
                dados = {
                    "nome": campo_nome.value,
                    "marca": campo_marca.value,
                    "quantidade": int(campo_quantidade.value) if campo_quantidade.value.isdigit() else 0,
                    "localizacao": campo_localizacao.value,
                }
            elif menu_tabela.value == "veiculos":
                dados = {
                    "modelo": campo_modelo.value,
                    "marca": campo_marca.value,
                    "ano": int(campo_ano.value) if campo_ano.value.isdigit() else 0,
                    "cor": campo_cor.value,
                }
            elif menu_tabela.value == "dispositivos_de_seguranca":
                dados = {
                    "nome": campo_nome.value,
                    "marca": campo_marca.value,
                    "quantidade": int(campo_quantidade.value) if campo_quantidade.value.isdigit() else 0,
                    "localizacao": campo_localizacao.value,
                }

            if adicionar_patrimonio(menu_tabela.value, dados):
                page.clean()
                exibir_pagina_principal()
                ver_patrimonio(e)
            else:
                campo_nome.error_text = "Erro ao adicionar item"
                page.update()

        page.add(
            ft.Column(
                [
                    menu_tabela,
                    campos_container,
                    ft.ElevatedButton(text="Salvar", on_click=salvar_item),
                    ft.ElevatedButton(text="Cancelar", on_click=lambda e: (page.clean(), exibir_pagina_principal())),
                ],
                spacing=20,
            )
        )



    def atualizar_item_ui(e):
        def salvar_atualizacao(e):
            dados = {}
            if menu_tabela.value == "equipamentos":
                dados = {
                    "nome": campo_nome.value,
                    "marca": campo_marca.value,
                    "quantidade": int(campo_quantidade.value),
                    "localizacao": campo_localizacao.value,
                }
            elif menu_tabela.value == "veiculos":
                dados = {
                    "modelo": campo_modelo.value,
                    "marca": campo_marca.value,
                    "ano": int(campo_ano.value),
                    "cor": campo_cor.value,
                }
            elif menu_tabela.value == "dispositivos_de_seguranca":
                dados = {
                    "nome": campo_nome.value,
                    "marca": campo_marca.value,
                    "quantidade": int(campo_quantidade.value),
                    "localizacao": campo_localizacao.value,
                }

            if atualizar_patrimonio(menu_tabela.value, int(campo_id.value), dados):
                page.clean()
                exibir_pagina_principal()
                ver_patrimonio(e)
            else:
                campo_id.error_text = "Erro ao atualizar item"
                page.update()

        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text("Atualizar Item do Patrimônio", size=18, weight=ft.FontWeight.BOLD),
                    menu_tabela := ft.Dropdown(
                        label="Tabela",
                        options=[
                            ft.dropdown.Option("equipamentos"),
                            ft.dropdown.Option("veiculos"),
                            ft.dropdown.Option("dispositivos_de_seguranca"),
                        ],
                        width=300,
                    ),
                    campo_id := ft.TextField(label="ID do Item", width=300),
                    campo_nome := ft.TextField(label="Nome", width=300),
                    campo_marca := ft.TextField(label="Marca", width=300),
                    campo_quantidade := ft.TextField(label="Quantidade", width=300),
                    campo_localizacao := ft.TextField(label="Localização", width=300),
                    ft.ElevatedButton(text="Salvar", on_click=salvar_atualizacao),
                    ft.ElevatedButton(text="Cancelar", on_click=lambda e: (page.clean(), exibir_pagina_principal())),
                ],
                spacing=20,
            )
        )

    def remover_item_ui(e):
        def confirmar_remocao(e):
            if remover_patrimonio(menu_tabela.value, int(campo_id.value)):
                page.clean()
                exibir_pagina_principal()
                ver_patrimonio(e)
            else:
                campo_id.error_text = "Erro ao remover item"
                page.update()

        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text("Remover Item do Patrimônio", size=18, weight=ft.FontWeight.BOLD),
                    menu_tabela := ft.Dropdown(
                        label="Tabela",
                        options=[
                            ft.dropdown.Option("equipamentos"),
                            ft.dropdown.Option("veiculos"),
                            ft.dropdown.Option("dispositivos_de_seguranca"),
                        ],
                        width=300,
                    ),
                    campo_id := ft.TextField(label="ID do Item", width=300),
                    ft.ElevatedButton(text="Confirmar Remoção", on_click=confirmar_remocao),
                    ft.ElevatedButton(text="Cancelar", on_click=lambda e: (page.clean(), exibir_pagina_principal())),
                ],
                spacing=20,
            )
        )

    campo_matricula = ft.TextField(label="Matrícula", width=300)
    campo_senha = ft.TextField(label="Senha", width=300, password=True)
    botao_login = ft.ElevatedButton(text="Login", on_click=login)

    page.add(
        ft.Column(
            [
                ft.Text("Login", size=20, weight=ft.FontWeight.BOLD),
                campo_matricula,
                campo_senha,
                botao_login,
            ],
            spacing=20,
        )
    )


ft.app(target=main)