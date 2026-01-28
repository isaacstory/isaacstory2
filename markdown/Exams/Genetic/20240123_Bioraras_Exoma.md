# Relatório de Análise de Exoma Completo (NGS)

**Data**: 2024-01-23
**Provider**: BioRaras (Dra. Vanessa Zanette, Dra. Cristiane Benincá)
**Lab**: Tismoo (sequenciamento) / BioRaras (análise)
**Patient**: Isaac Lobato França
**Protocolo**: JST2203
**DN**: 06/11/2018

---

## Metodologia

- **Modalidade**: Exoma Completo
- **Genoma de Referência**: GRCh38
- **DNA Mitocondrial**: rCRS (NC_012920)
- **Cobertura mínima**: 20x por base
- **Classificação**: Segundo guidelines ACMG
- **Hipótese diagnóstica**: Atraso de desenvolvimento, TEA, acidose metabólica, distúrbio gastrointestinal

---

## Resultado Principal

**Não foram encontradas variantes patogênicas que justifiquem o quadro clínico.**

Foram encontradas **uma variante patogênica** e **seis variantes de significado clínico incerto (VUS)** como achados complementares.

---

## Variantes Patogênicas

| Gene | Localização | Variante | Zigosidade | Classificação | Condição Associada | dbSNP |
|------|-------------|----------|------------|---------------|-------------------|-------|
| GALT | Chr9:34647858 | NM_000155:c.C404T (p.S135L) | Heterozigoto (C/T) | **Patogênica** | Galactosemia – AR (OMIM: 230400) | rs111033690 |

### Detalhes - Variante GALT

- **Frequência populacional**: ABraOM: 0.0004%, GnomAD: 0.0009%
- **Função do gene**: Expressa a proteína Galactose-1-fosfato uridil transferase (GALT), que catalisa a segunda etapa da via de Leloir do metabolismo da galactose
- **Fenótipo associado**: Galactosemia (OMIM: 230400) - caracterizada por catarata, cirrose, vômito, diarréia, atraso de desenvolvimento e anemia hemolítica
- **Herança**: Autossômica Recessiva
- **Nota importante**: Achado isolado em heterozigose - não encontrada segunda variante em trans. Não suficiente para desenvolvimento da síndrome.

---

## Variantes de Significado Incerto (VUS)

### Tabela 1: Genes associados a quadros fenotípicos similares

| Gene | Localização | Variante | Zigosidade | Classificação (ACMG) | Condição Associada | dbSNP |
|------|-------------|----------|------------|---------------------|-------------------|-------|
| MED13 | Chr17:62031587 | NM_005121:c.A866T (p.D289V) | Heterozigoto (T/A) | VUS (PM2, PP3, BP1) | Transtorno de desenvolvimento intelectual – AD (OMIM: 618009) | rs925249026 |
| ASS1 | Chr9:130458525 | NM_054012:c.G299A (p.R100H) | Heterozigoto (G/A) | VUS (PM1, PM2, PM5, PP5, BP4) | Citrulinemia – AR (OMIM: 215700) | rs138279074 |
| TAT | Chr16:71570312 | NM_000353:c.G998A (p.R333H) | Heterozigoto (C/T) | VUS (PM2, BP4) | Tirosinemia, tipo II – AR (OMIM: 276600) | rs771408463 |
| FHL1 | ChrX:136208570 | NM_001159699:c.A665G (p.Q222R) | Hemizigoto (A/G) | VUS (PM2, BP4, PM1) | Distrofias musculares/Miopatias – LXR/LXD (OMIM: 300717, 300718, 300695) | rs915687031 |

### Tabela 2: Genes de susceptibilidade ao TEA

| Gene | Localização | Variante | Zigosidade | Classificação (ACMG) | Score SFARI | dbSNP |
|------|-------------|----------|------------|---------------------|-------------|-------|
| DLGAP1 | Chr18:3879219 | NM_001242761:c.A850G (p.T284A) | Heterozigoto (T/C) | VUS (PM2, PP2, BP4) | 2 (Forte candidato) | rs200178260 |
| MED13 | Chr17:62031587 | NM_005121:c.A866T (p.D289V) | Heterozigoto (T/A) | VUS (PM2, PP3, BP1) | 1 (Associação comprovada) | rs925249026 |

