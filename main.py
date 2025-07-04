import streamlit as st
import pandas as pd
import json
from github import Github
import base64

st.set_page_config(page_title="Uploader de Matérias", layout="centered")

st.title("📚 Uploader de Matérias para GitHub")

# GitHub config
github_token = st.sidebar.text_input("Token do GitHub", type="password")
repo_name = "80anna/nathguima_temp"
file_in_repo = st.sidebar.text_input("Caminho do arquivo JSON no repo", value="materias.json")
commit_message = st.sidebar.text_input("Mensagem de commit", value="Atualização do arquivo materias.json")

uploaded_file = st.file_uploader("Faça upload do arquivo .xlsx", type="xlsx")

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        df.fillna("", inplace=True)

        def tags_para_lista(tags):
            if isinstance(tags, str):
                return [tag.strip() for tag in tags.split(',') if tag.strip()]
            return []

        df["tags"] = df["tags"].apply(tags_para_lista)
        df["data"] = df["data"].astype(str)

        json_data = df.to_dict(orient='records')
        json_str = json.dumps(json_data, indent=2, ensure_ascii=False)

        st.subheader("📄 Pré-visualização do JSON")
        st.code(json_str, language="json")

        if github_token and repo_name:
            if st.button("🚀 Enviar para o GitHub"):
                try:
                    g = Github(github_token)
                    repo = g.get_repo(repo_name)

                    try:
                        contents = repo.get_contents(file_in_repo)
                        repo.update_file(contents.path, commit_message, json_str, contents.sha)
                        st.success(f"✅ Atualizado {file_in_repo} no repositório {repo_name}")
                    except:
                        repo.create_file(file_in_repo, commit_message, json_str)
                        st.success(f"✅ Criado {file_in_repo} no repositório {repo_name}")
                except Exception as e:
                    st.error(f"Erro ao enviar para o GitHub: {e}")
        else:
            st.warning("⚠️ Preencha as informações do GitHub na barra lateral.")

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
