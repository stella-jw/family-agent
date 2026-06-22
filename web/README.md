# Web App 测试说明

## 1. 安装依赖

```bash
cd web
npm install
```

## 2. 启动开发服务器

需要先启动 REST API 服务器（参见 backend/api/main.py）

```bash
npm run dev
```

访问 http://localhost:3000

## 3. Vercel 部署

1. 在 Vercel 导入 Git 仓库
2. 设置构建命令：`npm run build`
3. 设置输出目录：`dist`
4. 配置环境变量：
   - `VITE_API_URL`: 你的 API 服务器地址

## 4. API 地址配置

开发环境：Vite 代理到 localhost:8000

生产环境：修改 vercel.json 中的 `YOUR_API_URL` 为实际 API 地址
