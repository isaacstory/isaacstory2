# Isaac Story - Site

Site estático Vue 3 + Vite para visualização da documentação clínica do Isaac.

## Desenvolvimento

```bash
cd site
npm install
npm run dev
```

O site estará disponível em `http://localhost:5173`

## Build

### Para GitHub Pages (base `/`)
```bash
npm run build
```

### Para Nginx local (base `/isaacstory/`)
```bash
npm run build:nginx
# ou
VITE_BASE=/isaacstory/ npm run build
```

Os arquivos ficam em `site/dist/`

## Deploy no Nginx

1. Fazer o build para Nginx:
```bash
npm run build:nginx
```

2. Criar symlink (precisa de sudo):
```bash
sudo ln -sfn /home/ai/clawd/repos/isaacstory2/site/dist /var/www/html/isaacstory
```

3. Recarregar Nginx (opcional, só se mudar config):
```bash
sudo nginx -t && sudo systemctl reload nginx
```

4. Acessar: http://localhost/isaacstory/ ou http://<IP>/isaacstory/

## Estrutura

```
site/
├── src/
│   ├── App.vue          # Componente principal
│   └── main.js          # Entry point
├── public/              # Assets estáticos
├── dist/                # Build output
├── vite.config.js       # Configuração Vite
└── package.json
```

## Próximos passos

- [ ] Implementar leitura dos dados do repositório
- [ ] Criar views para Consultas, Exames, Prescrições
- [ ] Adicionar navegação/router
- [ ] Timeline visual
- [ ] Configurar GitHub Pages
