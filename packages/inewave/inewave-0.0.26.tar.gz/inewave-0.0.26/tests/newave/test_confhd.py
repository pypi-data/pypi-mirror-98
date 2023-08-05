# Rotinas de testes associadas ao arquivo confhd.dat do NEWAVE
from inewave.newave.confhd import LeituraConfhd, EscritaConfhd


leitor = LeituraConfhd("tests/_arquivos")
leitor.le_arquivo()


def test_leitura():
    assert len(leitor.confhd.usinas) > 0


def test_escrita_e_leitura():
    escritor = EscritaConfhd("tests/_saidas")
    escritor.escreve_arquivo(leitor.confhd)
    leitor2 = LeituraConfhd("tests/_saidas")
    leitor2.le_arquivo()
    assert leitor.confhd == leitor2.confhd


def test_eq_confhd():
    leitor2 = LeituraConfhd("tests/_arquivos")
    leitor2.le_arquivo()
    assert leitor2.confhd == leitor.confhd


def test_neq_confhd():
    leitor2 = LeituraConfhd("tests/_arquivos")
    leitor2.le_arquivo()
    leitor2.confhd.usinas[4].existente = False
    assert leitor2.confhd != leitor.confhd
    assert leitor2.confhd is not None
