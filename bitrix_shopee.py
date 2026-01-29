import time
import os
import subprocess
import socket
from playwright.sync_api import sync_playwright

# --- CONFIGURAÇÕES ---
# usuario_atual = os.environ.get('USERNAME') or os.getlogin()

# 1. Caminho do Opera GX
CAMINHO_OPERA = r"C:/Users/T-GAMER/AppData/Local/Programs/Opera GX/opera.exe" 

# 2. Onde salvar os Prints (Mude aqui se quiser outra pasta)
PASTA_PRINTS = r"C:/Users/T-GAMER/Downloads"

def forcar_abertura_opera():
    print(f"📂 Procurando Opera em: {CAMINHO_OPERA}")
    if not os.path.exists(CAMINHO_OPERA):
        print("❌ ERRO: Executável do Opera não encontrado!")
        return False
    print("⚠️ Reiniciando Opera em modo Debug...")
    os.system("taskkill /F /IM opera.exe >nul 2>&1")
    time.sleep(2)
    try:
        subprocess.Popen([CAMINHO_OPERA, "--remote-debugging-port=9222", "--no-first-run", "--no-default-browser-check"])
        time.sleep(6)
        return True
    except Exception as e:
        print(f"❌ Erro ao iniciar: {e}")
        return False

def garantir_navegador_aberto():
    print("🔌 Verificando porta 9222...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 9222))
    sock.close()
    if result == 0:
        print("✅ Porta ativa.")
        return True
    else:
        return forcar_abertura_opera()

def automacao_v59_ajustes_finais():
    print("🚀 Iniciando V59")
    
    if not garantir_navegador_aberto(): return

    with sync_playwright() as p:
        browser = None
        context = None
        
        # Conexão Robusta
        for tentativa in range(2):
            try:
                print(f"🔌 Conectando (Tentativa {tentativa+1})...")
                browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=15000)
                context = browser.contexts[0]
                if len(context.pages) == 0: context.new_page()
                print(f"✅ Conectado! Abas: {len(context.pages)}")
                break
            except:
                if tentativa == 0: forcar_abertura_opera()
                else: return

        # Localizar Abas
        page_tera = None
        page_bitrix = None
        page_shopee = None

        print("🔍 Procurando as abas corretas...")

        for page in context.pages:
            try:
                page.wait_for_load_state("domcontentloaded", timeout=1000)
                url = page.url
                if "terabyteshop" in url and "admin" not in url: 
                    page_tera = page
                elif "bitrix24" in url: 
                    page_bitrix = page
                elif "seller.shopee" in url and "returnrefundcancel" in url: 
                    page_shopee = page
            except: continue

        if not page_tera:
            print("❌ Aba Terabyte não encontrada.")
            browser.close()
            return

        # 1. EXTRAÇÃO TERABYTE
        print("📄 1. Lendo Terabyte...")
        frame_tera = page_tera
        for frame in page_tera.frames:
            if frame.locator("text=Número do Pedido").count() > 0:
                frame_tera = frame
                break

        def cacar(rotulo):
            try: return frame_tera.locator(f"(//*[contains(text(), '{rotulo}')]/following::*[string-length(text()) > 0])[1]").inner_text(timeout=500).strip().replace("#", "")
            except: return ""

        id_prod = ""
        try:
            seletor_preciso = ".tabelaProdutos table tbody tr td:nth-child(2)"
            if frame_tera.locator(seletor_preciso).count() > 0:
                id_prod = frame_tera.locator(seletor_preciso).first.inner_text().strip()
            else:
                id_prod = frame_tera.locator("/html/body/div[1]/div[9]/div[1]/div[1]/table/tbody/tr/td[2]").first.inner_text().strip()
        except: pass

        dados = {
            "pedido": cacar("Número do Pedido"),
            "mkt_ref": cacar("MKT Referência"),
            "nome": cacar("Nome"),
            "cpf": cacar("CPF/CNPJ"),
            "email": cacar("E-mail"),
            "total": cacar("Total"),
            "id_produto": id_prod
        }
        if not dados["total"]:
             try: dados["total"] = frame_tera.locator("xpath=//*[contains(text(), 'R$') and string-length(text()) < 20]").first.inner_text().strip()
             except: pass
        
        print(f"📋 Dados: {dados}")

        # 2. PREENCHIMENTO BITRIX (Parte 1)
        if page_bitrix:
            print("🔄 2. Preenchendo Bitrix (Parte 1)...")
            page_bitrix.bring_to_front()
            
            if page_bitrix.locator("iframe.side-panel-iframe").count() == 0:
                try: page_bitrix.locator("xpath=//*[@id='uiToolbarContainer']/div[2]/div").click(timeout=2000)
                except: pass
                time.sleep(2)

            frame_bitrix = None
            try:
                element_handle = page_bitrix.query_selector_all("iframe.side-panel-iframe")[-1]
                frame_bitrix = element_handle.content_frame()
                frame_bitrix.wait_for_selector("#deal_0_details_editor_container", timeout=8000)
            except:
                print("❌ Iframe Bitrix falhou.")
                browser.close()
                return

            def texto(xpath, valor):
                if not valor: return
                try: frame_bitrix.locator(f"xpath={xpath}").fill(str(valor), timeout=1000)
                except: pass

            texto("//*[@id='deal_0_details_editor_container']/form/div[2]/div/div[2]/div/div[3]/div[3]/span/span/input", dados["pedido"])
            texto("//*[@id='deal_0_details_editor_container']/form/div[2]/div/div[2]/div/div[4]/div[3]/span/span/input", dados["mkt_ref"])
            texto("//*[@id='deal_0_details_editor_container']/form/div[2]/div/div[2]/div/div[2]/div[3]/div/div[1]/input", dados["total"][3:])
            texto("//*[@id='deal_0_details_editor_container']/form/div[2]/div/div[2]/div/div[8]/div[3]/span/span/input", dados["nome"])
            texto("//*[@id='deal_0_details_editor_container']/form/div[2]/div/div[2]/div/div[9]/div[3]/span/span/input", dados["cpf"])
            texto("//*[@id='deal_0_details_editor_container']/form/div[2]/div/div[2]/div/div[10]/div[3]/span/span/input", dados["email"])
            texto("//*[@id='deal_0_details_editor_container']/form/div[2]/div/div[2]/div/div[14]/div[3]/span/span/input", dados["id_produto"])

            def digitar_e_enter(nome, codigo_data_name, valor_texto):
                try:
                    container = frame_bitrix.locator(f"div[data-name='{codigo_data_name}']").first
                    input_search = container.locator("input.main-ui-square-search-item")
                    container.scroll_into_view_if_needed()
                    time.sleep(0.1)
                    container.click(force=True)
                    input_search.fill(valor_texto)
                    time.sleep(0.3)
                    input_search.press("Enter")
                    print(f"✅ {nome}: OK")
                except: pass

            digitar_e_enter("Estoque Origem", "UF_CRM_1757679236575", "SC")
            digitar_e_enter("Marketplace", "UF_CRM_1757083264665", "Shopee")
            digitar_e_enter("Tipo Pedido", "UF_CRM_1738152509803", "Total")

            try: frame_bitrix.locator("select[name='UF_CRM_9_1731343162081']").select_option(label="DEV"); print("✅ Motivo: OK")
            except: pass
            try: frame_bitrix.locator("div.ui-text-editor-editable").first.click(); frame_bitrix.locator("div.ui-text-editor-editable").first.fill("-"); print("✅ Comentário: OK")
            except: pass
            
            # Solicitante
            try:
                container = frame_bitrix.locator("//div[starts-with(@id, 'cont_UF_CRM_9_1731343334')]").first
                container.scroll_into_view_if_needed()
                botao_add = container.locator("span.ui-tag-selector-add-button-caption").first
                if botao_add.count() > 0: botao_add.click(force=True)
                else: container.click(force=True)
                time.sleep(0.5)
                input_tag = container.locator("input.ui-tag-selector-text-box").first
                if input_tag.count() > 0:
                    input_tag.fill("Mauro Vieira")
                    time.sleep(1.0)
                    item_lista = page_bitrix.locator("div.ui-selector-item-title:text-is('Mauro Vieira')").first
                    if item_lista.count() > 0:
                        page_bitrix.locator("div.ui-selector-item").filter(has=item_lista).first.click(force=True)
                        print("✅ Solicitante: OK")
                    else: input_tag.press("Enter")
            except: pass

        # 3. SHOPEE (PESQUISA -> EXTRAÇÃO IMEDIATA -> NOVA ABA -> PRINT)
        id_solicitacao_extraido = ""
        
        if page_shopee:
            print("🔄 3. Processando Shopee...")
            try:
                page_shopee.bring_to_front()
                time.sleep(1.0)
                
                # A. Pesquisa
                print(f"   ↳ Pesquisando MKT Ref: {dados['mkt_ref']}")
                campo_busca = page_shopee.locator("input[placeholder*='Insira aqui o ID']").first
                if campo_busca.count() == 0: campo_busca = page_shopee.locator("input.eds-input__input").first

                if campo_busca.count() > 0:
                    campo_busca.click()
                    campo_busca.fill(dados['mkt_ref'])
                    time.sleep(0.5)
                    campo_busca.press("Enter")
                    time.sleep(4.0)
                    
                    # B. ESTRATÉGIA SEGURA: Copiar o ID ANTES de abrir a aba
                    # Localiza o elemento span.id-content
                    link_pedido = page_shopee.locator("span.id-content").last
                    
                    if link_pedido.count() > 0:
                        # 1. Copia o Texto
                        id_solicitacao_extraido = link_pedido.inner_text().strip()
                        print(f"   ✅ ID DA SOLICITAÇÃO COPIADO (DA LISTA): {id_solicitacao_extraido}")

                        # 2. Clica para abrir a nova aba (apenas para o print)
                        print("   ↳ Abrindo aba para print...")
                        with context.expect_page() as nova_aba_info:
                            link_pedido.click()
                        
                        nova_aba_shopee = nova_aba_info.value
                        print(f"   ⏳ Carregando nova aba...")
                        
                        # 3. Espera e Print
                        nova_aba_shopee.wait_for_load_state("domcontentloaded")
                        try: nova_aba_shopee.wait_for_load_state("networkidle", timeout=12000)
                        except: pass 
                        time.sleep(5.0)

                        nome_arq_shopee = f"print_shopee_{dados['pedido']}.png"
                        print(f"   📸 Tirando print Full Page...")
                        nova_aba_shopee.screenshot(path=nome_arq_shopee, full_page=True)
                        print(f"   ✅ Print salvo em: {PASTA_PRINTS}{nome_arq_shopee}")
                        
                        # 4. Fecha a aba para não pesar
                        # nova_aba_shopee.close() 

                    else:
                        print("⚠️ MKT Ref não encontrado na Shopee.")
                else:
                    print("⚠️ Campo de busca Shopee não achado.")
                
            except Exception as e:
                print(f"⚠️ Erro na Shopee: {e}")
        else:
            print("⚠️ Aba da Shopee não encontrada.")

        # 4. VOLTA AO BITRIX (COLAR O ID)
        if page_bitrix and id_solicitacao_extraido:
            print(f"🔄 4. Voltando ao Bitrix para colar ID: {id_solicitacao_extraido}...")
            page_bitrix.bring_to_front()
            
            try:
                # Re-adquire o frame
                element_handle = page_bitrix.query_selector_all("iframe.side-panel-iframe")[-1]
                frame_bitrix = element_handle.content_frame()
                
                # Campo ID Devolução
                campo_devolucao = frame_bitrix.locator("input[name='UF_CRM_1757082717772']")
                
                campo_devolucao.scroll_into_view_if_needed()
                time.sleep(0.5)
                
                campo_devolucao.click(force=True)
                campo_devolucao.fill(id_solicitacao_extraido)
                frame_bitrix.locator("body").click(position={"x": 0, "y": 0})
                
                print(f"✅ ID Devolução colado com sucesso!")
                
            except Exception as e:
                print(f"❌ Erro ao colar ID Devolução: {e}")

        print("✅ Finalizado com Sucesso!")
        browser.close()

if __name__ == "__main__":
    automacao_v59_ajustes_finais()