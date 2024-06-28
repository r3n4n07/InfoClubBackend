from flask import Flask
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

@app.route('/WebScraping/<clube>', methods=['GET'])
def Web_Scraping(clube):
    try:
        nome_clube = ''
        escudo_clube = ''
        jogadores_convocados = []
        posicao= ''
        jogos= ''
        vitorias= ''
        empates= ''
        derrotas= ''
        gols= ''
        ultimos_jogos = []
        pontos = ''
        capa_video_ultimo_jogo = 'https://'
        link_video_ultimo_jogo = ''

        # Configurações do navegador
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized") # Maximiza a janela do navegador ao iniciar

        # Abre o navegador
        pagina = webdriver.Chrome(options=chrome_options)
        pagina.get('https://www.sofascore.com/pt/')

        # Aguarda a barra de pesquisa aparecer para permitir a entrada do nome do clube
        WebDriverWait(pagina, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#__next > header > div.upper.wrap > div > div > div.Box.Flex.jdCaQN.jALysY > div > form > input" ))).send_keys(clube)

        # Aguarda a opção do clube aparecer na lista de sugestões de pesquisa para poder selecioná-la
        WebDriverWait(pagina, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#__next > header > div.upper.wrap > div > div > div.Box.Flex.jdCaQN.jALysY > div > div > div.Box.sc-jXbUNg.eJEDPA.cfPkwg > div > div > div:nth-child(1) > a"))).click()

        # Captura o nome do clube inserido corretamente
        nome_clube = WebDriverWait(pagina, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#__next > main > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.Box.Flex.ggRYVx.cQgcrM.Grid.dRBNa > div.Box.clAhaB.Col.bzYVms > div.Box.gIubnq > div > div.Box.Flex.INtcV.ijPrqM > div > div.Box.Flex.dIuVWC.iGVEVf > div.Box.Flex.kIPsJP.inEcLY > h2"))).text

        # Captura a imagem do escudo do clube
        escudo_clube = pagina.find_element(By.CSS_SELECTOR, "#__next > main > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.Box.Flex.ggRYVx.cQgcrM.Grid.dRBNa > div.Box.clAhaB.Col.bzYVms > div.Box.gIubnq > div > div.Box.Flex.INtcV.ijPrqM > div > div.Box.Flex.dIuVWC.iGVEVf > div.Box.nWtju > img").get_attribute('src')

        # Obtém a classificação completa do clube
        classificacao = WebDriverWait(pagina, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#__next > main > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.Box.Flex.ggRYVx.cQgcrM.Grid.dRBNa > div.Box.clAhaB.Col.bzYVms > div.Box.klGMtt > div.Box.fiZFJg > div.Box.klGMtt > div.Box.iHEIFv > div.TabPanel.bpHovE > div > a > div")))
        
        # Percorre toda a tabela até encontrar a equipe que foi pesquisada
        for equipe in classificacao:
            try:

                # Obtém a url da imagem do escudo do clube
                imagem_equipe_selecionada = equipe.find_element(By.CSS_SELECTOR, 'div:nth-child(3) > img').get_attribute("src")

                # Quando o clube for encontrado na classificação, a condição do if será verdadeira e as informações do clube serão obtidas
                if imagem_equipe_selecionada == escudo_clube: 
                    posicao = equipe.find_element(By.CSS_SELECTOR, 'div:nth-child(2)').text
                    jogos = equipe.find_element(By.CSS_SELECTOR, 'div:nth-child(5)').text
                    vitorias = equipe.find_element(By.CSS_SELECTOR, 'div:nth-child(6)').text
                    empates = equipe.find_element(By.CSS_SELECTOR, 'div:nth-child(7)').text
                    derrotas = equipe.find_element(By.CSS_SELECTOR, 'div:nth-child(8)').text
                    gols = equipe.find_element(By.CSS_SELECTOR, 'div:nth-child(9)').text
                    ultimos_jogos = equipe.find_element(By.CSS_SELECTOR, 'div:nth-child(10)').text.split()
                    pontos = equipe.find_element(By.CSS_SELECTOR, 'div:nth-child(11)').text
                    break
            except:
                pass
            

        # Se as informações do clube não forem encontradas, fecha a página e retorna uma resposta apropriada
        if posicao == '':
            print("Nenhum Clube foi Encontrado")
            pagina.quit()
            return {"status": 404, "mensagem": "Nenhum clube foi encontrado"}

        # Este bloco try-except trata a exceção quando jogadores convocados não são encontrados para este clube
        try:
            # Clica no botão que exibe a lista de jogadores convocados
            pagina.find_element(By.CSS_SELECTOR,"#__next > main > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.Box.Flex.ggRYVx.cQgcrM.Grid.dRBNa > div.Box.clAhaB.Col.bzYVms > div.Box.bhOjZO > div.Box.Flex.ggRYVx.delKRF > div.Box.laShVk > div.Box.cNWmcN > div > div:nth-child(4) > div.Box.Flex.daGDON.gSUrXm > div").click()
            
            # Captura a lista de jogadores convocados
            lista_jogadores_convocados = pagina.find_elements(By.CSS_SELECTOR, "#portals > div > div > div > div > div.Box.sc-jXbUNg.gxtjVX.cfPkwg.ps.ps--active-x.ps--active-y > div:nth-child(1) > div > a")
            componente_lista = WebDriverWait(pagina,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#portals > div > div > div > div > div.Box.sc-jXbUNg.gxtjVX.cfPkwg.ps.ps--active-y")))

            for index, info_jogador in enumerate(lista_jogadores_convocados):
                imagem_jogador = info_jogador.find_element(By.CSS_SELECTOR, "div > img").get_attribute('src') # Captura a imagem do jogador convocado
                imagem_pais_jogador = info_jogador.find_element(By.CSS_SELECTOR, "div.Box.Flex.ggRYVx.cRYpNI > img").get_attribute('src') # Captura a imagem do pais do jogador convocado
                nome_jogador = info_jogador.find_element(By.CSS_SELECTOR, "div > div.Box.kUNcqi").text # Captura o nome do jogador convocado
                jogadores_convocados.append({"imagem_jogador":imagem_jogador, "imagem_pais_jogador":imagem_pais_jogador, "nome_jogador":nome_jogador}) # Cria um array com os jogadores convocados
                
                # Se houver mais que 7 jogadores, vai ser feito um scroll na lista de jogadores convocados
                if index > 7: 
                    pagina.execute_script("arguments[0].scrollBy(0, 300);", componente_lista)
                    time.sleep(1)
            pagina.find_element(By.CSS_SELECTOR, "#portals > div > div > div > div > div.Box.Flex.ggRYVx.gyrVAS > div > button").click() # Fecha a lista de jogadores
            
        except:
            print('Nenhum jogador desta equipe foi convocado')
            pagina.execute_script("window.scrollTo(0, 1800);") # Faz um scroll na tela
            pass

    
        # Captura o nome do time da casa
        nome_time_casa = pagina.find_element(By.CSS_SELECTOR, '#__next > main > div:nth-child(2) > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(2) > div > div:nth-child(1) > div > div > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(1) > div > a > div > div > bdi').text

        # Captura o nome do time visitante
        nome_time_visitante = pagina.find_element(By.CSS_SELECTOR, "#__next > main > div:nth-child(2) > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(2) > div > div:nth-child(1) > div > div > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(3) > div > a > div > div > bdi").text
    
        # Captura o escudo do time da casa
        escudo_clube_casa = pagina.find_element(By.CSS_SELECTOR, "#__next > main > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.Box.Flex.ggRYVx.cQgcrM.Grid.dRBNa > div.Box.clAhaB.Col.bzYVms > div.Box.ebVsRG > div > div:nth-child(2) > div:nth-child(2) > div > div:nth-child(1) > div > div > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(1) > div > a > div > img").get_attribute("src")
    
        # Captura o escudo do clube visitante
        escudo_clube_visitante = pagina.find_element(By.CSS_SELECTOR, "#__next > main > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.Box.Flex.ggRYVx.cQgcrM.Grid.dRBNa > div.Box.clAhaB.Col.bzYVms > div.Box.ebVsRG > div > div:nth-child(2) > div:nth-child(2) > div > div:nth-child(1) > div > div > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(3) > div > a > div > img").get_attribute("src")

        # Captura informações sobre o próximo jogo
        info_proximo_jogo = pagina.find_element(By.CSS_SELECTOR, "#__next > main > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.Box.Flex.ggRYVx.cQgcrM.Grid.dRBNa > div.Box.clAhaB.Col.bzYVms > div.Box.ebVsRG > div > div.Box.Flex.ggRYVx.cQgcrM > div:nth-child(2) > div > div:nth-child(1) > div > div > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(2) > div").text.split('\n')
        
        
        # Este bloco try-except trata a exceção quando não são encontrados vídeos dos jogos desse clube
        try:
            # Captura a imagem do vídeo do último jogo
            capa_video_ultimo_jogo = WebDriverWait(pagina, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#__next > main > div.fresnel-container.fresnel-greaterThanOrEqual-mdMin > div > div.Box.Flex.ggRYVx.cQgcrM.Grid.dRBNa > div.Box.kUNcqi.Col.ePbOsj > div.Box.klGMtt > div > div > a:nth-child(1) > div.Box.cORqut > img'))).get_attribute('src')
        
            # Captura o link do vídeo do último jogo
            link_video_ultimo_jogo = pagina.find_element(By.CSS_SELECTOR, "#__next > main > div:nth-child(2) > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(5) > div > div > a:nth-child(1)").get_attribute("href")
        except:
            print("Não há vídeo de último jogo")
            pass

        pagina.quit()
        
        return {
            "status":200, 
            "dados":{
                "nomeClube": nome_clube,
                "escudoClube": escudo_clube,
                "posicao":posicao,
                "pontos":pontos,
                "ultimosJogos":ultimos_jogos,
                "gols": gols,
                "derrotas":derrotas,
                "empates": empates,
                "vitorias": vitorias,
                "jogos": jogos,
                "nomeTimeCasa":nome_time_casa,
                "nomeTimeVisitante":nome_time_visitante,
                "escudoClubeCasa": escudo_clube_casa,
                "escudoClubeVisitante":escudo_clube_visitante,
                "infoProximoJogo": info_proximo_jogo,
                "JogadoresConvocados": jogadores_convocados,
                "capaVideoUltimoJogo": capa_video_ultimo_jogo,
                "linkVideoUltimoJogo": link_video_ultimo_jogo
            },
            "mensagem":"ok"
            }
    
    except Exception as error:
        return {"status":500, "mensagem":error}

if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.10',port=5010)