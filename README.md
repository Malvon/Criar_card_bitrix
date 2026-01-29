# 🤖 Bitrix24 & Marketplace Integration Bot

## 📋 Sobre o Projeto
Este projeto é uma solução de automação de alto nível desenvolvida para otimizar o fluxo de trabalho de devoluções do e-commerce que trabalho. O script integra três plataformas distintas — Terabyte (E-commerce), Bitrix24 (CRM) e Shopee (Marketplace) — para automatizar processos que anteriormente eram executados manualmente, reduzindo drasticamente o tempo de operação e eliminando erros humanos.

Este projeto marca uma evolução técnica no meu portfólio, utilizando a conexão CDP (Chrome DevTools Protocol) para interagir com instâncias de navegadores já existentes (Opera GX), aproveitando sessões ativas e cookies.

## 🚀 O Desafio
O processo manual de registro de devoluções era fragmentado e lento, envolvendo:

- **Extração de Dados:** Coleta manual de informações do cliente e do pedido no painel administrativo da Terabyte.
- **Registro no CRM:** Preenchimento de múltiplos campos (CPF, SKU, Valor, E-mail) dentro de Iframes complexos no Bitrix24.
- **Validação Externa:** Busca manual da disputa no portal do vendedor Shopee para localizar o ID da solicitação.
- **Gestão de Evidências:** Captura manual de prints de tela para comprovação de processos.

## 💡 Soluções e Evolução Técnica
O desenvolvimento deste bot aplicou conceitos avançados de automação para resolver gargalos reais de negócio:

- **Conexão Robusta via CDP:** O bot utiliza a porta 9222 para se conectar a um navegador já aberto. Isso permite que a automação utilize sessões e logins ativos, contornando barreiras de autenticação (2FA) e acelerando o processo.
- **Manipulação de Iframes:** O script identifica e interage com elementos dentro de frames aninhados (side-panel-iframe), superando um desafio comum em CRMs modernos.
- **Seletores Inteligentes:** Uso de lógica XPath e CSS para localizar dados em tabelas dinâmicas onde os IDs de elementos mudam constantemente.
- **Evidência Automática:** O bot não apenas extrai o ID da Shopee, mas tira um Screenshot Full Page automaticamente, salvando o arquivo com o número do pedido para garantir a rastreabilidade.

## ✨ Funcionalidades
- **Auto-Detection:** Verifica se o navegador está aberto em modo de debug e o reinicia automaticamente se necessário.
- **Multi-Tab Sync:** Alterna entre abas da Terabyte, Bitrix e Shopee para sincronizar informações em tempo real.
- **Data Validation:** Extrai IDs de solicitações diretamente da interface da Shopee para evitar erros de cópia manual.
- **Custom Form Filling:** Preenche campos de seleção (dropdowns), datas e campos de busca dinâmica no Bitrix24.

## 🛠️ Tecnologias Utilizadas
- **Python:** Linguagem principal do projeto.
- **Playwright (Sync API):** Framework de automação de navegador de alta performance.
- **Socket & Subprocess:** Utilizados para gestão de processos do sistema e verificação de conectividade da porta de debug.
- **OS:** Para manipulação de caminhos de arquivos e integração com o sistema operacional.

## Pontos de Melhoria
Algumas ficaram faltando alguns passos para deixar o processo 100% automatizado, dentre eles:

- O script abrir um link do google drive com o video de recebimento do item que tem que ser validado manualmente por mim
- Anexar o screenshot no final do card
- Copiar a URL do card (após criado), voltar a Terabyte e colar a URL no Log de Ações
- Printar a o Log de Ações após incluir a URL, voltar ao Bitrix e anexar a screenshot na sessão comentarios do card 
- Colocar o processo todo dentro de um for para que ele consiga fazer com todos os pedidos de devolução que estiverem pendentes, independente da quantidade

---
*Este projeto foi desenvolvido com o auxílio de IA para resolver uma demanda real de negócio, reduzindo drasticamente o tempo operacional de SAC.*
