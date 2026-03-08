# 邀请码管理系统

## 概述

邀请码存储在两个地方：
1. **`invite_codes.csv`** - 文件存储（便于管理和版本控制）
2. **数据库** - 运行时使用（`invite_codes` 表）

## 文件结构

```
invite_codes.csv
├── code: 邀请码（如 INV-7B27D1D4）
├── created_by: 创建者（system/generated/admin）
├── status: 状态（available/used）
└── used_at: 使用时间
```

## 管理命令

### 1. 查看所有邀请码

```bash
# 查看可用邀请码
python manage_invite_codes.py list

# 查看所有邀请码（包括已使用）
python manage_invite_codes.py list --used
```

### 2. 生成新的邀请码

```bash
# 生成 10 个新邀请码（默认）
python manage_invite_codes.py generate

# 生成指定数量的邀请码
python manage_invite_codes.py generate 20
```

### 3. 同步到数据库

```bash
# 将 CSV 中的邀请码同步到数据库
python manage_invite_codes.py sync
```

### 4. 查看统计信息

```bash
python manage_invite_codes.py stats
```

## 初始化流程

### 本地开发

```bash
# 1. 初始化数据库表
python init_db.py

# 2. 邀请码会自动从 CSV 导入到数据库
```

### Render 部署

1. 确保 `invite_codes.csv` 文件已提交到 git
2. 推送到 Render 后，启动时会自动导入邀请码到数据库
3. 或者在 Render Shell 中手动运行：
   ```bash
   python init_db.py
   ```

## 数据库表结构

```sql
CREATE TABLE invite_codes (
    id SERIAL PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    created_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    used_by TEXT,
    used_at TIMESTAMP,
    is_used BOOLEAN DEFAULT FALSE
);
```

## 添加邀请码的三种方式

### 方式 1：编辑 CSV 文件（推荐）

直接编辑 `invite_codes.csv` 添加新行：

```csv
code,created_by,status,used_at
INV-NEWCODE1,admin,available,
INV-NEWCODE2,admin,available,
```

然后同步到数据库：
```bash
python manage_invite_codes.py sync
```

### 方式 2：使用生成命令

```bash
python manage_invite_codes.py generate 10
python manage_invite_codes.py sync
```

### 方式 3：直接在数据库添加

```sql
-- PostgreSQL
INSERT INTO invite_codes (code, created_by, is_used)
VALUES ('INV-CUSTOM1', 'admin', FALSE);

-- SQLite
INSERT INTO invite_codes (code, created_by, is_used)
VALUES ('INV-CUSTOM1', 'admin', 0);
```

## 安全建议

1. **生产环境**：建议将 `invite_codes.csv` 添加到 `.gitignore`，避免公开邀请码
2. **定期备份**：定期导出数据库中的邀请码使用情况
3. **监控使用**：定期检查已使用的邀请码，发现异常及时处理

## 故障排除

### 问题：邀请码无法使用

1. 检查数据库中是否存在该邀请码：
   ```sql
   SELECT * FROM invite_codes WHERE code = 'INV-XXXX';
   ```

2. 检查是否已被使用：
   ```sql
   SELECT code, is_used, used_by, used_at FROM invite_codes;
   ```

3. 重新同步 CSV 到数据库：
   ```bash
   python manage_invite_codes.py sync
   ```

### 问题：CSV 文件丢失

从数据库中导出：
```bash
# PostgreSQL
psql $DATABASE_URL -c "COPY (SELECT code, created_by, is_used FROM invite_codes) TO STDOUT WITH CSV HEADER" > invite_codes.csv
```
