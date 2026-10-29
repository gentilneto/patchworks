# Validação local do Patch Works

**Data:** 29 de outubro de 2026
**Versão examinada:** branch local `codex/site-demo-improvements`
**Objetivo:** registrar o que foi verificado para a demonstração local e distinguir simulação de integração real.

## Resultado resumido

O projeto inicia com MySQL local, as páginas principais respondem e a cotação de demonstração retorna duas opções identificadas como simulação. A suíte automatizada passou com 21 testes. A integração real do Melhor Envio ainda não foi validada: esta instalação não tem token OAuth salvo.

## O que mudou nesta cópia

- Dois iniciadores ajudam a abrir o projeto localmente e preparar uma apresentação temporária.
- `seed_demo` carrega produtos de exemplo apenas quando o catálogo está vazio; não cria contas.
- O foco do teclado fica mais visível e há um atalho para ir direto ao conteúdo.
- O token OAuth fica no arquivo local ignorado pelo Git; o modo local não precisa guardar tokens no MySQL.
- O frete da demonstração é uma simulação. A integração Melhor Envio continua no projeto, mas não foi testada com autorização real.

## Verificações automatizadas

| Verificação | Resultado | Observação |
|---|---|---|
| Suíte Django | **21 testes aprovados** | Executada em 29/10/2026 com `core.test_settings`, usando banco SQLite em memória para testes. |
| Verificação do Django | **Sem problemas** | `manage.py check` concluiu sem avisos. |
| Migrações no MySQL local | **Todas aplicadas** | `showmigrations --plan` mostrou as migrações de `core` até `0009`, além das migrações do Django, aplicadas. |
| Carga de demonstração | **Aprovada** | Os testes confirmam carga em catálogo vazio, ausência de contas de usuário no fixture e preservação de catálogo já preenchido. |
| Navegação acessível | **2 testes aprovados** | Verificam o atalho “Pular para o conteúdo”, o destino principal e os estilos de foco/contraste adicionados. |

Comando da suíte:

```powershell
.\.venv\Scripts\python.exe manage.py test --settings=core.test_settings -v 1
```

## Verificações manuais no servidor local

| Ação | Resultado observado |
|---|---|
| Iniciar em modo local com a porta 8000 ocupada | O iniciador escolheu a porta 8001 e manteve o processo antigo intacto. |
| Abrir `/`, `/produtos/` e `/contato/` | Todas responderam HTTP 200. |
| Carregar os CSS principal e de produtos | Ambos responderam HTTP 200; os novos estilos de acessibilidade estavam servidos. |
| Consultar frete pelo endpoint `/api/frete/cotar/` | HTTP 200, `ok=true`, `simulado=true`, duas opções. O teste usou produto 3, CEP `01001000` e quantidade 1. |
| Conferir aceitação do host no modo apresentação | O host HTTPS informado foi aceito (HTTP 200); um host diferente foi rejeitado (HTTP 400). Foi um teste local de cabeçalhos, não uma apresentação pública pelo túnel. |

## Acessibilidade examinada

- O layout agora oferece um link de salto para o conteúdo principal, visível quando recebe foco do teclado.
- O destino é o marco principal da página (`main`) e pode receber foco programático.
- Os cartões de produto têm contorno de foco visível para navegação por teclado.
- O texto pequeno de desconto e de erro usa a cor de texto principal. A cor de cobre antiga tinha contraste calculado de aproximadamente 4,47:1 sobre o fundo claro; o texto principal tem 16,97:1 sobre o mesmo fundo.
- Já existiam texto alternativo nas imagens de produto/avaliação, rótulos ARIA no diálogo, anúncio do estado de frete e suporte a Escape e Tab no modal.

Os testes verificam a presença do atalho e dos estilos no código. Uma avaliação com leitor de tela e uma rodada manual completa só com teclado ainda não foram registradas.

## Limites do que foi comprovado

- A cotação acima é **simulada** e não consulta transportadoras nem representa tarifa ou prazo real.
- O código OAuth do Melhor Envio está presente, mas não há token salvo neste ambiente local. Não foi feita cotação real autenticada.
- Os 21 testes automatizados usam SQLite em memória; eles não substituem uma suíte integral contra MySQL. A conexão e as migrações do MySQL local foram verificadas separadamente.
- O teste de host do modo apresentação não comprova disponibilidade de um túnel público, domínio estável ou hospedagem permanente.
- As alterações e este documento estão na cópia local do projeto; ainda não foram publicados no GitHub.

## Reproduzir a cotação simulada

1. Inicie `INICIAR_LOCAL.bat` e abra o endereço informado.
2. Entre em **Produtos**, abra um item que aceite quantidade 1 e use o CEP `01001000`.
3. Clique em **Calcular**. O resultado correto para este modo traz aviso explícito de simulação e duas opções ilustrativas.
