# MemorialChat 💫

一个基于 LLM 的纪念亲人网页应用，让你能与思念的人"对话"。

## 功能特性

- ✅ **用户认证** - 用户名+密码注册/登录
- ✅ **亲人档案** - 创建亲人档案（姓名+性格+聊天记录+照片）
- ✅ **聊天功能** - 文字对话+历史记录
- 🎨 **简洁 UI** - 现代化渐变设计，温暖治愈风格
- 🕐 **时间感知** - LLM 根据当前时间、季节、节日调整回复内容
- 🌤️ **天气感知** - 支持实时天气 API，让关心更贴心
- 📸 **图片提取** - 上传聊天记录截图，AI 自动识别并提取文字

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | HTML + CSS + JavaScript (原生) |
| 后端 | Python FastAPI |
| 数据库 | SQLite (轻量级，无需额外部署) |
| LLM | OpenAI API 兼容接口 (支持 Kimi/OpenAI/Gemini 等) |

## 快速开始

### 1. 环境准备

确保已安装 Python 3.8+:

```bash
python --version
```

### 2. 安装依赖

```bash
# 创建虚拟环境 (推荐)
python -m venv .venv

# Windows 激活
.venv\Scripts\activate

# macOS/Linux 激活
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制示例配置文件
cp .env.example .env

# 编辑 .env 文件，填入你的配置
```

主要配置项：

```env
# 选择 LLM 提供商 (kimi/openai/gemini/custom)
LLM_PROVIDER=kimi

# Kimi API Key (从 https://platform.moonshot.cn/ 获取)
KIMI_API_KEY=your-api-key

# 天气 API (可选，用于实时天气关心)
# 注册地址: https://openweathermap.org/api
OPENWEATHER_API_KEY=your-weather-api-key
WEATHER_CITY=Beijing
```

### 4. 启动服务

```bash
python main.py
```

服务启动后，访问 http://localhost:8000

## 使用指南

### 首次使用

1. **注册账号** - 使用用户名和密码注册
2. **创建档案** - 填写亲人信息：
   - 姓名
   - 性格描述
   - 真实聊天记录 (AI 会学习语言风格)
   - 照片 (可选)
3. **开始对话** - 在聊天页面与"亲人"交流

### 档案说明

**聊天记录的作用：**
- AI 会分析聊天记录中的语言风格
- 学习用词习惯、表情使用、语气特点
- 聊天记录越多，模仿得越真实

**建议的聊天记录格式：**
```
亲人：吃饭了吗？
我：刚吃完
亲人：多吃点，别饿着，最近工作忙吗？
我：还行，就是有点累
亲人：注意休息，别太累了
```

### 智能时间感知

MemorialChat 会根据以下因素让 AI 的回复更真实自然：

| 因素 | 示例 |
|------|------|
| **时间段** | 早上问候早安、深夜提醒早睡 |
| **季节** | 夏天提醒防暑、冬天提醒保暖 |
| **节日** | 春节说吉祥话、生日送祝福 |
| **天气** | 下雨天提醒带伞、大热天提醒多喝水 |

**支持的中国传统节日：**
- 春节、元宵节、端午节、七夕、中秋节、重阳节
- 公历节日：元旦、情人节、妇女节、劳动节、儿童节、国庆节、圣诞节等

**天气功能配置：**
如需实时天气，在 `.env` 中配置 OpenWeather API Key：
```env
OPENWEATHER_API_KEY=your-api-key
WEATHER_CITY=Beijing
```

## API 文档

启动服务后访问：http://localhost:8000/docs

### 主要接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/register` | POST | 用户注册 |
| `/api/login` | POST | 用户登录 |
| `/api/profile` | GET/POST/DELETE | 档案操作 |
| `/api/chat` | POST | 发送消息 |
| `/api/chat/history` | GET/DELETE | 聊天记录 |

## LLM 提供商支持

### Kimi (Moonshot AI) - 推荐 🇨🇳
- 官网: https://platform.moonshot.cn/
- 配置: `LLM_PROVIDER=kimi`
- 特点: 中文效果好，国内访问稳定

### OpenAI
- 配置: `LLM_PROVIDER=openai`
- 需要: `OPENAI_API_KEY`

### Google Gemini
- 配置: `LLM_PROVIDER=gemini`
- 需要: `GEMINI_API_KEY`

### 其他 OpenAI 兼容 API
- 配置: `LLM_PROVIDER=custom`
- 可接入各种第三方 API

## 项目结构

```
MemorialChat/
├── main.py              # FastAPI 后端入口
├── database.py          # SQLite 数据库操作
├── llm_provider.py      # LLM 提供商封装
├── requirements.txt     # Python 依赖
├── .env.example         # 环境变量示例
├── README.md           # 项目说明
├── static/             # 前端静态文件
│   ├── index.html      # 主页面
│   ├── css/
│   │   └── style.css   # 样式文件
│   ├── js/
│   │   └── app.js      # 前端逻辑
│   └── uploads/        # 上传的照片
└── memorial_chat.db    # SQLite 数据库 (自动创建)
```

## 注意事项

1. **隐私保护** - 聊天记录仅存储在本地数据库
2. **照片上传** - 支持 JPG/PNG/GIF/WEBP，最大 5MB
3. **生产部署** - 请修改 `SECRET_KEY`，使用 HTTPS

## 许可证

MIT License

---

💫 愿逝者安息，愿生者坚强
