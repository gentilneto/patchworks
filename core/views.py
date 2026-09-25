import json
import re

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from .models import Avaliacao, Produto, Categoria
from .services.melhor_envio import (
    MelhorEnvioError,
    build_authorize_url,
    calcular_frete_produtos,
    exchange_code_for_token,
)
from .services.viacep import ViaCepError, consultar_cep


def home(request):
    return render(request, 'core/home.html')


def avaliacoes(request):
    avaliacoes = Avaliacao.objects.all().order_by('-criado_em')
    return render(request, 'core/avaliacoes.html', {'avaliacoes': avaliacoes})


@ensure_csrf_cookie
def produtos(request):
    busca = request.GET.get('busca', '')
    categoria_id = request.GET.get('categoria', '')

    produtos = Produto.objects.all().order_by('-criado_em')

    if busca:
        produtos = produtos.filter(nome__icontains=busca)

    if categoria_id:
        produtos = produtos.filter(categoria_id=categoria_id)

    categorias = Categoria.objects.all().order_by('nome')

    return render(request, 'core/produtos.html', {
        'produtos': produtos,
        'categorias': categorias,
        'busca': busca,
        'categoria_id': categoria_id,
    })


def contato(request):
    return render(request, 'core/contato.html')


@require_GET
def api_consultar_cep(request):
    cep = request.GET.get('cep', '')
    try:
        endereco = consultar_cep(cep)
        return JsonResponse({'ok': True, 'endereco': endereco})
    except ViaCepError as exc:
        return JsonResponse(
            {'ok': False, 'error': exc.message},
            status=exc.status_code or 400,
        )


@require_POST
def api_cotar_frete(request):
    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'JSON inválido.'}, status=400)

    produto_id = payload.get('produto_id')
    cep_destino = payload.get('cep', '')
    quantidade = payload.get('quantidade', 1)

    if not produto_id:
        return JsonResponse({'ok': False, 'error': 'produto_id é obrigatório.'}, status=400)

    try:
        quantidade = int(quantidade)
    except (TypeError, ValueError):
        return JsonResponse({'ok': False, 'error': 'Quantidade inválida.'}, status=400)

    if quantidade < 1:
        return JsonResponse({'ok': False, 'error': 'Quantidade deve ser pelo menos 1.'}, status=400)

    produto = get_object_or_404(Produto, pk=produto_id)

    if produto.quantidade_minima and quantidade < produto.quantidade_minima:
        return JsonResponse(
            {
                'ok': False,
                'error': f'Quantidade mínima deste produto é {produto.quantidade_minima}.',
            },
            status=400,
        )

    # Valida CEP no ViaCEP antes de cotar
    try:
        endereco = consultar_cep(cep_destino)
    except ViaCepError as exc:
        return JsonResponse(
            {'ok': False, 'error': exc.message},
            status=exc.status_code or 400,
        )

    dims = produto.dimensoes_unidade()
    insurance = float(produto.preco_seguro)

    products = [{
        'id': str(produto.codigo or produto.id),
        'width': dims['width'],
        'height': dims['height'],
        'length': dims['length'],
        'weight': dims['weight'],
        'insurance_value': insurance,
        'quantity': quantidade,
    }]

    try:
        opcoes = calcular_frete_produtos(
            cep_destino=cep_destino,
            products=products,
        )
    except MelhorEnvioError as exc:
        status = exc.status_code if exc.status_code and 400 <= exc.status_code < 600 else 502
        return JsonResponse(
            {
                'ok': False,
                'error': exc.message,
                'details': exc.details,
                'endereco': endereco,
            },
            status=status,
        )

    return JsonResponse({
        'ok': True,
        'endereco': endereco,
        'origem_cep': re.sub(r'\D', '', str(settings.STORE_CEP)),
        'produto': {
            'id': produto.id,
            'nome': produto.nome,
            'codigo': produto.codigo,
            'quantidade': quantidade,
            'dimensoes_unidade': dims,
            'peso_total_kg': round(dims['weight'] * quantidade, 3),
        },
        'opcoes': opcoes,
    })


@require_GET
def melhorenvio_autorizar(request):
    """Redireciona para o OAuth do Melhor Envio (sandbox/produção)."""
    try:
        url = build_authorize_url(state='patchworks')
    except MelhorEnvioError as exc:
        return HttpResponse(
            f'<h1>Configuração incompleta</h1><p>{exc.message}</p>'
            '<p>Defina MELHOR_ENVIO_CLIENT_ID, MELHOR_ENVIO_CLIENT_SECRET e '
            'MELHOR_ENVIO_REDIRECT_URI no arquivo .env.</p>',
            status=exc.status_code or 503,
        )
    return redirect(url)


@require_GET
def melhorenvio_callback(request):
    """Recebe o ?code= do Melhor Envio e troca por access_token."""
    error = request.GET.get('error')
    if error:
        return HttpResponseBadRequest(
            f'<h1>Autorização negada</h1><p>{error}: {request.GET.get("error_description", "")}</p>'
        )

    code = request.GET.get('code')
    if not code:
        return HttpResponseBadRequest('<h1>Callback sem code</h1><p>Parâmetro code não encontrado.</p>')

    try:
        data = exchange_code_for_token(code)
    except MelhorEnvioError as exc:
        return HttpResponse(
            f'<h1>Falha ao obter token</h1><p>{exc.message}</p><pre>{exc.details}</pre>',
            status=exc.status_code or 502,
        )

    expires = data.get('expires_in', '?')
    return HttpResponse(
        '<h1>Token Melhor Envio salvo</h1>'
        f'<p>access_token obtido com sucesso (expires_in={expires}s).</p>'
        '<p>Arquivo: <code>melhorenvio_token.json</code></p>'
        '<p><a href="/produtos/">Voltar aos produtos e testar a cotação</a></p>'
    )
