param(
    [ValidateSet('local', 'apresentacao')]
    [string]$Modo = 'local',
    [ValidateRange(1, 65535)]
    [int]$Porta = 8000,
    [string]$UrlApresentacao
)

$ErrorActionPreference = 'Stop'
$raiz = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$pythonVenv = Join-Path $raiz '.venv\Scripts\python.exe'
$arquivoEnv = Join-Path $raiz '.env'
$arquivoExemplo = Join-Path $raiz '.env.example'
$arquivoRequisitos = Join-Path $raiz 'requirements.txt'
$marcaRequisitos = Join-Path $raiz '.venv\.requirements.sha256'

Push-Location $raiz
try {
    function Testar-PortaLocal([int]$numeroPorta) {
        $teste = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $numeroPorta)
        try { $teste.Start(); return $true }
        catch { return $false }
        finally { $teste.Stop() }
    }

    $portaDisponivel = Testar-PortaLocal $Porta
    if (-not $portaDisponivel -and $Modo -eq 'local') {
        $portaSolicitada = $Porta
        while (-not $portaDisponivel -and $Porta -lt 65535) {
            $Porta++
            $portaDisponivel = Testar-PortaLocal $Porta
        }
        if ($portaDisponivel) {
            Write-Host "A porta $portaSolicitada já estava em uso; vou iniciar sem encerrar nada na porta $Porta."
        }
    }
    if (-not $portaDisponivel) {
        Write-Host "A porta $Porta já está ocupada. Não encerrei o processo existente."
        Write-Host 'Feche o servidor antigo no terminal dele e execute este iniciador novamente.'
        exit 1
    }

    $urlPublica = $null
    if ($Modo -eq 'apresentacao') {
        if (-not $UrlApresentacao) {
            Write-Host 'Antes, abra outro terminal e execute:'
            Write-Host "cloudflared tunnel --url http://127.0.0.1:$Porta"
            Write-Host 'Depois execute este iniciador com -UrlApresentacao https://SEU-LINK.trycloudflare.com.'
            exit 1
        }
        try { $urlPublica = [uri]$UrlApresentacao } catch {
            Write-Host 'Informe a URL HTTPS completa do túnel Cloudflare.'
            exit 1
        }
        if ($urlPublica.Scheme -ne 'https' -or -not $urlPublica.Host) {
            Write-Host 'A URL de apresentação precisa começar com https://.'
            exit 1
        }
    }

    if (-not (Test-Path $pythonVenv)) {
        if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
            Write-Host 'Instale o Python 3.12 ou mais recente e execute novamente.'
            exit 1
        }
        Write-Host 'Preparando o ambiente Python local...'
        & py -3 -m venv (Join-Path $raiz '.venv')
        if ($LASTEXITCODE -ne 0 -or -not (Test-Path $pythonVenv)) {
            Write-Host 'Não consegui criar o ambiente virtual. Confirme se o Python 3 está instalado.'
            exit 1
        }
    }

    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytesRequisitos = [System.IO.File]::ReadAllBytes($arquivoRequisitos)
        $hashRequisitos = [System.BitConverter]::ToString($sha256.ComputeHash($bytesRequisitos)).Replace('-', '')
    } finally { $sha256.Dispose() }
    $hashInstalado = if (Test-Path $marcaRequisitos) { (Get-Content $marcaRequisitos -Raw).Trim() } else { '' }
    if ($hashRequisitos -ne $hashInstalado) {
        Write-Host 'Conferindo e instalando as dependências do projeto...'
        & $pythonVenv -m pip install -r $arquivoRequisitos
        if ($LASTEXITCODE -ne 0) {
            Write-Host 'A instalação das dependências falhou. Confira sua conexão e tente novamente.'
            exit 1
        }
        [System.IO.File]::WriteAllText($marcaRequisitos, $hashRequisitos, [System.Text.UTF8Encoding]::new($false))
    }

    if (-not (Test-Path $arquivoEnv)) {
        Copy-Item $arquivoExemplo $arquivoEnv
        Write-Host 'Criei o arquivo .env local a partir do exemplo.'
    }

    $conteudoEnv = [System.IO.File]::ReadAllText($arquivoEnv)
    $chaveVazia = $conteudoEnv -match '(?m)^DJANGO_SECRET_KEY\s*=\s*(?:#.*)?$'
    if ($chaveVazia) {
        $chaveGerada = (& $pythonVenv -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())').Trim()
        if ($LASTEXITCODE -ne 0 -or -not $chaveGerada) {
            Write-Host 'Não consegui gerar a chave local do Django.'
            exit 1
        }
        $linhaChave = [regex]'(?m)^DJANGO_SECRET_KEY\s*=.*$'
        if ($linhaChave.IsMatch($conteudoEnv)) {
            $substitutoChave = [System.Text.RegularExpressions.MatchEvaluator]{
                param($correspondencia)
                return "DJANGO_SECRET_KEY=$chaveGerada"
            }
            $conteudoEnv = $linhaChave.Replace($conteudoEnv, $substitutoChave, 1)
        } else {
            $conteudoEnv += "`r`nDJANGO_SECRET_KEY=$chaveGerada`r`n"
        }
        [System.IO.File]::WriteAllText($arquivoEnv, $conteudoEnv, [System.Text.UTF8Encoding]::new($false))
        Write-Host 'Gerei uma chave Django privada no .env local; ela não foi exibida nem enviada ao Git.'
    }

    if ($Modo -eq 'local') {
        $env:DJANGO_DEBUG = 'True'
        $env:DJANGO_TRUST_PROXY_SSL_HEADER = 'False'
        $env:DJANGO_SECURE_SSL_REDIRECT = 'False'
        $env:DJANGO_SESSION_COOKIE_SECURE = 'False'
        $env:DJANGO_CSRF_COOKIE_SECURE = 'False'
        $env:DJANGO_SECURE_HSTS_SECONDS = '0'
        $env:MELHOR_ENVIO_SIMULATE_FREIGHT = 'True'
        Write-Host "Modo local: frete simulado; endereço http://127.0.0.1:$Porta."
    } else {
        $env:DJANGO_DEBUG = 'False'
        $env:DJANGO_TRUST_PROXY_SSL_HEADER = 'True'
        $env:DJANGO_SECURE_SSL_REDIRECT = 'True'
        $env:DJANGO_SESSION_COOKIE_SECURE = 'True'
        $env:DJANGO_CSRF_COOKIE_SECURE = 'True'
        $env:DJANGO_SECURE_HSTS_SECONDS = '3600'
        $env:DJANGO_SERVE_MEDIA_FILES = 'True'
        $hostes = @('127.0.0.1', 'localhost') + @($env:DJANGO_ALLOWED_HOSTS -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ })
        if ($hostes -notcontains $urlPublica.Host) { $hostes += $urlPublica.Host }
        $env:DJANGO_ALLOWED_HOSTS = $hostes -join ','
        $origens = @($env:DJANGO_CSRF_TRUSTED_ORIGINS -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ })
        $origemPublica = $urlPublica.GetLeftPart([System.UriPartial]::Authority)
        if ($origens -notcontains $origemPublica) { $origens += $origemPublica }
        $env:DJANGO_CSRF_TRUSTED_ORIGINS = $origens -join ','
        Write-Host "Modo apresentação: HTTPS em $origemPublica; servidor ligado apenas ao computador."
    }

    & $pythonVenv (Join-Path $raiz 'manage.py') check
    if ($LASTEXITCODE -ne 0) {
        Write-Host 'A verificação do Django falhou. Revise o arquivo .env local.'
        exit 1
    }

    & $pythonVenv (Join-Path $raiz 'manage.py') migrate --noinput
    if ($LASTEXITCODE -ne 0) {
        Write-Host 'Não conectei ao MySQL. Confirme que ele está ligado e que MYSQL_* no .env correspondem ao seu banco local.'
        exit 1
    }

    & $pythonVenv (Join-Path $raiz 'manage.py') seed_demo
    if ($LASTEXITCODE -ne 0) {
        Write-Host 'Não consegui preparar o catálogo. O banco não foi apagado; confira a saída acima.'
        exit 1
    }

    $argumentosServidor = @((Join-Path $raiz 'manage.py'), 'runserver', "127.0.0.1:$Porta")
    if ($Modo -eq 'apresentacao') { $argumentosServidor += '--insecure' }
    if ($Modo -eq 'apresentacao') { Write-Host "Link de apresentação: $origemPublica" }
    else { Write-Host "Abra http://127.0.0.1:$Porta no navegador." }
    Write-Host 'Para encerrar, pressione Ctrl+C nesta janela.'
    & $pythonVenv @argumentosServidor
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
