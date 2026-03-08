# Neon PostgreSQL 设置指南

## 1. 创建 Neon 账户

1. 访问 [https://neon.tech](https://neon.tech)
2. 点击 "Sign Up" 注册账户（支持 GitHub、Google 或邮箱注册）
3. 免费版提供 0.5GB 存储空间，足够本项目使用

## 2. 创建数据库项目

1. 登录 Neon Console 后，点击 "**+ New Project**"
2. 输入项目名称：`echoes-of-farewell`（或任意名称）
3. 选择 PostgreSQL 版本（默认即可）
4. 点击 "**Create project**"

## 3. 获取数据库连接字符串

1. 在项目页面，找到 "**Connection Details**" 部分
2. 点击 "**Copy**" 复制连接字符串
3. 连接字符串格式类似：
   ```
   postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
   ```

## 4. 配置 Render 环境变量

1. 登录 [Render Dashboard](https://dashboard.render.com/)
2. 进入你的 `echoes-of-farewell` Web Service
3. 点击 "**Environment**" 标签页
4. 点击 "**Add Environment Variable**"
5. 添加以下变量：
   - **Key**: `DATABASE_URL`
   - **Value**: 粘贴你从 Neon 复制的连接字符串
6. 点击 "**Save changes**"

## 5. 配置本地 .env 文件（可选）

如果你在本地开发，复制 `.env` 文件并填入 Neon 连接字符串：

```bash
cp .env .env.local
```

编辑 `.env.local`：

```
NEON_DATABASE_URL=postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
```

## 6. 重新部署 Render

1. 在 Render Dashboard 进入你的服务
2. 点击 "**Manual Deploy**" -> "**Clear build cache & deploy**"
3. 等待部署完成

## 7. 初始化数据库（如需要）

如果需要手动初始化数据库表，可以在 Render 的 Shell 中运行：

```bash
python init_db.py
```

## Neon 免费版限制

| 项目 | 限制 |
|------|------|
| 存储空间 | 0.5 GB |
| 计算时间 | 每天约 30 分钟活跃时间 |
| 自动休眠 | 15 分钟无活动后自动休眠 |
| 唤醒时间 | 约 1-2 秒 |

**注意**: Neon 免费版在 15 分钟无活动后会进入休眠状态，下次请求时会短暂唤醒（约 1-2 秒）。这对个人项目影响不大。

## 常见问题

### Q: 连接字符串中的 `sslmode=require` 是什么？
A: 这是 PostgreSQL 的 SSL 连接模式，Neon 强制要求 SSL 连接以保证安全。

### Q: 可以在本地使用 SQLite，生产使用 Neon 吗？
A: 可以！代码会自动检测 `DATABASE_URL` 环境变量：
- 如果设置了 `DATABASE_URL`，使用 Neon PostgreSQL
- 如果未设置，使用 SQLite（本地开发）

### Q: 如何备份 Neon 数据库？
A: Neon 免费版不支持自动备份，但可以：
1. 使用 `pg_dump` 手动导出
2. 升级到付费计划获得自动备份
