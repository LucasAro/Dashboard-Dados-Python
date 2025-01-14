# Documentação do Projeto

Este repositório foi criado como parte dos meus estudos de Análise de Dados, explorando a construção de dashboards interativos com Python e Streamlit. A aplicação exibe insights e informações relevantes acerca dos dados em questão, tornando mais simples a compreensão e exploração dos resultados obtidos.

---

## Requisitos

- **Docker** instalado na máquina
- Acesso aos arquivos deste repositório

---

## Como executar a aplicação

1. **Clonar o repositório**  
   ```bash
   git clone https://github.com/LucasAro/Dashboard-Dados-Python.git
   ```
2. **Acessar a pasta do projeto**  
   ```bash
   cd Dashboard-Dados-Python
   ```
3. **Construir a imagem Docker**  
   ```bash
   docker build -t streamlit-app .
   ```
4. **Executar o contêiner**  
   ```bash
   docker run -p 8501:8501 streamlit-app
   ```
5. **Acessar a aplicação**  
   Abra o navegador em [http://localhost:8501](http://localhost:8501) para visualizar o dashboard.

---

## Estrutura de Arquivos

- **📊 Main Page.py**: Arquivo principal do Streamlit, contendo a lógica e a interface do dashboard.  
- **requirements.txt**: Lista de bibliotecas Python necessárias para rodar a aplicação.  
- **Dockerfile**: Arquivo que define o contêiner Docker para a aplicação.  
- **data/**: Pasta onde se encontram o arquivo de dados utilizado.

---

Este Dockerfile:

1. Utiliza a imagem base `python:3.12`.
2. Cria um diretório de trabalho `/app`.
3. Copia o arquivo `requirements.txt` e instala as dependências.
4. Copia o restante dos arquivos para o diretório de trabalho.
5. Expõe a porta 8501, utilizada pelo Streamlit.
6. Define o comando para iniciar o Streamlit.

---

## Observações

- Caso deseje modificar alguma dependência, basta atualizá-la no `requirements.txt` e reconstruir a imagem Docker.  
- É recomendável manter um ambiente de desenvolvimento separado do de produção, facilitando testes e garantindo o funcionamento estável do projeto em diferentes estágios.

---

**Espero que este projeto seja útil nos seus estudos de Análise de Dados!** Fique à vontade para abrir **issues** ou contribuir com **pull requests** sempre que encontrar oportunidades de melhorias.  

Bom aprendizado e boa exploração dos dados!
