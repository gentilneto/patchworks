"""Consulta ViaCEP para validar e enriquecer o CEP de destino."""

from __future__ import annotations

import requests


class ViaCepError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def consultar_cep(cep: str) -> dict:
    cep_limpo = ''.join(ch for ch in str(cep) if ch.isdigit())
    if len(cep_limpo) != 8:
        raise ViaCepError('CEP inválido. Informe 8 dígitos.', status_code=400)

    url = f'https://viacep.com.br/ws/{cep_limpo}/json/'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise ViaCepError('Não foi possível consultar o CEP agora.', status_code=502) from exc

    if data.get('erro'):
        raise ViaCepError('CEP não encontrado.', status_code=404)

    return {
        'cep': data.get('cep') or cep_limpo,
        'logradouro': data.get('logradouro') or '',
        'bairro': data.get('bairro') or '',
        'localidade': data.get('localidade') or '',
        'uf': data.get('uf') or '',
    }