---

## Detalhes das Variantes VUS

### MED13 (rs925249026)
- **Frequência**: Não encontrada em bases populacionais (variante de novo potencial)
- **Predições bioinformáticas**: 8 patogênicas, 12 incertas, 0 neutras
- **PhastCons100way**: 1.000 (alta conservação)
- **Fenótipo AD**: Atraso global no desenvolvimento, desenvolvimento intelectual prejudicado, atraso na fala, TEA, TDAH, características dismórficas, obstipação, anomalias oculares, baixo crescimento
- **Score SFARI**: 1 (Associação comprovada com TEA)

### ASS1 (rs138279074)
- **Frequência**: ABraOM: 0.001%, GnomAD: 0.00018%
- **Região Hotspot**: Sim (PM1)
- **Predições bioinformáticas**: 8 patogênicas, 13 incertas, 3 neutras
- **PhastCons100way**: 1.000 (alta conservação)
- **Fenótipo AR**: Citrulinemia - vômitos, hepatomegalia, letargia, convulsão, atraso de desenvolvimento, irritabilidade, intoxicação por amônia
- **Nota**: Achado isolado em heterozigose

### TAT (rs771408463)
- **Frequência**: ALFA: 0.000028%, GnomAD: 0.000024%
- **Predições bioinformáticas**: 1 patogênica, 8 incertas, 15 neutras
- **PhastCons100way**: 0.901 (alta conservação)
- **Fenótipo AR**: Tirosinemia tipo II - atraso de desenvolvimento, queratoses puntiformes dolorosas
- **Nota**: Achado isolado em heterozigose

### FHL1 (rs915687031)
- **Frequência**: ABraOM: 0.001%, TOMMO: 0.00008%
- **Região Hotspot**: Sim (PM1)
- **Predições bioinformáticas**: 0 patogênicas, 12 incertas, 7 neutras
- **PhastCons100way**: 1.000 (alta conservação)
- **Fenótipos associados**:
  - Distrofia muscular de Emery-Dreifuss tipo 6 (OMIM: 300696) - LXR
  - Miopatia corporal redutora tipo 1A (OMIM: 300717) - LXD
  - Miopatia corporal redutora tipo 1B (OMIM: 300718) - LX
  - Miopatia escapuloperoneal (OMIM: 300695) - LXD

### DLGAP1 (rs200178260)
- **Frequência**: ExAC: 0.000009%
- **Predições bioinformáticas**: 7 patogênicas, 10 incertas, 5 neutras
- **PhastCons100way**: 0.901 (alta conservação)
- **Score SFARI**: 2 (Forte candidato para associação com TEA)

---

## Observações e Recomendações

1. **Aconselhamento genético recomendado** para melhor interpretação dos resultados
2. Necessária **correlação clínica** com os achados descritos
3. Variantes relatadas devem ser **confirmadas por outro método** (sequenciamento ou genotipagem)
4. Variantes classificadas como potencialmente patogênicas por algoritmos bioinformáticos **não devem ser consideradas patogênicas** sem estudo funcional

---

## Limitações da Metodologia

- Não avalia sequências não codificantes
- Não avalia regiões reguladoras
- Não avalia regiões intrônicas profundas
- Não detecta variações em número de cópias (CNVs)

---

## Responsáveis Técnicos

- **Dra. Vanessa Zanette (PhD)** - CRF-PR: 24574 - Geneticista, Pós-doutorado em Bioinformática (Responsável Técnica)
- **Dra. Cristiane Benincá (PhD)** - CRBio: 108143/07-D - Geneticista, Pós-doutorado em Genética Humana

---

*Source: /Users/tony/isaacstory/isaacstory2/Exams/Genetic/20240123_Bioraras_Exoma.pdf*
*Generated: 2026-01-28*
*Template: Genetic v1.0*